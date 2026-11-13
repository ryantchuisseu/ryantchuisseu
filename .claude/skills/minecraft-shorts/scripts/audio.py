"""Synthesised music bed + SFX for a project. Usage: python3 -I audio.py <project> [mood]
mood: happy (default) | calm | tense | epic. A shot may override with "mood" in shots.json (first shot wins for the bed).
SFX keys used by scenarios (sfx:[[key,u]]): chime, pop, whoosh, thud, poof, clang, boing. Cuts get a whoosh; caption chunks get a pop (when no voice)."""
import numpy as np, json, wave, sys, os
os.chdir(sys.argv[1] if len(sys.argv)>1 else '.')
SR=44100; shots=json.load(open('shots.json')); TOT=shots[-1]['t0']+shots[-1]['d']
mood=(sys.argv[2] if len(sys.argv)>2 else None) or next((s['mood'] for s in shots if s.get('mood')),'happy')
voice=os.path.exists('voix.mp3')
N=int(SR*(TOT+.2)); out=np.zeros(N); rng=np.random.default_rng(1)
mid=lambda m:440*2**((m-69)/12)
def add(sig,t,g=1.):
    i=int(t*SR)
    if i>=N or i<0: return
    s=sig[:N-i]*g; out[i:i+len(s)]+=s
def note(m,d,kind='mar',g=.25):
    n=int(d*SR); x=np.arange(n)/SR; f=mid(m)
    if kind=='mar': s=(np.sin(2*np.pi*f*x)+.35*np.sin(4*np.pi*f*x)*np.exp(-x*8)+.12*np.sin(2*np.pi*3.01*f*x)*np.exp(-x*14))*np.exp(-x*4.5)
    elif kind=='pad': s=(np.sin(2*np.pi*f*x)+.5*np.sin(2*np.pi*f*1.005*x))*np.minimum(1,x/.4)*np.exp(-x/(d*.8))*.5
    else: s=np.sign(np.sin(2*np.pi*f*x))*np.exp(-x*9)*.5     # plucky square
    return s*np.minimum(1,x/.004)
def kick():
    n=int(.35*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
# ---- bed ----
if mood=='happy':
    mel=[76,79,81,79,76,72,74,76,79,76,74,72,76,79,84,81,79,76]; bass=[48,53,48,55]
    for i in range(int(TOT/.35)): add(note(mel[i%len(mel)],.5),i*.35,.17)
    for i in range(int(TOT/1.4)): add(note(bass[i%4],1.2),i*1.4,.2)
elif mood=='calm':
    ch=[[57,60,64],[53,57,60],[55,59,62],[52,55,59]]
    for i in range(int(TOT/3)+1):
        for m in ch[i%4]: add(note(m,3.2,'pad'),i*3,.08)
    for i in range(int(TOT/.75)): add(note(ch[(i//4)%4][i%3]+12,.6),i*.75,.07)
elif mood in('tense','epic'):
    bpm=100 if mood=='tense' else 120; beat=60/bpm; prog=[38,34,31,33] if mood=='tense' else [41,43,45,43]; b=0;t=0.
    while t<TOT-.3:
        root=prog[(b//4)%4]
        if mood=='epic' or b%2==0: add(kick(),t,.5)
        add(note(root+12,beat*.9,'pluck'),t,.12); add(note(root+12,beat*.9,'pluck'),t+beat*.5,.09)
        if b%4==0:
            for m in (root+12,root+15,root+19): add(note(m,beat*4,'pad'),t,.09)
        b+=1;t+=beat
# ---- SFX ----
def lp(x,k=.1):
    y=np.zeros_like(x); a=0.
    for i in range(len(x)): a+=k*(x[i]-a); y[i]=a
    return y
def whoosh(): n=int(.3*SR); return lp(rng.standard_normal(n),.06)*np.sin(np.linspace(0,np.pi,n))**2*1.4
def pop(): n=int(.09*SR); x=np.arange(n)/SR; return np.sin(2*np.pi*(500+900*np.exp(-x*40))*x)*np.exp(-x*45)
def thud(): n=int(.6*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*(60+40*np.exp(-t*20))*t)*np.exp(-t*6)*1.1+lp(rng.standard_normal(n),.2)*np.exp(-t*25)
def chime(): return sum(note(m,.9,'mar')*g for m,g in [(84,1),(88,.8),(91,.7)])*1.2
def poofs(): n=int(.5*SR); return lp(rng.standard_normal(n),.12)*np.exp(-np.arange(n)/SR*8)*1.2
def clang(): n=int(.7*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*660*t)+.6*np.sin(2*np.pi*1040*t)+.4*np.sin(2*np.pi*1730*t))*np.exp(-t*7)*.5
def boing(): n=int(.5*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*np.cumsum(200+160*np.sin(t*40)*np.exp(-t*6))/SR)*np.exp(-t*7)*.6
FX=dict(whoosh=whoosh,pop=pop,thud=thud,chime=chime,poof=poofs,clang=clang,boing=boing)
for s in shots:
    if s['t0']>0: add(whoosh(),s['t0']-.05,.35)
    if not voice:
        for i in range(s['ncap']): add(pop(),s['t0']+i*s['d']/max(1,s['ncap']),.3)
    if s.get('stamp') is not None: add(thud(),s['stamp'],.8)
    for k,at in s['sfx']: add(FX[k](),at,.5)
out[-int(.4*SR):]*=np.linspace(1,0,int(.4*SR))
out=np.clip(out/max(1e-6,np.max(np.abs(out)))*.8,-1,1)
with wave.open('music.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
print('music.wav',TOT,'s mood',mood)
