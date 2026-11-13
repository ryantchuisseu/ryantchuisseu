const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');const {spawn}=require('child_process');
const root=process.env.PROJ||process.cwd();const mode=process.argv[2]||'preview';
const srv=http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);return r.end();}
 const ext=path.extname(f);r.writeHead(200,{'Content-Type':{'.html':'text/html','.js':'text/javascript','.woff2':'font/woff2','.woff':'font/woff'}[ext]||'application/octet-stream'});r.end(d);});}).listen(+(process.env.PORT||8765));
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const p=await b.newPage({viewport:{width:720,height:1280}});p.on('console',m=>console.log('PAGE',m.text()));p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('http://localhost:'+(process.env.PORT||8765)+'/index.html?scenario='+(process.env.SCENARIO||'scenario.js')+(process.env.SIZE?'&w='+process.env.SIZE.split('x')[0]+'&h='+process.env.SIZE.split('x')[1]:''));await p.waitForFunction('window.READY',null,{timeout:60000});
 const total=await p.evaluate('TOTAL'), fps=30; const N=Math.round(total*fps);
 fs.writeFileSync(path.join(root,'shots.json'),JSON.stringify(await p.evaluate('SHOTS')));
 if(mode==='preview'){const ts=process.argv.slice(3).map(Number);fs.mkdirSync(root+'/prev',{recursive:true});
   for(const t of ts){const d=await p.evaluate(f=>renderFrame(f).replace('image/jpeg','image/jpeg'),Math.round(t*fps));fs.writeFileSync(`${root}/prev/f_${String(t).padStart(5,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));}
 } else {const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium',root+'/video_noaudio.mp4']);
   const t0=Date.now();for(let f=0;f<N;f++){const d=await p.evaluate(f=>renderFrame(f),f);if(!ff.stdin.write(Buffer.from(d.split(',')[1],'base64')))await new Promise(r=>ff.stdin.once('drain',r));if(f%90==0)console.log(f,'/',N,((Date.now()-t0)/1000).toFixed(0)+'s');}
   ff.stdin.end();await new Promise(r=>ff.on('close',r));}
 await b.close();srv.close();})();
