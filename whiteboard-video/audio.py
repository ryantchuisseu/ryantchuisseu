import json, numpy as np, wave, sys
from scipy.signal import butter, lfilter
SR=44100
a=json.load(open('out/active.json')); fps=a['fps']; act=np.array(a['active'],float)
N=int(len(act)/fps*SR); t=np.arange(N)/SR
rng=np.random.default_rng(3)
# --- marker scribble: band-passed noise, gated by "drawing" + stroke-like tremolo
env=np.interp(t, np.arange(len(act))/fps, act)
env=np.convolve(env, np.ones(800)/800, 'same')
b,aa=butter(2,[1800/(SR/2),6500/(SR/2)],'band'); noise=lfilter(b,aa,rng.standard_normal(N))
trem=0.55+0.45*np.abs(np.sin(2*np.pi*(5.5+2*np.sin(t*0.7))*t))
marker=noise*env*trem*0.16
# --- music: soft pluck arpeggio + pad, C G Am F
bpm=92; beat=60/bpm
def note(m): return 440*2**((m-69)/12)
chords=[[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60]]
mus=np.zeros(N)
def add(f,start,dur,amp,decay):
  i0=int(start*SR); n=min(int(dur*SR),N-i0)
  if n<=0: return
  tt=np.arange(n)/SR
  s=(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt)+0.1*np.sin(6*np.pi*f*tt))*np.exp(-tt*decay)
  s*=np.minimum(1,tt/0.005); mus[i0:i0+n]+=s*amp
bar=4*beat; k=0; st=0
while st<N/SR:
  ch=chords[k%4]
  add(note(ch[0]-12),st,bar,0.10,1.2)
  for j in range(8):
    add(note(ch[[1,2,3,2,1,2,3,2][j]]+12),st+j*beat/2,beat*2,0.045,4.0)
  for m in ch[1:]: add(note(m),st,bar,0.018,0.4)
  st+=bar; k+=1
# fade
fade=np.minimum(1,t/1.0)*np.minimum(1,(N/SR-t)/1.5)
mus*=fade
# --- final "ding" when banner finishes drawing
last=np.where(act>0)[0][-1]/fps
for f,d in [(1318.5,0),(1760,0.09)]: add(f,last+0.15+d,1.5,0.0,0) 
ding=np.zeros(N)
for f,d in [(1318.5,0),(1975.5,0.1)]:
  i0=int((last+0.15+d)*SR); n=min(int(1.6*SR),N-i0); tt=np.arange(n)/SR
  ding[i0:i0+n]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*3.5)*0.12
out=marker+mus+ding
out/=max(1e-9,np.abs(out).max())/0.85
pcm=(np.stack([out,out],1)*32767).astype('<i2')
w=wave.open('out/audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('ok', N/SR)
