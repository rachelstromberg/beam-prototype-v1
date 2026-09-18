"""Package only the reviewed app and handout; exclude originals and earlier versions."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
files = ['README.md', 'LEADERSHIP_GUIDE.pdf', 'streamlit_app.py', 'requirements.txt', 'VALIDATION.md', '.gitignore']
assets = ['index.html', 'styles.css', 'app.js', 'copy.js', 'data.json']
files += [f'{folder}/{name}' for folder in ('public', 'dist') for name in assets]
files += [f'scripts/{name}' for name in ('build.py', 'prepare_data.py', 'package.py', 'render_briefing.py')]
files += ['tests/test_data.py']
destination = ROOT / 'magic-notes-customer-review.zip'
with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
    for relative in files:
        archive.write(ROOT / relative, 'magic-notes-customer-review/' + relative)
with ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(files)
print(f'Packaged {len(files)} files: {destination.name}')
