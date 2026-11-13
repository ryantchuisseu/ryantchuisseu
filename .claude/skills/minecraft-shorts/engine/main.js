import * as THREE from 'three';
// Minecraft-style short-video engine (generic, original assets only: no official textures/skins/logos).
await document.fonts.load('80px VT','AB'); await document.fonts.load('900 74px Mont','AB');
const QP=new URLSearchParams(location.search); const W=+(QP.get('w')||720), H=+(QP.get('h')||1280), FPS=30;

// ---------- utils ----------
function rng(seed){ let s = seed>>>0 || 1; return ()=>{ s ^= s<<13; s>>>=0; s ^= s>>17; s ^= s<<5; s>>>=0; return s/4294967296; }; }
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=clamp(x);return x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;};
const easeOutBack=x=>{x=clamp(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
const lerp=(a,b,t)=>a+(b-a)*t;
const V=(x,y,z)=>new THREE.Vector3(x,y,z);
function hex2rgb(h){const n=parseInt(h.slice(1),16);return [(n>>16)&255,(n>>8)&255,n&255];}
function pixTex(n, painter, repeat){
  const c=document.createElement('canvas'); c.width=c.height=n;
  const g=c.getContext('2d'); painter(g,n);
  const t=new THREE.CanvasTexture(c); t.magFilter=THREE.NearestFilter; t.minFilter=THREE.NearestFilter; t.colorSpace=THREE.SRGBColorSpace;
  if(repeat){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(repeat[0],repeat[1]);}
  return t;
}
function noisePainter(color, amt=0.12, seed=7){
  return (g,n)=>{const r=rng(seed);const [R,G,B]=hex2rgb(color);
    for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=1+(r()-.5)*2*amt;g.fillStyle=`rgb(${R*k|0},${G*k|0},${B*k|0})`;g.fillRect(x,y,1,1);} };
}
const matCache={};
function noiseMat(color, amt=0.1, repeat){
  const key=color+amt+(repeat||'');
  if(!matCache[key]) matCache[key]=new THREE.MeshLambertMaterial({map:pixTex(8,noisePainter(color,amt,parseInt(color.slice(1),16)%997+3),repeat)});
  return matCache[key];
}

// ---------- block textures (generated, original) ----------
const T = {
  grass: pixTex(16,(g,n)=>{const r=rng(3);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=r();g.fillStyle=k<.15?'#5d9b32':k<.5?'#6fb33c':k<.85?'#7bc142':'#86cc4a';g.fillRect(x,y,1,1);}},[40,40]),
  stone: pixTex(16,(g,n)=>{const r=rng(5);g.fillStyle='#8a8a8a';g.fillRect(0,0,n,n);
    for(let i=0;i<10;i++){const x=r()*n|0,y=r()*n|0,w=3+r()*5|0,h=2+r()*4|0;const v=110+r()*50|0;g.fillStyle=`rgb(${v},${v},${v})`;g.fillRect(x,y,w,h);}
    g.fillStyle='#5f5f5f';for(let i=0;i<14;i++){g.fillRect(r()*n|0,r()*n|0,1+(r()*3|0),1);} },[1,1]),
  planks: pixTex(16,(g,n)=>{const r=rng(9);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=1+(r()-.5)*.15;g.fillStyle=`rgb(${168*k|0},${128*k|0},${78*k|0})`;g.fillRect(x,y,1,1);}
    g.fillStyle='#6e5230';for(let y=3;y<n;y+=4)g.fillRect(0,y,n,1);g.fillRect(5,0,1,4);g.fillRect(12,4,1,4);g.fillRect(2,8,1,4);g.fillRect(9,12,1,4);}),
  bricks: pixTex(16,(g,n)=>{g.fillStyle='#9a9a8a';g.fillRect(0,0,n,n);const r=rng(11);
    for(let row=0;row<4;row++){for(let b=0;b<3;b++){const off=(row%2)*4;const x=(b*8+off)%16;const v=1+(r()-.5)*.25;g.fillStyle=`rgb(${150*v|0},${86*v|0},${62*v|0})`;g.fillRect(x,row*4,7,3);if(x+7>16)g.fillRect(0,row*4,x+7-16,3);}}}),
  log: pixTex(16,(g,n)=>{const r=rng(13);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const s=(x%4==0)?.75:1;const k=(1+(r()-.5)*.15)*s;g.fillStyle=`rgb(${102*k|0},${78*k|0},${48*k|0})`;g.fillRect(x,y,1,1);}}),
  leaves: pixTex(16,(g,n)=>{const r=rng(17);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=r();g.fillStyle=k<.2?'#2f6e1f':k<.6?'#3d8a28':'#4a9c31';g.fillRect(x,y,1,1);}}),
  cobble: pixTex(16,(g,n)=>{const r=rng(19);g.fillStyle='#505050';g.fillRect(0,0,n,n);
    for(let i=0;i<9;i++){const x=r()*14|0,y=r()*14|0;const v=90+r()*60|0;g.fillStyle=`rgb(${v},${v},${v})`;g.fillRect(x,y,3+(r()*3|0),3+(r()*2|0));}}),
  glow: pixTex(16,(g,n)=>{const r=rng(23);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=r();g.fillStyle=k<.3?'#f7d36b':k<.7?'#fde58f':'#ffeeb0';g.fillRect(x,y,1,1);}}),
  carpet: pixTex(8,noisePainter('#c0302a',.08,29)),
  gold: pixTex(8,noisePainter('#e8b830',.1,31)),
  sand: pixTex(16,noisePainter('#dcd08a',.08,37)),
  water: pixTex(16,(g,n)=>{const r=rng(41);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const k=r();g.fillStyle=k<.5?'#3d6fd1':'#4a7de0';g.fillRect(x,y,1,1);}}),
  dirt: pixTex(16,noisePainter('#7a5230',.18,43)),
  plazaStone: pixTex(32,(g,n)=>{const r=rng(37);g.fillStyle='#7d7d7d';g.fillRect(0,0,n,n);
    for(let by=0;by<4;by++)for(let bx=0;bx<4;bx++){const v=120+r()*30|0;g.fillStyle=`rgb(${v},${v},${v})`;g.fillRect(bx*8+1,by*8+1,7,7);
      for(let i=0;i<6;i++){const w=110+r()*40|0;g.fillStyle=`rgb(${w},${w},${w})`;g.fillRect(bx*8+1+(r()*6|0),by*8+1+(r()*6|0),1,1);}}},[14,14]),
  glass: pixTex(8,(g,n)=>{g.fillStyle='#a8d8ef';g.fillRect(0,0,n,n);g.fillStyle='#e6f6ff';g.fillRect(1,1,2,1);g.fillRect(1,2,1,1);g.fillStyle='#6d6d6d';g.fillRect(0,0,n,1);g.fillRect(0,0,1,n);}),
};
const M = {};
for(const k in T) M[k]=new THREE.MeshLambertMaterial({map:T[k]});
M.glass.transparent=true; M.glass.opacity=.85; M.water.transparent=true; M.water.opacity=.85;
M.glow=new THREE.MeshBasicMaterial({map:T.glow});
M.iron=new THREE.MeshLambertMaterial({color:'#4a4a4a'});

// ---------- renderer / scene ----------
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
renderer.setSize(W,H); renderer.setPixelRatio(1);
renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap; renderer.outputColorSpace=THREE.SRGBColorSpace;
const scene=new THREE.Scene();
scene.background=new THREE.Color('#86bdf5'); scene.fog=new THREE.Fog('#a9d0f7',40,95);
const camera=new THREE.PerspectiveCamera(52,W/H,0.1,300);
const hemi=new THREE.HemisphereLight('#dbeeff','#6a8a4a',1.25); scene.add(hemi);
const sun=new THREE.DirectionalLight('#fff6e0',2.1); sun.position.set(14,26,16); sun.castShadow=true; sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera,{left:-28,right:28,top:28,bottom:-28,near:1,far:80}); sun.shadow.bias=-0.0005; scene.add(sun);
function setSky(bg,fog,hemiTop,hemiBottom,sunColor){ // mood presets: night, sunset, cave...
  scene.background=new THREE.Color(bg); scene.fog=new THREE.Fog(fog||bg,40,95);
  if(hemiTop) hemi.color.set(hemiTop); if(hemiBottom) hemi.groundColor.set(hemiBottom); if(sunColor) sun.color.set(sunColor); }

let HOST=scene;                          // default decor is built into WORLD so a scenario can hide it all
const WORLD=new THREE.Group(); scene.add(WORLD); HOST=WORLD;
function box(w,h,d,mat,x,y,z,parent=HOST,{cast=true,recv=true}={}){
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat); m.position.set(x,y,z); m.castShadow=cast; m.receiveShadow=recv; parent.add(m); return m; }
function texRepeat(mat,rx,ry){const m=mat.clone();m.map=mat.map.clone();m.map.wrapS=m.map.wrapT=THREE.RepeatWrapping;m.map.repeat.set(rx,ry);m.map.needsUpdate=true;return m;}

// ---------- default village plaza ----------
const ground=new THREE.Mesh(new THREE.PlaneGeometry(200,200),M.grass); ground.rotation.x=-Math.PI/2; ground.receiveShadow=true; WORLD.add(ground);
const plaza=new THREE.Mesh(new THREE.PlaneGeometry(28,28),M.plazaStone); plaza.rotation.x=-Math.PI/2; plaza.position.set(0,0.01,0); plaza.receiveShadow=true; WORLD.add(plaza);
for(const [x,z,w,d] of [[0,14,28.6,.6],[0,-14,28.6,.6],[14,0,.6,28],[-14,0,.6,28]]) box(w,.18,d,M.cobble,x,.09,z);
{const r=rng(99);const cm=new THREE.MeshBasicMaterial({color:'#ffffff',transparent:true,opacity:.92,fog:false});
 for(let i=0;i<14;i++){const g=new THREE.Group();const x=(r()-.5)*160,z=-30-r()*90;const n=2+(r()*3|0);
  for(let j=0;j<n;j++){const m=new THREE.Mesh(new THREE.BoxGeometry(8+r()*10,1.6,5+r()*6),cm);m.position.set(j*6-(n*3),0,(r()-.5)*4);g.add(m);}
  g.position.set(x,34+r()*10,z);WORLD.add(g);}}
// stage + sign board (the "infographic" in the set)
const podium=new THREE.Group(); WORLD.add(podium);
box(5.2,.8,3,M.planks,0,.4,-4.2,podium); box(5.4,.12,3.2,M.gold,0,.62,-4.2,podium); box(5.2,.2,3,M.planks,0,.78,-4.2,podium);
box(1.6,.04,3,M.carpet,0,.9,-4.2,podium); box(2,.4,.6,M.planks,0,.2,-2.45,podium); box(1.6,.04,.6,M.carpet,0,.42,-2.45,podium); box(2,.2,.5,M.planks,0,.6,-2.75,podium);
function lamp(x,z,h=2.6,parent=HOST){box(.22,h,.22,M.log,x,h/2,z,parent);box(.6,.6,.6,M.glow,x,h+.3,z,parent,{cast:false});}
lamp(-2.9,-3,3.4); lamp(2.9,-3,3.4);
const BOARD_POS=V(0,4.5,-6.4), BW=7.2, BH=3.8;
const boardCanvas=document.createElement('canvas'); boardCanvas.width=1024; boardCanvas.height=540;
const boardTex=new THREE.CanvasTexture(boardCanvas); boardTex.colorSpace=THREE.SRGBColorSpace; boardTex.anisotropy=8;
const boardGroup=new THREE.Group(); boardGroup.position.copy(BOARD_POS); scene.add(boardGroup);
{ const g=boardGroup, fm=texRepeat(M.cobble,8,1);
  const face=new THREE.Mesh(new THREE.PlaneGeometry(BW,BH),new THREE.MeshLambertMaterial({map:boardTex})); face.position.z=.16; face.receiveShadow=true; g.add(face);
  box(BW,BH,.3,M.planks,0,0,0,g); box(BW+.8,.4,.5,fm,0,BH/2+.2,0,g); box(BW+.8,.4,.5,fm,0,-BH/2-.2,0,g);
  box(.4,BH,.5,M.cobble,-BW/2-.2,0,0,g); box(.4,BH,.5,M.cobble,BW/2+.2,0,0,g);
  box(.4,2.6,.4,M.cobble,-BW/2+.3,-BH/2-1.5,0,g); box(.4,2.6,.4,M.cobble,BW/2-.3,-BH/2-1.5,0,g); }
let boardKey='';
function tally(g,x,y,n,h=46){ g.lineWidth=7; g.strokeStyle='#2a2a2a'; g.lineCap='round';
  for(let i=0;i<n;i++){const grp=i/5|0, k=i%5; const gx=x+grp*78; g.beginPath(); if(k<4){g.moveTo(gx+k*15,y);g.lineTo(gx+k*15,y+h);} else {g.moveTo(gx-8,y+h-6);g.lineTo(gx+54,y+6);} g.stroke();} }
function setBoard(key, draw){ if(key===boardKey) return; boardKey=key;
  const g=boardCanvas.getContext('2d'); g.fillStyle='#e9e5da'; g.fillRect(0,0,1024,540);
  const r=rng(41); for(let i=0;i<900;i++){g.fillStyle=`rgba(0,0,0,${r()*.04})`;g.fillRect(r()*1024,r()*540,3,3);}
  g.textAlign='center'; g.textBaseline='middle'; draw(g); boardTex.needsUpdate=true; }
const title=(g,t,y=90,s=96,c='#a8322c')=>{g.fillStyle=c;g.font=`${s}px VT`;g.fillText(t,512,y);};
const line=(g,t,y,s=72,c='#333')=>{g.fillStyle=c;g.font=`${s}px VT`;g.fillText(t,512,y);};
// stamp
const stampCanvas=document.createElement('canvas'); stampCanvas.width=1024; stampCanvas.height=300;
const stampTex=new THREE.CanvasTexture(stampCanvas); stampTex.colorSpace=THREE.SRGBColorSpace;
const stamp=new THREE.Mesh(new THREE.PlaneGeometry(5.6,1.64),new THREE.MeshBasicMaterial({map:stampTex,transparent:true})); stamp.position.set(0,4.4,-6.1); scene.add(stamp);
let stampKey='';
function setStamp(text,color='#c62020'){ if(stampKey===text+color) return; stampKey=text+color;
  const g=stampCanvas.getContext('2d'); g.clearRect(0,0,1024,300); g.strokeStyle=color; g.lineWidth=22; g.strokeRect(30,30,964,240);
  g.fillStyle=color; g.font='200px VT'; g.textAlign='center'; g.textBaseline='middle'; g.fillText(text,512,160);
  const r=rng(51); g.globalCompositeOperation='destination-out'; for(let i=0;i<500;i++){g.fillStyle=`rgba(0,0,0,${.3+r()*.5})`;g.fillRect(r()*1024,r()*300,2+r()*6,2+r()*6);} g.globalCompositeOperation='source-over'; stampTex.needsUpdate=true; }

// ---------- scenery helpers ----------
function house(x,z,rot=0,w=6,d=5,h=4,parent=HOST){
  const g=new THREE.Group(); g.position.set(x,0,z); g.rotation.y=rot; parent.add(g);
  box(w,h,d,texRepeat(M.bricks,w,h),0,h/2,0,g);
  for(let i=0;i<4;i++) box(w+.6-i*1.4*(w/d)*.6,.7,d+.6-i*1.4,texRepeat(M.planks,w,1),0,h+.35+i*.7,0,g);
  box(1,1.9,.1,M.log,0,.95,d/2+.02,g); box(1,1,.1,M.glass,-w/2+1.3,2.4,d/2+.02,g); box(1,1,.1,M.glass,w/2-1.3,2.4,d/2+.02,g);
  for(const sx of [-1,1]) box(.4,h,.4,M.log,sx*(w/2),h/2,d/2,g); return g; }
function tree(x,z,h=4,parent=HOST){box(.8,h,.8,M.log,x,h/2,z,parent); box(3.6,1.6,3.6,M.leaves,x,h+.4,z,parent); box(2.4,1.2,2.4,M.leaves,x,h+1.6,z,parent);}
house(-12,-6,Math.PI/4); house(12,-8,-Math.PI/5,6,5,4.5); house(-12,8,Math.PI*0.75,5,5,4); house(13,9,-Math.PI*0.7,6,5,4); house(-4,-14,0,6,5,4.5); house(6,-15,0,5,5,4);
tree(-16,-1,4.5); tree(17,0,5); tree(-6,17,4); tree(8,17,4.5); tree(-18,-14,5); tree(18,-16,4); tree(0,22,5);
HOST=scene;   // anything a scenario builds from here on goes straight into the scene
function hideWorld(){WORLD.visible=false;} function showWorld(){WORLD.visible=true;}

// ---------- characters ----------
function faceTex(o,open){
  return pixTex(8,(g)=>{
    g.fillStyle=o.skin; g.fillRect(0,0,8,8);
    g.fillStyle=o.hair; g.fillRect(0,0,8,2); g.fillRect(0,2,1,1); g.fillRect(7,2,1,1);
    if(o.glasses){g.fillStyle='#111'; g.fillRect(1,3,6,2); g.fillStyle='#444'; g.fillRect(2,3,1,1); g.fillRect(5,3,1,1);}
    else if(o.blank){g.fillStyle='#f4f4f4'; g.fillRect(1,3,2,2); g.fillRect(5,3,2,2);}   // empty white eyes
    else {g.fillStyle='#fff'; g.fillRect(1,4,1,1); g.fillRect(6,4,1,1); g.fillStyle=o.eye||'#3a2a8a'; g.fillRect(2,4,1,1); g.fillRect(5,4,1,1);}
    if(o.smile){g.fillStyle='#2a1a1a'; g.fillRect(2,6,4,1); g.fillRect(1,5,1,1); g.fillRect(6,5,1,1);}   // wide fixed smile
    else if(open){g.fillStyle='#5a1f1a'; g.fillRect(3,6,2,2);} else {g.fillStyle=o.mouth||'rgba(80,30,20,.55)'; g.fillRect(3,6,2,1);}
    if(o.beard){g.fillStyle=o.hair; g.fillRect(1,6,1,2); g.fillRect(6,6,1,2); g.fillRect(2,7,4,1); if(open){g.fillStyle='#5a1f1a';g.fillRect(3,6,2,1);} }
  });
}
function sideTex(o,back){return pixTex(8,(g)=>{g.fillStyle=o.skin;g.fillRect(0,0,8,8);g.fillStyle=o.hair;g.fillRect(0,0,8,back?5:2);if(!back)g.fillRect(o.right?0:6,2,2,2);});}
function shirtTex(o){return pixTex(8,(g)=>{noisePainter(o.shirt,.08,5)(g,8);
  if(o.collar){g.fillStyle=o.collar;g.fillRect(2,0,4,1);g.fillRect(3,1,2,1);}
  if(o.tie){g.fillStyle=o.tie;g.fillRect(3,1,2,1);g.fillRect(3,2,2,4);}
  if(o.buttons){g.fillStyle=o.buttons;g.fillRect(4,2,1,1);g.fillRect(4,4,1,1);g.fillRect(4,6,1,1);}
  if(o.belt){g.fillStyle=o.belt;g.fillRect(0,6,8,1);g.fillStyle='#e8b830';g.fillRect(3,6,2,1);}
  if(o.badge){g.fillStyle=o.badge;g.fillRect(1,2,2,2);} });}
const ALLCHARS=[], ALLSPRITES=[];
/* makeChar options: skin, hair, eye, shirt, sleeve, longSleeve, pants, shoes, collar, tie, buttons, belt, badge,
   glasses, beard, cap, brim, helmet, crown, cape, hat (top hat), bald, smile (fixed wide smile), blank (empty white eyes) */
function makeChar(o){
  o=Object.assign({skin:'#c8956a',hair:'#3b2716',shirt:'#3aa7a7',pants:'#3b3fa8',shoes:'#333'},o);
  const root=new THREE.Group(); scene.add(root); const body=new THREE.Group(); root.add(body);
  const sk=noiseMat(o.skin,.05);
  const faceClosed=new THREE.MeshLambertMaterial({map:faceTex(o,false)}), faceOpen=new THREE.MeshLambertMaterial({map:faceTex(o,true)});
  const headMats=[new THREE.MeshLambertMaterial({map:sideTex(o,false)}), new THREE.MeshLambertMaterial({map:sideTex({...o,right:1},false)}),
    noiseMat(o.bald?o.skin:o.hair,.1), sk, faceClosed, new THREE.MeshLambertMaterial({map:sideTex(o,true)})];
  const head=new THREE.Group(); head.position.y=1.5; body.add(head);
  const hm=new THREE.Mesh(new THREE.BoxGeometry(.5,.5,.5),headMats); hm.position.y=.25; hm.castShadow=true; head.add(hm);
  const shirt=new THREE.MeshLambertMaterial({map:shirtTex(o)}), shirtPlain=noiseMat(o.shirt,.08);
  const torso=new THREE.Mesh(new THREE.BoxGeometry(.5,.75,.25),[shirtPlain,shirtPlain,shirtPlain,shirtPlain,shirt,shirtPlain]); torso.position.y=1.125; torso.castShadow=true; body.add(torso);
  const limb=(mat,mat2,x,y)=>{const p=new THREE.Group();p.position.set(x,y,0);body.add(p);
    const m=new THREE.Mesh(new THREE.BoxGeometry(.25,.75,.25),mat);m.position.y=-.375;m.castShadow=true;p.add(m);
    if(mat2){const hnd=new THREE.Mesh(new THREE.BoxGeometry(.255,.2,.255),mat2);hnd.position.y=-.65;p.add(hnd);} return p;};
  const sleeve=noiseMat(o.sleeve||o.shirt,.08);
  const armL=limb(sleeve,o.longSleeve?sk:null,-.375,1.5), armR=limb(sleeve,o.longSleeve?sk:null,.375,1.5);
  if(!o.longSleeve){for(const a of [armL,armR]){a.children[0].material=sk;const sl=new THREE.Mesh(new THREE.BoxGeometry(.26,.25,.26),sleeve);sl.position.y=-.12;a.add(sl);}}
  const pants=noiseMat(o.pants,.08);
  const legL=limb(pants,noiseMat(o.shoes,.1),-.125,.75), legR=limb(pants,noiseMat(o.shoes,.1),.125,.75);
  if(o.cap){const c=noiseMat(o.cap,.08);const cp=new THREE.Mesh(new THREE.BoxGeometry(.56,.16,.56),c);cp.position.y=.54;head.add(cp);
    const br=new THREE.Mesh(new THREE.BoxGeometry(.5,.05,.22),o.brim?noiseMat(o.brim,.05):c);br.position.set(0,.47,.34);head.add(br);}
  if(o.helmet){const h=new THREE.Mesh(new THREE.BoxGeometry(.58,.3,.58),noiseMat(o.helmet,.08));h.position.y=.42;head.add(h);}
  if(o.hat){const hb=noiseMat(o.hat,.06);const b=new THREE.Mesh(new THREE.BoxGeometry(.7,.06,.7),hb);b.position.y=.52;head.add(b);const t=new THREE.Mesh(new THREE.BoxGeometry(.45,.5,.45),hb);t.position.y=.8;head.add(t);}
  if(o.crown){const gold=M.gold;const b=new THREE.Mesh(new THREE.BoxGeometry(.54,.1,.54),gold);b.position.y=.55;head.add(b);
    for(const [x,z] of [[-.2,-.2],[.2,-.2],[-.2,.2],[.2,.2],[0,0]]){const p=new THREE.Mesh(new THREE.BoxGeometry(.1,.16,.1),gold);p.position.set(x,.68,z);head.add(p);}}
  if(o.cape){const cp=new THREE.Mesh(new THREE.BoxGeometry(.56,1.3,.06),noiseMat(o.cape,.08));cp.position.set(0,.85,-.17);cp.castShadow=true;body.add(cp);}
  const C={root,body,head,armL,armR,legL,legR,o,faceClosed,faceOpen,hm,headMats,scale:1}; ALLCHARS.push(C); return C;
}
/* pose(c,{x,y,z,ry,t,walk,wave,armsUp,point,cross,headTilt,talk,crouch}) — walk: local time (>=0) animates legs; talk: truthy opens/closes mouth with t */
function pose(c,{x=0,y=0,z=0,ry=0,walk=-1,t=0,wave=0,armsUp=0,point=0,cross=0,headTilt=0,talk=false,salute=0,lie=0}={}){
  c.root.position.set(x,y+(lie?.25*lie:0),z); c.root.rotation.set(-Math.PI/2*lie,ry,0,'YXZ'); c.root.visible=true; c.root.scale.setScalar(c.scale||1);
  let la=0,ra=0,ll=0,rl=0,laz=0,raz=0;
  if(walk>=0){const s=Math.sin(walk*Math.PI*2*1.8);la=s*.7;ra=-s*.7;ll=-s*.7;rl=s*.7;c.body.position.y=Math.abs(Math.cos(walk*Math.PI*2*1.8))*.05;}
  else {c.body.position.y=Math.sin(t*2.2)*.012; la=Math.sin(t*1.7)*.05; ra=-Math.sin(t*1.7)*.05;}
  if(wave){ra=-Math.PI*.9*wave; raz=.2+Math.sin(t*12)*.35*wave;}
  if(armsUp){la=-Math.PI*.85*armsUp;ra=-Math.PI*.85*armsUp;laz=-.35*armsUp;raz=.35*armsUp; c.body.position.y=Math.abs(Math.sin(t*8))*.18*armsUp;}
  if(point){ra=-Math.PI*.5*point;}
  if(salute){ra=-Math.PI*.75*salute; raz=.7*salute;}
  if(cross){la=-1.2*cross;ra=-1.2*cross;laz=-.9*cross;raz=.9*cross;}
  c.armL.rotation.set(la,0,laz); c.armR.rotation.set(ra,0,raz); c.legL.rotation.x=ll; c.legR.rotation.x=rl;
  c.head.rotation.set(headTilt,0,0);
  c.headMats[4]=(talk&&Math.sin(t*14)>-.1)?c.faceOpen:c.faceClosed; c.hm.material=c.headMats;
}
function hide(c){c.root.visible=false;}
function faceTo(x,z,tx,tz){return Math.atan2(tx-x,tz-z);}

// ---------- default cast: a diverse crowd of 9 villagers ----------
const vColors=[['#d64a3a','#2f4f8f','#f1c27d','#5a3a1a'],['#4caf50','#5d4037','#8d5524','#1a1a1a'],['#f2b134','#37474f','#e0ac69','#b5651d'],['#8e44ad','#263238','#c68642','#2b1b0e'],
  ['#e67e22','#1e3a5f','#f1c27d','#d4a24c'],['#16a085','#4e342e','#8d5524','#111'],['#e84393','#2d3436','#ffdbac','#6b3e1f'],['#2980b9','#3e2723','#c68642','#3b2716'],['#c0392b','#455a64','#e0ac69','#111']];
const crowd=vColors.map(([s,p,sk,h])=>makeChar({shirt:s,pants:p,skin:sk,hair:h}));
const crowdSpots=[[-3.2,1.2],[-1.6,2.2],[0.2,1.4],[1.8,2.4],[3.4,1.3],[-2.6,3.6],[-0.6,3.8],[1.2,4.2],[3,3.7]];
function crowdLook(t,opts={},except=[],target=[0,-4.2]){crowd.forEach((c,i)=>{if(except.includes(i))return;const [x,z]=crowdSpots[i];
  pose(c,{x,z,ry:faceTo(x,z,target[0],target[1]),t:t+i*.7,...(typeof opts==='function'?opts(i):opts)});});}

// ---------- sprites / effects ----------
function textSprite(text,{font='54px VT',color='#fff',bg='rgba(0,0,0,.38)',scale=.0062,pad=14}={}){
  const c=document.createElement('canvas');const g=c.getContext('2d');g.font=font;const w=Math.ceil(g.measureText(text).width)+pad*2;c.width=w;c.height=74;
  const g2=c.getContext('2d');if(bg){g2.fillStyle=bg;g2.fillRect(0,0,w,74);}g2.font=font;g2.fillStyle=color;g2.textBaseline='middle';g2.textAlign='center';
  g2.shadowColor='rgba(0,0,0,.6)';g2.shadowOffsetX=4;g2.shadowOffsetY=4;g2.fillText(text,w/2,40);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.minFilter=THREE.LinearFilter;
  const s=new THREE.Sprite(new THREE.SpriteMaterial({map:t,depthTest:false,transparent:true}));s.scale.set(w*scale,74*scale,1);s.renderOrder=10;scene.add(s);ALLSPRITES.push(s);return s; }
const qMarks=[0,1,2,3,4].map(()=>textSprite('?',{font:'120px VT',color:'#ffd23f',bg:null,scale:.009}));
const exMarks=[0,1,2].map(()=>textSprite('!',{font:'120px VT',color:'#ff4757',bg:null,scale:.009}));
const checkMark=textSprite('✔',{font:'bold 90px sans-serif',color:'#4cd137',bg:null,scale:.009});
const confetti=[];{const r=rng(71);const cols=['#ff4757','#ffa502','#2ed573','#1e90ff','#ff6b81','#eccc68'];
 for(let i=0;i<140;i++){const m=new THREE.Mesh(new THREE.PlaneGeometry(.14,.09),new THREE.MeshBasicMaterial({color:cols[i%6],side:THREE.DoubleSide}));
  m.userData={x:(r()-.5)*9,z:-4+(r()-.5)*6,y0:7+r()*3,sp:1.2+r()*1.4,ph:r()*10};scene.add(m);confetti.push(m);}}
const poofMat=new THREE.MeshBasicMaterial({color:'#f2f2f2',transparent:true});
const poofs=[];for(let i=0;i<60;i++){const m=new THREE.Mesh(new THREE.BoxGeometry(.3,.3,.3),poofMat.clone());scene.add(m);poofs.push(m);}
let poofIdx=0;
function poof(center,age,seed){ const r=rng(seed);
  for(let i=0;i<12;i++){const m=poofs[poofIdx++%poofs.length];const dx=(r()-.5),dy=r()*.8+.2,dz=(r()-.5);
    if(age<0||age>.7){m.visible=false;continue;} const k=age/.7; m.visible=true;
    m.position.set(center.x+dx*2*k*1.2,center.y+dy*1.4*k+.6,center.z+dz*2*k*1.2); m.scale.setScalar(1.4-k); m.material.opacity=1-k;} }
function confettiRain(u,t0=0){confetti.forEach(m=>{const d=m.userData,k=u-t0;m.visible=true;m.position.set(d.x+Math.sin(k*3+d.ph)*.3,d.y0-k*d.sp*2.2,d.z);m.rotation.set(k*5+d.ph,k*3,d.ph);});}

// ---------- 2D overlay ----------
const out=document.createElement('canvas'); out.width=W; out.height=H; document.body.appendChild(out);
const og=out.getContext('2d');
const CAP={y:.5,color:'#fff',hl:'#ffd23f',size:74,wordSize:92};
function caption(text,age,color,size){
  if(!text) return; color=color||CAP.color; size=size||CAP.size;
  const s=easeOutBack(age/.16); const sc=.6+.4*s;
  og.save(); og.translate(W/2,H*(window.CAPY||CAP.y)); og.scale(sc,sc);
  og.font=`900 ${size}px Mont`; og.textAlign='center'; og.textBaseline='middle';
  const words=text.split(' '); const lines=[]; let cur='';
  for(const w of words){const tst=cur?cur+' '+w:w; if(og.measureText(tst).width>W-90&&cur){lines.push(cur);cur=w;} else cur=tst;} lines.push(cur);
  const lh=size*1.13; const y0=-(lines.length-1)*lh/2;
  lines.forEach((l,i)=>{og.lineJoin='round'; og.lineWidth=size*.18; og.strokeStyle='#000'; og.strokeText(l,0,y0+i*lh); og.fillStyle=color; og.fillText(l,0,y0+i*lh);});
  og.restore(); }
function chat(text,age,color='#ffff55',row=0){
  if(age<0) return; const a=clamp(age/.2); og.save(); og.globalAlpha=a; og.font='46px VT';
  const w=og.measureText(text).width+28; og.fillStyle='rgba(0,0,0,.45)'; const Y=H*0.70+row*66; og.fillRect(24,Y,w,58);
  og.fillStyle='#3a3a00'; og.fillText(text,40,Y+43); og.fillStyle=color; og.fillText(text,37,Y+40); og.restore(); }
function vignette(){const g=og.createRadialGradient(W/2,H/2,H*.3,W/2,H/2,H*.75);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.28)');og.fillStyle=g;og.fillRect(0,0,W,H);}

// ---------- scenario ----------
const E={THREE,scene,camera,V,rng,clamp,ease,easeOutBack,lerp,box,texRepeat,M,T,noiseMat,pixTex,makeChar,pose,hide,faceTo,textSprite,poof,confettiRain,
  setBoard,title,line,tally,setStamp,house,tree,lamp,crowd,crowdSpots,crowdLook,qMarks,exMarks,checkMark,confetti,boardGroup,BOARD_POS,
  setSky,hideWorld,showWorld,CAP,HL:[]};
const SCEN=new URLSearchParams(location.search).get('scenario')||'scenario.js';
const shots=(await import('./'+SCEN+'?v='+Date.now())).default(E);
let WORDS=null; try{const r=await fetch('words.json?v='+Date.now()); if(r.ok) WORDS=await r.json();}catch(e){}
let acc=0; for(const s of shots){s.t0=acc;acc+=s.d;} const TOTAL=acc;
window.TOTAL=TOTAL; window.FPS=FPS;
window.SHOTS=shots.map(s=>({t0:s.t0,d:s.d,stamp:s.stamp?s.t0+s.stamp[1]:null,ncap:(s.cap||[]).length,sfx:(s.sfx||[]).map(([k,at])=>[k,s.t0+at]),mood:s.mood||null}));
function resetAll(){
  ALLCHARS.forEach(hide); ALLSPRITES.forEach(s=>s.visible=false);
  confetti.forEach(m=>m.visible=false); poofs.forEach(m=>m.visible=false); poofIdx=0; stamp.visible=false; }
function renderAt(t){
  resetAll();
  let i=shots.findIndex(s=>t>=s.t0&&t<s.t0+s.d); if(i<0) i=shots.length-1;
  const s=shots[i], u=t-s.t0;
  let b=null; for(let j=i;j>=0;j--){if(shots[j].board){b=shots[j].board;break;}}
  boardGroup.visible=!!b;
  if(b){ const key=typeof b[0]==='function'?b[0](u):b[0]; let draw=b[1];
    if(!draw) for(let j=i;j>=0;j--){const bb=shots[j].board;if(bb&&bb[1]&&bb[0]===b[0]){draw=bb[1];break;}}
    if(draw) setBoard(key,typeof b[0]==='function'?draw(u):draw); }
  if(s.stamp && u>=s.stamp[1]){setStamp(s.stamp[0]);stamp.visible=boardGroup.visible;const k=easeOutBack((u-s.stamp[1])/.18);stamp.scale.setScalar(lerp(2.2,1,clamp(k)));stamp.rotation.z=-.12;}
  s.run(u);
  const k=ease(u/s.d);
  camera.position.lerpVectors(s.cam[0],s.cam[1],k); camera.position.x+=Math.sin(t*1.3)*.03; camera.position.y+=Math.sin(t*1.7)*.02;
  const L=new THREE.Vector3().lerpVectors(s.look[0],s.look[1],k);
  if(s.stamp&&u>=s.stamp[1]&&u<s.stamp[1]+.25){const a=(1-(u-s.stamp[1])/.25)*.08;camera.position.x+=Math.sin(u*90)*a;camera.position.y+=Math.cos(u*77)*a;}
  camera.lookAt(L); renderer.render(scene,camera);
  og.drawImage(renderer.domElement,0,0); vignette();
  if(WORDS){ let k2=-1; for(let j=0;j<WORDS.length;j++){ if(WORDS[j].t<=t) k2=j; else break; }
    if(k2>=0){const w=WORDS[k2]; if(t<w.e+0.45) caption(w.w,t-w.t,(E.HL||[]).includes(w.k)?CAP.hl:CAP.color,CAP.wordSize);} }
  else if(s.cap&&s.cap.length){ const n=s.cap.length, seg=s.d/n; const ci=Math.min(n-1,Math.floor(u/seg)); caption(s.cap[ci],u-ci*seg); }
  (s.chat||[]).forEach(([txt,at,col],ri)=>{if(u>at) chat(txt,u-at,col||'#ffff55',ri);});
  if(t<.2){og.fillStyle=`rgba(0,0,0,${1-t/.2})`;og.fillRect(0,0,W,H);}
  if(t>TOTAL-.35){og.fillStyle=`rgba(0,0,0,${(t-(TOTAL-.35))/.35})`;og.fillRect(0,0,W,H);}
}
window.renderFrame=(f)=>{renderAt(f/FPS);return out.toDataURL('image/jpeg',.93);};
window.READY=true;
