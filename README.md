# Magic Notes customer review

Live prototype: https://beam-magic-notes-customer-review.streamlit.app/

A clickable customer leadership review: target support where ratings are lower, look beyond ratings, and set expectations for generation time. It uses the supplied historical sample across three local authorities.

## Run with Streamlit

Requires Python 3.10 or later. From the extracted project folder:

```sh
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

Open the local address printed by Streamlit. The interface uses the bundled aggregate data; no API key or original data files are needed.

## Run without installing packages

Requires Python 3.9 or later and a current browser. No package installation, API key, login, or internet connection is needed for the app.

From the extracted project folder:

```sh
python3 -m http.server 5186 --bind 127.0.0.1 --directory dist
```

On Windows, use `py -3` instead of `python3`. Open **http://127.0.0.1:5186/**. If the port is already in use, choose another unused port and use the same number in the browser. Stop the server with Ctrl+C. Serve `dist`, not the project root. Double-clicking the HTML file will not load the prepared data.

## Use

- The three priority tabs replace the main view. Arrow keys, Home, and End navigate the tabs.
- Select a workflow to see its rating distribution and grouped comments. The overall comparison and recommendation remain in place. Positive and critical comments are included; repeated phrases appear once with counts and their associated rating breakdowns.
- Open or close written feedback and methodology as needed. Accuracy and timing comparisons show their meaning without controls or hovering.

This is a local prototype. It does not update cases, assign work, call an AI model, or monitor live production.

## Included files

- `dist/`: the ready-to-run application, containing five public assets.
- `public/`: editable HTML, CSS, JavaScript, and anonymised aggregate data.
- `LEADERSHIP_GUIDE.pdf`: a one-page customer leadership summary and use guide, explaining the findings, their limits, and how to plan a follow-up.
- `streamlit_app.py` and `requirements.txt`: the Streamlit entry point and pinned dependency.
- `scripts/build.py`: copies the five allowed public assets into `dist`.
- `scripts/prepare_data.py`: rebuilds aggregates from the five original CSVs.
- `tests/test_data.py`: source reconciliation and aggregation checks.
- `VALIDATION.md`: the checks performed for this review build.

## Rebuild and verify

```sh
python3 scripts/build.py
python3 tests/test_data.py
```

The original extracts are intentionally not included in the submission. Prepared aggregates are sufficient to build and run the app. To regenerate them, supply the authorised originals in a folder containing `summaries.csv`, `transcripts.csv`, `prompt_templates.csv`, `feedback.csv`, and `users.csv`:

```sh
python3 scripts/prepare_data.py --source /path/to/db_extracts
python3 tests/test_data.py /path/to/db_extracts
python3 scripts/build.py
```

Preparation validates keys, joins, reference counts, and duration bands before writing data. A discrepancy stops the script rather than silently changing the expected findings. Scripts use Python's standard library except the optional `render_briefing.py`, which requires ReportLab to regenerate the PDF. The PDF is already included; ReportLab is not needed to run the app. Its content is maintained in `scripts/render_briefing.py`.

## Interpretation

Ratings are observed satisfaction, not verified accuracy. Reported concerns require investigation. A completed generation is not necessarily reviewed, accepted, or submitted. Some transcripts produced multiple outputs; the transcript table does not establish council ownership. Differences between tasks, small samples, and repeated transcripts limit comparison. Each template has one model in the extract, so effects cannot be isolated.

The app calculates all eight workflow averages and distributions from feedback records. Written feedback is grouped by exact wording after trimming whitespace; duplicate records remain in the counts. Processing time uses completed generations and the associated recording duration. The 90th percentile uses linear interpolation at `(n−1) × 0.9`; displayed seconds are rounded. Times are generation times, not transcription time or time saved.

The supplied metadata and feedback do not include source conversations or generated notes. Proposed actions identify what to investigate together, and proposed success measures need baselines. Detailed coverage is available within the prototype.

The package excludes original source extracts, the credential-bearing task brief, staff names, email addresses, individual records, and previous versions. The published V1 remains separate.

## Separate Streamlit deployment

Create a new Community Cloud app with `streamlit_app.py` as its main file. This version is prepared on a separate `customer-review` branch of `rachelstromberg/beam-prototype-v1`. The original app remains on `release/v1`, using `versions/v1/streamlit_app.py`. Do not change the original app’s branch or entry point.

## Task deliverables

The ZIP contains the runnable application, this README, and the customer leadership summary/use guide as a PDF. The guide adds context for interpreting the sample and organising a useful follow-up, rather than repeating the interface. Original extracts and superseded handouts are excluded.
