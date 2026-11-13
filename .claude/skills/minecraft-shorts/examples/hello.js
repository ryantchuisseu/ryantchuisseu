// 7 s — "Oula, bonjour, moi je m'appelle Claude. Comment tu vas ?" : minimal 3-shot example.
export default function(E){
  const {V,pose,title,line,crowdLook,makeChar,textSprite,easeOutBack,clamp,CAP}=E;
  CAP.y=0.2;                                   // captions in the upper area, away from faces
  const hero=makeChar({skin:'#8d5524',hair:'#1a1a1a',shirt:'#d97757',pants:'#2b2b38',collar:'#ffffff'});
  const tag=textSprite('Claude');
  const place=(u,extra={},showTag=false)=>{pose(hero,{x:0,y:.9,z:-4.3,ry:0,t:u,talk:true,...extra});tag.visible=showTag;tag.position.set(0,3.35,-4.3);};
  const BOARD=['hi',g=>{title(g,'BONJOUR !',200,120);line(g,'JE SUIS CLAUDE',360,80,'#2b4f9e');}];
  return [
    {d:2.2,cap:['Oula,','bonjour !'],cam:[V(0,3.6,9.5),V(0,3.3,7.2)],look:[V(0,3.0,-4),V(0,3.0,-4)],board:BOARD,
     chat:[['Claude joined the game',.15]],sfx:[['chime',.1]],
     run(u){place(u,{wave:easeOutBack(u/.4)},true);crowdLook(u,i=>({armsUp:u>1.1&&i%2?clamp((u-1.1)/.3):0}));}},
    {d:2.6,cap:['Moi,','je m’appelle','Claude.'],cam:[V(1.3,2.5,-1.0),V(.8,2.6,-1.7)],look:[V(0,2.7,-4.3),V(0,2.75,-4.3)],board:null,
     run(u){place(u,{headTilt:Math.sin(u*3)*.08});hero.armR.rotation.set(-1.1*clamp((u-.5)/.3),0,.5*clamp((u-.5)/.3));}},
    {d:2.2,cap:['Comment','tu vas ?'],cam:[V(.4,2.95,-2.0),V(.1,3.0,-2.7)],look:[V(0,2.98,-4.3),V(0,2.98,-4.3)],board:null,
     run(u){place(u,{wave:.55,headTilt:.12*Math.sin(u*4)});}}
  ];
}
