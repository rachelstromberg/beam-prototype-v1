"""Source reconciliation and percentile-boundary checks."""
import importlib.util
import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare', ROOT / 'scripts/prepare_data.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)
data = json.loads((ROOT / 'public/data.json').read_text())
assert prepare.percentile([1, 2, 3, 4], .9) == 3.7
assert prepare.percentile([7], .9) == 7
assert sum(w['written'] for w in data['workflows']) == 79
assert sum(w['n'] for w in data['workflows']) == 150
early = next(w for w in data['workflows'] if w['name'] == 'Early Help Assessment Note')
assert early['distribution'] == [3, 2, 3, 3, 6], early['distribution']
assert early['written'] == 6
assert sorted(f['count'] for f in early['feedback']) == [1, 1, 2, 2]
for w in data['workflows']:
    scores = [rating for rating, count in enumerate(w['distribution'], 1) for _ in range(count)]
    assert abs(mean(scores) - w['average']) < 1e-9
    assert len({f['text'] for f in w['feedback']}) == len(w['feedback'])
    for f in w['feedback']:
        assert len(f['ratings']) == 5
        assert sum(f['ratings']) == f['count'], 'Comment ratings must retain every repeated response'
    for i in range(5):
        assert sum(f['ratings'][i] for f in w['feedback']) <= w['distribution'][i]
assert [(r['low'], r['high']) for r in data['concerns']] == [(2, 4), (3, 2), (2, 1)]
assert [w['n'] for w in data['waits']] == [58, 62, 53]
assert [round(w['median']) for w in data['waits']] == [10, 24, 44]
assert all(w['p90'] >= w['median'] for w in data['waits'])
assert not any(key in json.dumps(data) for key in ('email', 'user_id', 'feedback_id', 'summary_id'))
if len(sys.argv) > 1:
    assert data == prepare.prepare(Path(sys.argv[1])), 'Prepared data does not reconcile with source'
print('PASS: rating distributions, duplicate counts, concern splits, duration bands, percentiles, and source reconciliation.')
