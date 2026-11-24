# JCIA 2027 — présentation v2 « éditoriale » : une idée par slide, photos plein cadre, Sora.
import sys, os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

IMG, BRAND, OUT = sys.argv[1], sys.argv[2], sys.argv[3]   # dossier photos, dossier logo/carte, fichier de sortie
TOGHU = sys.argv[4]

# === Design tokens (charte JCIA) ===
NUIT = RGBColor(0x0F, 0x13, 0x27); NUIT_HEX = '0F1327'
SURF = RGBColor(0x18, 0x20, 0x39)
LIGNE = RGBColor(0x2C, 0x31, 0x47)
ORANGE = RGBColor(0xF6, 0xA3, 0x43)
TURQ = RGBColor(0x2D, 0xB8, 0xBD)
TERRA = RGBColor(0xCD, 0x60, 0x35)
VIOLET = RGBColor(0x9D, 0x87, 0xDC)
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
GRIS = RGBColor(0xB5, 0xBA, 0xD0)
FANTOME = RGBColor(0x3A, 0x41, 0x5E)       # grands chiffres en retrait
AXES = [ORANGE, TURQ, TERRA, VIOLET]
F_DISPLAY, F_BOLD, F_SEMI, F_BODY, F_LIGHT = 'Sora ExtraBold', 'Sora', 'Sora SemiBold', 'Sora', 'Sora Light'

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
M = Inches(0.75)                               # marge
TOTAL = 17
st = {'n': 0}

# === Outils ===
def tx(s, x, y, w, h, paras, font=F_BODY, size=18, color=BLANC, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       spacing=1.05, track=0, bold=False):
    """paras: str | list de paragraphes; paragraphe = str | list[(texte, opts)]"""
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    tf.vertical_anchor = anchor
    for i, p in enumerate(paras if isinstance(paras, list) else [paras]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align; para.line_spacing = spacing
        for seg, o in (p if isinstance(p, list) else [(p, {})]):
            r = para.add_run(); r.text = seg; f = r.font
            f.name = o.get('font', font); f.size = Pt(o.get('size', size)); f.color.rgb = o.get('color', color)
            f.bold = o.get('bold', bold)
            t = o.get('track', track)
            if t: r._r.get_or_add_rPr().set('spc', str(int(t)))
        sa = (p[0][1].get('after') if isinstance(p, list) and p else None)
        if sa is not None: para.space_after = Pt(sa)
    return tb

def label(s, x, y, t, color=ORANGE, w=Inches(8)):
    return tx(s, x, y, w, Inches(0.3), t.upper(), font=F_SEMI, size=11, color=color, track=300)

def box(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(shape, x, y, w, h); r.fill.solid(); r.fill.fore_color.rgb = color
    r.line.fill.background(); r.shadow.inherit = False
    return r

def gradient(s, x, y, w, h, stops, angle):
    """Voile en dégradé : stops = [(position%, alpha%)], angle en degrés (0 = gauche→droite, 90 = haut→bas)."""
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h); r.line.fill.background(); r.shadow.inherit = False
    spPr = r._element.spPr
    for tag in ('a:solidFill', 'a:noFill', 'a:gradFill'):
        for e in spPr.findall(qn(tag)): spPr.remove(e)
    g = etree.SubElement(spPr, qn('a:gradFill')); g.set('rotWithShape', '1')
    lst = etree.SubElement(g, qn('a:gsLst'))
    for pos, a in stops:
        gs = etree.SubElement(lst, qn('a:gs')); gs.set('pos', str(int(pos * 1000)))
        c = etree.SubElement(gs, qn('a:srgbClr')); c.set('val', NUIT_HEX)
        al = etree.SubElement(c, qn('a:alpha')); al.set('val', str(int(a * 1000)))
    lin = etree.SubElement(g, qn('a:lin')); lin.set('ang', str(int(angle * 60000))); lin.set('scaled', '0')
    # le remplissage doit précéder la ligne dans spPr
    ln = spPr.find(qn('a:ln'))
    if ln is not None: spPr.remove(ln); spPr.append(ln)
    return r

def photo(s, name, x, y, w, h, focus_y=0.4):
    path = os.path.join(IMG, name + '.jpg'); iw, ih = Image.open(path).size
    pic = s.shapes.add_picture(path, x, y, w, h)
    box_r, img_r = w / h, iw / ih
    if img_r > box_r:
        c = (1 - box_r / img_r) / 2; pic.crop_left = c; pic.crop_right = c
    else:
        c = 1 - img_r / box_r; pic.crop_top = c * focus_y; pic.crop_bottom = c * (1 - focus_y)
    return pic

def fade_pic(pic, amount):
    blip = pic._element.find('.//' + qn('a:blip'))
    a = etree.SubElement(blip, qn('a:alphaModFix')); a.set('amt', str(int(amount * 1000)))

def toghu(s, y=None, height=None):
    h = height or int(W * 72 / 1100)
    s.shapes.add_picture(TOGHU, 0, (H - h) if y is None else y, width=W, height=h)

def slide(bg=NUIT, chrome=True, notes=''):
    s = prs.slides.add_slide(prs.slide_layouts[6]); st['n'] += 1
    s.background.fill.solid(); s.background.fill.fore_color.rgb = bg
    # transition en fondu
    tr = etree.SubElement(s._element, qn('p:transition')); tr.set('spd', 'slow')
    etree.SubElement(tr, qn('p:fade'))
    if notes: s.notes_slide.notes_text_frame.text = notes
    s._chrome = chrome
    return s

def chrome(s, light=False):
    """Repères discrets : marque en haut, pagination en bas (ajoutés en dernier pour rester au-dessus des photos)."""
    c = GRIS
    tx(s, M, Inches(0.42), Inches(4), Inches(0.3), [[('JCIA ', {'font': F_DISPLAY}), ('2027', {'font': F_LIGHT})]], size=12, color=BLANC, track=100)
    tx(s, W - M - Inches(3), Inches(0.42), Inches(3), Inches(0.3), [[(f'{st["n"]:02d}', {'font': F_SEMI, 'color': BLANC}), (f'  /  {TOTAL:02d}', {'font': F_LIGHT, 'color': c})]],
       size=12, align=PP_ALIGN.RIGHT, track=100)

LOGO = os.path.join(BRAND, 'logo.png'); CARTE = os.path.join(BRAND, 'carte.png')

# =============================================================
# VERSION FINALE — un seul gabarit pour toutes les slides :
# panneau bleu nuit à gauche (filet orange), cartes encadrées, photo encadrée d'orange à droite.
LOGO_DIR = sys.argv[5]
PANEL = RGBColor(0x1A, 0x22, 0x3C)
PAD = Inches(0.32)
LX = Inches(0.8)
YEL = RGBColor(0xF5, 0xC5, 0x18)
CREAM_O = RGBColor(0xF9, 0xCF, 0x9B)

def base(n, lab=None, lab_color=ORANGE, full=False):
    s = slide()
    s.background.fill.solid(); s.background.fill.fore_color.rgb = NUIT
    pw = (W - 2 * PAD) if full else Inches(7.55)
    box(s, PAD, PAD, pw, H - 2 * PAD, PANEL)
    box(s, PAD, PAD, pw, Inches(0.07), ORANGE)
    tx(s, LX, Inches(0.7), Inches(6.5), Inches(0.3), f'JCIA 2027  ·  {n:02d} / 17', font=F_SEMI, size=11, color=GRIS, track=200)
    if lab:
        tx(s, LX, Inches(1.0), Inches(9), Inches(0.3), lab, font=F_SEMI, size=11, color=lab_color, track=200)
    return s

def ttl(s, lines, y=Inches(1.35), size=32, w=Inches(6.9)):
    tx(s, LX, y, w, Inches(1.8), [[(t, {'color': c})] for t, c in lines], font=F_DISPLAY, size=size, color=BLANC, spacing=1.0)

def card(s, x, y, w, h, color, fill=NUIT, width=1.5):
    c = box(s, x, y, w, h, fill, MSO_SHAPE.ROUNDED_RECTANGLE); c.adjustments[0] = 0.07
    c.line.color.rgb = color; c.line.width = Pt(width)
    return c

def framed(s, x, y, w, h, name, focus=0.4, color=ORANGE):
    box(s, x - Inches(0.06), y - Inches(0.06), w + Inches(0.12), h + Inches(0.12), color)
    photo(s, name, x, y, w, h, focus)

def stat(s, x, y, w, h, val, lab, color, vsize=24):
    card(s, x, y, w, h, color)
    tx(s, x + Inches(0.2), y + Inches(0.12), w - Inches(0.4), Inches(0.55), val, font=F_DISPLAY, size=vsize, color=color)
    tx(s, x + Inches(0.2), y + h - Inches(0.5), w - Inches(0.4), Inches(0.4), lab, font=F_LIGHT, size=12, color=GRIS, spacing=1.1)

RX, RW = Inches(8.2), Inches(4.75)

# 01 — COUVERTURE
s = slide(chrome=False, notes='Journées Camerounaises de l’Intelligence Artificielle, 3e édition, 27 et 28 avril 2027, Hilton Hotel de Yaoundé. Événement satellite du Geneva AI Summit 2027. Photo : JCIA 2025.')
box(s, PAD, PAD, Inches(7.55), H - 2 * PAD, PANEL); box(s, PAD, PAD, Inches(7.55), Inches(0.07), ORANGE)
s.shapes.add_picture(LOGO, LX, Inches(0.8), width=Inches(2.7))
tx(s, LX, Inches(2.55), Inches(6.5), Inches(0.3), '3e édition  ·  Geneva AI Summit 2027', font=F_SEMI, size=11, color=ORANGE, track=200)
ttl(s, [('Penser l’IA au Cameroun,', BLANC), ('pour le Cameroun.', ORANGE)], y=Inches(2.95), size=34)
tx(s, LX, Inches(4.6), Inches(6.5), Inches(0.9), [[('Journées Camerounaises de l’Intelligence Artificielle', {'font': F_SEMI, 'size': 15, 'color': BLANC})], [('27 & 28 avril 2027  ·  Hilton Hotel, Yaoundé', {'size': 14, 'color': GRIS})]], font=F_LIGHT, spacing=1.4)
box(s, LX, Inches(6.35), Inches(6.7), Pt(1), LIGNE)
tx(s, LX, Inches(6.5), Inches(6.7), Inches(0.4), 'Événement satellite du Geneva AI Summit 2027', font=F_LIGHT, size=12, color=GRIS)
framed(s, RX, Inches(0.5), RW, Inches(6.2), 'public_salle', 0.4)

# 02 — POSITIONNEMENT
s = base(2, 'POSITIONNEMENT')
s.notes_slide.notes_text_frame.text = 'Message clé : les JCIA 2027 sont l’événement satellite (side event) préparatoire du Geneva AI Summit 2027 et la porte d’entrée nationale vers le AI for Good Global Summit de l’UIT.'
ttl(s, [('De Yaoundé', BLANC), ('à Genève.', ORANGE)], y=Inches(1.45), size=46)
tx(s, LX, Inches(3.3), Inches(6.4), Inches(1.5), 'Les JCIA 2027 sont l’événement satellite du Geneva AI Summit 2027 et la porte d’entrée nationale vers le AI for Good Global Summit de l’UIT.', font=F_LIGHT, size=16, color=GRIS, spacing=1.35)
pill = box(s, LX, Inches(5.2), Inches(3.9), Inches(0.5), PANEL, MSO_SHAPE.ROUNDED_RECTANGLE); pill.adjustments[0] = 0.5
pill.line.color.rgb = ORANGE; pill.line.width = Pt(1.25)
tx(s, LX, Inches(5.2), Inches(3.9), Inches(0.5), 'LABEL ROAD TO GENEVA AI SUMMIT', font=F_SEMI, size=11, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, track=150)
card(s, RX, Inches(0.5), RW, Inches(6.2), ORANGE, fill=PANEL)
mh = Inches(5.5); mw = int(mh * 328 / 476)
s.shapes.add_picture(CARTE, RX + (RW - mw) // 2, Inches(0.85), mw, mh)

# 03 — L'ORGANISATEUR
s = base(3, 'L’ORGANISATEUR')
s.notes_slide.notes_text_frame.text = 'IAC – CAIPI : organisation à but non lucratif fondée le 6 octobre 2023 à Yaoundé. Partenariats stratégiques : GTEK et Geneva AI Governance Institute (GAIGI). Photo : visite officielle, JCIA 2025.'
ttl(s, [('IAC – CAIPI', BLANC)], y=Inches(1.35), size=40)
tx(s, LX, Inches(2.4), Inches(6.6), Inches(0.9), 'Think tank et plateforme de dialogue multi-acteurs, fondé le 6 octobre 2023 à Yaoundé.', font=F_LIGHT, size=15, color=GRIS, spacing=1.3)
box(s, LX, Inches(3.4), Inches(0.06), Inches(0.85), ORANGE)
tx(s, LX + Inches(0.28), Inches(3.4), Inches(6.2), Inches(0.9), '« Faire du Cameroun une nation qui conçoit, développe et gouverne l’IA de manière souveraine, éthique et inclusive. »', font=F_SEMI, size=14, color=BLANC, spacing=1.2)
steps = ['Accompagner l’État dans sa Stratégie nationale de l’IA', 'Fédérer chercheurs, startups, entreprises et diaspora', 'Promouvoir une IA éthique, conforme à l’UNESCO']
fills = [RGBColor(0x1B, 0x26, 0x4A), RGBColor(0x17, 0x3F, 0x63), RGBColor(0x12, 0x5C, 0x6E)]
for i, t in enumerate(steps):
    y = Inches(4.5 + i * 0.78)
    ch = s.shapes.add_shape(MSO_SHAPE.PENTAGON, LX, y, Inches(6.7), Inches(0.66))
    ch.fill.solid(); ch.fill.fore_color.rgb = fills[i]; ch.line.fill.background(); ch.shadow.inherit = False
    tx(s, LX + Inches(0.3), y, Inches(0.6), Inches(0.66), f'0{i+1}', font=F_DISPLAY, size=18, color=AXES[i], anchor=MSO_ANCHOR.MIDDLE)
    tx(s, LX + Inches(1.0), y, Inches(5.3), Inches(0.66), t, font=F_SEMI, size=14, color=BLANC, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
framed(s, RX, Inches(0.5), RW, Inches(6.2), 'officiels', 0.3, color=YEL)

# 04 — LE CONSTAT
s = base(4, 'POURQUOI LES JCIA')
s.notes_slide.notes_text_frame.text = 'Contexte : Recommandation UNESCO sur l’éthique de l’IA (nov. 2021, 193 États) ; Stratégie continentale de l’IA de l’Union africaine (juil. 2024) ; Stratégie nationale de l’IA du Cameroun (juil. 2025) ; rapport UNESCO RAM (fév. 2026) ; le Cameroun parmi les 29 pays fondateurs de WAICO (juil. 2026).'
ttl(s, [('Un écosystème qui', BLANC), ('bouillonne, mais encore trop', BLANC), ('peu visible, financé et connecté.', ORANGE)], y=Inches(1.4), size=26)
tx(s, LX, Inches(3.15), Inches(6.5), Inches(0.9), 'Comment en faire un écosystème structuré, financé, visible et compétitif ?', font=F_LIGHT, size=17, color=BLANC, spacing=1.3)
tx(s, LX, Inches(4.3), Inches(6.5), Inches(1.2), 'Les JCIA 2027 apportent une réponse intégrée à quatre enjeux : visibilité, financement, structuration et projection internationale.', font=F_LIGHT, size=14, color=GRIS, spacing=1.35)
tl = [('2021', 'Éthique de l’IA : recommandation UNESCO'), ('2024', 'Stratégie continentale de l’IA (UA)'), ('2025', 'Stratégie nationale de l’IA du Cameroun'),
      ('2026', 'Le Cameroun, membre fondateur de WAICO'), ('2027', 'JCIA 2027, en route vers Genève')]
for i, (yv, t) in enumerate(tl):
    y = Inches(0.5 + i * 1.09); last = i == 4
    card(s, RX, y, RW, Inches(0.95), ORANGE if last else LIGNE)
    tx(s, RX + Inches(0.25), y, Inches(1.1), Inches(0.95), yv, font=F_DISPLAY, size=22, color=ORANGE if last else BLANC, anchor=MSO_ANCHOR.MIDDLE)
    tx(s, RX + Inches(1.45), y, Inches(3.15), Inches(0.95), t, font=F_LIGHT, size=13, color=BLANC, anchor=MSO_ANCHOR.MIDDLE, spacing=1.15)

# 05 — LES CHIFFRES 2027
s = base(5, 'CHANGEMENT D’ÉCHELLE  ·  OBJECTIFS 2027')
s.notes_slide.notes_text_frame.text = 'Objectifs 2027 (toujours « attendus ») : 7 000+ participants en présentiel, 5 000+ en ligne, 150+ startups et exposants, 40+ intervenants, 20+ délégations diplomatiques, 500+ rencontres B2B et B2G, 2 millions de personnes touchées.'
tx(s, LX, Inches(1.4), Inches(6.9), Inches(1.9), '7 000+', font=F_DISPLAY, size=100, color=ORANGE, spacing=0.9)
tx(s, LX, Inches(3.5), Inches(6.7), Inches(0.5), 'participants attendus au Hilton de Yaoundé.', font=F_LIGHT, size=20, color=BLANC)
tx(s, LX, Inches(4.3), Inches(6.4), Inches(1.0), 'D’un événement national phare à une plateforme africaine d’influence.', font=F_LIGHT, size=15, color=GRIS, spacing=1.35)
box(s, LX, Inches(5.7), Inches(1.2), Inches(0.06), ORANGE)
framed(s, RX, Inches(0.5), RW, Inches(2.7), 'panel_intervenante', 0.35)
sts = [('5 000+', 'en ligne'), ('150+', 'startups et exposants'), ('40+', 'intervenants'), ('20+', 'délégations'), ('500+', 'rendez-vous B2B / B2G'), ('2 M+', 'personnes touchées')]
for i, (k, v) in enumerate(sts):
    stat(s, RX + (i % 2) * Inches(2.5), Inches(3.5) + (i // 2) * Inches(1.1), Inches(2.25), Inches(0.95), k, v, AXES[i % 4], 20)

# 06 — TRAJECTOIRE
s = base(6, 'NOTRE TRAJECTOIRE')
s.notes_slide.notes_text_frame.text = '2023 : 1re édition (IRIC et ENSPY, décembre), 1 000+ participants, 17 intervenants. 2025 : 2e édition (Hilton, ENSPY, IRIC, avril), 5 000 sur place + 2 000 en ligne, ~100 startups, 60+ organisations, 1ers Awards, 1er Salon 100 % IA. 2027 : 7 000+ sur place et 5 000+ en ligne attendus.'
ttl(s, [('Trois éditions, une', BLANC), ('ambition qui grandit.', ORANGE)], y=Inches(1.4), size=30)
eds = [('2023', 'L’acte fondateur', '1 000+ participants · 17 intervenants'), ('2025', 'L’étape décisive', '5 000 + 2 000 en ligne · ~100 startups'), ('2027', 'Cap sur Genève', '7 000+ attendus · side event du AI for Good')]
for i, (yv, t, d) in enumerate(eds):
    y = Inches(2.9 + i * 1.3); last = i == 2
    card(s, LX, y, Inches(6.7), Inches(1.15), ORANGE if last else LIGNE)
    tx(s, LX + Inches(0.3), y, Inches(1.5), Inches(1.15), yv, font=F_DISPLAY, size=30, color=ORANGE if last else GRIS, anchor=MSO_ANCHOR.MIDDLE)
    tx(s, LX + Inches(1.95), y, Inches(4.6), Inches(1.15), [[(t, {'font': F_SEMI, 'size': 16, 'color': BLANC, 'after': 3})], [(d, {'font': F_LIGHT, 'size': 12, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE, spacing=1.15)
card(s, RX, Inches(0.5), RW, Inches(6.2), ORANGE, fill=PANEL)
tx(s, RX + Inches(0.3), Inches(0.75), Inches(4.2), Inches(0.35), 'PARTICIPANTS PAR ÉDITION', font=F_SEMI, size=11, color=GRIS, track=200)
for j, (c, t) in enumerate([(GRIS, 'Sur place'), (CREAM_O, 'En ligne')]):
    box(s, RX + Inches(0.3 + j * 1.6), Inches(1.2), Inches(0.16), Inches(0.16), c)
    tx(s, RX + Inches(0.55 + j * 1.6), Inches(1.14), Inches(1.3), Inches(0.3), t, font=F_LIGHT, size=11, color=GRIS)
base_y = Inches(6.0); sc = Inches(3.5) / 12000
bars = [(0, 1000, 0, GRIS, CREAM_O, '1 000+'), (1, 5000, 2000, GRIS, CREAM_O, '7 000'), (2, 7000, 5000, ORANGE, CREAM_O, '12 000+')]
for i, on, onl, c1, c2, tot in bars:
    x = RX + Inches(0.4 + i * 1.5)
    h1, h2 = int(on * sc), int(onl * sc)
    box(s, x, base_y - h1, Inches(1.1), h1, c1)
    if h2: box(s, x, base_y - h1 - h2, Inches(1.1), h2, c2)
    tx(s, x - Inches(0.1), base_y - h1 - h2 - Inches(0.45), Inches(1.3), Inches(0.4), tot, font=F_DISPLAY, size=16, color=ORANGE if i == 2 else BLANC, align=PP_ALIGN.CENTER)
    tx(s, x - Inches(0.1), base_y + Inches(0.1), Inches(1.3), Inches(0.35), ['2023', '2025', '2027'][i], font=F_SEMI, size=13, color=ORANGE if i == 2 else GRIS, align=PP_ALIGN.CENTER)
box(s, RX + Inches(0.3), base_y, RW - Inches(0.6), Pt(1.5), LIGNE)

# 07 — JCIA 2025
s = base(7, 'CE QUE NOUS AVONS DÉJÀ BÂTI')
s.notes_slide.notes_text_frame.text = 'Retour sur la 2e édition (22–24 avril 2025, Hilton Hotel de Yaoundé, ENSPY et IRIC) sous le patronage du Ministère des Postes et Télécommunications et de la Commission nationale pour l’UNESCO. Photos : JCIA 2025.'
ttl(s, [('JCIA 2025', BLANC)], y=Inches(1.4), size=42)
st25 = [('5 000', 'participants sur place'), ('2 000', 'participants en ligne'), ('~100', 'startups'), ('60+', 'organisations'), ('53', 'projets aux 1ers Awards'), ('1er', 'Salon National 100 % IA')]
for i, (k, v) in enumerate(st25):
    stat(s, LX + (i % 2) * Inches(3.45), Inches(2.75) + (i // 2) * Inches(1.3), Inches(3.25), Inches(1.15), k, v, AXES[i % 4], 26)
framed(s, RX, Inches(0.5), RW, Inches(3.5), 'officiels_scene', 0.3)
framed(s, RX, Inches(4.35), Inches(2.3), Inches(2.3), 'pupitre_hilton', 0.3)
framed(s, RX + Inches(2.45), Inches(4.35), Inches(2.3), Inches(2.3), 'salon_echange', 0.4)

# 08 — THÈME
s = base(8)
s.notes_slide.notes_text_frame.text = 'Thème officiel de la 3e édition : « Penser l’intelligence artificielle au Cameroun, pour le Cameroun ». Quatre piliers : innovation souveraine, excellence camerounaise, solutions locales, influence mondiale. Photos : plénière et intervenants, JCIA 2025.'
ttl(s, [('Penser l’IA', BLANC), ('au Cameroun,', ORANGE), ('pour le Cameroun.', BLANC)], y=Inches(1.3), size=36)
tx(s, LX, Inches(3.1), Inches(6.7), Inches(0.6), 'Le thème de la 3e édition : une IA pensée par et pour les Camerounais.', font=F_LIGHT, size=14, color=GRIS, spacing=1.3)
pillars = [('Innovation souveraine', 'Maîtriser technologies, données, modèles et compétences.'), ('Excellence camerounaise', 'Célébrer nos talents au niveau des standards mondiaux.'),
           ('Solutions locales', 'Langues nationales, agriculture, santé, services publics.'), ('Influence mondiale', 'Prendre notre place dans la gouvernance de l’IA.')]
for i, (t, d) in enumerate(pillars):
    x = LX + (i % 2) * Inches(3.5); y = Inches(3.9) + (i // 2) * Inches(1.6)
    card(s, x, y, Inches(3.25), Inches(1.4), AXES[i])
    tx(s, x + Inches(0.28), y + Inches(0.17), Inches(0.9), Inches(0.5), f'0{i+1}', font=F_DISPLAY, size=24, color=AXES[i])
    tx(s, x + Inches(0.28), y + Inches(0.66), Inches(2.8), Inches(0.35), t, font=F_SEMI, size=14, color=BLANC)
    tx(s, x + Inches(0.28), y + Inches(0.96), Inches(2.8), Inches(0.42), d, font=F_LIGHT, size=11, color=GRIS, spacing=1.15)
framed(s, RX, Inches(0.5), RW, Inches(3.9), 'conf_panel', 0.45)
framed(s, RX, Inches(5.0), Inches(2.3), Inches(1.9), 'panel_intervenante', 0.35)
framed(s, RX + Inches(2.5), Inches(5.0), Inches(2.25), Inches(1.9), 'public_proche', 0.35)

# 09 — GENÈVE
s = base(9, 'ÉVÉNEMENT SATELLITE')
s.notes_slide.notes_text_frame.text = 'Le AI for Good Global Summit est organisé par l’UIT avec plus de 50 agences des Nations Unies : 11 000+ participants, 800+ intervenants, 19 milliards d’impressions médias.'
ttl(s, [('La route du Geneva AI', BLANC), ('Summit 2027 passe par', BLANC), ('Yaoundé.', ORANGE)], y=Inches(1.4), size=28)
box(s, LX, Inches(3.35), Inches(0.28), Inches(0.28), ORANGE, MSO_SHAPE.OVAL)
for k in range(14):
    box(s, LX + Inches(0.45 + k * 0.33), Inches(3.46), Inches(0.17), Pt(3), LIGNE if k % 2 else GRIS)
box(s, LX + Inches(5.1), Inches(3.35), Inches(0.28), Inches(0.28), TURQ, MSO_SHAPE.OVAL)
tx(s, LX, Inches(3.75), Inches(3), Inches(0.8), [[('Yaoundé', {'font': F_DISPLAY, 'size': 18})], [('27 & 28 avril 2027', {'font': F_LIGHT, 'size': 12, 'color': ORANGE})]], spacing=1.1)
tx(s, LX + Inches(4.4), Inches(3.75), Inches(2.3), Inches(0.8), [[('Genève', {'font': F_DISPLAY, 'size': 18})], [('21 & 22 juin 2027', {'font': F_LIGHT, 'size': 12, 'color': TURQ})]], spacing=1.1, align=PP_ALIGN.RIGHT)
tx(s, LX, Inches(4.85), Inches(6.5), Inches(0.3), 'AI FOR GOOD GLOBAL SUMMIT  ·  UIT', font=F_SEMI, size=10, color=GRIS, track=200)
for i, (k, v) in enumerate([('11 000+', 'participants'), ('800+', 'intervenants'), ('50+', 'agences ONU')]):
    stat(s, LX + i * Inches(2.25), Inches(5.25), Inches(2.1), Inches(1.2), k, v, AXES[i], 22)
framed(s, RX, Inches(0.5), RW, Inches(2.0), 'visite_stand', 0.4)
objs = [('Préparer', 'la délégation nationale et ses messages'), ('Promouvoir', 'les solutions camerounaises les plus mûres'), ('Faire rayonner', 'le Cameroun auprès de l’ONU et des médias'),
        ('Investir', 'en reliant porteurs de projets et investisseurs'), ('Coopérer', 'avec des partenaires technologiques étrangers')]
for i, (t, d) in enumerate(objs):
    y = Inches(2.85 + i * 0.76); c = (AXES + [ORANGE])[i]
    card(s, RX, y, RW, Inches(0.66), c)
    tx(s, RX + Inches(0.2), y, Inches(0.6), Inches(0.66), f'0{i+1}', font=F_DISPLAY, size=16, color=c, anchor=MSO_ANCHOR.MIDDLE)
    tx(s, RX + Inches(0.85), y, Inches(3.8), Inches(0.66), [[(t, {'font': F_SEMI, 'size': 13, 'color': BLANC, 'after': 1})], [(d, {'font': F_LIGHT, 'size': 10.5, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)

# 10 — QUATRE AXES
s = base(10, 'AXES STRATÉGIQUES')
s.notes_slide.notes_text_frame.text = 'Quatre enjeux de l’écosystème camerounais de l’IA, quatre réponses concrètes en 2027.'
ttl(s, [('Quatre enjeux,', BLANC), ('une réponse intégrée.', ORANGE)], y=Inches(1.4), size=30)
axes = [('Visibilité', 'UNE VITRINE', 'Le Salon National 100 % IA'), ('Financement', 'UN PONT', 'Startup Pitch, investisseurs et sponsors'),
        ('Structuration', 'UN OUTIL', 'L’Annuaire national des acteurs de l’IA'), ('Rayonnement', 'UN TREMPLIN', 'Side event du AI for Good et délégation à Genève')]
for i, (t, k, d) in enumerate(axes):
    x = LX + (i % 2) * Inches(3.5); y = Inches(2.8) + (i // 2) * Inches(2.1)
    card(s, x, y, Inches(3.25), Inches(1.9), AXES[i])
    tx(s, x + Inches(0.25), y + Inches(0.15), Inches(0.9), Inches(0.5), f'0{i+1}', font=F_DISPLAY, size=24, color=AXES[i])
    tx(s, x + Inches(0.25), y + Inches(0.7), Inches(2.8), Inches(0.35), t, font=F_SEMI, size=15, color=BLANC)
    tx(s, x + Inches(0.25), y + Inches(1.02), Inches(2.8), Inches(0.25), k, font=F_SEMI, size=9, color=AXES[i], track=200)
    tx(s, x + Inches(0.25), y + Inches(1.28), Inches(2.8), Inches(0.55), d, font=F_LIGHT, size=11.5, color=GRIS, spacing=1.15)
framed(s, RX, Inches(0.5), RW, Inches(6.2), 'public_proche', 0.4)

# 11 — PROGRAMME
s = base(11, 'AU PROGRAMME  ·  27 & 28 AVRIL 2027')
s.notes_slide.notes_text_frame.text = 'Jour 1 (mardi 27 avril, 08h00–18h00) : cérémonie officielle d’ouverture ; inauguration du Salon ; plénières « Souveraineté et modèles d’IA africains » et « Financer l’excellence » ; démos et rencontres B2B/B2G. Jour 2 (mercredi 28 avril) : quatre masterclasses avec attestation ; Startup Pitch ; Women in AI Forum ; Young AI Leaders Forum ; gala des Awards (sur invitation). Photo : conférence, JCIA 2025.'
ttl(s, [('Conférences et', BLANC), ('masterclasses.', ORANGE)], y=Inches(1.4), size=32)
def prog_card(y, title, color, items):
    card(s, LX, y, Inches(6.7), Inches(1.85), color)
    tx(s, LX + Inches(0.25), y + Inches(0.2), Inches(6.2), Inches(0.35), title, font=F_SEMI, size=12, color=color, track=200)
    for j, it in enumerate(items):
        yy = y + Inches(0.58 + j * 0.31)
        box(s, LX + Inches(0.27), yy + Inches(0.1), Inches(0.1), Inches(0.1), color, MSO_SHAPE.OVAL)
        tx(s, LX + Inches(0.5), yy, Inches(6.0), Inches(0.32), it, font=F_LIGHT, size=14, color=BLANC)
prog_card(Inches(2.75), 'CONFÉRENCES', ORANGE, ['Cérémonie officielle d’ouverture', 'Plénière · Souveraineté et modèles d’IA africains', 'Plénière · Financer l’excellence', 'Women in AI  ·  Young AI Leaders'])
prog_card(Inches(4.8), 'MASTERCLASSES CERTIFIANTES', TURQ, ['IA générative et administration publique', 'IA et santé', 'IA, agriculture et sécurité alimentaire', 'Cybersécurité et gouvernance de l’IA'])
tx(s, LX, Inches(6.85), Inches(6.9), Inches(0.3), [[('Et aussi : ', {'font': F_SEMI, 'color': ORANGE}), ('Startup Pitch  ·  AI Career Fair  ·  B2B / B2G  ·  Gala des Awards', {})]], font=F_LIGHT, size=12, color=GRIS)
framed(s, RX, Inches(0.5), RW, Inches(4.5), 'conf_panel', 0.4)
for i, (k, v) in enumerate([('2', 'jours'), ('4', 'masterclasses'), ('1', 'gala')]):
    x = RX + i * Inches(1.65)
    box(s, x, Inches(5.35), Inches(1.5), Pt(1.5), AXES[i])
    tx(s, x, Inches(5.5), Inches(1.5), Inches(0.6), k, font=F_DISPLAY, size=30, color=AXES[i])
    tx(s, x, Inches(6.1), Inches(1.5), Inches(0.4), v, font=F_LIGHT, size=13, color=GRIS)

# 12 — SALON
s = base(12, 'AXE 01  ·  VISIBILITÉ')
s.notes_slide.notes_text_frame.text = 'Exposants : startups, entreprises tech, laboratoires, administrations, universités, incubateurs, diaspora. Les 50 projets présélectionnés aux CAIA exposent gratuitement. Réserver un stand : contact@jciacm.com. Photo : stand, JCIA 2025.'
ttl(s, [('Le Salon National', BLANC), ('100 % IA', ORANGE)], y=Inches(1.4), size=32)
tx(s, LX, Inches(2.75), Inches(6.5), Inches(0.9), 'La plus grande exposition du Cameroun dédiée à l’IA, inaugurée par des membres du Gouvernement.', font=F_LIGHT, size=15, color=GRIS, spacing=1.3)
for i, (k, v) in enumerate([('150+', 'exposants'), ('200', 'solutions'), ('2', 'jours')]):
    stat(s, LX + i * Inches(2.25), Inches(3.75), Inches(2.1), Inches(1.15), k, v, AXES[i], 26)
for i, t in enumerate(['Démonstrations en continu sur la scène du Salon', 'Rencontres B2B et B2G', 'Application de mise en relation']):
    y = Inches(5.15 + i * 0.62)
    card(s, LX, y, Inches(6.7), Inches(0.5), LIGNE)
    box(s, LX + Inches(0.22), y + Inches(0.2), Inches(0.1), Inches(0.1), AXES[i], MSO_SHAPE.OVAL)
    tx(s, LX + Inches(0.5), y, Inches(6.0), Inches(0.5), t, font=F_LIGHT, size=14, color=BLANC, anchor=MSO_ANCHOR.MIDDLE)
framed(s, RX, Inches(0.5), RW, Inches(6.2), 'salon_siad', 0.4)

# 13 — AWARDS
s = base(13, 'CAMEROON AI AWARDS 2027')
s.notes_slide.notes_text_frame.text = '10 catégories : santé, agriculture, éducation, fintech, administration publique, cybersécurité, langues nationales et culture, recherche, Femme de l’année en IA, Jeune talent. Calendrier : candidatures du 15 nov. 2026 au 28 fév. 2027 ; 50 présélectionnés publiés le 15 mars ; vote du public du 20 mars au 15 avril ; gala le 28 avril 2027. Photo : lauréats, JCIA 2025.'
ttl(s, [('L’excellence,', BLANC), ('célébrée.', ORANGE)], y=Inches(1.4), size=32)
fun = [(300, 'candidatures visées', 6.0, RGBColor(0x2E, 0x37, 0x5A)), (50, 'projets présélectionnés', 4.6, RGBColor(0x55, 0x60, 0x9A)), (10, 'lauréats', 3.2, ORANGE)]
for i, (n, t, wd, c) in enumerate(fun):
    y = Inches(2.85 + i * 0.95); x = LX + Inches((6.7 - wd) / 2)
    b = box(s, x, y, Inches(wd), Inches(0.78), c, MSO_SHAPE.ROUNDED_RECTANGLE); b.adjustments[0] = 0.15
    tx(s, x, y, Inches(wd), Inches(0.78), [[(str(n) + '  ', {'font': F_DISPLAY, 'size': 24}), (t, {'font': F_LIGHT, 'size': 12})]], color=NUIT if i == 2 else BLANC, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, LX, Inches(5.85), Inches(4.0), Inches(0.36), TURQ); box(s, LX + Inches(4.0), Inches(5.85), Inches(2.7), Inches(0.36), VIOLET)
tx(s, LX, Inches(5.85), Inches(4.0), Inches(0.36), 'Jury 60 %', font=F_SEMI, size=12, color=NUIT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
tx(s, LX + Inches(4.0), Inches(5.85), Inches(2.7), Inches(0.36), 'Vote du public 40 %', font=F_SEMI, size=12, color=NUIT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
tx(s, LX, Inches(6.5), Inches(6.7), Inches(0.4), '10 catégories, de la santé à la recherche scientifique.', font=F_LIGHT, size=12, color=GRIS)
framed(s, RX, Inches(0.5), RW, Inches(2.64), 'awards_2025', 0.5)
cal = [('15 nov. 2026', 'Ouverture des candidatures'), ('28 fév. 2027', 'Clôture des candidatures'), ('20 mars → 15 avril', 'Vote du public'), ('28 avril 2027', 'Gala et remise des prix')]
for i, (d, t) in enumerate(cal):
    y = Inches(3.5 + i * 0.82); last = i == 3
    card(s, RX, y, RW, Inches(0.72), ORANGE if last else LIGNE)
    tx(s, RX + Inches(0.25), y, Inches(4.3), Inches(0.72), [[(d, {'font': F_SEMI, 'size': 14, 'color': ORANGE if last else BLANC, 'after': 1})], [(t, {'font': F_LIGHT, 'size': 11.5, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)

# 14 — ANNUAIRE
s = base(14, 'AXE 03  ·  STRUCTURATION', lab_color=TERRA)
s.notes_slide.notes_text_frame.text = 'Réalisé sous la supervision du Comité scientifique : appel public, vérification, catégorisation standardisée, mise à jour annuelle. Consentement explicite, droit de rectification, minimisation des données. Inscription : contact@jciacm.com. La répartition des points par famille est illustrative. Photo : échanges entre acteurs, JCIA 2025.'
ttl(s, [('L’Annuaire national', BLANC), ('des acteurs de l’IA', ORANGE)], y=Inches(1.4), size=30)
tx(s, LX, Inches(2.85), Inches(6.5), Inches(0.9), 'Les acteurs clés de l’écosystème, recensés et vérifiés. Édition imprimée et version en ligne : catalogue.jcia.cm.', font=F_LIGHT, size=14, color=GRIS, spacing=1.3)
for k in range(100):
    r_, c_ = divmod(k, 20)
    box(s, LX + Inches(c_ * 0.33), Inches(3.95 + r_ * 0.3), Inches(0.2), Inches(0.2), AXES[min(3, k // 25)], MSO_SHAPE.OVAL)
tx(s, LX, Inches(5.7), Inches(4), Inches(1.0), [[('1 000+', {'font': F_DISPLAY, 'size': 32, 'color': ORANGE})], [('acteurs visés  ·  1 point = 10 acteurs', {'font': F_LIGHT, 'size': 12, 'color': GRIS})]], spacing=1.05)
framed(s, RX, Inches(0.5), RW, Inches(4.5), 'salon_echange', 0.4)
card(s, RX, Inches(5.3), RW, Inches(1.35), LIGNE)
for i, f in enumerate(['Chercheurs', 'Startups', 'Entreprises', 'Institutions']):
    x = RX + Inches(0.3 + (i % 2) * 2.2); y = Inches(5.55 + (i // 2) * 0.5)
    box(s, x, y + Inches(0.07), Inches(0.16), Inches(0.16), AXES[i], MSO_SHAPE.OVAL)
    tx(s, x + Inches(0.3), y, Inches(1.7), Inches(0.3), f, font=F_LIGHT, size=13, color=BLANC)

# 15 — PARTENAIRES
s = base(15, 'UN ÉCOSYSTÈME DE PARTENAIRES DE PREMIER PLAN', full=True)
s.notes_slide.notes_text_frame.text = 'Ordre : patronage du Ministère des Postes et Télécommunications et de la Commission nationale pour l’UNESCO ; Geneva AI Governance Institute (GAIGI) ; Road to Geneva AI Summit (21–22 juin 2027) ; UIT – Membre de Secteur ; Université Bordeaux Montaigne ; Global Technology & Associates (GTA) ; Cyber Inno Shield Foundation ; Selam ; Bureau régional de l’UNESCO. Partenaires des éditions précédentes : AUF, Gouvernement du Canada, Business France, MILA, ENSPY, IRIC, ESSFAR, Atos, Huawei, Port Autonome de Kribi…'
ttl(s, [('Ils nous ont fait confiance.', BLANC)], y=Inches(1.4), size=32, w=Inches(11))
ORDER = ['patronage', 'gaigi', 'road_to_geneva', 'itu', 'bordeaux_montaigne', 'gta', 'cyber_inno_shield', 'selam', 'unesco_regional']
gx = Inches(0.3); cw = (Inches(11.75) - 2 * gx) / 3; chh = Inches(1.3)
for i, n in enumerate(ORDER):
    x = int(LX + (i % 3) * (cw + gx)); y = int(Inches(2.3) + (i // 3) * (chh + Inches(0.2)))
    c = box(s, x, y, int(cw), chh, BLANC, MSO_SHAPE.ROUNDED_RECTANGLE); c.adjustments[0] = 0.12
    if i == 0: c.line.color.rgb = ORANGE; c.line.width = Pt(2.5)
    path = os.path.join(LOGO_DIR, n + ('.png' if n == 'unesco_regional' else '@4x.png')); iw, ih = Image.open(path).size
    mw, mh = int(cw) - Inches(0.9), chh - Inches(0.4)
    sc = min(mw / iw, mh / ih); pw, ph = int(iw * sc), int(ih * sc)
    s.shapes.add_picture(path, x + (int(cw) - pw) // 2, y + (chh - ph) // 2, pw, ph)
tx(s, LX, Inches(6.85), Inches(11.5), Inches(0.3), 'Sous le haut patronage du Ministère des Postes et Télécommunications et de la Commission nationale pour l’UNESCO.', font=F_LIGHT, size=12, color=GRIS)

# 16 — DEVENIR PARTENAIRE
s = base(16, 'DEVENIR PARTENAIRE', full=True)
s.notes_slide.notes_text_frame.text = 'Places limitées dans chaque formule : disponibilité confirmée par le secrétariat. Sponsoring à la carte (stands, prises de parole, parrainages, visibilité) et contributions en nature acceptées. Dossier complet : jciacm.com/documents/Dossier-Partenariat-JCIA-2027.pdf · contact@jciacm.com · +237 699 089 937.'
ttl(s, [('Six formules pour rejoindre la route vers Genève.', BLANC)], y=Inches(1.4), size=28, w=Inches(11.5))
offers = [('Platinum', '10 M', '1 place', ['Exclusivité sectorielle', 'Stand premium 36 m²', '15 invitations VIP']), ('Diamond', '5 M', '2 places', ['Parrainage d’une plénière', 'Stand 24 m²', '10 invitations VIP']),
          ('Gold', '3 M', '4 places', ['Parrainage masterclass', 'Stand 18 m²', '6 invitations VIP']), ('Silver', '1 M', '6 places', ['Stand 12 m²', 'Prise de parole au Salon', '4 invitations VIP']),
          ('Bronze', '500 000', '10 places', ['Stand 9 m²', 'Logo sur les supports', '2 invitations VIP']), ('Supporter', '100 000', 'Illimité', ['Stand partagé 4 m²', 'Certificat de soutien', '1 invitation VIP'])]
gp = Inches(0.16); cw = (Inches(11.75) - 5 * gp) / 6
tcol = [ORANGE, VIOLET, TURQ, TERRA, GRIS, GRIS]
for i, (n, p, pl, perks) in enumerate(offers):
    x = int(LX + i * (cw + gp)); top = i == 0
    if top:
        c = box(s, x, Inches(2.35), int(cw), Inches(4.35), ORANGE, MSO_SHAPE.ROUNDED_RECTANGLE); c.adjustments[0] = 0.06
    else:
        c = card(s, x, Inches(2.5), int(cw), Inches(4.2), tcol[i])
    fg = NUIT if top else BLANC; sub = NUIT if top else GRIS; y0 = Inches(2.35) if top else Inches(2.5)
    if top: tx(s, x, y0 + Inches(0.15), int(cw), Inches(0.3), 'EXCLUSIF', font=F_SEMI, size=9, color=NUIT, align=PP_ALIGN.CENTER, track=250)
    tx(s, x + Inches(0.18), y0 + Inches(0.5), int(cw) - Inches(0.3), Inches(1.5), [[(n, {'font': F_DISPLAY, 'size': 16, 'color': fg, 'after': 4})], [(p, {'font': F_DISPLAY, 'size': 22, 'color': NUIT if top else ORANGE})], [('FCFA · ' + pl, {'font': F_LIGHT, 'size': 10, 'color': sub})]], spacing=1.05)
    box(s, x + Inches(0.18), y0 + Inches(2.0), int(cw) - Inches(0.36), Pt(1), NUIT if top else LIGNE)
    for j, pk in enumerate(perks):
        yy = y0 + Inches(2.2 + j * 0.62)
        box(s, x + Inches(0.18), yy + Inches(0.08), Inches(0.1), Inches(0.1), NUIT if top else TURQ, MSO_SHAPE.OVAL)
        tx(s, x + Inches(0.36), yy, int(cw) - Inches(0.5), Inches(0.6), pk, font=F_LIGHT, size=11, color=fg, spacing=1.05)
tx(s, LX, Inches(6.9), Inches(11.5), Inches(0.25), 'Formules à la carte et contributions en nature possibles  ·  dossier complet sur jciacm.com', font=F_LIGHT, size=11, color=GRIS)

# 17 — CLÔTURE : photo du Hilton de nuit en fond, texte dans le ciel à droite
s = slide(chrome=False, notes='Merci. Contacts du secrétariat : contact@jciacm.com, +237 699 089 937 (WhatsApp), +237 677 238 022. Site : www.jciacm.com. Photo : Hilton Hotel, Yaoundé.')
photo(s, 'hilton_nuit', 0, 0, W, H, 0.5)
gradient(s, 0, 0, W, H, [(0, 0), (58, 0), (68, 60), (100, 85)], 0)
HX = Inches(8.85)
s.shapes.add_picture(LOGO, HX, Inches(0.6), width=Inches(2.5))
tx(s, HX, Inches(2.3), Inches(4.2), Inches(1.9), [[('Rendez-vous', {})], [('au Hilton de', {'color': ORANGE})], [('Yaoundé.', {'color': ORANGE})]], font=F_DISPLAY, size=32, spacing=1.0)
tx(s, HX, Inches(4.2), Inches(4.2), Inches(0.5), '27 & 28 avril 2027', font=F_SEMI, size=20, color=BLANC)
tx(s, HX, Inches(4.75), Inches(4.2), Inches(0.9), 'Participez, exposez, candidatez aux Awards ou devenez partenaire.', font=F_LIGHT, size=14, color=BLANC, spacing=1.3)
for i, (k, v) in enumerate([('Site', 'www.jciacm.com'), ('E-mail', 'contact@jciacm.com'), ('WhatsApp', '+237 699 089 937')]):
    y = Inches(5.8 + i * 0.4)
    tx(s, HX, y, Inches(1.2), Inches(0.35), k.upper(), font=F_SEMI, size=10, color=ORANGE, track=200)
    tx(s, HX + Inches(1.3), y - Inches(0.03), Inches(3.0), Inches(0.35), v, font=F_SEMI, size=12, color=BLANC)
toghu(s, height=Inches(0.5))

from lxml import etree as _et
_PNS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
def add_anim(sl):
    ids = [sh.shape_id for sh in sl.shapes]
    if not ids: return
    cid = 5; effs = []
    for i, sid in enumerate(ids):
        delay = min(i, 12) * 120
        nt = 'afterEffect' if i == 0 else 'withEffect'
        effs.append(f'<p:par><p:cTn id="{cid}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{nt}"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="{cid+1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{cid+2}" dur="600"/><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>')
        cid += 3
    xml = (f'<p:timing xmlns:p="{_PNS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
           f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
           f'<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>' + ''.join(effs) +
           '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
           '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
           '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
    el = _et.fromstring(xml)
    sl._element.append(el)
for _sl in prs.slides:
    add_anim(_sl)


prs.save(OUT)
print("ok", len(prs.slides))
