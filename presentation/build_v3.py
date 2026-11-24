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
# v3 — juste milieu : esthétique v2, informations de la v1 en version courte.

def head(s, lab, title, size=34, w=Inches(11.8)):
    label(s, M, Inches(1.2), lab)
    tx(s, M, Inches(1.55), w, Inches(1.0), title, font=F_DISPLAY, size=size)


def bg(s, name, mode='full', focus=0.35):
    """Photo plein cadre + voile : 'left' (texte à gauche), 'right' (texte à droite), 'full' (voile uniforme)."""
    photo(s, name, 0, 0, W, H, focus)
    if mode == 'left':
        gradient(s, 0, 0, W, H, [(0, 97), (48, 88), (100, 28)], 0)
    elif mode == 'right':
        gradient(s, 0, 0, W, H, [(0, 28), (52, 88), (100, 97)], 0)
    else:
        gradient(s, 0, 0, W, H, [(0, 86), (100, 74)], 90)

def dot_list(s, x, y, w, items, size=15, step=0.52, colors=None, color=BLANC):
    for i, t in enumerate(items):
        yy = y + Inches(i * step)
        box(s, x, yy + Inches(0.11), Inches(0.11), Inches(0.11), (colors or AXES)[i % 4], MSO_SHAPE.OVAL)
        tx(s, x + Inches(0.28), yy, w - Inches(0.28), Inches(step), t, font=F_LIGHT, size=size, color=color, spacing=1.15)

# 01 — COUVERTURE
s = slide(chrome=False, notes='Journées Camerounaises de l’Intelligence Artificielle, 3e édition, 27 et 28 avril 2027, Hilton Hotel de Yaoundé. Événement satellite du Geneva AI Summit 2027. Photo : JCIA 2025.')
photo(s, 'public_salle', 0, 0, W, H)
gradient(s, 0, 0, W, H, [(0, 97), (45, 88), (100, 25)], 0)
gradient(s, 0, Inches(4.5), W, Inches(3.0), [(0, 0), (100, 85)], 90)
s.shapes.add_picture(LOGO, M, Inches(0.6), width=Inches(2.9))
label(s, M, Inches(2.95), '3e édition  ·  Événement satellite du Geneva AI Summit 2027')
tx(s, M, Inches(3.35), Inches(11), Inches(2.0), [[('Penser l’IA au Cameroun,', {})], [('pour le Cameroun.', {'color': ORANGE})]], font=F_DISPLAY, size=48, spacing=0.98)
tx(s, M, Inches(5.25), Inches(8), Inches(0.9), [[('Journées Camerounaises de l’Intelligence Artificielle', {'font': F_SEMI})],
   [('27 & 28 avril 2027  ·  Hilton Hotel, Yaoundé', {'color': GRIS})]], font=F_LIGHT, size=16, spacing=1.3)
toghu(s, height=Inches(0.62))

# 02 — DE YAOUNDÉ À GENÈVE
s = slide(notes='Message clé : les JCIA 2027 sont l’événement satellite (side event) préparatoire du Geneva AI Summit 2027 et la porte d’entrée nationale vers le AI for Good Global Summit de l’UIT.')
pic = s.shapes.add_picture(CARTE, Inches(8.4), Inches(0.55), height=Inches(6.6)); fade_pic(pic, 55)
label(s, M, Inches(1.75), 'Positionnement')
tx(s, M, Inches(2.15), Inches(9), Inches(2.8), [[('De Yaoundé', {})], [('à Genève.', {'color': ORANGE})]], font=F_DISPLAY, size=80, spacing=0.92)
tx(s, M, Inches(4.85), Inches(6.8), Inches(1.0), 'Les JCIA 2027 sont l’événement satellite du Geneva AI Summit 2027 et la porte d’entrée nationale vers le AI for Good Global Summit de l’UIT.',
   font=F_LIGHT, size=17, color=GRIS, spacing=1.3)
pill = box(s, M, Inches(6.0), Inches(3.6), Inches(0.46), NUIT, MSO_SHAPE.ROUNDED_RECTANGLE)
pill.adjustments[0] = 0.5; pill.line.color.rgb = ORANGE; pill.line.width = Pt(1)
tx(s, M, Inches(6.0), Inches(3.6), Inches(0.46), 'LABEL ROAD TO GENEVA AI SUMMIT', font=F_SEMI, size=11, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, track=150)

# 03 — L'ORGANISATEUR
s = slide(notes='IAC – CAIPI : Intelligence Artificielle Cameroun – Cameroon Artificial Intelligence Policy Institute, organisation à but non lucratif fondée le 6 octobre 2023 à Yaoundé. Partenariats stratégiques : GTEK et Geneva AI Governance Institute (GAIGI). Photo : visite officielle, JCIA 2025.')
bg(s, 'officiels', 'left', 0.3)
head(s, 'L’organisateur', 'IAC – CAIPI', size=40, w=Inches(6.4))
tx(s, M, Inches(2.5), Inches(6.2), Inches(1.0), 'Think tank et plateforme de dialogue multi-acteurs, fondé le 6 octobre 2023 à Yaoundé.', font=F_LIGHT, size=16, color=GRIS, spacing=1.3)
box(s, M, Inches(3.55), Inches(0.06), Inches(1.25), ORANGE)
tx(s, M + Inches(0.3), Inches(3.55), Inches(6.0), Inches(1.3), '« Faire du Cameroun une nation qui conçoit, développe et gouverne l’IA de manière souveraine, éthique et inclusive. »',
   font=F_SEMI, size=17, color=BLANC, spacing=1.25)
dot_list(s, M, Inches(5.2), Inches(6.4), ['Accompagner l’État dans sa Stratégie nationale de l’IA', 'Fédérer chercheurs, startups, entreprises et diaspora', 'Promouvoir une IA éthique, conforme à l’UNESCO'], size=14, step=0.5)

# 04 — LE CONSTAT
s = slide(notes='Contexte : Recommandation UNESCO sur l’éthique de l’IA (nov. 2021, 193 États) ; Stratégie continentale de l’IA de l’Union africaine (juil. 2024) ; Stratégie nationale de l’IA du Cameroun (juil. 2025) ; rapport UNESCO RAM (fév. 2026) ; le Cameroun parmi les 29 pays fondateurs de WAICO (juil. 2026).')
head(s, 'Pourquoi les JCIA', 'Un écosystème qui bouillonne, mais encore trop peu visible, financé et connecté.', size=32)
tx(s, M, Inches(3.0), Inches(10.5), Inches(0.8), [[('Comment en faire un écosystème ', {}), ('structuré, financé, visible et compétitif', {'color': ORANGE, 'font': F_SEMI}), (' ?', {})]], font=F_LIGHT, size=20, color=BLANC)
steps = [('2021', 'Éthique de l’IA : Recommandation UNESCO'), ('2024', 'Stratégie continentale de l’IA (UA)'), ('2025', 'Stratégie nationale de l’IA du Cameroun'),
         ('2026', 'Le Cameroun, membre fondateur de WAICO'), ('2027', 'JCIA 2027, en route vers Genève')]
cw = (W - 2 * M) / 5
box(s, M, Inches(4.62), W - 2 * M, Pt(1), LIGNE)
for i, (y, t) in enumerate(steps):
    x = int(M + cw * i); last = i == 4
    box(s, x, Inches(4.53), Inches(0.2), Inches(0.2), ORANGE if last else GRIS, MSO_SHAPE.OVAL)
    tx(s, x, Inches(4.95), int(cw) - Inches(0.3), Inches(1.6), [[(y, {'font': F_DISPLAY, 'size': 24, 'color': ORANGE if last else BLANC})], [(t, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.2)

# 05 — LES CHIFFRES 2027
s = slide(notes='Objectifs 2027 (toujours « attendus ») : 7 000+ participants en présentiel, 5 000+ en ligne, 150+ startups et exposants, 40+ intervenants, 20+ délégations diplomatiques, 500+ rencontres B2B et B2G, 2 millions de personnes touchées.')
bg(s, 'salon_echange', 'full')
label(s, M, Inches(1.3), 'Changement d’échelle  ·  objectifs 2027')
tx(s, M, Inches(1.65), Inches(7.4), Inches(2.4), '7 000+', font=F_DISPLAY, size=140, color=ORANGE, spacing=0.9)
tx(s, M, Inches(4.1), Inches(6.6), Inches(0.9), 'participants attendus au Hilton de Yaoundé.', font=F_LIGHT, size=22, color=BLANC, spacing=1.25)
tx(s, M, Inches(5.0), Inches(6.6), Inches(1.0), 'D’un événement national phare à une plateforme africaine d’influence.', font=F_LIGHT, size=15, color=GRIS, spacing=1.3)
stats = [('5 000+', 'en ligne'), ('150+', 'startups et exposants'), ('40+', 'intervenants'), ('20+', 'délégations diplomatiques'), ('500+', 'rencontres B2B et B2G'), ('2 M+', 'personnes touchées')]
for i, (k, v) in enumerate(stats):
    x = Inches(8.1 + (i % 2) * 2.45); y = Inches(1.75 + (i // 2) * 1.6)
    box(s, x, y, Inches(2.2), Pt(1), LIGNE)
    tx(s, x, y + Inches(0.2), Inches(2.2), Inches(1.2), [[(k, {'font': F_DISPLAY, 'size': 30})], [(v, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.1)

# 06 — TRAJECTOIRE
s = slide(notes='Trois éditions : 2023 (IRIC et ENSPY, décembre), 2025 (Hilton, ENSPY et IRIC, avril), 2027 (Hilton, 27-28 avril).')
bg(s, 'visite_stand', 'full')
head(s, 'Notre trajectoire', 'Trois éditions, une ambition qui grandit.')
eds = [('2023', 'L’acte fondateur', ['1 000+ participants', '17 intervenants', 'Membres du Gouvernement présents'], FANTOME, GRIS),
       ('2025', 'L’étape décisive', ['5 000 participants + 2 000 en ligne', '~100 startups, 60+ organisations', '1ers Awards et 1er Salon 100 % IA'], FANTOME, GRIS),
       ('2027', 'Cap sur Genève', ['7 000+ participants attendus', 'Side event du AI for Good (UIT)', 'Lancement de l’Annuaire national'], ORANGE, ORANGE)]
cw = (W - 2 * M) / 3
box(s, M, Inches(3.82), W - 2 * M, Pt(1), LIGNE)
for i, (yr, t, items, cy, ck) in enumerate(eds):
    x = int(M + cw * i)
    tx(s, x, Inches(2.5), int(cw), Inches(1.3), yr, font=F_DISPLAY, size=64, color=cy)
    box(s, x, Inches(3.72), Inches(0.2), Inches(0.2), ck, MSO_SHAPE.OVAL)
    tx(s, x, Inches(4.15), int(cw) - Inches(0.4), Inches(0.5), t, font=F_DISPLAY, size=20, color=BLANC)
    for j, it in enumerate(items):
        tx(s, x, Inches(4.75 + j * 0.45), int(cw) - Inches(0.4), Inches(0.45), it, font=F_LIGHT, size=14, color=GRIS)

# 07 — JCIA 2025 EN IMAGES
s = slide(notes='Retour sur la 2e édition (avril 2025, Hilton Hotel de Yaoundé, ENSPY et IRIC) : cérémonie, panels, Salon National 100 % IA, premiers Cameroon AI Awards.')
bg(s, 'pupitre_hilton', 'right', 0.3)
label(s, Inches(7.5), Inches(1.2), 'Ce que nous avons déjà bâti')
tx(s, Inches(7.5), Inches(1.55), Inches(5.2), Inches(1.0), 'JCIA 2025', font=F_DISPLAY, size=44)
st25 = [('5 000', 'sur place'), ('2 000', 'en ligne'), ('~100', 'startups'), ('60+', 'organisations'), ('53', 'projets aux 1ers Awards'), ('1er', 'Salon National 100 % IA')]
for i, (k, v) in enumerate(st25):
    x = Inches(7.5 + (i % 2) * 2.65); y = Inches(2.65 + (i // 2) * 0.78)
    tx(s, x, y, Inches(2.6), Inches(0.75), [[(k + '  ', {'font': F_DISPLAY, 'size': 22, 'color': ORANGE}), (v, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE)
photo(s, 'salon_echange', Inches(7.5), Inches(5.2), Inches(1.65), Inches(1.6))
photo(s, 'panel_intervenante', Inches(9.27), Inches(5.2), Inches(1.65), Inches(1.6))
photo(s, 'public_proche', Inches(11.04), Inches(5.2), Inches(1.56), Inches(1.6))

# 08 — THÈME
s = slide(notes='Thème officiel de la 3e édition et ses quatre piliers.')
s.shapes.add_picture(CARTE, Inches(9.3), Inches(0.45), height=Inches(6.7))
label(s, M, Inches(1.2), 'Thème 2027  ·  L’IA Made in Cameroun')
tx(s, M, Inches(1.55), Inches(8.6), Inches(1.9), [[('« Penser l’intelligence artificielle ', {}), ('au Cameroun, pour le Cameroun', {'color': ORANGE}), (' »', {})]], font=F_DISPLAY, size=34, spacing=1.02)
pil = [('Innovation souveraine', 'Maîtriser technologies, données, modèles et compétences.'), ('Excellence camerounaise', 'Célébrer nos talents au niveau des standards mondiaux.'),
       ('Solutions locales', 'Langues nationales, agriculture, santé, services publics.'), ('Influence mondiale', 'Prendre notre place dans la gouvernance de l’IA.')]
for i, (t, d) in enumerate(pil):
    x = M + Inches((i % 2) * 4.2); y = Inches(3.75 + (i // 2) * 1.45)
    box(s, x, y, Inches(3.9), Inches(0.05), AXES[i])
    tx(s, x, y + Inches(0.2), Inches(3.9), Inches(1.1), [[(t, {'font': F_DISPLAY, 'size': 17, 'after': 4})], [(d, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.15)

# 09 — GENÈVE
s = slide(notes='Le AI for Good Global Summit est organisé par l’UIT avec plus de 50 agences des Nations Unies : 11 000+ participants, 800+ intervenants, 19 milliards d’impressions médias.')
bg(s, 'panel_5', 'full')
head(s, 'Événement satellite', 'La route du Geneva AI Summit 2027 passe par Yaoundé.', size=32)
rx = M
for i, (city, date, c) in enumerate([('Yaoundé', '27 & 28 avril 2027', ORANGE), ('Genève', 'juin 2027', TURQ)]):
    x = rx + Inches(i * 3.4)
    box(s, x, Inches(2.95), Inches(0.24), Inches(0.24), c, MSO_SHAPE.OVAL)
    tx(s, x + Inches(0.45), Inches(2.8), Inches(2.8), Inches(0.9), [[(city, {'font': F_DISPLAY, 'size': 24})], [(date, {'font': F_LIGHT, 'size': 13, 'color': c})]], spacing=1.1)
box(s, rx + Inches(2.3), Inches(3.06), Inches(0.9), Pt(2), LIGNE)
label(s, Inches(8.2), Inches(2.75), 'AI for Good Global Summit · UIT', color=GRIS)
for i, (k, v) in enumerate([('11 000+', 'participants'), ('800+', 'intervenants'), ('50+', 'agences ONU')]):
    tx(s, Inches(8.2 + i * 1.55), Inches(3.1), Inches(1.5), Inches(0.9), [[(k, {'font': F_DISPLAY, 'size': 20})], [(v, {'font': F_LIGHT, 'size': 12, 'color': GRIS})]], spacing=1.1)
objs = [('Préparer', 'la délégation nationale et ses messages'), ('Promouvoir', 'les solutions camerounaises les plus mûres'), ('Faire rayonner', 'le Cameroun auprès de l’ONU et des médias'),
        ('Investir', 'en reliant porteurs de projets et investisseurs'), ('Coopérer', 'avec des partenaires technologiques étrangers')]
box(s, M, Inches(4.35), W - 2 * M, Pt(1), LIGNE)
cw = (W - 2 * M) / 5
for i, (t, d) in enumerate(objs):
    x = int(M + cw * i)
    tx(s, x, Inches(4.6), int(cw) - Inches(0.25), Inches(1.9), [[(f'0{i+1}', {'font': F_DISPLAY, 'size': 22, 'color': (AXES + [ORANGE])[i], 'after': 6})], [(t, {'font': F_DISPLAY, 'size': 17, 'after': 4})], [(d, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.15)

# 10 — QUATRE AXES
s = slide(notes='Quatre enjeux de l’écosystème camerounais de l’IA, quatre réponses concrètes en 2027.')
head(s, 'Axes stratégiques', 'Quatre enjeux, une réponse intégrée.')
axes = [('Visibilité', 'Une vitrine', 'Le Salon National 100 % IA', '150+ exposants'), ('Financement', 'Un pont', 'Startup Pitch, investisseurs et sponsors', '500+ rendez-vous B2B / B2G'),
        ('Structuration', 'Un outil', 'L’Annuaire national des acteurs de l’IA', '1 000+ acteurs visés'), ('Rayonnement', 'Un tremplin', 'Side event du AI for Good et délégation à Genève', 'juin 2027')]
cw = (W - 2 * M - Inches(0.9)) / 4
for i, (t, k, d, f) in enumerate(axes):
    x = int(M + i * (cw + Inches(0.3)))
    box(s, x, Inches(2.8), int(cw), Inches(0.06), AXES[i])
    tx(s, x, Inches(3.05), int(cw), Inches(0.9), f'0{i+1}', font=F_DISPLAY, size=44, color=AXES[i])
    tx(s, x, Inches(4.0), int(cw), Inches(2.6), [[(t, {'font': F_DISPLAY, 'size': 21, 'after': 6})], [(k.upper(), {'font': F_SEMI, 'size': 11, 'color': AXES[i], 'after': 4})],
       [(d, {'font': F_LIGHT, 'size': 14, 'color': BLANC, 'after': 8})], [(f, {'font': F_SEMI, 'size': 13, 'color': GRIS})]], spacing=1.2)

# 11 — PROGRAMME
s = slide(notes='Jour 1 : 08h00–18h00. Jour 2 : 08h30–18h00, puis gala à 19h30 (sur invitation). Masterclasses : IA générative & administration publique ; IA & santé ; IA, agriculture & sécurité alimentaire ; cybersécurité, données & gouvernance. Programme sous réserve de modifications.')
bg(s, 'panel_intervenante', 'full')
head(s, 'Programme', 'Deux jours intensifs.')
days = [('Mardi 27 avril', [('10h00', 'Cérémonie officielle d’ouverture'), ('11h00', 'Inauguration du Salon National 100 % IA'), ('12h00', 'Plénière · Souveraineté et modèles d’IA africains'),
                            ('13h00', 'Plénière · Financer l’excellence'), ('15h00', 'Démos et rencontres B2B / B2G')]),
        ('Mercredi 28 avril', [('09h00', 'Quatre masterclasses certifiantes'), ('13h30', 'Startup Pitch Competition'), ('15h00', 'Women in AI Forum'),
                               ('16h15', 'Young AI Leaders Forum'), ('19h30', 'Gala des Cameroon AI Awards')])]
for i, (d, items) in enumerate(days):
    x = M + Inches(i * 6.1)
    tx(s, x, Inches(2.6), Inches(5.6), Inches(0.5), d, font=F_SEMI, size=15, color=ORANGE, track=100)
    box(s, x, Inches(3.1), Inches(5.6), Pt(1), LIGNE)
    for j, (h, t) in enumerate(items):
        y = Inches(3.3 + j * 0.68)
        tx(s, x, y, Inches(1.1), Inches(0.6), h, font=F_LIGHT, size=15, color=GRIS)
        tx(s, x + Inches(1.15), y, Inches(4.45), Inches(0.6), t, font=F_SEMI, size=15, color=BLANC, spacing=1.1)

# 12 — SALON
s = slide(notes='Exposants : startups, entreprises tech, laboratoires, administrations, universités, incubateurs, diaspora, institutions financières. Les 50 projets présélectionnés aux CAIA exposent gratuitement. Réserver un stand : contact@jciacm.com. Photo : JCIA 2025.')
photo(s, 'visite_officielle', 0, 0, W, H, 0.35)
gradient(s, 0, 0, W, H, [(0, 97), (50, 85), (100, 15)], 0)
label(s, M, Inches(1.4), 'Axe 01  ·  Visibilité')
tx(s, M, Inches(1.75), Inches(7), Inches(1.6), 'Le Salon National 100 % IA', font=F_DISPLAY, size=40, spacing=1.0)
tx(s, M, Inches(3.3), Inches(6.3), Inches(0.9), 'La plus grande exposition du Cameroun dédiée à l’IA, inaugurée par des membres du Gouvernement.', font=F_LIGHT, size=16, color=GRIS, spacing=1.3)
for i, (k, v) in enumerate([('150+', 'exposants'), ('200', 'solutions'), ('2', 'jours')]):
    tx(s, M + Inches(i * 2.1), Inches(4.25), Inches(2.0), Inches(0.9), [[(k, {'font': F_DISPLAY, 'size': 30, 'color': ORANGE})], [(v, {'font': F_LIGHT, 'size': 13, 'color': BLANC})]], spacing=1.05)
dot_list(s, M, Inches(5.4), Inches(6.5), ['Démonstrations en continu sur la scène du Salon', 'Rencontres B2B et B2G (commande publique innovante)', 'Application de mise en relation'], size=14, step=0.45)

# 13 — AWARDS
s = slide(notes='Concours national ouvert et gratuit, au Cameroun et dans la diaspora (18 ans et plus). Patronage : Bureau régional de l’UNESCO pour l’Afrique centrale et Haut-Commissariat britannique au Cameroun. Récompenses : trophée, mention « UNESCO Award Winner », financements, stages, stand gratuit, préparation à la délégation de Genève.')
bg(s, 'panel_4', 'full')
head(s, 'Cameroon AI Awards 2027', 'L’excellence, célébrée.')
tx(s, M, Inches(2.55), Inches(3), Inches(2.2), '10', font=F_DISPLAY, size=150, color=ORANGE, spacing=0.85)
tx(s, M, Inches(4.75), Inches(3.4), Inches(1.0), 'catégories, de la santé à la recherche.', font=F_LIGHT, size=16, color=BLANC, spacing=1.25)
cats = ['Santé', 'Agriculture', 'Éducation', 'Fintech', 'Administration', 'Cybersécurité', 'Langues et culture', 'Recherche', 'Femme de l’année', 'Jeune talent']
for i, c in enumerate(cats):
    x = Inches(4.3 + (i // 5) * 2.2); y = Inches(2.75 + (i % 5) * 0.62)
    tx(s, x, y, Inches(2.1), Inches(0.55), [[(f'{i+1:02d}  ', {'font': F_SEMI, 'color': ORANGE}), (c, {})]], font=F_LIGHT, size=14)
cal = [('15 nov. 2026', 'Ouverture des candidatures'), ('28 fév. 2027', 'Clôture'), ('20 mars → 15 avril', 'Vote du public · 40 %'), ('28 avril 2027', 'Gala · jury 60 %')]
box(s, Inches(9.1), Inches(2.95), Pt(1.5), Inches(2.7), LIGNE)
for i, (d, t) in enumerate(cal):
    y = Inches(2.75 + i * 0.85); last = i == 3
    box(s, Inches(9.02), y + Inches(0.12), Inches(0.18), Inches(0.18), ORANGE if last else GRIS, MSO_SHAPE.OVAL)
    tx(s, Inches(9.45), y, Inches(3.2), Inches(0.8), [[(d, {'font': F_SEMI, 'size': 15, 'color': ORANGE if last else BLANC})], [(t, {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.1)

# 14 — ANNUAIRE
s = slide(notes='Réalisé sous la supervision du Comité scientifique : appel public, vérification, catégorisation standardisée, mise à jour annuelle. Consentement explicite, droit de rectification, minimisation des données. Inscription : contact@jciacm.com.')
bg(s, 'salon_gta', 'right', 0.35)
label(s, Inches(6.0), Inches(1.2), 'Axe 03  ·  Structuration', color=TERRA)
tx(s, Inches(6.0), Inches(1.55), Inches(6.6), Inches(1.4), 'L’Annuaire national des acteurs de l’IA', font=F_DISPLAY, size=34, spacing=1.0)
tx(s, Inches(6.0), Inches(2.95), Inches(6.5), Inches(0.9), 'Une première nationale : les acteurs clés de l’écosystème, recensés et vérifiés. Édition imprimée et version en ligne.', font=F_LIGHT, size=15, color=GRIS, spacing=1.3)
tx(s, Inches(6.0), Inches(3.95), Inches(3), Inches(1.0), [[('1 000+', {'font': F_DISPLAY, 'size': 34, 'color': ORANGE})], [('acteurs visés', {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.05)
tx(s, Inches(9.2), Inches(3.95), Inches(3.4), Inches(1.0), [[('catalogue.jcia.cm', {'font': F_SEMI, 'size': 18})], [('version en ligne', {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.25)
dot_list(s, Inches(6.0), Inches(5.15), Inches(6.6), ['Pour l’État : piloter la Stratégie nationale de l’IA', 'Pour les investisseurs : un répertoire qualifié', 'Pour les startups : une visibilité durable'], size=14, step=0.48)

# 15 — PARTENAIRES INSTITUTIONNELS
s = slide(notes='Partenaires des éditions 2023 et 2025 : Commission nationale pour l’UNESCO, UIT, AI Council for Africa, GAIGI, AUF, Gouvernement du Canada, Business France, MILA, Université Bordeaux Montaigne, ENSPY, ESSFAR, IRIC, NumIAtech, Atos, Huawei, CAMPOST, Port Autonome de Kribi, SERVOO, GTEK.')
bg(s, 'salon_siad', 'full')
head(s, 'Ils portent les JCIA', 'Un écosystème de partenaires de premier plan.')
p27 = [('Organisateur', 'IAC – CAIPI'), ('Label international', 'Road to Geneva AI Summit'), ('Partenaire stratégique', 'Geneva AI Governance Institute'),
       ('Collaboration sectorielle', 'UIT · Membre de Secteur'), ('Patronage', 'Ministère des Postes et Télécommunications'), ('Égide des CAIA', 'Commission nationale pour l’UNESCO')]
cw = (W - 2 * M - Inches(0.6)) / 3
for i, (r, n) in enumerate(p27):
    x = int(M + (i % 3) * (cw + Inches(0.3))); y = Inches(2.75 + (i // 3) * 1.45)
    box(s, x, y, int(cw), Pt(1), LIGNE)
    tx(s, x, y + Inches(0.2), int(cw), Inches(1.1), [[(r.upper(), {'font': F_SEMI, 'size': 11, 'color': ORANGE, 'track': 150, 'after': 4})], [(n, {'font': F_DISPLAY, 'size': 17})]], spacing=1.2)
tx(s, M, Inches(5.85), W - 2 * M, Inches(0.9), [[('Ils nous ont fait confiance : ', {'font': F_SEMI, 'color': BLANC}), ('UNESCO, UIT, AUF, Gouvernement du Canada, Business France, MILA, Université Bordeaux Montaigne, ENSPY, IRIC, Atos, Huawei, Port Autonome de Kribi…', {})]],
   font=F_LIGHT, size=13, color=GRIS, spacing=1.3)

# 16 — DEVENIR PARTENAIRE
s = slide(notes='Places limitées dans chaque formule : disponibilité confirmée par le secrétariat. Sponsoring à la carte (stands, prises de parole, parrainages, visibilité) et contributions en nature acceptées. Dossier : jciacm.com/documents/Dossier-Partenariat-JCIA-2027.pdf')
bg(s, 'panel_2', 'full')
head(s, 'Devenir partenaire', 'Associez votre marque à la route vers Genève.', size=30)
tiers = [('Supporter', '100 000', 'Stand 4 m²'), ('Bronze', '500 000', 'Stand 9 m²'), ('Silver', '1 M', 'Stand 12 m²'),
         ('Gold', '3 M', 'Stand 18 m²'), ('Diamond', '5 M', 'Stand 24 m²'), ('Platinum', '10 M', 'Exclusivité · 36 m²')]
gap = Inches(0.22); bw = (W - 2 * M - gap * 5) / 6
base = Inches(6.45)
for i, (n, p, c) in enumerate(tiers):
    x = int(M + i * (bw + gap)); hh = Inches(0.7 + i * 0.36)
    top = i == 5
    box(s, x, base - hh, int(bw), hh, ORANGE if top else SURF)
    tx(s, x, base - hh - Inches(1.15), int(bw), Inches(1.1), [[(n, {'font': F_SEMI, 'size': 15, 'color': ORANGE if top else BLANC})], [(p + ' FCFA', {'font': F_LIGHT, 'size': 13, 'color': GRIS})], [(c, {'font': F_LIGHT, 'size': 12, 'color': BLANC})]], spacing=1.1)
tx(s, M, Inches(6.65), Inches(11.8), Inches(0.3), 'Formules à la carte et contributions en nature possibles. Dossier de sponsoring complet sur jciacm.com.', font=F_LIGHT, size=12, color=GRIS)

# 17 — CLÔTURE
s = slide(chrome=False, notes='Merci. Contacts du secrétariat : contact@jciacm.com, +237 699 089 937 (WhatsApp), +237 677 238 022. Site : www.jciacm.com.')
photo(s, 'public_proche', 0, 0, W, H, 0.35)
gradient(s, 0, 0, W, H, [(0, 92), (100, 92)], 0)
s.shapes.add_picture(LOGO, int((W - Inches(3.0)) / 2), Inches(0.9), width=Inches(3.0))
tx(s, 0, Inches(2.75), W, Inches(1.4), 'Rendez-vous à Yaoundé.', font=F_DISPLAY, size=60, align=PP_ALIGN.CENTER)
tx(s, 0, Inches(3.95), W, Inches(0.6), '27 & 28 avril 2027  ·  Hilton Hotel', font=F_LIGHT, size=22, color=ORANGE, align=PP_ALIGN.CENTER, track=50)
tx(s, 0, Inches(4.75), W, Inches(0.5), 'Participez, exposez, candidatez aux Awards ou devenez partenaire.', font=F_LIGHT, size=16, color=GRIS, align=PP_ALIGN.CENTER)
tx(s, 0, Inches(5.45), W, Inches(0.5), [[('www.jciacm.com', {'font': F_SEMI}), ('     ·     contact@jciacm.com     ·     +237 699 089 937', {})]], font=F_LIGHT, size=15, color=BLANC, align=PP_ALIGN.CENTER)
toghu(s, height=Inches(0.62))

for i, sl in enumerate(prs.slides):
    if i not in (0, TOTAL - 1):
        st['n'] = i + 1; chrome(sl)
prs.save(OUT)
print('ok', len(prs.slides))
