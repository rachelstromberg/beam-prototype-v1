import http from 'node:http';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(process.argv[2]||'.');
const files=new Set(['/index.html','/src/app.js','/src/narrative.js','/src/styles.css','/src/data.json']);
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8'};
http.createServer(async(req,res)=>{
 let file;try{file=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400).end();return}
 if(file==='/')file='/index.html';
 if(!files.has(file)){res.writeHead(404).end('Not found');return}
 try{const content=await readFile(path.join(root,file));res.writeHead(200,{'Content-Type':types[path.extname(file)],'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(content)}catch{res.writeHead(404).end('Build or file not found')}
}).listen(Number(process.env.PORT)||5173,'127.0.0.1',()=>console.log('Preview: http://127.0.0.1:'+ (process.env.PORT||5173)));
