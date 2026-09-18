import {rm,mkdir,copyFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
execFileSync(process.execPath,['scripts/check.mjs'],{stdio:'inherit'});
await rm('dist',{recursive:true,force:true});
await mkdir('dist/src',{recursive:true});
for(const file of ['index.html','src/app.js','src/styles.css','src/narrative.js','src/data.json']) await copyFile(file,`dist/${file}`);
console.log('Production build ready in dist/ (only explicitly allowed browser assets).');
