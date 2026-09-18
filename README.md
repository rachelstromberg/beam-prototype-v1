# Magic Notes — leadership review prototype

A focused, clickable presentation of four improvement priorities for dependable documentation and frontline experience. It uses the supplied historical sample across three councils, with plain JavaScript, HTML, and CSS. No installation, backend, external fonts, analytics, or AI services are required.

The repository also contains a frozen Streamlit-ready Version 1. See `VERSIONING.md` for the release and deployment model and `DEPLOYMENTS.md` for permanent links.

## Published Version 1

- Live app: **https://beam-magic-notes-v1.streamlit.app/**
- Immutable GitHub release: **https://github.com/rachelstromberg/beam-prototype-v1/releases/tag/v1.0.0**
- Frozen branch: `release/v1`

Future versions use a new `versions/vN/` directory, `release/vN` branch, semantic-version tag, immutable GitHub release, and Streamlit app URL. Version 1 is never redeployed from `main`.

## Run

Requires **Node.js 20+**. Extract the ZIP, open a terminal in `magic-notes-prototype`, and run:

```sh
node scripts/serve.mjs
```

Open **http://127.0.0.1:5173**. Stop with Ctrl+C. The server binds only to this computer and serves an explicit list of browser assets, never raw CSVs or the brief.

Build and preview production files, after stopping the development server:

```sh
node scripts/build.mjs
node scripts/serve.mjs dist
```

Optional npm equivalents: `npm run dev`, `npm run build`, `npm run preview`, and `npm run check`. The included manifest and lockfile intentionally contain zero dependencies. On macOS/Linux, use `PORT=5174 node scripts/serve.mjs` if port 5173 is occupied.

## Run the frozen Streamlit release

Version 1 is self-contained in `versions/v1/`. With Python 3.10 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r versions/v1/requirements.txt
.venv/bin/streamlit run versions/v1/streamlit_app.py
```

Open **http://127.0.0.1:8501**. Streamlit Community Cloud uses the same entrypoint. The editable root app and the frozen release render the same prototype; the frozen release bundles its CSS, JavaScript, and sanitized data into one registered Streamlit component.

## Edit

- `src/narrative.js`: priority headings, evidence statements, actions, success measures, and next questions.
- `src/data.json`: sanitized aggregates and grouped feedback phrases.
- `src/app.js`: page structure, template selection, chart rendering, and methodology text.
- `src/styles.css`: typography, colors, and responsive layout.
- `LEADERSHIP_SUMMARY.md`: standalone leadership summary.

Review editorial statements when changing the data. Rebuild after edits if viewing `dist`.

## Interaction and design

The four large links beside the title are the single navigation list. The template table is ordered by average rating and defaults to Early Help. Select any row to see all of that template's written feedback, grouped by exact phrase with counts. Positive feedback is retained. The selected row has a check mark and an accessible pressed state. Native buttons work with Tab and Enter/Space. On narrow screens, selection moves focus to the feedback panel; “Back to templates” returns to the table.

This exploration asks **what to test within a weaker template**, rather than repeating the same ranking in two charts. There are no arbitrary filters, individual record lists, simulated recovery actions, or claims about absent processes. Median bars and 90th-percentile marks show typical and slower processing times without another control. Qualifications and definitions are in the methodology disclosure.

## Definitions and reconciliation

- **Attempts and joins:** 200 summary rows. Unique primary keys and all referenced keys validated. Many-to-one joins to transcripts, templates, and users preserve 200 attempts.
- **Ratings:** 150 feedback rows, each linked to a different completed summary here. Average = arithmetic mean, 3.9066667, shown as 3.91/5. There are 79 nonempty written comments. “Rated 1–2” shows the count of ratings of 1 or 2 out of all ratings for that template. Grouped feedback counts sum to each template's written-comment count, and to 79 overall.
- **Reported concerns:** exact matches after trimming whitespace: “Incorrectly flagged a safeguarding concern that wasn't there.” (6; 4 rated 4–5); “Some of the names were mixed up in the output.” (5; 2 rated 4–5); “Missed some key details about the risk assessment.” (3; 1 rated 4–5). These are non-exhaustive reported concerns, not verified errors.
- **Template comparisons:** use the template associated with each attempt. Source validation confirms one recorded `summaries.ai_model` per template. Models are omitted from the interface. The data cannot isolate template or model effects or establish historical prompt-version provenance.
- **Processing times:** completed attempts with recorded milliseconds, divided by 1,000. Word bands are `[0,3000)`, `[3000,6000)`, `[6000,9000)`, and `[9000,infinity)`. Counts: 47, 41, 50, and 35. Medians: 8.128, 19.053, 34.990, and 47.088 seconds. The 90th percentile uses linear interpolation at zero-based position `(n−1) × 0.9`: 14.8196, 32.238, 52.6757, and 71.745 seconds. The chart rounds to whole seconds and uses a zero-based 0–90-second scale. Timestamp differences are not processing latency.
- **Statuses:** 173 completed, 15 failed, and 12 in progress, divided by all 200 attempts. Eleven in-progress records predate **2025-12-14 11:40:06** by more than 30 days. That is the latest summary creation timestamp, not a confirmed export date. Source timezone is unspecified; age is not observed waiting duration.
- **Coverage:** 200 transcript records; 131 link to attempts. Of those, 80 have one attempt, and 51 have multiple. Fifty link to multiple templates; one has two attempts with the same template. Sixty-nine have **no linked summary in supplied extract**. Thirty-nine link through summary users to multiple councils. These facts do not establish failures, retries, independence, ownership, collaboration, attendance, or authorized sharing.

## Reproduce and verify

The app runs from bundled sanitized JSON. To recalculate from the original files, place the five CSVs in a local `data/` directory and run `python3 scripts/derive.py` with Python 3.8+. This standard-library script checks joins, calculates metrics, and writes the sanitized JSON. The raw CSVs are deliberately excluded from the ZIP. All original headline figures reconcile; no discrepancies were forced to match.

`node scripts/check.mjs` checks denominators, distributions, grouped feedback totals, concern counts, statuses, percentiles, identity-field exclusions, and JavaScript syntax. The production build runs these checks. All eight template selections, keyboard selection, mobile return navigation, and methodology disclosure were checked in the running app. Layouts were visually inspected at desktop and phone widths. A clean extraction of the ZIP builds successfully.

All supplied comment phrases were inspected before inclusion. If changing the source, review the new text for personal information; this is not an automated PII detector. Packaging includes runnable source, scripts, sanitized data, manifest/lockfile, this README, and the leadership summary. It excludes raw user records, CSVs, credentials, the task brief, and dependency folders.

## Interpretation and proposed measures

These are historical proposals, not live monitoring or proof of causes, product-wide error rates, productivity gains, or service-user outcomes. Current processes are not described. Establish baselines before setting numeric improvement targets.

Accuracy checks should use the same representative cases and practitioner checklist for current and revised prompts. Measure active correction minutes per note. Define fixed review cohorts for reported-issue resolution and failure recovery; report unresolved cases alongside time-to-recovery among recovered cases. For waiting pilots, survey task interruption and track successful return among sessions that leave while processing, using a predefined follow-up period.

Additional checks found 5/55, 3/49, 4/56, and 3/40 failed attempts across ascending word-count bands, with no increasing pattern. Median input length across template groups ranged from 4,770.5 to 6,784 words, counting distinct transcripts within each group. Median completed-output length ranged from 657 to 1,150 words. These descriptive differences do not establish template effects or a further actionable finding, so they were not added to the leadership charts.
