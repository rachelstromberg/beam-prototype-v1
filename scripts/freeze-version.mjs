import {createHash} from 'node:crypto';
import {mkdir, readFile, readdir, stat, writeFile} from 'node:fs/promises';
import {basename, join, relative, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

const [versionName, semanticVersion] = process.argv.slice(2);

if (!/^v[1-9]\d*$/.test(versionName || '') || !/^\d+\.\d+\.\d+$/.test(semanticVersion || '')) {
  throw new Error('Usage: node scripts/freeze-version.mjs v<number> <semantic-version>');
}

const root = resolve(import.meta.dirname, '..');
const target = join(root, 'versions', versionName);

try {
  await stat(target);
  throw new Error(`${relative(root, target)} already exists. Frozen versions are never overwritten.`);
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}

const read = path => readFile(join(root, path), 'utf8');
const [sourceHtml, styles, sourceApp, dataText] = await Promise.all([
  read('index.html'),
  read('src/styles.css'),
  read('src/app.js'),
  read('src/data.json'),
]);
const {priorities, questions} = await import(pathToFileURL(join(root, 'src/narrative.js')));
const data = JSON.parse(dataText);
const sourcePackage = JSON.parse(await read('package.json'));
delete sourcePackage.scripts[`freeze:${versionName}`];
delete sourcePackage.scripts['verify:versions'];

const app = sourceApp
  .replace(
    "import {priorities, questions} from './narrative.js';",
    `const priorities=${JSON.stringify(priorities)};\nconst questions=${JSON.stringify(questions)};`,
  )
  .replace(
    "const response=await fetch('/src/data.json');\nif(!response.ok) throw new Error('Local evidence could not be loaded');\nconst data=await response.json(),c=data.coverage;",
    `const data=${JSON.stringify(data)},c=data.coverage;`,
  );

if (app.includes("from './narrative.js'") || app.includes("fetch('/src/data.json')")) {
  throw new Error('The source layout changed; refusing to create an incomplete snapshot.');
}

const resizeBridge = `
const sendToStreamlit=(type,data={})=>window.parent.postMessage({
  isStreamlitMessage:true,
  type,
  ...data
},'*');
const reportHeight=()=>sendToStreamlit('streamlit:setFrameHeight',{
  height:Math.ceil(document.body.scrollHeight)
});
sendToStreamlit('streamlit:componentReady',{apiVersion:1});
window.addEventListener('message',event=>{
  if(event.data?.type==='streamlit:render') reportHeight();
});
window.addEventListener('load',reportHeight);
new ResizeObserver(reportHeight).observe(document.body);
setTimeout(reportHeight,100);
`;

const description = sourceHtml.match(/<meta name="description" content="([^"]+)">/)?.[1] || '';
const title = sourceHtml.match(/<title>([^<]+)<\/title>/)?.[1] || 'Magic Notes';
const standalone = `<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#173d39"><meta name="description" content="${description}"><title>${title}</title><style>${styles}</style></head><body><a class="skip" href="#priorities">Skip to priorities</a><div id="app"><p class="loading">Loading the local evidence…</p></div><script>${app}\n${resizeBridge}<\/script></body></html>\n`;

await mkdir(join(target, 'source', 'src'), {recursive: true});
await Promise.all([
  writeFile(join(target, 'index.html'), standalone),
  writeFile(join(target, 'source', 'index.html'), sourceHtml),
  writeFile(join(target, 'source', 'src', 'styles.css'), styles),
  writeFile(join(target, 'source', 'src', 'app.js'), sourceApp),
  writeFile(join(target, 'source', 'src', 'data.json'), `${JSON.stringify(data, null, 2)}\n`),
  read('src/narrative.js').then(text => writeFile(join(target, 'source', 'src', 'narrative.js'), text)),
  writeFile(join(target, 'source', 'package.json'), `${JSON.stringify(sourcePackage, null, 2)}\n`),
  read('package-lock.json').then(text => writeFile(join(target, 'source', 'package-lock.json'), text)),
  read('scripts/build.mjs').then(text => writeFile(join(target, 'source', 'scripts', 'build.mjs'), text).catch(async error => {
    if (error.code !== 'ENOENT') throw error;
    await mkdir(join(target, 'source', 'scripts'), {recursive: true});
    await writeFile(join(target, 'source', 'scripts', 'build.mjs'), text);
  })),
]);

await mkdir(join(target, 'source', 'scripts'), {recursive: true});
for (const name of ['check.mjs', 'serve.mjs']) {
  await writeFile(join(target, 'source', 'scripts', name), await read(`scripts/${name}`));
}

const tag = `v${semanticVersion}`;
await writeFile(join(target, 'VERSION.json'), `${JSON.stringify({
  version: semanticVersion,
  label: `Version ${versionName.slice(1)}`,
  immutableTag: tag,
  streamlitEntrypoint: `versions/${versionName}/streamlit_app.py`,
  frozenAt: new Date().toISOString(),
}, null, 2)}\n`);

await writeFile(join(target, 'requirements.txt'), 'streamlit==1.64.0\n');
await writeFile(join(target, 'streamlit_app.py'), `from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Magic Notes · Version ${versionName.slice(1)}",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background: #f7f3ec; }
    .stMain { align-items: flex-start; }
    .block-container { max-width: none; padding: 0; }
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none; }
    iframe { display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

component_path = Path(__file__).resolve().parent
magic_notes = components.declare_component(
    "magic_notes_${versionName}", path=str(component_path)
)
magic_notes(key="magic-notes-${versionName}")
`);

async function filesUnder(directory) {
  const entries = await readdir(directory, {withFileTypes: true});
  const paths = [];
  for (const entry of entries) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) paths.push(...await filesUnder(path));
    else if (entry.name !== 'SHA256SUMS') paths.push(path);
  }
  return paths.sort();
}

const files = await filesUnder(target);
const manifest = [];
for (const path of files) {
  const hash = createHash('sha256').update(await readFile(path)).digest('hex');
  manifest.push(`${hash}  ${relative(target, path)}`);
}
await writeFile(join(target, 'SHA256SUMS'), `${manifest.join('\n')}\n`);

console.log(`Created frozen ${versionName} snapshot at ${relative(root, target)}.`);
console.log(`The command refuses to overwrite this directory.`);
