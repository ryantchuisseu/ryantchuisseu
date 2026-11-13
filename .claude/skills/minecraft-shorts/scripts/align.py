"""Aligne un script texte sur la voix off (sans modèle de reconnaissance vocale).

Usage : python3 -I align.py <voix.mp3> <script.txt> <words.json> [seuil_dB]

Méthode : ffmpeg silencedetect découpe la voix en segments parlés ; le script est découpé en
unités (à chaque ponctuation) ; une programmation dynamique répartit les unités contiguës sur
les segments en minimisant l'écart au débit moyen (caractères/seconde) ; dans chaque segment,
les mots reçoivent un temps proportionnel à leur longueur. Précision typique : ±0,15 s.
Sortie : [{"w": mot affiché, "k": clé minuscule sans ponctuation, "t": début, "e": fin}, ...]
et un rapport segment par segment sur stdout pour vérification.
"""
import json, re, subprocess, sys

audio, script, out = sys.argv[1], sys.argv[2], sys.argv[3]
thr = sys.argv[4] if len(sys.argv) > 4 else '-38'
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio],
                           capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-i', audio, '-af', f'silencedetect=n={thr}dB:d=0.16', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
sil = [(a, b) for a, b in zip(st, en) if a > 0.05]            # ignore leading silence
lead = en[0] if st and st[0] <= 0.05 else 0.0
segs, cur = [], lead
for a, b in sil:
    if a - cur > 0.05: segs.append([cur, a])
    cur = b
if dur - cur > 0.1: segs.append([cur, dur])

text = open(script, encoding='utf-8').read().replace('\n', ' ')
text = re.sub(r'[«»"]', '', text)
units = [u.strip() for u in re.split(r'(?<=[.?!:…,;])\s+', text) if u.strip()]
units = [u for u in units if re.search(r'\w', u)]

def chars(u): return len(re.sub(r'\s+', ' ', u))
# too many segments (pauses inside a unit): drop the shortest silences
while len(segs) > len(units):
    gaps = [(segs[i + 1][0] - segs[i][1], i) for i in range(len(segs) - 1)]
    _, i = min(gaps); segs[i] = [segs[i][0], segs[i + 1][1]]; del segs[i + 1]

U, S = len(units), len(segs)
cs = [chars(u) for u in units]
rate = sum(cs) / sum(b - a for a, b in segs)
pre = [0]
for c in cs: pre.append(pre[-1] + c)
INF = float('inf')
dp = [[INF] * (S + 1) for _ in range(U + 1)]; bk = [[0] * (S + 1) for _ in range(U + 1)]
dp[0][0] = 0
for j in range(1, S + 1):
    d = segs[j - 1][1] - segs[j - 1][0]
    for i in range(j, U - (S - j) + 1):
        for k in range(j - 1, i):
            if dp[k][j - 1] == INF: continue
            c = dp[k][j - 1] + (d - (pre[i] - pre[k]) / rate) ** 2
            if j < S and units[i - 1].endswith(','): c += 0.5   # pauses fall more often after . ? ! : …
            if c < dp[i][j]: dp[i][j], bk[i][j] = c, k
groups, i = [], U
for j in range(S, 0, -1):
    k = bk[i][j]; groups.append((k, i)); i = k
groups.reverse()

words = []
print(f'durée {dur:.2f}s · {S} segments · {U} unités · débit {rate:.1f} car/s')
for (a, b), (k, i) in zip(segs, groups):
    ws = ' '.join(units[k:i]).split()
    L = [len(w) + 1 for w in ws]; tot = sum(L); t = a
    print(f'[{a:6.2f}-{b:6.2f}] {" ".join(units[k:i])}')
    for w, l in zip(ws, L):
        d = (b - a) * l / tot
        key = re.sub(r"[^\w'-]", '', w.lower())
        words.append({'w': w, 'k': key, 't': round(t, 3), 'e': round(t + d, 3)})
        t += d
# glue lone punctuation ("?", ":") to the previous word
clean = []
for w in words:
    if not re.search(r'\w', w['w']) and clean:
        clean[-1]['w'] += ' ' + w['w']; clean[-1]['e'] = w['e']
    else: clean.append(w)
json.dump(clean, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f'{len(clean)} mots -> {out}')
