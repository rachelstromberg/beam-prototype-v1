"""Prepare anonymous aggregates from the five supplied Magic Notes extracts."""
import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]


def unique(rows, key):
    result = {r[key]: r for r in rows}
    assert len(result) == len(rows), f'Duplicate {key}'
    return result


def percentile(values, q):
    values = sorted(values)
    p = (len(values) - 1) * q
    lo, hi = math.floor(p), math.ceil(p)
    return values[lo] + (values[hi] - values[lo]) * (p - lo)


def prepare(source):
    tables = {}
    for name in ('summaries', 'transcripts', 'prompt_templates', 'feedback', 'users'):
        with (source / f'{name}.csv').open(newline='', encoding='utf-8-sig') as f:
            tables[name] = list(csv.DictReader(f))
    summaries = unique(tables['summaries'], 'summary_id')
    transcripts = unique(tables['transcripts'], 'transcript_id')
    templates = unique(tables['prompt_templates'], 'template_id')
    users = unique(tables['users'], 'user_id')
    unique(tables['feedback'], 'feedback_id')
    feedback = tables['feedback']
    by_template = defaultdict(list)
    by_transcript = defaultdict(list)
    for s in summaries.values():
        assert s['transcript_id'] in transcripts
        assert s['template_id'] in templates
        assert s['user_id'] in users
        by_transcript[s['transcript_id']].append(s)
    for f in feedback:
        assert f['summary_id'] in summaries
        assert f['user_id'] in users
        assert 1 <= int(f['rating']) <= 5
        assert summaries[f['summary_id']]['status'] == 'completed'
        by_template[summaries[f['summary_id']]['template_id']].append(f)

    workflows = []
    for tid, template in templates.items():
        rows = by_template[tid]
        scores = [int(r['rating']) for r in rows]
        phrases = Counter(r['comment'].strip() for r in rows if r['comment'].strip())
        workflows.append(dict(
            id=tid, name=template['name'].replace(' - ', ' – '),
            average=mean(scores) if scores else None, n=len(scores),
            distribution=[scores.count(i) for i in range(1, 6)],
            written=sum(phrases.values()),
            feedback=[dict(text=text, count=count,
                           ratings=[sum(r['comment'].strip() == text and int(r['rating']) == score for r in rows) for score in range(1, 6)])
                      for text, count in sorted(phrases.items(), key=lambda p: (-p[1], p[0]))],
        ))
    workflows.sort(key=lambda r: (r['average'] is None, r['average'] or 0, r['name']))
    concern_phrases = [
        ('Incorrect safeguarding flag', "Incorrectly flagged a safeguarding concern that wasn't there."),
        ('Names mixed up', 'Some of the names were mixed up in the output.'),
        ('Missing risk details', 'Missed some key details about the risk assessment.'),
    ]
    concerns = []
    for label, phrase in concern_phrases:
        rows = [r for r in feedback if r['comment'].strip() == phrase]
        concerns.append(dict(label=label, phrase=phrase, count=len(rows),
                             low=sum(int(r['rating']) <= 3 for r in rows),
                             high=sum(int(r['rating']) >= 4 for r in rows)))

    bands = [dict(label='0–30 min', times=[]),
             dict(label='30–60 min', times=[]),
             dict(label='Over 60 min', times=[])]
    for s in summaries.values():
        if s['status'] != 'completed':
            continue
        assert s['processing_time_ms'], 'Completed attempt missing processing time'
        duration = float(transcripts[s['transcript_id']]['duration_seconds'])
        assert duration > 0
        band = 0 if duration <= 1800 else 1 if duration <= 3600 else 2
        seconds = float(s['processing_time_ms']) / 1000
        assert seconds >= 0
        bands[band]['times'].append(seconds)
    waits = [dict(label=b['label'], n=len(b['times']), median=median(b['times']),
                  p90=percentile(b['times'], .9)) for b in bands]
    statuses = dict(Counter(r['status'] for r in summaries.values()))
    coverage = dict(
        transcripts=len(transcripts), attempts=len(summaries), feedback=len(feedback),
        written=sum(bool(r['comment'].strip()) for r in feedback),
        average=mean(int(r['rating']) for r in feedback),
        councils=len({r['council'] for r in users.values()}),
        linked=len(by_transcript), unlinked=len(transcripts) - len(by_transcript),
        noCompleted=sum(not any(s['status'] == 'completed' for s in rows) for rows in by_transcript.values()),
        multipleTemplates=sum(len({s['template_id'] for s in rows}) > 1 for rows in by_transcript.values()),
    )
    # Reference reconciliation fails visibly if the supplied data changes.
    assert (coverage['attempts'], coverage['feedback'], coverage['written'], coverage['linked']) == (200, 150, 79, 131)
    assert statuses == dict(completed=173, failed=15, in_progress=12)
    assert [(r['low'], r['high']) for r in concerns] == [(2, 4), (3, 2), (2, 1)]
    assert [w['n'] for w in waits] == [58, 62, 53]
    assert sum(w['n'] for w in workflows) == len(feedback)
    assert sum(w['written'] for w in workflows) == coverage['written']
    for w in workflows:
        assert sum(w['distribution']) == w['n']
        assert sum(f['count'] for f in w['feedback']) == w['written']
    return dict(coverage=coverage, workflows=workflows, concerns=concerns, waits=waits, statuses=statuses)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT / 'db_extracts')
    args = parser.parse_args()
    data = prepare(args.source)
    (ROOT / 'public').mkdir(exist_ok=True)
    (ROOT / 'public/data.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(dict(coverage=data['coverage'], waits=data['waits']), indent=2))
    print('Verified source relationships, counts, rating splits, and grouped feedback.')
