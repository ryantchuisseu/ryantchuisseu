import numpy as np, subprocess, sys, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(D, "assets")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, "video_noaudio.mp4")
PREVIEW = os.environ.get("PREVIEW")  # comma list of times -> png stills
W, H, FPS = 1080, 1920, 30

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_sub = ImageFont.truetype(SERIF_B, 58)
f_subi = ImageFont.truetype(SERIF_BI, 58)
f_tag1 = ImageFont.truetype(MONO, 17)
f_tag2 = ImageFont.truetype(SERIF_B, 25)
f_small = ImageFont.truetype(SANS_B, 18)

CREAM = (241, 232, 212)
INK = (28, 20, 14)
RED = (178, 28, 24)

# (image, start, end, words, red-word indexes, tag, pan(dx,dy), zoom(a,b), italic)
S = [
 ("s1", 0.0, 4.6, "« Je n'ai pas été le père que vous méritiez. »", {6}, "Alain, le père, au soir de sa vie", (0.00, -0.03), (1.10, 1.00), True),
 ("s2", 4.6, 9.6, "Ce soir-là, à Yaoundé, Alain, mourant, réunit ses enfants.", {5}, "Villa d'Ékounou, Yaoundé · chapitre 1", (0.00, 0.03), (1.00, 1.12), False),
 ("s3", 9.6, 14.8, "Quatre enfants. Quatre mères. Aucun ne connaît les autres.", {0, 2}, "Le salon d'Alain · la réunion", (0.02, 0.00), (1.12, 1.02), False),
 ("s4", 14.8, 20.4, "Kegne n'a connu son père que sous la forme d'un billet plié dans une enveloppe.", {10}, "Kegne et sa mère Fondjo · marché de Balengou", (-0.03, 0.0), (1.02, 1.12), False),
 ("s5", 20.4, 26.0, "Sa demi-sœur Ndutu l'a humiliée. Elles ne se sont jamais revues… jusqu'à ce soir.", {4}, "Kegne et Ndutu · au collège", (0.0, -0.03), (1.14, 1.02), False),
 ("s6", 26.0, 31.4, "« Va te plaindre chez ton père. » Mais quel père ? Elle ne lui avait jamais vu le visage.", {9}, "Hermine · Bertoua", (0.02, 0.02), (1.00, 1.12), False),
 ("s7", 31.4, 36.8, "Franck attendait un appel. Chaque fois qu'il le guettait, la sonnerie se taisait.", {3}, "Franck Ella · Ngaoundéré", (-0.02, 0.0), (1.12, 1.02), False),
 ("s8", 36.8, 43.2, "Et il y a elle. Trois ans qu'elle sert cet homme… sans savoir qu'il est son père.", {4, 16}, "Mariana · la domestique de la villa", (0.03, 0.0), (1.00, 1.14), False),
 ("s9", 43.2, 48.4, "Pour comprendre, il faut remonter jusqu'à un village appelé Wara…", {9}, "Le regard d'Alain", (0.0, 0.0), (1.00, 1.30), False),
]
END_T = 48.4
TOTAL = 56.0
XF = 0.45  # crossfade

def load(name):
    im = Image.open(os.path.join(A, name + ".png")).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s * 1.3), int(im.height * s * 1.3)), Image.LANCZOS)
    return im
IM = {s[0]: load(s[0]) for s in S}

def ease(x):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(x, 0), 1))

def kb(im, p, pan, zoom, focus=(0.5, 0.5)):
    z = zoom[0] + (zoom[1] - zoom[0]) * ease(p)
    base = im.width / 1.3 / W  # pixels in im per output px at zoom 1
    sc = base / (1.3 * z) * 1.3 / 1.0
    sc = (im.width / 1.3) / W / z
    cx = im.width * (focus[0] + pan[0] * (ease(p) - 0.5))
    cy = im.height * (focus[1] + pan[1] * (ease(p) - 0.5))
    x0 = cx - W / 2 * sc
    y0 = cy - H / 2 * sc
    x0 = min(max(x0, 0), im.width - W * sc); y0 = min(max(y0, 0), im.height - H * sc)
    return im.transform((W, H), Image.AFFINE, (sc, 0, x0, 0, sc, y0), Image.BILINEAR)

# vignette + grain
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.9 + ((yy - H * 0.47) / (H / 2)) ** 2)
VIG = np.clip(1.15 - 0.55 * r ** 1.8, 0.25, 1.0)[..., None].astype(np.float32)
rng = np.random.default_rng(3)
GRAIN = [rng.normal(0, 9, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
GRAIN = [np.kron(g, np.ones((2, 2), np.float32))[..., None] for g in GRAIN]

# dust particles
NP = 90
P0 = np.column_stack([rng.uniform(0, W, NP), rng.uniform(0, H, NP)])
PV = np.column_stack([rng.normal(0, 6, NP), rng.uniform(-28, -8, NP)])
PS = rng.uniform(1.5, 4.5, NP); PA = rng.uniform(0.25, 0.8, NP); PPH = rng.uniform(0, 6.28, NP)
def dust(arr, t):
    pos = P0 + PV * t
    pos[:, 0] = (pos[:, 0] + 15 * np.sin(t * 0.7 + PPH)) % W
    pos[:, 1] = pos[:, 1] % H
    for (x, y), s, a, ph in zip(pos, PS, PA, PPH):
        a = a * (0.6 + 0.4 * math.sin(t * 2 + ph))
        x0, x1 = int(max(x - s * 2, 0)), int(min(x + s * 2 + 1, W))
        y0, y1 = int(max(y - s * 2, 0)), int(min(y + s * 2 + 1, H))
        if x1 <= x0 or y1 <= y0: continue
        gy, gx = np.mgrid[y0:y1, x0:x1]
        g = np.exp(-((gx - x) ** 2 + (gy - y) ** 2) / (2 * (s * 0.6) ** 2)) * a
        arr[y0:y1, x0:x1] += g[..., None] * np.array([255, 205, 140], np.float32) * 0.9

def tag(draw, title, alpha):
    if alpha <= 0: return
    x, y = 46, 150
    l1 = "ILLUSTRATION IA · RECONSTITUTION"
    w1 = draw.textlength(l1, font=f_tag1); w2 = draw.textlength(title, font=f_tag2)
    a = int(235 * alpha)
    draw.rectangle([x, y, x + w1 + 20, y + 28], fill=CREAM + (a,))
    draw.text((x + 10, y + 5), l1, font=f_tag1, fill=(110, 95, 75, a))
    draw.rectangle([x, y + 32, x + w2 + 20, y + 72], fill=CREAM + (a,))
    draw.text((x + 10, y + 37), title, font=f_tag2, fill=INK + (a,))

def wrap(words, font, maxw, draw):
    lines, cur = [], []
    for i, w in enumerate(words):
        test = " ".join(x for _, x in cur + [(i, w)])
        if cur and draw.textlength(test, font=font) > maxw:
            lines.append(cur); cur = []
        cur.append((i, w))
    if cur: lines.append(cur)
    return lines

def subtitle(draw, text, reds, p, italic, alpha, y0=1270):
    font = f_subi if italic else f_sub
    words = text.split()
    lines = wrap(words, font, 900, draw)
    n = len(words)
    shown = p * n / 0.72  # words revealed over first 72% of scene
    sp = draw.textlength(" ", font=font)
    lh = 84
    y = y0
    for line in lines:
        widths = [draw.textlength(w, font=font) for _, w in line]
        tw = sum(widths) + sp * (len(line) - 1)
        x = (W - tw) / 2
        draw.rectangle([x - 16, y - 8, x + tw + 16, y + 66], fill=CREAM + (int(238 * alpha),))
        for (i, w), ww in zip(line, widths):
            k = min(max(shown - i, 0), 1)
            if i in reds and k >= 1:
                draw.rectangle([x - 6, y - 2, x + ww + 6, y + 62], fill=RED + (int(255 * alpha),))
                col = (255, 245, 235)
            else:
                col = INK
            a = int((70 + 185 * k) * alpha)
            draw.text((x, y), w, font=font, fill=col + (a,))
            x += ww + sp
        y += lh

def scene_frame(sc, t):
    name, t0, t1, text, reds, ttl, pan, zoom, ital = sc
    p = (t - t0) / (t1 - t0)
    zz = zoom
    focus = (0.5, 0.5)
    if name == "s9":
        focus = (0.5, 0.46)
        # accelerate into the iris at the end
        if p > 0.7:
            q = (p - 0.7) / 0.3
            zz = (zoom[0], zoom[1] + 2.4 * q ** 3)
    img = kb(IM[name], p, pan, zz, focus)
    return img

def ui(img, sc, t, a_ui=1.0):
    name, t0, t1, text, reds, ttl, *_ = sc
    p = (t - t0) / (t1 - t0)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    fin = min((t - t0) / 0.35, 1) * min((t1 - t) / 0.3, 1)
    tag(d, ttl, max(fin, 0) * a_ui)
    subtitle(d, text, reds, p, ital := sc[8], max(fin, 0) * a_ui)
    d.text((40, H - 70), "AI-generated", font=f_small, fill=(230, 220, 200, 120))
    img = img.convert("RGBA"); img.alpha_composite(ov)
    return img.convert("RGB")

# end card
COVER = Image.open(os.path.join(A, "cover.jpg")).convert("RGB")
BG_END = IM["s3"].resize((W, int(W * IM["s3"].height / IM["s3"].width))).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(28))
BG_END = Image.blend(BG_END, Image.new("RGB", (W, H), (20, 10, 6)), 0.55)
f_e1 = ImageFont.truetype(MONO, 26); f_e2 = ImageFont.truetype(SERIF_B, 46); f_e3 = ImageFont.truetype(SERIF_I, 36); f_e4 = ImageFont.truetype(SANS_B, 34)
def end_frame(t):
    p = (t - END_T) / (TOTAL - END_T)
    img = BG_END.copy()
    cw = int(600 * (1.0 + 0.04 * p)); ch = int(cw * COVER.height / COVER.width)
    cv = COVER.resize((cw, ch), Image.LANCZOS)
    cx, cy = (W - cw) // 2, 300 + int(10 * (1 - ease(min((t - END_T) / 1.2, 1))) * 8)
    sh = Image.new("RGBA", (cw + 120, ch + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([60, 70, cw + 60, ch + 70], fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(25))
    img = img.convert("RGBA"); img.alpha_composite(sh, (cx - 60, cy - 60)); img.paste(cv, (cx, cy))
    d = ImageDraw.Draw(img)
    def ctext(y, s, f, col, a):
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=col + (int(255 * a),))
    a1 = ease((t - END_T - 0.3) / 0.8)
    ctext(200, "L E   R O M A N", f_e1, CREAM, a1)
    a2 = ease((t - END_T - 1.2) / 0.8)
    ctext(cy + ch + 50, "Une enfance volée", f_e2, CREAM, a2)
    ctext(cy + ch + 108, "Un père mal connu · Pouni Ichaka Hamadjoda", f_e3, (220, 200, 170), a2)
    a3 = ease((t - END_T - 2.2) / 0.7)
    s = "DISPONIBLE SUR BOOKSHOP.ORG"; w = d.textlength(s, font=f_e4)
    by = cy + ch + 190
    d.rectangle([(W - w) / 2 - 30, by, (W + w) / 2 + 30, by + 74], fill=RED + (int(255 * a3),))
    d.text(((W - w) / 2, by + 17), s, font=f_e4, fill=(255, 245, 235, int(255 * a3)))
    ctext(by + 100, "Broché · 17,99 $  —  lien en bio", f_e3, CREAM, a3)
    return img.convert("RGB")

def frame(t):
    if t >= END_T:
        img = end_frame(t)
        arr = np.asarray(img, np.float32)
        # white flash fading out
        fl = max(0.0, 1 - (t - END_T) / 0.6)
        arr = arr * (1 - fl) + 255 * fl
    else:
        cur = [s for s in S if s[1] <= t < s[2]][0]
        i = S.index(cur)
        img = ui(scene_frame(cur, t), cur, t)
        # crossfade with next scene
        if i + 1 < len(S) and t > cur[2] - XF and S[i + 1][0] != "s9":
            nxt = S[i + 1]
            k = (t - (cur[2] - XF)) / XF
            img2 = ui(scene_frame(nxt, nxt[1]), nxt, nxt[1], 0)
            img = Image.blend(img, img2, ease(k))
        arr = np.asarray(img, np.float32)
        # fades: in from black at start, dip to black before s9, white flash end of s9
        if t < 0.6: arr *= t / 0.6
        if cur[0] == "s8" and t > cur[2] - 0.35: arr *= (cur[2] - t) / 0.35
        if cur[0] == "s9" and t < cur[1] + 0.4: arr *= (t - cur[1]) / 0.4
        if cur[0] == "s9" and t > cur[2] - 0.5:
            k = (t - (cur[2] - 0.5)) / 0.5; arr = arr * (1 - k) + 255 * k
        # impact shake on scene start
        dt = t - cur[1]
        if 0 < dt < 0.25 and cur[0] in ("s1", "s5", "s8"):
            sh = int(10 * (1 - dt / 0.25) * math.sin(dt * 90))
            arr = np.roll(arr, sh, axis=0)
    arr *= VIG
    # warm grade
    arr[..., 0] *= 1.04; arr[..., 2] *= 0.93
    dust(arr, t)
    arr += GRAIN[int(t * FPS) % 6]
    return np.clip(arr, 0, 255).astype(np.uint8)

if PREVIEW:
    for tt in PREVIEW.split(","):
        Image.fromarray(frame(float(tt))).resize((540, 960)).save(os.path.join(D, f"prev_{tt}.jpg"), quality=85)
    sys.exit()

N = int(TOTAL * FPS)
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for n in range(N):
    pr.stdin.write(frame(n / FPS).tobytes())
    if n % 150 == 0: print(n, "/", N, flush=True)
pr.stdin.close(); pr.wait()
print("done")
