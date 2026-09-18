# Versioning and deployment

This repository keeps the editable prototype at the root and permanent releases in `versions/`.

## Version 1

- Frozen application: `versions/v1/index.html`
- Streamlit entrypoint: `versions/v1/streamlit_app.py`
- Release branch: `release/v1`
- Immutable release tag: `v1.0.0`

The frozen directory contains a self-contained application, its source, version metadata, and a SHA-256 manifest. The snapshot builder refuses to overwrite an existing version. The verification workflow checks every snapshot and compares released versions with their tags.

GitHub must protect `release/**` from updates and deletions, and immutable releases must be enabled. Streamlit deploys Version 1 from the `release/v1` branch. Work on `main` cannot update that deployment.

## Create a later version

1. Make and validate changes on `main`.
2. Run `node scripts/freeze-version.mjs v2 2.0.0`. Use the next unused version number; the command stops if the directory already exists.
3. Commit the new snapshot to `main`.
4. Create `release/v2` at that commit and tag it `v2.0.0`.
5. Publish an immutable GitHub release for the tag.
6. Create a new Streamlit app that targets branch `release/v2` and entrypoint `versions/v2/streamlit_app.py`. Choose a new custom app URL ending in `-v2`.
7. Add the final GitHub release and Streamlit URLs to `DEPLOYMENTS.md`.

Never reuse a version directory, branch, tag, release, or Streamlit app. Each deployed version gets a new set.
