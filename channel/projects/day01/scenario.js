// Day 1 — "The Village Where Nobody Sleeps" (voice-driven: cuts on voice segment starts)
export default function(E){
  const {THREE,scene,V,pose,hide,makeChar,textSprite,qMarks,exMarks,checkMark,crowd,box,M,T,setSky,hideWorld,clamp,ease,easeOutBack,lerp,faceTo,CAP}=E;
  hideWorld(); CAP.y=.78; CAP.wordSize=96;
  E.HL=['moon','dreams','dream','dreamer','dreamers','empty','hollows','lamp','dying','sleep','slept','secret','dark','last','me','hungry','flicker','flickered','strange','awake','understood','humming'];
  const lights=scene.children.filter(l=>l.isLight), hemi=lights.find(l=>l.isHemisphereLight), sun=lights.find(l=>l.isDirectionalLight);
  const SKY={
    dusk:['#e98a54','#e9a073','#ffd2a0','#5a3a2a','#ffb070',1.0,1.5],
    night:['#0a1030','#0a1030','#7080d0','#2a3050','#9fb4ff',1.15,.95],
    dawn:['#ffb98a','#ffcfa8','#ffe0c0','#4a5a3a','#ffd9a0',1.1,1.7],
    dark:['#05060f','#05060f','#6a78c0','#2a3050','#8a9ae0',.95,.6],
    dream:['#0b1650','#0b1650','#5a6adf','#141a4a','#a8b8ff',.9,.5],
    day:['#86bdf5','#a9d0f7','#dbeeff','#6a8a4a','#fff6e0',1.25,2.1]};
  const sky=n=>{const k=SKY[n];setSky(k[0],k[1],k[2],k[3],k[4]);hemi.intensity=k[5];sun.intensity=k[6];};

  // ---------- set ----------
  const SQ=new THREE.Group(); scene.add(SQ);
  const gm=E.texRepeat(M.grass,70,70);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(300,300),gm); ground.rotation.x=-Math.PI/2; ground.receiveShadow=true; SQ.add(ground);
  const plaza=new THREE.Mesh(new THREE.PlaneGeometry(22,22),M.plazaStone); plaza.rotation.x=-Math.PI/2; plaza.position.y=.02; plaza.receiveShadow=true; SQ.add(plaza);
  for(const [x,z,w,d] of [[0,11,22.6,.5],[0,-11,22.6,.5],[11,0,.5,22],[-11,0,.5,22]]) box(w,.16,d,M.cobble,x,.08,z,SQ);
  // Great Lamp
  const LAMP=new THREE.Group(); SQ.add(LAMP);
  box(2.4,.5,2.4,M.cobble,0,.25,0,LAMP); box(.5,5,.5,M.log,0,3,0,LAMP); box(1.6,.2,1.6,M.planks,0,5.55,0,LAMP);
  const glowM=new THREE.MeshBasicMaterial({map:T.glow}); const head=box(1.5,1.5,1.5,glowM,0,6.4,0,LAMP,{cast:false});
  const hc=document.createElement('canvas'); hc.width=hc.height=128; {const g=hc.getContext('2d'),r=g.createRadialGradient(64,64,0,64,64,64); r.addColorStop(0,'rgba(255,214,120,1)'); r.addColorStop(.35,'rgba(255,190,90,.45)'); r.addColorStop(1,'rgba(255,170,60,0)'); g.fillStyle=r; g.fillRect(0,0,128,128);}
  const haloM=new THREE.SpriteMaterial({map:new THREE.CanvasTexture(hc),transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,opacity:.8}); const halo=new THREE.Sprite(haloM); halo.position.set(0,6.4,0); halo.scale.setScalar(7); LAMP.add(halo);
  const lampLight=new THREE.PointLight('#ffd98a',120,60,1.2); lampLight.position.set(0,6.4,0); SQ.add(lampLight);
  const lampLevel=L=>{glowM.color.setScalar(.15+.85*Math.min(1.4,L)); haloM.opacity=.75*Math.min(1.3,L); lampLight.intensity=150*L; const s=1+.12*Math.max(0,L-1); head.scale.setScalar(s); halo.scale.setScalar(7*s);};
  // houses with lit windows
  const houseSpots=[[-14,-12],[-5,-17],[6,-17],[15,-11],[18,6],[-13,15],[14,16]];
  for(const [x,z] of houseSpots){const g=E.house(x,z,Math.atan2(-x,-z),6,5,4,SQ); box(.9,.9,.12,M.glow,-1.7,2.4,2.58,g,{cast:false}); box(.9,.9,.12,M.glow,1.7,2.4,2.58,g,{cast:false});}
  for(const [x,z,h] of [[-22,-8,5],[22,-4,4.5],[-8,24,4],[9,25,5],[-26,12,5],[27,14,4],[0,-26,5]]) E.tree(x,z,h,SQ);
  // windmill
  const WM=new THREE.Group(); WM.position.set(-26,0,-3); WM.rotation.y=Math.PI/2.6; SQ.add(WM);
  box(3.6,7,3.6,M.planks,0,3.5,0,WM); box(4.4,.8,4.4,M.log,0,7.3,0,WM); box(3,.8,3,M.bricks,0,8.1,0,WM); box(1.6,.8,1.6,M.log,0,8.9,0,WM); box(1,2.2,.1,M.log,0,1.1,1.82,WM);
  const blades=new THREE.Group(); blades.position.set(0,6,2.3); WM.add(blades);
  for(let i=0;i<4;i++){const b=new THREE.Group(); b.rotation.z=i*Math.PI/2; blades.add(b); box(.35,6.4,.15,M.planks,0,3.2,0,b); box(1.3,3,.08,M.carpet,.55,4.2,.1,b);}
  // bench, bed, straw (props for the "nobody sits / lies down" beats)
  const bench=new THREE.Group(); bench.position.set(8,0,3.5); bench.rotation.y=-Math.PI/2; SQ.add(bench);
  box(2.6,.25,.8,M.planks,0,.6,0,bench); box(2.6,.7,.15,M.planks,0,1.05,-.4,bench); for(const x of [-1.1,1.1]) box(.2,.6,.6,M.log,x,.3,0,bench);
  const bed=new THREE.Group(); bed.position.set(-9,0,6.5); SQ.add(bed);
  box(1.4,.5,2.4,M.planks,0,.25,0,bed); box(1.3,.2,1.6,M.carpet,0,.6,.35,bed); box(1.2,.18,.6,new THREE.MeshLambertMaterial({color:'#f2f2f2'}),0,.62,-.8,bed);
  // moon + beam
  const moonM=new THREE.MeshBasicMaterial({color:'#eef2ff',fog:false}); const moon=new THREE.Mesh(new THREE.BoxGeometry(9,9,1.5),moonM); moon.position.set(-16,48,-70); SQ.add(moon);
  for(const [x,y,s] of [[-1.5,1.2,2],[1.8,-1.4,2.4],[1.6,2,1.2],[-2,-2,1.5]]){const c=new THREE.Mesh(new THREE.BoxGeometry(s,s,.2),new THREE.MeshBasicMaterial({color:'#c3c9e6',fog:false})); c.position.set(x,y,.8); moon.add(c);}
  const moonHalo=new THREE.Mesh(new THREE.BoxGeometry(14,14,1),new THREE.MeshBasicMaterial({color:'#9fb4ff',transparent:true,opacity:.22,fog:false,depthWrite:false})); moonHalo.position.set(0,0,-.6); moon.add(moonHalo);
  const beam=new THREE.Mesh(new THREE.CylinderGeometry(7,7,80,24,1,true),new THREE.MeshBasicMaterial({color:'#aac4ff',transparent:true,opacity:.2,side:THREE.FrontSide,depthWrite:false,fog:false})); beam.position.set(0,40,0); SQ.add(beam);
  // dream field (far from the square)
  const DR=new THREE.Group(); DR.position.set(120,0,0); scene.add(DR);
  const lanterns=[]; {const r=E.rng(8); for(let i=0;i<34;i++){const m=box(.7,.9,.7,glowM,(r()-.5)*34,1+r()*6,(r()-.5)*30-4,DR,{cast:false}); m.userData={y0:m.position.y,ph:r()*6};lanterns.push(m);}}
  box(.5,6,.5,M.glow,-1.6,3,-16,DR,{cast:false}); box(.5,6,.5,M.glow,1.6,3,-16,DR,{cast:false}); box(3.7,.5,.5,M.glow,0,6,-16,DR,{cast:false});
  box(2.7,5.6,.2,new THREE.MeshLambertMaterial({color:'#d8e0f0'}),0,2.8,-16,DR);
  // wisps (stolen dreams) + beam of dreams into lamp
  const wisps=[]; for(let i=0;i<18;i++) wisps.push(box(.35,.35,.35,glowM,0,-50,0,scene,{cast:false}));
  const hideWisps=()=>wisps.forEach(w=>w.visible=false);
  const stream=(from,to,u,n=14,speed=.9)=>{for(let i=0;i<n;i++){const k=((u*speed+i/n)%1);const w=wisps[i%wisps.length];w.visible=true;
    w.position.set(lerp(from.x,to.x,k),lerp(from.y,to.y,k)+Math.sin(k*Math.PI)*1.5+Math.sin(i*2+u*3)*.2,lerp(from.z,to.z,k)+Math.sin(i+u*2)*.25);w.scale.setScalar(1-.5*Math.abs(k-.5)*2);}};

  // ---------- cast ----------
  const milo=makeChar({skin:'#d2a07a',hair:'#3a2415',shirt:'#4a7bd0',pants:'#2b2b38'});
  const ava=makeChar({skin:'#c68642',hair:'#2b1b0e',shirt:'#e57fa0',pants:'#444444'}); ava.scale=.72;
  const rowan=makeChar({skin:'#e0ac69',hair:'#e6e6e6',beard:true,shirt:'#6b4a8a',longSleeve:true,pants:'#3a2a4a',cape:'#4b2f66'});
  const elderOpt={skin:'#e0ac69',hair:'#dcdcdc',beard:true,shirt:'#7a5a3a',longSleeve:true,pants:'#3a2f25',cape:'#5a3a2a'};
  const elders=[0,1,2].map(i=>makeChar({...elderOpt,shirt:['#7a5a3a','#3d6a5a','#8a4a4a'][i]}));
  const hollows=[0,1,2,3,4,5,6].map(i=>makeChar({skin:'#a6adb5',hair:'#6a6f76',shirt:['#8f959d','#7d8590','#9aa0a8'][i%3],pants:'#585d66',blank:true,smile:true}));
  const extra=[['#c0392b','#2d3436','#c68642','#222'],['#27ae60','#34495e','#e0ac69','#5a3a1a'],['#f39c12','#1e272e','#8d5524','#111'],['#8e44ad','#2c3e50','#f1c27d','#8a5a2a'],['#16a085','#4a3a2a','#ffdbac','#333']].map(([s,p,sk,h])=>makeChar({shirt:s,pants:p,skin:sk,hair:h}));
  const walkers=[...crowd,...extra];
  const tagMilo=textSprite('Milo'), tagAva=textSprite('Ava'), tagRowan=textSprite('Elder Rowan'), tagHollow=textSprite('Hollow');
  const place=(c,x,z,u,o={})=>pose(c,{x,z,y:0,t:u,...o});
  const circle=(u,{r=6,sp=.32,list=walkers,skip=[],r2=null}={})=>list.forEach((c,i)=>{if(skip.includes(i))return;const a=u*sp+i*2*Math.PI/list.length, rr=(r2&&i%2)?r2:r;
    const x=rr*Math.cos(a), z=rr*Math.sin(a); const vx=-Math.sin(a), vz=Math.cos(a); pose(c,{x,z,ry:Math.atan2(vx,vz),walk:u+i*.13});});
  const hollowRow=(u,{z=-9,wake=false}={})=>hollows.forEach((c,i)=>{const x=-6.6+i*2.2; pose(c,{x,z,ry:Math.sin(u*.6+i)*.25,t:u+i,headTilt:Math.sin(u*.5+i)*.08});});
  const M0=[1.5,3.5];
  const stand=(c,x,z,u,o={})=>pose(c,{x,z,ry:0,t:u,...o});
  const dropLines=()=>{};

  // ---------- per-frame environment ----------
  const env=(t,{L=1,beamOn=0,sk='night',vis=true}={})=>{beam.position.x=0;moon.scale.setScalar(1);sky(sk); lampLevel(L); beam.visible=beamOn>0; beam.material.opacity=.2*beamOn; hideWisps();
    blades.rotation.z=t*.5; lanterns.forEach(m=>{m.position.y=m.userData.y0+Math.sin(t*1.2+m.userData.ph)*.4;}); };
  const flick=u=>Math.max(.05,.7+.3*Math.sin(u*38)*Math.sin(u*11)-u*.12);

  const S=[]; const add=(t0,o)=>{o.t0=t0;S.push(o);};
  const mili=(u,o={})=>stand(milo,M0[0],M0[1],u,{talk:false,...o});

  // 1 hook: wide dusk village, villagers walking circles
  add(0,{cam:[V(0,7,22),V(0,6,17)],look:[V(0,3,0),V(0,3,0)],mood:'tense',run(u){env(u,{sk:'dusk',L:1});circle(u,{});}});
  add(2.71,{cam:[V(1.1,1.95,6.4),V(1.4,1.9,5.6)],look:[V(1.5,1.85,3.5),V(1.5,1.85,3.5)],run(u){env(u,{sk:'dusk'});mili(u,{});circle(u,{r:7,skip:[0,1]});}});
  // 2 intro
  add(3.57,{cam:[V(.3,2.2,7.2),V(.9,2.1,6.2)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'dusk'});mili(u,{talk:true,wave:ease(u/.5)*.7});tagMilo.visible=true;tagMilo.position.set(1.5,2.9,3.5);circle(u,{r:8});}});
  // 3 evening circles from above
  add(6.16,{cam:[V(-10,13,16),V(8,12,15)],look:[V(0,2.5,0),V(0,2.5,0)],run(u){env(u,{sk:'dusk',L:1.05});circle(u+6,{});}});
  // 4 nobody sits / lies / closes eyes
  add(11.41,{cam:[V(10.5,1.8,7.5),V(10,1.7,6.2)],look:[V(8,1,3.5),V(8,1,3.5)],run(u){env(u,{sk:'dusk'});circle(u+11,{r:6});}});
  add(12.33,{cam:[V(-6.5,2.4,10.5),V(-7.5,2.2,9.4)],look:[V(-9,.6,6.5),V(-9,.6,6.5)],run(u){env(u,{sk:'dusk'});circle(u+12,{r:6});}});
  add(13.44,{cam:[V(.5,2.0,8.2),V(.5,2.0,7.0)],look:[V(0,1.9,4.9),V(0,1.9,4.9)],run(u){env(u,{sk:'night'});const c=walkers[2];pose(c,{x:0,z:4.9,ry:0,t:u});circle(u+13,{r:7,skip:[2]});}});
  // 5 the elders say there is one rule
  add(15.15,{cam:[V(3.6,2.3,5.6),V(3.5,2.2,4.7)],look:[V(3.5,2.1,2.5),V(3.5,2.1,2.5)],run(u){env(u,{sk:'night'});place(rowan,3.5,2.5,u,{talk:true});tagRowan.visible=true;tagRowan.position.set(3.5,2.95,2.5);[[1.6,1.6],[5.6,1.4],[6.6,3.2]].forEach(([x,z],i)=>place(elders[i],x,z,u,{ry:0}));circle(u,{r:8});}});
  // 6 never fall asleep because the moon is hungry
  add(16.98,{cam:[V(0,2.5,14),V(0,4,13)],look:[V(0,18,-60),V(-4,26,-62)],run(u){env(u,{sk:'night',L:.9});circle(u+17,{r:9});}});
  add(18.40,{cam:[V(-6,3.5,12),V(-9,5,9)],look:[V(-16,40,-70),V(-16,43,-70)],run(u){env(u,{sk:'night',L:.8});exMarks.forEach((m,i)=>{m.visible=true;m.position.set(-6+i*3,7+Math.sin(u*3+i)*.3,-4);});}});
  // 7 if you sleep it steals your dreams, you wake up empty
  add(20.09,{cam:[V(3,2.4,6.5),V(2,2.6,5.4)],look:[V(0,.5,2.5),V(0,.7,2.5)],run(u){env(u,{sk:'night',L:.9,beamOn:ease(u/.5)});pose(walkers[4],{x:0,y:0,z:2.5,ry:Math.PI*.7,lie:1,t:u});}});
  add(20.88,{cam:[V(4,3.2,8),V(2.4,5.2,5.5)],look:[V(0,2,2.5),V(0,9,0)],run(u){env(u,{sk:'night',L:.9,beamOn:1});pose(walkers[4],{x:0,y:0,z:2.5,ry:Math.PI*.7,lie:1,t:u});stream(V(0,.8,2.5),V(-8,40,-60),u,14,.35);}});
  add(22.15,{cam:[V(1,2.0,6.2),V(.6,2.05,5.4)],look:[V(0,1.9,2.5),V(0,1.9,2.5)],run(u){env(u,{sk:'night',L:.7});pose(hollows[0],{x:0,z:2.5,ry:0,t:u});hollows[0].head.rotation.x=.05;}});
  // 8 the Hollows
  add(23.47,{cam:[V(-.6,2.2,6),V(-.2,2.1,5)],look:[V(0,1.9,2.5),V(0,1.9,2.5)],run(u){env(u,{sk:'night',L:.8});pose(hollows[1],{x:0,z:2.5,ry:0,t:u});tagHollow.visible=true;tagHollow.position.set(0,3,2.5);}});
  // 9 smiling at nothing
  add(25.28,{cam:[V(-1,1.9,-1),V(1.2,1.9,-3.2)],look:[V(-.5,1.9,-9),V(.5,1.9,-9)],run(u){env(u,{sk:'night',L:.9});hollowRow(u,{});}});
  // 10 seven of them / nobody goes near
  add(27.55,{cam:[V(0,4.2,5),V(0,4.0,-.5)],look:[V(0,1.4,-9),V(0,1.4,-9)],run(u){env(u,{sk:'night',L:.9});hollowRow(u,{});}});
  add(28.48,{cam:[V(9,2.5,0),V(8,2.5,-4)],look:[V(0,1.6,-9),V(0,1.6,-9)],run(u){env(u,{sk:'night',L:.9});hollowRow(u,{});circle(u,{r:5,list:walkers,skip:[]});}});
  // 11 but here is my secret
  add(29.91,{cam:[V(1.1,1.95,6.3),V(1.3,1.95,5.5)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'night',L:.8});mili(u,{talk:true,headTilt:.1});}});
  // 12 I sleep every night (windmill, asleep)
  add(31.30,{cam:[V(-16.5,2.6,7.5),V(-17.5,2.8,6.3)],look:[V(-21,.7,3),V(-21,.7,3)],run(u){env(u,{sk:'night',L:.9});pose(milo,{x:-21,y:0,z:3,ry:Math.PI*.6,lie:1,t:u});}});
  // 13 hide in the old windmill / dream of lanterns
  add(33.19,{cam:[V(-9,5,15),V(-13,6,12)],look:[V(-26,5.5,-3),V(-26,5.5,-3)],run(u){env(u,{sk:'night',L:.9});pose(milo,{x:-21,y:0,z:3,ry:Math.PI*.6,lie:1,t:u});}});
  add(35.20,{cam:[V(120,2.2,14),V(120,3.2,-4)],look:[V(120,3,-16),V(120,3,-16)],run(u){env(u,{sk:'dream',L:.9});pose(milo,{x:120,z:6-u*1.2,ry:Math.PI,t:u,walk:u});}});
  // 14 every morning I wake up fine
  add(37.57,{cam:[V(-17.5,2.3,7),V(-18.5,2.4,6.2)],look:[V(-21,.8,3),V(-21,1.0,3)],run(u){env(u,{sk:'dawn',L:1.2});const k=ease(u/1.0);pose(milo,{x:-21,y:0,z:3,ry:Math.PI*.6+k*.6,lie:1-k,armsUp:k*.8,t:u});}});
  // 15 nothing stolen nothing empty
  add(39.22,{cam:[V(1.0,2.0,6.4),V(1.3,1.95,5.5)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'dawn',L:1.3});mili(u,{talk:true});checkMark.visible=true;checkMark.position.set(2.7,2.9+Math.sin(u*3)*.05,3.5);}});
  // 16 never told anyone, not even Ava
  add(40.97,{cam:[V(.3,2.2,6.6),V(.9,2.1,5.9)],look:[V(1.5,1.7,3.5),V(1.5,1.7,3.5)],run(u){env(u,{sk:'dawn',L:1.2});mili(u,{talk:true,salute:0});milo.armR.rotation.set(-1.5*ease(u/.4),0,.2);}});
  add(42.12,{cam:[V(3.6,1.4,7.4),V(3.0,1.3,6.4)],look:[V(3,.9,4.4),V(3,.9,4.4)],run(u){env(u,{sk:'dawn',L:1.2});mili(u,{});place(ava,3,4.4,u,{ry:.4,wave:.5});tagAva.visible=true;tagAva.position.set(3,2.2,4.4);}});
  // 17 noticed something strange
  add(43.67,{cam:[V(1.3,2.0,6.4),V(1.4,2.0,5.5)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'dawn',L:1.3});mili(u,{headTilt:.12});qMarks.forEach((m,i)=>{if(i<3){m.visible=true;m.position.set(.4+i*1.0,3.2+Math.sin(u*3+i)*.08,3.5);}});}});
  // 18 lamp brightest at dawn
  add(45.38,{cam:[V(3,.8,8),V(1.5,1.2,6.5)],look:[V(0,6.4,0),V(0,6.6,0)],run(u){env(u,{sk:'dawn',L:1.5+Math.sin(u*2)*.1});mili(u,{ry:Math.PI*.15});}});
  // 19 so one night I stayed awake
  add(49.02,{cam:[V(1.2,1.95,6.4),V(1.4,1.95,5.5)],look:[V(1.5,1.95,3.5),V(1.5,1.95,3.5)],run(u){env(u,{sk:'night',L:1});mili(u,{headTilt:-.05});}});
  // 20 midnight lamp flickers
  add(51.05,{cam:[V(2,1.6,6.5),V(1,3.2,4.0)],look:[V(0,6.2,0),V(0,6.4,0)],run(u){env(u,{sk:'night',L:flick(u)});circle(u,{r:8});}});
  // 21 in a hundred years it had never flickered
  add(53.42,{cam:[V(-4,1.8,7),V(-2,1.8,5.5)],look:[V(0,2.5,0),V(0,3,0)],run(u){env(u,{sk:'night',L:flick(u+2)});walkers.forEach((c,i)=>{const a=i*2*Math.PI/walkers.length;pose(c,{x:5.5*Math.cos(a),z:5.5*Math.sin(a),ry:Math.atan2(-Math.cos(a),-Math.sin(a)),t:u+i,headTilt:-.35});});}});
  // 22 soon almost dark
  add(55.82,{cam:[V(0,3,14),V(0,3.5,12)],look:[V(0,3,0),V(0,3,0)],run(u){env(u,{sk:'dark',L:Math.max(.08,.35-u*.2)});walkers.forEach((c,i)=>{const a=i*2*Math.PI/walkers.length;pose(c,{x:6*Math.cos(a),z:6*Math.sin(a),ry:Math.atan2(-Math.cos(a),-Math.sin(a)),t:u+i});});}});
  // 23 and then I heard it
  add(57.46,{cam:[V(1.0,1.9,6.2),V(1.3,1.95,5.4)],look:[V(1.5,1.95,3.5),V(1.5,1.95,3.5)],run(u){env(u,{sk:'dark',L:.15});mili(u,{headTilt:.15});exMarks[0].visible=true;exMarks[0].position.set(1.5,3.1,3.5);}});
  // 24 humming from the moon
  add(58.78,{cam:[V(0,2,12),V(0,4,10)],look:[V(-16,38,-70),V(-16,46,-70)],run(u){env(u,{sk:'dark',L:.12,beamOn:.35*ease(u/2)});moon.scale.setScalar(1+.04*Math.sin(u*9));}});
  // 25 silver light poured down
  add(61.49,{cam:[V(-8,2.5,14),V(-4,3.5,10)],look:[V(0,12,0),V(0,6,0)],run(u){env(u,{sk:'dark',L:.1,beamOn:ease(u/.6)});circle(u,{r:6.5,sp:.1});}});
  add(63.76,{cam:[V(7,3,9),V(3,3,7)],look:[V(0,1.6,0),V(-3,1.6,-2)],run(u){env(u,{sk:'dark',L:.1,beamOn:1});beam.position.x=Math.sin(u*2.2)*4;walkers.forEach((c,i)=>{const a=i*2*Math.PI/walkers.length;pose(c,{x:5*Math.cos(a),z:5*Math.sin(a),ry:Math.atan2(-Math.cos(a),-Math.sin(a)),t:u+i});});}});
  // 27 the seven Hollows turn and walk toward me
  add(64.74,{cam:[V(1.5,2.3,8.2),V(1.7,2.0,6.4)],look:[V(0,1.8,-6),V(0,1.8,-2)],run(u){env(u,{sk:'dark',L:.12,beamOn:1});beam.position.x=0;mili(u,{});
    hollows.forEach((c,i)=>{const x0=-6.6+i*2.2, z0=-9; const k=clamp((u-1.0)/3.2); const tx=lerp(x0,M0[0]+(i-3)*.9,k), tz=lerp(z0,M0[1]-2.2,k);
      pose(c,{x:tx,z:tz,ry:lerp(Math.sin(i)*.2,faceTo(tx,tz,M0[0],M0[1]),ease(u/.9)),walk:k>0&&k<1?u:-1,t:u});});}});
  // 28 elders block every street
  add(68.96,{cam:[V(0,2.6,10.5),V(0,2.4,9)],look:[V(0,1.5,4),V(0,1.5,4)],run(u){env(u,{sk:'dark',L:.12,beamOn:.8});
    const r=clamp(u/1.1);pose(milo,{x:lerp(1.5,-1,r),z:lerp(3.5,6.2,r),ry:Math.PI*.1,walk:u,t:u});
    elders.forEach((c,i)=>place(c,-4+i*4,7.8,u,{ry:0,cross:.9}));place(rowan,0,6.9,u,{ry:0});}});
  // 29 Rowan holds up his hands
  add(71.58,{cam:[V(-1,2.2,10),V(-.4,2.4,8.4)],look:[V(0,2.2,6.9),V(0,2.2,6.9)],run(u){env(u,{sk:'dark',L:.15});place(rowan,0,6.9,u,{ry:0,armsUp:.55*ease(u/.4),talk:u>.8});tagRowan.visible=true;tagRowan.position.set(0,2.95,6.9);}});
  // 30 "Milo, please. Go to sleep. The lamp is dying."
  add(73.35,{cam:[V(.4,2.1,9.4),V(0,2.2,8.4)],look:[V(0,2.1,6.9),V(0,2.1,6.9)],run(u){env(u,{sk:'dark',L:.1});place(rowan,0,6.9,u,{ry:0,talk:true,armsUp:.5});}});
  add(75.26,{cam:[V(2,2,12),V(1,3.4,10)],look:[V(0,6.2,0),V(0,6.0,0)],run(u){env(u,{sk:'dark',L:.12*(1+Math.sin(u*40)*.4)});}});
  // 31 that's when I understood
  add(76.67,{cam:[V(1.1,1.95,6.2),V(1.4,1.95,5.4)],look:[V(1.5,1.95,3.5),V(1.5,1.95,3.5)],run(u){env(u,{sk:'dark',L:.2});mili(u,{});exMarks.forEach((m,i)=>{if(i<2){m.visible=true;m.position.set(.7+i*1.6,3.1,3.5);}});}});
  // 32 lamp never burned on oil; burned on dreams
  add(78.03,{cam:[V(0,1.6,7),V(0,3.8,4.2)],look:[V(0,5.4,0),V(0,6.2,0)],run(u){env(u,{sk:'dark',L:.4});}});
  add(79.92,{cam:[V(5,3,9),V(3,4.2,6.5)],look:[V(0,5,0),V(0,6,0)],run(u){env(u,{sk:'dark',L:.4+.3*ease(u/1.4)});stream(V(120,3,-8),V(0,6.4,0),u,16,.5);}});
  // 33 only one dreamer left. Me.
  add(81.48,{cam:[V(1.0,1.9,6.6),V(1.4,1.95,5.5)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'dark',L:.4});mili(u,{talk:false});walkers.forEach((c,i)=>{const a=i*2*Math.PI/walkers.length;pose(c,{x:7.5*Math.cos(a)+(i<3?-1:0),z:7.5*Math.sin(a)-2,ry:Math.atan2(-Math.cos(a),-Math.sin(a)),t:u+i});});}});
  add(85.02,{cam:[V(1.0,1.95,6.0),V(1.4,1.95,5.4)],look:[V(1.5,1.9,3.5),V(1.5,1.9,3.5)],run(u){env(u,{sk:'dark',L:.5});mili(u,{headTilt:.12});}});
  // 34 elders walked in circles
  add(85.69,{cam:[V(-12,6,12),V(10,6,12)],look:[V(0,2,0),V(0,2,0)],run(u){env(u,{sk:'night',L:.6});circle(u+3,{r:7});elders.forEach((c,i)=>{const a=-u*.3+i*2.1,x=4.5*Math.cos(a),z=4.5*Math.sin(a);pose(c,{x,z,ry:Math.atan2(Math.sin(a),-Math.cos(a)),walk:u+i});});}});
  // 35 keep everyone awake, one dreamer to feed
  add(88.26,{cam:[V(3,3,12),V(-1,3.5,9)],look:[V(0,3,0),V(0,3,0)],run(u){env(u,{sk:'night',L:.7});circle(u+5,{r:8});mili(u,{});stream(V(1.5,2.2,3.5),V(0,6.4,0),u,12,.7);}});
  // 36 hollows, who were they
  add(92.58,{cam:[V(1,2.3,7.2),V(1.4,2.2,6.0)],look:[V(0,1.9,2),V(0,1.9,2)],run(u){env(u,{sk:'night',L:.5});hollows.slice(0,5).forEach((c,i)=>pose(c,{x:-3.2+i*1.6,z:2-(i%2)*.8,ry:Math.PI*0,t:u+i}));}});
  // 37 Rowan stared at the ground / they were dreamers too
  add(94.61,{cam:[V(.2,1.9,4.3),V(.1,2.0,3.4)],look:[V(0,1.9,1),V(0,1.7,1)],run(u){env(u,{sk:'night',L:.5});place(rowan,0,1,u,{ry:0,headTilt:.55,talk:true});tagRowan.visible=true;tagRowan.position.set(0,2.95,1);}});
  add(96.60,{cam:[V(0,2.3,8),V(0,2.2,6.5)],look:[V(0,1.5,1),V(0,1.5,1)],run(u){env(u,{sk:'night',L:.5});hollows.slice(0,5).forEach((c,i)=>pose(c,{x:-3.2+i*1.6,z:1.5-(i%2)*.8,ry:0,t:u+i,headTilt:.1}));}});
  // 38 Ava steps out and takes my hand
  add(97.93,{cam:[V(2,1.4,8),V(2,1.3,6.5)],look:[V(2,1.0,3.5),V(2,1.0,3.5)],run(u){env(u,{sk:'night',L:.6});mili(u,{});const k=clamp(u/2.4);place(ava,lerp(5,2.4,ease(k)),lerp(8,4.0,ease(k)),u,{ry:Math.PI*1.1,walk:k<1?u:-1});}});
  // 39 Milo, you were never the first dreamer
  add(101.29,{cam:[V(2.2,1.5,6.6),V(2.3,1.45,6.0)],look:[V(2.4,1.3,4.0),V(2.4,1.35,4.0)],run(u){env(u,{sk:'night',L:.7});mili(u,{});place(ava,2.4,4.0,u,{ry:.25,talk:true});}});
  add(101.91,{cam:[V(2.3,1.45,6.5),V(2.4,1.45,5.9)],look:[V(2.4,1.3,4.0),V(2.4,1.4,4.0)],run(u){env(u,{sk:'night',L:.7});mili(u,{});place(ava,2.4,4.0,u,{ry:.25,talk:true});}});
  // 40 you are the last one. And tonight, the lamp needs more than a dream.
  add(103.54,{cam:[V(2.5,1.5,6.4),V(2.4,1.5,5.8)],look:[V(2.4,1.35,4.0),V(2.4,1.4,4.0)],run(u){env(u,{sk:'night',L:.9});mili(u,{});place(ava,2.4,4.0,u,{ry:.25,talk:true});}});
  add(104.73,{cam:[V(4,1.6,10),V(1,3,6)],look:[V(0,5.5,0),V(0,6,0)],run(u){env(u,{sk:'night',L:1+ease(u/2.6)*1.4});}});

  // durations from the next start; the video ends 0.8 s after the voice
  const END=108.0; S.forEach((s,i)=>{s.d=(i<S.length-1?S[i+1].t0:END)-s.t0; s.cap=[]; s.board=null;});
  S[0].mood='tense'; return S;
}
