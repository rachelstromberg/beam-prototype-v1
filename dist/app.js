import { priorities } from './copy.js';

const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fixed = (value, decimals = 2) => Number(value).toFixed(decimals);
let data, current = 0, selected = 0;

function workflowComparison() {
  return `<figure class="chart-card"><figcaption>User ratings by workflow</figcaption>
    <div class="workflow-head" aria-hidden="true"><span>Workflow</span><span class="workflow-scale"><span>1</span><span>5</span></span><span>Avg. (ratings)</span></div>
    <ul class="workflow-rows">${data.workflows.map((w, i) => `<li>
      <button class="workflow-button" data-workflow="${i}" aria-pressed="${i === selected}" aria-controls="workflow-feedback" aria-label="Explore ${esc(w.name)}: ${w.n ? fixed(w.average) + ' out of 5, ' + w.n + ' ratings' : 'no ratings'}">
        <span class="workflow-name">${esc(w.name)}</span>
        <span class="workflow-track" aria-hidden="true">${w.n ? `<span class="workflow-dot" style="left:${(w.average - 1) / 4 * 100}%"></span>` : ''}</span>
        <span class="workflow-value"><strong>${w.n ? fixed(w.average) : '—'}</strong> <small>(${w.n})</small></span>
      </button></li>`).join('')}</ul></figure>`;
}

function feedbackContent() {
  const w = data.workflows[selected];
  const maximum = Math.max(1, ...w.distribution);
  return `<h3 class="feedback-title" id="feedback-title" tabindex="-1">${esc(w.name)}</h3>
    <p class="feedback-count">${w.n} ratings · ${w.written} written comments</p>
    <figure class="distribution"><figcaption>Ratings, from 1 to 5 stars</figcaption>
      <div role="img" aria-label="${w.distribution.map((n, i) => `${i + 1} star${i ? 's' : ''}: ${n} ratings`).join('; ')}">
        <div class="distribution-bars" aria-hidden="true">${w.distribution.map(n => `<div class="distribution-column"><strong>${n}</strong><span class="distribution-bar" style="height:${n / maximum * 62}px"></span></div>`).join('')}</div>
        <div class="distribution-labels" aria-hidden="true">${[1,2,3,4,5].map(n => `<span>${n} ★</span>`).join('')}</div>
      </div>
    </figure>
    ${w.written ? `<details class="feedback-details" open><summary>Written feedback<span class="feedback-summary">${w.written} comments · ${w.feedback.length} distinct responses</span></summary>
      <ul class="feedback-phrases">${w.feedback.map(f => `<li><div><span>“${esc(f.text)}”</span><div class="comment-ratings">${f.ratings.map((count, i) => count ? `<span aria-label="${count} ${count === 1 ? 'response' : 'responses'} rated ${i + 1} out of 5">${i + 1} ★${count > 1 ? ` × ${count}` : ''}</span>` : '').join('')}</div></div><strong aria-label="${f.count} comment${f.count !== 1 ? 's' : ''}">${f.count}</strong></li>`).join('')}</ul>
    </details>` : '<p class="empty">No written feedback for this workflow.</p>'}`;
}

function supportView() {
  return `<div class="workspace-grid">${workflowComparison()}
    <section class="feedback-panel" id="workflow-feedback" aria-labelledby="feedback-title">${feedbackContent()}</section>
  </div>`;
}

function accuracyView() {
  const max = Math.max(...data.concerns.map(r => r.count));
  return `<div class="chart-layout"><figure class="chart-card"><figcaption>Reported concerns, split by user rating</figcaption>
    <div class="legend"><span><i class="key low" aria-hidden="true"></i>Rated 1–3</span><span><i class="key high" aria-hidden="true"></i>Rated 4–5</span></div>
    ${data.concerns.map(r => `<div class="concern-row"><div class="bar-label">${esc(r.label)}<small>${r.count} reports</small></div>
      <div class="stack-area" role="img" aria-label="${esc(r.label)}: ${r.low} reports rated 1–3, ${r.high} rated 4–5">
        <div class="stack" style="width:${r.count / max * 100}%" aria-hidden="true"><span class="low" style="width:${r.low / r.count * 100}%">${r.low}</span><span class="high" style="width:${r.high / r.count * 100}%">${r.high}</span></div>
      </div></div>`).join('')}
    <div class="bar-axis" aria-hidden="true"><span>0</span><span>${max / 2}</span><span>${max} reports</span></div>
  </figure></div>`;
}

function waitsView() {
  const max = Math.ceil(Math.max(...data.waits.map(w => w.p90)) / 30) * 30;
  return `<div class="chart-layout"><figure class="chart-card"><figcaption>Summary-generation time by recording length</figcaption>
    <div class="legend"><span><i class="key median-key" aria-hidden="true"></i>Median</span><span><i class="percentile-key" aria-hidden="true"></i>90% completed within</span></div>
    ${data.waits.map(w => `<div class="wait-row"><div class="bar-label">${esc(w.label)}<small>${w.n} completed generations</small></div>
      <div class="wait-track" role="img" aria-label="${esc(w.label)}: median ${fixed(w.median,1)} seconds; 90 percent completed within ${fixed(w.p90,1)} seconds">
        <div class="wait-bar" style="width:${w.median / max * 100}%" aria-hidden="true"></div>
        <span class="median-value" style="left:${w.median / max * 100}%" aria-hidden="true">${Math.round(w.median)}s</span>
        <div class="p90-mark" style="left:${w.p90 / max * 100}%" aria-hidden="true"><strong>${Math.round(w.p90)}s</strong></div>
      </div></div>`).join('')}
    <div class="bar-axis" aria-hidden="true"><span>0</span><span>${max / 2}</span><span>${max} seconds</span></div>
  </figure></div>`;
}

function action(p) {
  return `<aside class="next-step" aria-labelledby="next-step-title">
    <h3 id="next-step-title" class="next-step-title">Recommended next steps</h3>
    <div><h4>What your team can do</h4><p>${esc(p.council)}</p></div>
    <div><h4>Where Beam can help</h4><p>${esc(p.beam)}</p></div>
    <div class="measure"><h4>How we would measure success</h4><ul>${p.measure.map(m => `<li>${esc(m)}</li>`).join('')}</ul></div>
  </aside>`;
}

function methodology() {
  const c = data.coverage;
  return `<div class="supporting">
    <details><summary>Methodology & data coverage</summary><div class="method-grid">
      <div><h3>Scope</h3><p>Historical sample across ${c.councils} local authorities: ${c.transcripts} transcript records, ${c.attempts} generation attempts linked to ${c.linked} distinct transcripts, and ${c.feedback} ratings. ${c.written} ratings include written feedback. These extracts contain metadata and feedback, not original transcripts or generated notes.</p>
        <p>Multiple outputs may use the same transcript. The transcript table has no council ownership field. These data do not establish causes, time saved, or service-user outcomes. Existing review processes are not described; the proposed actions do not assume they are absent.</p></div>
      <div><h3>Ratings and feedback</h3><p>Workflow averages use all ratings for each template; the five bars show their counts. Templates are ordered by observed average, with sample sizes visible. Small samples, different tasks, and repeated transcripts limit comparison. Each template has one recorded model, so the effects cannot be separated.</p>
        <p>The three lowest-rated workflows provide a manageable starting point, not a statistical cutoff. Child & Family is close behind Housing, at 3.76 versus 3.71.</p><p>Identical comments are grouped after trimming whitespace, with every feedback record retained in the count. Positive and critical feedback are both included. Each response shows its associated ratings; × indicates repeated responses at that rating. The source does not establish whether comments came from a dropdown.</p></div>
      <div><h3>Reported concerns</h3><p>The three categories match these phrases exactly: ${data.concerns.map(r => `“${esc(r.phrase)}”`).join('; ')} These are reported concerns, not verified errors or an exhaustive measure of quality. High ratings mean 4 or 5 stars; the other group is 1–3 stars.</p>
        <p>These reports were selected because incorrect names, false safeguarding flags, and missing risk details could affect how a case is understood or acted on. This is a judgment about potential consequences, not a frequency or verified severity ranking. Other reported problems may also matter.</p><p>Proposed success measures require representative reviews and a baseline. A generation marked completed has not necessarily been reviewed, accepted, or submitted.</p></div>
      <div><h3>Generation times and incomplete work</h3><p>Timing uses all ${data.statuses.completed} completed generations, linking their processing time to the recording duration. Bands are at most 30 minutes, over 30 to 60 minutes, and over 60 minutes. Processing milliseconds are converted to seconds. Medians and 90th percentiles are calculated within each band; percentiles use linear interpolation at (n−1) × 0.9. Displayed times are rounded. The slower-wait marker describes this sample, not a service guarantee.</p>
        <p>There are ${data.statuses.failed} failed attempts and ${data.statuses.in_progress} marked in progress; these are excluded from timing comparisons, and the extract does not establish whether they relate to long waits. ${c.noCompleted} linked transcripts have no completed output in the extract. ${c.unlinked} transcripts have no generation record linked. These are historical statuses, not a verified live backlog.</p></div>
    </div></details></div>`;
}

function selectWorkflow(index) {
  if (!Number.isInteger(index) || !data.workflows[index]) return;
  selected = index;
  document.querySelectorAll('[data-workflow]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.workflow) === selected)));
  document.querySelector('#workflow-feedback').innerHTML = feedbackContent();
  document.querySelector('#selection-status').textContent = `Showing ratings and feedback for ${data.workflows[selected].name}.`;
  if (window.matchMedia('(max-width: 760px)').matches) {
    const title = document.querySelector('#feedback-title');
    title.focus({preventScroll: true});
    title.scrollIntoView({block:'start', behavior:'instant'});
  }
}

function renderView(index) {
  current = index;
  document.querySelector('#selection-status').textContent = '';
  const p = priorities[index];
  document.querySelectorAll('[data-priority]').forEach(button => {
    const active = Number(button.dataset.priority) === index;
    button.setAttribute('aria-selected', String(active));
    button.tabIndex = active ? 0 : -1;
  });
  const view = document.querySelector('#review');
  view.setAttribute('aria-labelledby', `tab-${p.id}`);
  view.innerHTML = `<div class="section-heading"><h2>${esc(p.title)}</h2>${p.evidence ? `<p>${esc(p.evidence)}</p>` : ''}</div>${[supportView,accuracyView,waitsView][index]()}${action(p)}`;
  document.querySelectorAll('[data-workflow]').forEach(button => button.addEventListener('click', () => selectWorkflow(Number(button.dataset.workflow))));
}

async function init() {
  const response = await fetch('./data.json');
  if (!response.ok) throw new Error('The prepared data could not be loaded.');
  data = await response.json();
  const c = data.coverage;
  document.querySelector('#app').innerHTML = `<header class="masthead"><div class="wordmark">Magic Notes</div><div class="context">Customer leadership review</div></header>
    <main><div class="hero"><h1>Three ways to get more from Magic Notes</h1></div>
      <div class="priority-nav" role="tablist" aria-label="Improvement priorities">${priorities.map((p,i) => `<button type="button" role="tab" id="tab-${p.id}" data-priority="${i}" aria-selected="${i === 0}" aria-controls="review" tabindex="${i === 0 ? 0 : -1}"><span aria-hidden="true">0${i + 1}</span>${esc(p.nav)}</button>`).join('')}</div>
      <section id="review" role="tabpanel" aria-labelledby="tab-support" tabindex="0"></section>
      <p id="selection-status" class="sr-only" role="status" aria-live="polite"></p>
      ${methodology()}
    </main><footer>Magic Notes · Customer and Beam review</footer>`;
  document.querySelectorAll('[data-priority]').forEach(button => {
    button.addEventListener('click', () => renderView(Number(button.dataset.priority)));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (current + 1) % priorities.length;
      else if (event.key === 'ArrowLeft') next = (current - 1 + priorities.length) % priorities.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = priorities.length - 1;
      else return;
      event.preventDefault();
      renderView(next);
      document.querySelector(`[data-priority="${next}"]`).focus();
    });
  });
  renderView(0);
}

init().catch(error => {
  document.querySelector('#app').innerHTML = `<main class="error"><h1>The review could not load.</h1><p>Use the local server described in the README, then refresh this page.</p></main>`;
  console.error(error);
});
