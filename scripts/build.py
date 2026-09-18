"""Build the five public assets; no installation or external requests."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ('index.html', 'styles.css', 'app.js', 'copy.js', 'data.json')
data = json.loads((ROOT / 'public/data.json').read_text())
assert data['coverage']['feedback'] == sum(w['n'] for w in data['workflows'])
assert sum(r['count'] for r in data['concerns']) == 14
(ROOT / 'dist').mkdir(exist_ok=True)
for name in FILES:
    shutil.copy2(ROOT / 'public' / name, ROOT / 'dist' / name)
assert {p.name for p in (ROOT / 'dist').iterdir()} == set(FILES), 'Unexpected public assets'
print('Customer review built in dist/ — five public assets.')
