# Review build validation

Checked 18 September 2026. Revised after Rachel's manual review; checks below include the updated build.

## Data

- Source keys and foreign-key relationships validated before aggregation.
- 200 generation attempts; 150 ratings; 79 written comments; 131 linked transcripts; average rating 3.9067/5.
- All eight workflow distributions reconcile with their rating counts and averages. Grouped comments retain all 79 records; each phrase appears only once per workflow.
- Three reported-concern splits reconcile to 2/4, 3/2, and 2/1 for ratings 1–3 versus 4–5: seven of fourteen reports accompany higher ratings.
- Completed-generation counts by recording duration: 58, 62, and 53. Medians: 9.9765, 24.2205, and 44.028 seconds. 90th percentiles: 18.748, 45.7087, and 66.1496 seconds.
- Included aggregate data excludes staff details and individual feedback, transcript, and summary records.
- `tests/test_data.py` passed, including full regeneration/reconciliation against the source extracts and percentile interpolation checks.

## Browser

- Tested all eight workflow selections against the visible selected heading and grouped feedback.
- Confirmed the selected workflow is retained when switching away and returning.
- Checked all three priority views and the complete rating split, without requiring a toggle.
- Checked arrow-key and Home navigation between priority tabs, focus styling, and mobile focus movement to selected feedback.
- Checked laptop presentation and all three views at 390-pixel mobile width; no horizontal page overflow.
- Inspected timing labels, median bars, and slower-wait markers visually.
- Browser reported no errors or warnings during interaction checks.

## Delivery

- Build copies an explicit allowlist of five assets to `dist`.
- A one-page PDF leadership use guide accompanies the runnable app and README.
- Packaging uses an explicit file list and excludes original extracts, the original task brief, earlier versions, and dependencies.
- A local preview is provided for the next manual review. No changes have been published to the deployed V1.

## Review revisions

- Reconciled associated rating counts for every grouped comment with the original extracts; all 79 written responses retained.
- Checked updated copy, all eight workflow selections, all three action panels, and timing labels in the browser.
- Confirmed the revised views fit a 390-pixel mobile viewport without horizontal overflow.
- Browser reported no errors or warnings during the revised workflow checks.
- Created and visually inspected the one-page PDF use guide, including decision context, rationale, follow-up design, and sample limitations.
- Removed the overview statistics strip, opening scope line, and closing question. Folded the useful review action into the first recommended next steps panel.

## Streamlit release

- Added a separate Streamlit entry point using the same five public assets and an adaptive component height.
- JavaScript syntax and Python entry-point compilation passed.
- Published the separate customer-review branch to https://beam-magic-notes-customer-review.streamlit.app/. The original release/v1 app is unchanged.
- Verified the live workflow selector, accuracy view, timing view, and revised action panels.
- Package includes the runnable application, README, and LEADERSHIP_GUIDE.pdf required for the prototype exercise.
