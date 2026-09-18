MAGIC NOTES PROTOTYPE — HOW TO RUN

Requirements
Node.js version 20 or newer. No dependency installation is needed.

Start the application
1. Extract this ZIP completely.
2. Open a terminal in the extracted submission folder.
3. Run:

   cd application
   node scripts/serve.mjs

4. Open http://127.0.0.1:5173 in a browser.

Keep the terminal running while viewing the prototype. Press Ctrl+C to stop.
Do not open index.html directly; the local server loads the bundled data.

Production build
From the application folder, after stopping the server, run:

   node scripts/build.mjs
   node scripts/serve.mjs dist

Then open http://127.0.0.1:5173.

What is included
- LEADERSHIP_BRIEFING.pdf: one-page leadership handout on the tool, findings, and next steps.
- LEADERSHIP_BRIEFING.docx: editable Word version of the handout.
- application/: runnable source, sanitized data, dependency manifest, and lockfile.
- application/README.md: metric definitions, editing guidance, and verification details.

About the prototype
This is a local, clickable presentation of historical data across three councils.
The template table lets readers explore grouped feedback behind the ratings.
It requires no backend, account, API key, or external AI service.
The task brief, raw CSVs, personal user records, and credentials are excluded.
