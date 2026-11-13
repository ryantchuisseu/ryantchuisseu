"""Dark-cinematic music bed for day 1 ("The Village Where Nobody Sleeps"), music only (no voice).
Usage: python3 -I music.py <out.wav>
Style taken from signal analysis of 3 reference shorts: A-minor sustained pad, sub drone that swells in the last third,
slow heartbeat pulse (~60 bpm, accelerating toward the climax), sparse bell notes, a few big impacts at plot beats, no drums.
Edit CHORDS / INT / HITS / RISERS / HEART below to re-time it for another episode."""
import numpy as np, scipy.signal as ss, wave, sys
SR=44100; DUR=108.0; TAIL=3.0; N=int(SR*(DUR+TAIL)); rng=np.random.default_rng(7)
mid=lambda m:440*2**((m-69)/12); T=np.arange(N)/SR
def curve(pts): ts,vs=zip(*pts); return np.interp(T,ts,vs)
# ---- timeline (seconds) ----
INT=curve([(0,.25),(14,.35),(30,.4),(33,.3),(45,.45),(49,.5),(58,.6),(61,.8),(76.2,.85),(76.67,.1),(78,.5),(85,.45),(97,.6),(104,.95),(107.0,1.0),(111,.0)])
DUCK=np.ones(N); i0,i1,i2=int(76.1*SR),int(76.66*SR),int(77.6*SR); DUCK[i0:i1]=np.linspace(1,.03,i1-i0); DUCK[i1:i2]=np.linspace(.03,1,i2-i1)
Am=[45,52,57,60,64]; F=[41,48,53,57,60]; C=[48,52,55,60,64]; G=[43,50,55,59,62]; Dm=[50,53,57,62,65]; E=[40,47,52,56,59]; AmB=[45,52,57,58,64]
CHORDS=[Am,Am,F,F,Am,Am,G,E, C,G,Am,F, Am,AmB,Am, Dm,Am,E,AmB,E, F,C,Dm,Am, Am,F,E,E]   # 4 s per bar
HITS=[(49.0,.35),(51.05,.5),(58.78,.7),(64.74,.75),(71.58,.4),(76.67,1.0),(85.02,.55),(97.93,.4),(101.29,.5),(105.45,.7),(107.02,1.0)]
RISERS=[(56.4,58.78,.5),(74.4,76.6,.8),(97.9,107.0,1.0)]
HUM=(58.78,77.0)
def place(buf,sig,t0,gl=1.,gr=1.):
    i=int(t0*SR); n=min(len(sig),N-i)
    if n>0: buf[0,i:i+n]+=sig[:n]*gl; buf[1,i:i+n]+=sig[:n]*gr
dry=np.zeros((2,N)); wet=np.zeros((2,N))
# ---- pad ----
padL=np.zeros(N); padR=np.zeros(N)
for b,ch in enumerate(CHORDS):
    t0=b*4.0; d=5.6; m=int(d*SR); x=np.arange(m)/SR; e=np.clip(np.minimum(x/1.3,(d-x)/1.6),0,1)**1.5
    for k,n in enumerate(ch):
        f=mid(n); s_l=sum(2*(((x*f*(1+c))+ph)%1)-1 for c,ph in ((-.004,0),(0,.3),(.004,.6)))/3; s_r=sum(2*(((x*f*(1+c))+ph)%1)-1 for c,ph in ((.004,.2),(0,.5),(-.004,.8)))/3
        g=.5 if n<48 else .35; i=int(t0*SR); j=min(N,i+m)
        padL[i:j]+=s_l[:j-i]*e[:j-i]*g; padR[i:j]+=s_r[:j-i]*e[:j-i]*g
dk=ss.butter(2,420,'low',fs=SR,output='sos'); br=ss.butter(2,1700,'low',fs=SR,output='sos'); W=np.clip(INT*.9,0,1)
pad=[ss.sosfilt(dk,p)*(1-W)+ss.sosfilt(br,p)*W for p in (padL,padR)]
dry[0]+=pad[0]*.22*DUCK; dry[1]+=pad[1]*.22*DUCK; wet[0]+=pad[0]*.09*DUCK; wet[1]+=pad[1]*.09*DUCK
# ---- sub drone A1/A2 swelling with intensity ----
lfo=.8+.2*np.sin(2*np.pi*.17*T)
sub=(np.sin(2*np.pi*55*T)+.5*np.sin(2*np.pi*55.35*T)+.35*np.sin(2*np.pi*110*T+1))*lfo*(INT**1.8)*.30*DUCK
dry[0]+=sub; dry[1]+=sub
# ---- "moon hum": formant-ish vocal-like drone ----
a,b=HUM; hm=int((b-a+2)*SR); x=np.arange(hm)/SR; vib=1+.004*np.sin(2*np.pi*5*x); he=np.clip(np.minimum((x)/2.4,(b-a+2-x)/1.6),0,1)**2
hum=sum(np.sin(2*np.pi*110*vib*h*x+h)/ (h**1.1) * (1.0 if h in (1,2,3,5) else .45) for h in range(1,9))+.7*sum(np.sin(2*np.pi*111.6*vib*h*x)/h for h in (1,2,3))
hum=ss.sosfilt(ss.butter(2,900,'low',fs=SR,output='sos'),hum)*he*.065
place(dry,hum,a,1.,1.); place(wet,hum,a,.5,.5)
# ---- heartbeat (lub-dub), accelerating at the climax ----
def thump(f0=95,f1=42,d=.26):
    n=int(d*SR); x=np.arange(n)/SR; f=f1+(f0-f1)*np.exp(-x*28); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*15)
def beats(a,b,bpm_pts):
    t=a; out=[]
    while t<b: out.append(t); t+=60/np.interp(t,*zip(*bpm_pts))
    return out
HEART=[(14,49,[(14,60),(49,60)],.22),(49,58,[(49,60),(58,66)],.32),(58,76.0,[(58,66),(76,92)],.42),(78,96,[(78,58),(96,60)],.3),(97,107,[(97,62),(107,118)],.5)]
for a,b,pts,g in HEART:
    for t in beats(a,b,pts):
        gi=g*np.interp(t,T[::4410],INT[::4410])
        place(dry,thump()*gi,t); place(dry,thump(85,40,.22)*gi*.65,t+.27)
# ---- bells (music-box) ----
def bell(f,vel=1.,d=3.2):
    n=int(d*SR); x=np.arange(n)/SR
    return (np.sin(2*np.pi*f*x)*np.exp(-x*2.6)+.4*np.sin(2*np.pi*2*f*x)*np.exp(-x*5)+.14*np.sin(2*np.pi*3.02*f*x)*np.exp(-x*9)+.05*np.sin(2*np.pi*5.4*f*x)*np.exp(-x*14))*vel*np.minimum(1,x/.004)
def bellat(m,t,v=.3,pan=0.):
    s=bell(mid(m),v*.5); place(dry,s,t,.6*(1-pan),.6*(1+pan)); place(wet,s,t,1.0,1.0)
pent=[69,72,74,76,79,81,84]  # A minor pentatonic
tt=3.0
while tt<30: bellat(int(rng.choice(pent))+12,tt,.32,rng.uniform(-.7,.7)); tt+=rng.uniform(2.2,4.2)
motif=[88,86,84,86,88,91,88,86]  # lantern motif
for k in range(24): bellat(motif[k%8],35.0+k*.5,.36,-.5 if k%2 else .5)
for k,(n,t) in enumerate([(69,85.5),(76,87.5),(72,89.5),(69,91.5),(64,93.5),(72,95.5),(69,99.0)]): bellat(n,t,.3,0.)
bellat(81,105.45,.4,-.4); bellat(82,105.45,.4,.4)   # dissonant pair at "tonight, the lamp needs more than a dream"
# ---- impacts and risers ----
def boom(vel):
    n=int(3.4*SR); x=np.arange(n)/SR; f=32+55*np.exp(-x*9); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*1.3)*.9
    nz=ss.sosfilt(ss.butter(2,[60,900],'band',fs=SR,output='sos'),rng.standard_normal(n))*np.exp(-x*7)*.5; return (s+nz)*vel
for t,v in HITS:
    s=boom(v); place(dry,s,t,.8,.8); place(wet,s,t,.5,.5)
for a,b,v in RISERS:
    n=int((b-a)*SR); x=np.arange(n)/SR; u=x/(b-a)
    nz=ss.sosfilt(ss.butter(2,[1200,7000],'band',fs=SR,output='sos'),rng.standard_normal((2,n)),axis=1)*(u**2.5)*.22*v
    f=110*np.exp(u*np.log(4)); ton=np.sin(2*np.pi*np.cumsum(f)/SR)*(u**2)*.16*v
    place(dry,ton,a,1,1); dry[0,int(a*SR):int(a*SR)+n]+=nz[0]; dry[1,int(a*SR):int(a*SR)+n]+=nz[1]; place(wet,ton,a,.4,.4)
# ---- reverb on the wet bus ----
L=int(3.0*SR); x=np.arange(L)/SR; ir=rng.standard_normal((2,L))*np.exp(-x*2.1)[None]; ir=ss.sosfilt(ss.butter(2,5500,'low',fs=SR,output='sos'),ir,axis=1); ir=ss.sosfilt(ss.butter(2,160,'high',fs=SR,output='sos'),ir,axis=1); ir/=np.sqrt((ir**2).sum(1,keepdims=True))
rev=np.stack([ss.fftconvolve(wet[c],ir[c])[:N] for c in range(2)])
mix=dry+rev*.9
mix[:, -int(.6*SR):]*=np.linspace(1,0,int(.6*SR))
mix=np.tanh(mix*1.1)/np.tanh(1.1); mix*=0.89/np.max(np.abs(mix))
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix.T*32767).astype('<i2').tobytes())
print('ok',round(N/SR,1),'s; peak',round(float(np.max(np.abs(mix))),2))
