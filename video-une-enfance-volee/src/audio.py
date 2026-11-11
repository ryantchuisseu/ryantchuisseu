import numpy as np, wave, os
SR = 44100; T = 56.0; N = int(SR * T)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
out = np.zeros((N, 2))

def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR); j = min(i + len(sig), N); sig = sig[: j - i] * gain
    out[i:j, 0] += sig * (1 - max(pan, 0)); out[i:j, 1] += sig * (1 + min(pan, 0))

def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); s = 0.0
    for k in range(len(x)): s += a * (x[k] - s); y[k] = s
    return y

# 1) drone (A minor), swelling, cut for the silence before the end card
drone = (np.sin(2*np.pi*55*t) + 0.6*np.sin(2*np.pi*55.4*t) + 0.35*np.sin(2*np.pi*82.4*t) + 0.2*np.sin(2*np.pi*110.3*t))
drone *= 0.5 + 0.25*np.sin(2*np.pi*t/9)
de = np.clip(t/3, 0, 1) * np.clip((48.0 - t)/0.4, 0, 1)
de += (t > 48.4) * np.clip((t-48.4)/0.2, 0, 1) * np.clip((T - t)/2.5, 0, 1) * 0.9
out += (drone * de * 0.10)[:, None]

# 2) melancholic piano-like notes
def note(f, d=3.5):
    n = int(d*SR); tt = np.arange(n)/SR
    s = sum(a*np.sin(2*np.pi*f*h*tt) * np.exp(-tt*(1.4+h*0.9)) for h, a in [(1,1),(2,.45),(3,.2),(4,.08)])
    return s * env(n, 0.005, 0.3)
A3,C4,D4,E4,F4,G4,A4,B3 = 220,261.6,293.7,329.6,349.2,392,440,246.9
mel = [(0.6,A4),(2.4,E4),(4.6,C4),(6.4,E4),(8.0,D4),(9.6,A3),(11.4,C4),(13.0,E4),(14.8,F4),(16.6,E4),(18.4,D4),(20.4,A3),
       (22.2,C4),(24.0,B3),(26.0,A3),(27.8,C4),(29.6,E4),(31.4,F4),(33.2,E4),(35.0,D4),(36.8,A4),(38.6,G4),(40.4,E4),(42.0,C4),
       (43.2,A3),(45.0,E4),(46.6,A4)]
for at, f in mel: add(note(f), at, 0.11, pan=0.25*np.sin(at))
# bass hits per scene
for at, f in [(0,55),(4.6,55),(9.6,43.6),(14.8,49),(20.4,55),(26,43.6),(31.4,49),(36.8,55),(43.2,41.2)]:
    add(note(f, 4.5), at, 0.22)

# 3) impacts (low boom) on key cuts
def boom(d=1.6, f0=90, f1=35):
    n = int(d*SR); tt = np.arange(n)/SR
    f = f1 + (f0-f1)*np.exp(-tt*6); ph = 2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*2.6) + 0.3*rng.normal(0,1,n)*np.exp(-tt*25)
for at, g in [(0.0,.55),(20.4,.4),(36.8,.5),(48.4,.75)]: add(boom(), at, g)

# 4) whooshes into each transition
def whoosh(d=0.7):
    n = int(d*SR); x = rng.normal(0,1,n); x = lp(x, 0.08)
    return x * np.sin(np.linspace(0, np.pi, n))**2 * 3
for at in [4.6,9.6,14.8,20.4,26.0,31.4,36.8,43.2]: add(whoosh(), at-0.5, 0.18, pan=rng.uniform(-.5,.5))

# 5) clock ticks (scenes 2-8)
tick = rng.normal(0,1,int(0.012*SR)) * np.exp(-np.arange(int(0.012*SR))/80)
for k, at in enumerate(np.arange(5.0, 43.0, 1.0)): add(tick, at, 0.10 if k % 2 else 0.07, pan=0.3)

# 6) muffled phone ring (scene 7)
def ring(d=1.0):
    n = int(d*SR); tt = np.arange(n)/SR
    s = (np.sin(2*np.pi*440*tt)+np.sin(2*np.pi*480*tt)) * (np.sin(2*np.pi*20*tt) > 0)
    return lp(s, 0.12) * env(n, 0.02, 0.1)
add(ring(), 32.6, 0.10, -0.3); add(ring(0.55), 34.4, 0.07, -0.3)

# 7) heartbeat (scene 9), accelerating
def beat():
    n = int(0.16*SR); tt = np.arange(n)/SR
    return np.sin(2*np.pi*50*tt)*np.exp(-tt*28)
at = 43.5; gap = 0.95
while at < 48.0:
    add(beat(), at, 0.8); add(beat(), at+0.2, 0.55); at += gap; gap *= 0.88

# 8) paper rustle on the subtitles of scenes 4-5
for at in [15.0, 20.6]:
    n = int(0.35*SR); x = rng.normal(0,1,n) * (rng.random(n) > 0.7)
    add(x*env(n,0.02,0.2), at, 0.05)

# master
out = np.tanh(out * 1.4) * 0.85
out[: int(0.05*SR)] *= np.linspace(0, 1, int(0.05*SR))[:, None]
pcm = (out * 32767).astype(np.int16)
with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", np.abs(out).max())
