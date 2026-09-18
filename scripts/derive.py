"""Local-only derivation. Raw files are never copied into the app or ZIP."""
import csv, json, statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(name): return list(csv.DictReader((root/'data'/f'{name}.csv').open()))
def index(rows,key):
 result={r[key]:r for r in rows}
 assert len(result)==len(rows), f'Duplicate {key}'
 return result
T,S,F,P,U=[read(n) for n in ['transcripts','summaries','feedback','prompt_templates','users']]
t,s,p,u=index(T,'transcript_id'),index(S,'summary_id'),index(P,'template_id'),index(U,'user_id')
index(F,'feedback_id'); assert len({r['summary_id'] for r in F})==len(F)
for r in S: assert r['transcript_id'] in t and r['template_id'] in p and r['user_id'] in u
for r in F: assert r['summary_id'] in s and r['user_id'] in u and s[r['summary_id']]['status']=='completed'
models=defaultdict(set)
for r in S: models[r['template_id']].add(r['ai_model'])
assert all(len(v)==1 for v in models.values())
# All distinct comments were manually inspected: no personal names or emails appear.
comments=[]
for r in F:
 a=s[r['summary_id']]
 comments.append(dict(comment=r['comment'].strip(),rating=int(r['rating']),template=p[a['template_id']]['name'],model=a['ai_model']))
mapping={"Incorrectly flagged a safeguarding concern that wasn't there.":'Incorrect safeguarding flag','Some of the names were mixed up in the output.':'Names mixed up','Missed some key details about the risk assessment.':'Missing risk-assessment details'}
concerns=[]
for exact,label in mapping.items():
 rows=[r for r in comments if r['comment']==exact]
 concerns.append(dict(label=label,match=exact,count=len(rows),low=sum(r['rating']<=3 for r in rows),high=sum(r['rating']>=4 for r in rows)))
configs=[]
for v in sorted(P,key=lambda r:r['name']):
 rows=[r for r in comments if r['template']==v['name']]
 configs.append(dict(name=v['name'],n=len(rows),average=statistics.mean(r['rating'] for r in rows),distribution=[sum(r['rating']==i for r in rows) for i in range(1,6)],written=sum(bool(r['comment']) for r in rows),feedback=[dict(text=text,count=count) for text,count in sorted(Counter(r['comment'] for r in rows if r['comment']).items(),key=lambda pair:(-pair[1],pair[0]))]))
def band(w): return 0 if w<3000 else 1 if w<6000 else 2 if w<9000 else 3
assert [band(x) for x in [0,2999,3000,5999,6000,8999,9000]]==[0,0,1,1,2,2,3]
def percentile(values, q):
 ordered=sorted(values)
 position=(len(ordered)-1)*q
 lower=int(position)
 upper=min(lower+1,len(ordered)-1)
 return ordered[lower]+(ordered[upper]-ordered[lower])*(position-lower)
assert percentile([0,10],.9)==9
lengths=[]
for i,label in enumerate(['Under 3,000','3,000–5,999','6,000–8,999','9,000+']):
 times=[float(r['processing_time_ms'])/1000 for r in S if r['status']=='completed' and r['processing_time_ms'] and band(int(t[r['transcript_id']]['word_count']))==i]
 lengths.append(dict(label=label,n=len(times),median=statistics.median(times),p90=percentile(times,.9)))
linked=defaultdict(list)
for r in S: linked[r['transcript_id']].append(r)
ref=max(datetime.fromisoformat(r['created_at']) for r in S)
inprogress=sorted([dict(created=r['created_at'],ageDays=(ref-datetime.fromisoformat(r['created_at'])).total_seconds()/86400) for r in S if r['status']=='in_progress'],key=lambda r:r['created'])
coverage=dict(transcripts=len(T),attempts=len(S),feedback=len(F),written=sum(bool(r['comment']) for r in comments),average=statistics.mean(r['rating'] for r in comments),distinctLinked=len(linked),single=sum(len(v)==1 for v in linked.values()),multiple=sum(len(v)>1 for v in linked.values()),multipleTemplates=sum(len({r['template_id'] for r in v})>1 for v in linked.values()),sameTemplateRepeated=sum(any(n>1 for n in Counter(r['template_id'] for r in v).values()) for v in linked.values()),unlinked=len(T)-len(linked),crossCouncil=sum(len({u[r['user_id']]['council'] for r in v})>1 for v in linked.values()),councils=len({v['council'] for v in U}),users=len(U))
result=dict(coverage=coverage,concerns=concerns,configs=configs,lengths=lengths,status=dict(Counter(r['status'] for r in S)),reference=ref.isoformat(sep=' '),olderInProgress=sum(x['ageDays']>30 for x in inprogress))
assert [x['n'] for x in lengths]==[47,41,50,35]
assert [round(x['median'],3) for x in lengths]==[8.128,19.053,34.990,47.088]
assert [(x['count'],x['high']) for x in concerns]==[(6,4),(5,2),(3,1)]
assert result['status']=={'completed':173,'failed':15,'in_progress':12}
assert sum(x['ageDays']>30 for x in inprogress)==11
assert [coverage[k] for k in ['transcripts','attempts','feedback','written','distinctLinked','single','multiple','multipleTemplates','sameTemplateRepeated','unlinked','crossCouncil']]==[200,200,150,79,131,80,51,50,1,69,39]
assert [round(c['average'],2) for c in configs]==[4.41,4.50,3.76,3.41,3.71,3.55,3.92,4.23]
(root/'src'/'data.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['configs','concerns','inprogress']},indent=2))
print('All supplied headline figures reconciled; unique keys and foreign keys valid. No join inflation.')
