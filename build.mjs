import fs from 'node:fs/promises';import path from 'node:path';import crypto from 'node:crypto';import {pages} from './source/content.mjs';import {render,validateRegistry} from './source/site.mjs';
const errors=validateRegistry();if(errors.length)throw new Error('ROUTE_REGISTRY_INVALID '+errors.join(','));
await fs.rm('public',{recursive:true,force:true});await fs.mkdir('public',{recursive:true});const manifest=[];
for(const p of pages){const html=render(p.path);const rel=p.path==='/'?'index.html':path.join(p.path.replace(/^\//,''),'index.html');const out=path.join('public',rel);await fs.mkdir(path.dirname(out),{recursive:true});await fs.writeFile(out,html);manifest.push({path:p.path,title:p.title,sha256:crypto.createHash('sha256').update(html).digest('hex'),bytes:Buffer.byteLength(html)})}
await fs.writeFile('public/route-manifest.json',JSON.stringify({schema:'keddeh.frontage.routes.v1',built_at:new Date().toISOString(),routes:manifest},null,2)+'\n');
await fs.writeFile('public/robots.txt','User-agent: *\nAllow: /\nSitemap: https://www.keddeh.com/sitemap.xml\n');
await fs.writeFile('public/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+pages.map(p=>`<url><loc>https://www.keddeh.com${p.path}</loc></url>`).join('')+'</urlset>\n');
console.log(JSON.stringify({routes:manifest.length,totalBytes:manifest.reduce((n,r)=>n+r.bytes,0)}));
