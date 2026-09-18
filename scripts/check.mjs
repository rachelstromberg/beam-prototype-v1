import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const d=JSON.parse(readFileSync('src/data.json','utf8'));
assert.equal(d.configs.reduce((n,r)=>n+r.n,0),150);
assert.equal(d.coverage.written,79);
assert.equal(d.configs.reduce((n,r)=>n+r.written,0),79);
for(const r of d.configs){
 assert.equal(r.feedback.reduce((n,v)=>n+v.count,0),r.written);
 assert.equal(new Set(r.feedback.map(v=>v.text)).size,r.feedback.length);
 assert.ok(r.feedback.every(v=>v.count>0 && v.text.trim().length>0));
}
const early=d.configs.find(r=>r.name==='Early Help Assessment Note');
assert.equal(early.written,6);
assert.equal(early.feedback.find(r=>r.text.startsWith('Incorrectly flagged')).count,2);
assert.equal(early.feedback.find(r=>r.text.startsWith('The summary was too long')).count,2);
for(const r of d.configs){assert.equal(r.distribution.reduce((a,b)=>a+b,0),r.n);assert.ok(Math.abs(r.distribution.reduce((n,v,i)=>n+v*(i+1),0)/r.n-r.average)<1e-12)}
assert.equal(d.concerns.reduce((n,r)=>n+r.count,0),14);
assert.equal(d.concerns.reduce((n,r)=>n+r.high,0),7);
for(const r of d.concerns){assert.equal(r.low+r.high,r.count);assert.ok(r.match.length>0)}
assert.equal(d.lengths.reduce((n,r)=>n+r.n,0),173);
assert.equal(Object.values(d.status).reduce((a,b)=>a+b,0),200);
assert.equal(d.olderInProgress,11);
assert.deepEqual(d.lengths.map(r=>Number(r.p90.toFixed(4))),[14.8196,32.238,52.6757,71.745]);
for(const r of d.lengths) assert.ok(r.p90>=r.median);
assert.ok(!/"(?:email|first_name|last_name|user_id|transcript_id|summary_id|feedback_id)"|sk-[a-zA-Z0-9_-]{15}/.test(JSON.stringify(d)));
for(const file of ['src/app.js','src/narrative.js','scripts/serve.mjs'])execFileSync(process.execPath,['--check',file]);
console.log('Checks passed: denominators, distributions, concern mapping, statuses, privacy fields and JavaScript syntax.');
