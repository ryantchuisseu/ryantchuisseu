# Construit la présentation JCIA 2027 (python-pptx).
import sys, os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, 'img')
ASSETS = sys.argv[1]
OUT = sys.argv[2]

# --- Charte JCIA ---
NUIT = RGBColor(0x0F, 0x13, 0x27)
CARTE = RGBColor(0x18, 0x20, 0x39)
SECTION = RGBColor(0x1A, 0x22, 0x3C)
BORD = RGBColor(0x2C, 0x31, 0x47)
ORANGE = RGBColor(0xF6, 0xA3, 0x43)
ORANGE2 = RGBColor(0xE3, 0x84, 0x3D)
TURQ = RGBColor(0x2D, 0xB8, 0xBD)
TERRA = RGBColor(0xCD, 0x60, 0x35)
VIOLET = RGBColor(0x5D, 0x46, 0x96)
VIOLET2 = RGBColor(0x9D, 0x87, 0xDC)
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
GRIS = RGBColor(0xB5, 0xBA, 0xD0)
ENCRE = RGBColor(0x19, 0x20, 0x3A)
SABLE = RGBColor(0xF4, 0xE6, 0xD2)
FONT = 'Arial'
ENJEUX = [ORANGE, TURQ, TERRA, VIOLET2]

# --- Préparation des visuels de marque (fond rendu transparent) ---
def keyout(src, dst, bg, tol=26):
    im = Image.open(src).convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            d = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
            if d < tol:
                px[x, y] = (r, g, b, 0)
            elif d < tol * 2:
                px[x, y] = (r, g, b, int(255 * (d - tol) / tol))
    im.save(dst)
LOGO = os.path.join(BASE, 'logo.png'); keyout(os.path.join(ASSETS, 'logo-jcia.png'), LOGO, (15, 19, 39))
CARTE_CM = os.path.join(BASE, 'carte.png'); keyout(os.path.join(ASSETS, 'carte-cameroun.png'), CARTE_CM, (23, 28, 51), 30)
TOGHU = os.path.join(ASSETS, 'bande-toghu.png')

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
state = {'n': 0}

# --- Outils ---
def set_alpha(shape, alpha):
    fill = shape.fill._xPr.find(qn('a:solidFill'))
    clr = fill[0]
    a = etree.SubElement(clr, qn('a:alpha')); a.set('val', str(int(alpha * 100000)))

def rect(s, x, y, w, h, color, alpha=None, shape=MSO_SHAPE.RECTANGLE, line=None):
    r = s.shapes.add_shape(shape, x, y, w, h)
    r.fill.solid(); r.fill.fore_color.rgb = color
    if alpha is not None: set_alpha(r, alpha)
    if line is None: r.line.fill.background()
    else: r.line.color.rgb = line; r.line.width = Pt(1.25)
    r.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: r.adjustments[0] = 0.08
    return r

def text(s, x, y, w, h, runs, size=16, color=BLANC, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=1.1, italic=False):
    """runs: str, or list of paragraphs; each paragraph is str or list of (text, {opts})."""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0); tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) else [runs]
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align; para.line_spacing = spacing
        segs = p if isinstance(p, list) else [(p, {})]
        for seg, o in segs:
            r = para.add_run(); r.text = seg
            f = r.font; f.name = FONT
            f.size = Pt(o.get('size', size)); f.bold = o.get('bold', bold); f.italic = o.get('italic', italic)
            f.color.rgb = o.get('color', color)
        if isinstance(p, list) and p and p[0][1].get('space_after') is not None:
            para.space_after = Pt(p[0][1]['space_after'])
    return tb

def photo(s, path, x, y, w, h):
    """Image recadrée pour remplir exactement le cadre."""
    im = Image.open(path); iw, ih = im.size
    pic = s.shapes.add_picture(path, x, y, w, h)
    box = w / h; ratio = iw / ih
    if ratio > box:
        c = (1 - box / ratio) / 2; pic.crop_left = c; pic.crop_right = c
    else:
        c = (1 - ratio / box) / 2; pic.crop_top = c * 0.6; pic.crop_bottom = c * 1.4
    return pic

def filet(s, y=Inches(0), h=Inches(0.07)):
    seg = W / 4
    for i, c in enumerate(ENJEUX):
        rect(s, int(seg * i), y, int(seg) + 1, h, c)

def notes(s, t):
    s.notes_slide.notes_text_frame.text = t

def new_slide(bg=NUIT, footer=True, band=True):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = bg
    state['n'] += 1
    if band: filet(s)
    if footer:
        c = GRIS if bg != SABLE else ENCRE
        text(s, Inches(0.6), Inches(7.05), Inches(9), Inches(0.3),
             'JCIA 2027 · 3e édition · 27 & 28 avril 2027 · Hilton Hotel, Yaoundé', size=10, color=c)
        text(s, Inches(11.7), Inches(7.05), Inches(1.05), Inches(0.3), str(state['n']), size=10, color=c, align=PP_ALIGN.RIGHT)
    return s

def eyebrow(s, t, x=Inches(0.6), y=Inches(0.55), color=TURQ):
    text(s, x, y, Inches(9), Inches(0.3), t.upper(), size=12, color=color, bold=True)

def title(s, t, x=Inches(0.6), y=Inches(0.85), w=Inches(12), size=34, color=BLANC, h=Inches(1.2)):
    text(s, x, y, w, h, t, size=size, color=color, bold=True, spacing=1.0)

def card(s, x, y, w, h, top=None, fill=CARTE):
    rect(s, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    if top is not None:
        rect(s, x + Inches(0.25), y, w - Inches(0.5), Inches(0.07), top)

# =========================================================
# 1. COUVERTURE
s = new_slide(footer=False, band=False)
photo(s, os.path.join(IMG, 'public_salle.jpg'), 0, 0, W, H)
rect(s, 0, 0, W, H, NUIT, alpha=0.55)
rect(s, 0, 0, Inches(8.4), H, NUIT, alpha=0.82)
s.shapes.add_picture(LOGO, Inches(0.6), Inches(0.5), width=Inches(3.4))
pill = rect(s, Inches(0.6), Inches(2.35), Inches(6.1), Inches(0.42), NUIT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=ORANGE)
pill.adjustments[0] = 0.5
text(s, Inches(0.6), Inches(2.35), Inches(6.1), Inches(0.42), 'ÉVÉNEMENT SATELLITE DU GENEVA AI SUMMIT 2027',
     size=12, color=ORANGE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(0.6), Inches(3.0), Inches(7.6), Inches(1.9),
     'Journées Camerounaises de l’Intelligence Artificielle 2027', size=40, bold=True, spacing=0.95)
text(s, Inches(0.6), Inches(4.95), Inches(7.7), Inches(0.8),
     '« Penser l’intelligence artificielle au Cameroun, pour le Cameroun »', size=17, color=ORANGE, italic=True)
for i, (k, v) in enumerate([('27 & 28 avril 2027', 'Mardi et mercredi'), ('Hilton Hotel', 'Yaoundé, Cameroun'), ('3e édition', 'De Yaoundé à Genève')]):
    x = Inches(0.6 + i * 2.55)
    rect(s, x, Inches(5.95), Inches(0.05), Inches(0.62), ENJEUX[i])
    text(s, x + Inches(0.18), Inches(5.93), Inches(2.3), Inches(0.7),
         [[(k, {'bold': True, 'size': 15})], [(v, {'size': 12, 'color': GRIS})]])
bh = int(W * 72 / 1100)
s.shapes.add_picture(TOGHU, 0, H - bh, width=W)
notes(s, 'Présentation de la 3e édition des Journées Camerounaises de l’Intelligence Artificielle (JCIA 2027), les 27 et 28 avril 2027 au Hilton Hotel de Yaoundé. Les JCIA 2027 sont l’événement satellite préparatoire du Geneva AI Summit 2027. Photo : JCIA 2025.')

# =========================================================
# 2. EN UN COUP D'ŒIL
s = new_slide()
eyebrow(s, 'JCIA 2027 en un coup d’œil')
title(s, 'La plateforme nationale de référence de l’IA au Cameroun change d’échelle')
text(s, Inches(0.6), Inches(2.25), Inches(4.6), Inches(3.8), [
    [('Depuis 2023, les JCIA réunissent le Gouvernement, les universités, les entreprises, les chercheurs, les startups, la société civile et les partenaires internationaux autour d’un même programme.', {'space_after': 12})],
    [('Réflexion stratégique, démonstrations, formation et célébration de l’excellence.', {'space_after': 12})],
    [('En 2027, les JCIA passent d’un événement national phare à une plateforme africaine d’influence, sur la route de Genève.', {'bold': True, 'color': ORANGE})],
], size=15, color=GRIS, spacing=1.2)
kpis = [('7 000+', 'participants en présentiel'), ('5 000+', 'participants en ligne'), ('150+', 'startups et exposants'),
        ('40+', 'intervenants de haut niveau'), ('20+', 'délégations diplomatiques'), ('500+', 'rencontres B2B et B2G')]
for i, (k, v) in enumerate(kpis):
    cx = Inches(5.7 + (i % 3) * 2.45); cy = Inches(2.25 + (i // 3) * 2.0)
    card(s, cx, cy, Inches(2.25), Inches(1.75), top=ENJEUX[i % 4])
    text(s, cx + Inches(0.25), cy + Inches(0.35), Inches(1.9), Inches(0.7), k, size=32, bold=True, color=ORANGE)
    text(s, cx + Inches(0.25), cy + Inches(1.05), Inches(1.9), Inches(0.6), v, size=13, color=BLANC)
text(s, Inches(5.7), Inches(6.35), Inches(7), Inches(0.3), 'Chiffres attendus pour l’édition 2027. Plus de 2 millions de personnes touchées visées (TV, radio, presse, digital).', size=11, color=GRIS, italic=True)
notes(s, 'Les chiffres présentés sont des objectifs attendus pour 2027 (source : jciacm.com).')

# =========================================================
# 3. L'ORGANISATEUR
s = new_slide()
photo(s, os.path.join(IMG, 'officiels.jpg'), Inches(7.2), Inches(0.07), W - Inches(7.2), Inches(6.85))
rect(s, Inches(7.2), Inches(0.07), Inches(0.08), Inches(6.85), ORANGE)
eyebrow(s, 'L’organisateur')
title(s, 'IAC – CAIPI', h=Inches(0.7))
text(s, Inches(0.6), Inches(1.6), Inches(6.2), Inches(1.0),
     'Intelligence Artificielle Cameroun (IAC) – Cameroon Artificial Intelligence Policy Institute (CAIPI). Organisation à but non lucratif fondée le 6 octobre 2023 à Yaoundé : think tank, plateforme de dialogue multi-acteurs et acteur de référence de l’écosystème africain de l’IA.',
     size=13, color=GRIS, spacing=1.2)
card(s, Inches(0.6), Inches(3.05), Inches(6.2), Inches(1.45), top=ORANGE)
text(s, Inches(0.9), Inches(3.3), Inches(5.6), Inches(1.1),
     '« Faire du Cameroun une nation qui conçoit, développe et gouverne l’IA de manière souveraine, éthique et inclusive, au bénéfice de tous les Camerounais et pour le rayonnement de l’Afrique. »',
     size=14, italic=True, spacing=1.15)
missions = ['Accompagner l’État dans sa politique d’adoption et de gouvernance de l’IA (Stratégie nationale)',
            'Fédérer l’écosystème : recherche, startups, entreprises, administrations, investisseurs, diaspora',
            'Promouvoir les initiatives camerounaises à l’international (diplomatie scientifique et numérique)',
            'Former et promouvoir une IA éthique, inclusive et souveraine, conforme à la Recommandation de l’UNESCO']
for i, m in enumerate(missions):
    y = Inches(4.75 + i * 0.55)
    rect(s, Inches(0.6), y + Inches(0.08), Inches(0.14), Inches(0.14), ENJEUX[i], shape=MSO_SHAPE.OVAL)
    text(s, Inches(0.9), y, Inches(5.9), Inches(0.5), m, size=12)
notes(s, 'Partenariats internationaux stratégiques : GTEK (société franco-britannique) et le Geneva AI Governance Institute (GAIGI). Photo : visite officielle, JCIA 2025.')

# =========================================================
# 4. TRAJECTOIRE
s = new_slide()
eyebrow(s, 'Notre parcours')
title(s, 'Trois éditions, une ambition qui grandit')
rect(s, Inches(0.9), Inches(2.62), Inches(11.5), Inches(0.04), BORD)
eds = [('2023', '1re édition · l’acte fondateur', 'IRIC & ENSPY, Yaoundé · décembre',
        ['1 000+ participants', '17 intervenants', '~15 exposants', 'Membres du Gouvernement présents'], TURQ),
       ('2025', '2e édition · une étape décisive', 'Hilton Hotel, ENSPY & IRIC · avril',
        ['5 000 participants + 2 000 en ligne', '~100 startups, 60+ organisations', '1ers Cameroon AI Awards (53 projets)', '1er Salon National 100 % IA'], VIOLET2),
       ('2027', '3e édition · de Yaoundé à Genève', 'Hilton Hotel, Yaoundé · 27 & 28 avril',
        ['7 000+ participants attendus', 'Side event du AI for Good (UIT)', 'Lancement de l’Annuaire national', 'Délégation camerounaise à Genève'], ORANGE)]
for i, (yr, t1, t2, items, c) in enumerate(eds):
    x = Inches(0.6 + i * 4.15)
    rect(s, x + Inches(0.25), Inches(2.47), Inches(0.34), Inches(0.34), c, shape=MSO_SHAPE.OVAL)
    hi = (i == 2)
    card(s, x, Inches(3.1), Inches(3.85), Inches(3.55), fill=CARTE if not hi else SECTION)
    if hi: rect(s, x, Inches(3.1), Inches(3.85), Inches(3.55), NUIT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=ORANGE).fill.background()
    text(s, x + Inches(0.3), Inches(1.95), Inches(3), Inches(0.5), yr, size=26, bold=True, color=c)
    text(s, x + Inches(0.3), Inches(3.35), Inches(3.3), Inches(0.9), [[(t1, {'bold': True, 'size': 16})], [(t2, {'size': 12, 'color': GRIS})]])
    for j, it in enumerate(items):
        text(s, x + Inches(0.3), Inches(4.45 + j * 0.5), Inches(3.4), Inches(0.45), [[('— ', {'color': c, 'bold': True}), (it, {})]], size=13)
notes(s, 'De 1 000 participants en 2023 à plus de 7 000 attendus en 2027. Source : jciacm.com.')

# =========================================================
# 5. JCIA 2025 EN IMAGES
s = new_slide()
eyebrow(s, 'Retour sur la 2e édition')
title(s, 'JCIA 2025 en images', h=Inches(0.7))
g = Inches(0.12)
photo(s, os.path.join(IMG, 'pupitre_hilton.jpg'), Inches(0.6), Inches(1.75), Inches(6.0), Inches(4.0))
photo(s, os.path.join(IMG, 'public_proche.jpg'), Inches(6.72), Inches(1.75), Inches(3.0), Inches(1.94))
photo(s, os.path.join(IMG, 'panel_intervenante.jpg'), Inches(9.84), Inches(1.75), Inches(2.9), Inches(1.94))
photo(s, os.path.join(IMG, 'salon_echange.jpg'), Inches(6.72), Inches(3.81), Inches(3.0), Inches(1.94))
photo(s, os.path.join(IMG, 'visite_officielle.jpg'), Inches(9.84), Inches(3.81), Inches(2.9), Inches(1.94))
stats = [('5 000', 'participants sur place'), ('2 000', 'en ligne'), ('~100', 'startups'), ('60+', 'organisations'), ('53', 'projets aux 1ers CAIA')]
for i, (k, v) in enumerate(stats):
    x = Inches(0.6 + i * 2.43)
    text(s, x, Inches(5.95), Inches(2.3), Inches(0.9), [[(k, {'bold': True, 'size': 24, 'color': ORANGE})], [(v, {'size': 12, 'color': GRIS})]])
notes(s, 'Photos de la 2e édition (avril 2025) : cérémonie au Hilton, public, panels, Salon National 100 % IA et visite officielle des stands.')

# =========================================================
# 6. LE CONSTAT ET LE CONTEXTE
s = new_slide()
eyebrow(s, 'Pourquoi les JCIA')
title(s, 'Un écosystème qui bouillonne, mais encore trop peu visible, financé et connecté', h=Inches(1.3))
card(s, Inches(0.6), Inches(2.35), Inches(12.1), Inches(1.05), fill=SECTION)
rect(s, Inches(0.6), Inches(2.35), Inches(0.09), Inches(1.05), ORANGE)
text(s, Inches(0.95), Inches(2.35), Inches(11.5), Inches(1.05),
     'Comment faire de ce potentiel un écosystème structuré, financé, visible et compétitif ? Les JCIA 2027 apportent une réponse intégrée à quatre enjeux.',
     size=17, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(0.6), Inches(3.75), Inches(6), Inches(0.4), 'UN CONTEXTE HISTORIQUE', size=12, bold=True, color=TURQ)
steps = [('Nov. 2021', 'Recommandation de l’UNESCO sur l’éthique de l’IA (193 États)'),
         ('Juil. 2024', 'Stratégie continentale de l’IA de l’Union africaine'),
         ('Juil. 2025', 'Le Cameroun présente sa Stratégie nationale de l’IA'),
         ('Fév. 2026', 'Rapport UNESCO d’évaluation de l’état de préparation (RAM)'),
         ('Juil. 2026', 'Le Cameroun parmi les 29 pays fondateurs de WAICO'),
         ('Avr. 2027', 'JCIA 2027 : la porte d’entrée du Cameroun vers Genève')]
rect(s, Inches(0.8), Inches(4.62), Inches(11.7), Inches(0.04), BORD)
for i, (d, t) in enumerate(steps):
    x = Inches(0.6 + i * 2.03); last = i == len(steps) - 1
    rect(s, x + Inches(0.1), Inches(4.5), Inches(0.28), Inches(0.28), ORANGE if last else TURQ, shape=MSO_SHAPE.OVAL)
    text(s, x, Inches(4.95), Inches(1.9), Inches(1.6), [[(d, {'bold': True, 'size': 14, 'color': ORANGE if last else BLANC})], [(t, {'size': 12, 'color': GRIS})]], spacing=1.1)
notes(s, 'Les JCIA s’inscrivent dans une dynamique internationale, continentale et nationale de gouvernance de l’IA.')

# =========================================================
# 7. THÈME 2027
s = new_slide()
s.shapes.add_picture(CARTE_CM, Inches(9.6), Inches(1.0), height=Inches(5.6))
eyebrow(s, 'Thème 2027 · L’IA Made in Cameroun')
text(s, Inches(0.6), Inches(0.95), Inches(8.6), Inches(1.6),
     '« Penser l’intelligence artificielle au Cameroun, pour le Cameroun »', size=32, bold=True, color=ORANGE, spacing=1.0)
piliers = [('Innovation souveraine', 'Maîtriser les technologies, données, modèles et compétences qui fondent notre autonomie stratégique.'),
           ('Excellence camerounaise', 'Célébrer chercheurs, ingénieurs, entrepreneurs et étudiants au niveau des standards internationaux.'),
           ('Solutions locales', 'Des solutions pensées pour nos réalités : langues nationales, agriculture, santé communautaire, services publics.'),
           ('Influence mondiale', 'De Yaoundé à Genève : faire rayonner le savoir-faire camerounais et prendre notre place dans la gouvernance de l’IA.')]
for i, (t, d) in enumerate(piliers):
    x = Inches(0.6 + (i % 2) * 4.45); y = Inches(2.85 + (i // 2) * 2.0)
    card(s, x, y, Inches(4.25), Inches(1.8), top=ENJEUX[i])
    text(s, x + Inches(0.3), y + Inches(0.3), Inches(3.7), Inches(1.4), [[(t, {'bold': True, 'size': 17, 'space_after': 6})], [(d, {'size': 13, 'color': GRIS})]], spacing=1.12)
notes(s, 'Le thème officiel de la 3e édition et ses quatre piliers.')

# =========================================================
# 8. DE YAOUNDÉ À GENÈVE (positionnement satellite)
s = new_slide(bg=SECTION)
eyebrow(s, 'Positionnement stratégique', color=ORANGE)
title(s, 'De Yaoundé à Genève : un événement satellite du Geneva AI Summit 2027', h=Inches(1.3))
text(s, Inches(0.6), Inches(2.3), Inches(6.2), Inches(2.2), [
    [('Les JCIA 2027 sont l’événement satellite (side event) préparatoire du Geneva AI Summit 2027 et la porte d’entrée nationale vers le ', {}), ('AI for Good Global Summit', {'bold': True, 'color': BLANC}), (', organisé par l’Union internationale des télécommunications (UIT) avec plus de 50 agences des Nations Unies.', {})],
    [('', {})],
    [('Label international « Road to Geneva AI Summit ».', {'bold': True, 'color': ORANGE})],
], size=15, color=GRIS, spacing=1.2)
# Parcours Yaoundé -> Genève
for i, (city, date, c) in enumerate([('Yaoundé', '27 & 28 avril 2027', ORANGE), ('Genève', 'juin 2027', TURQ)]):
    x = Inches(7.4 + i * 3.05)
    card(s, x, Inches(2.3), Inches(2.6), Inches(1.6), top=c, fill=NUIT)
    text(s, x + Inches(0.3), Inches(2.6), Inches(2.1), Inches(1.2), [[(city, {'bold': True, 'size': 24})], [(date, {'size': 14, 'color': c})]])
arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.05), Inches(2.9), Inches(0.35), Inches(0.4))
arr.fill.solid(); arr.fill.fore_color.rgb = ORANGE; arr.line.fill.background()
text(s, Inches(7.4), Inches(4.05), Inches(5.6), Inches(0.4), 'L’AI FOR GOOD GLOBAL SUMMIT EN CHIFFRES', size=12, bold=True, color=TURQ)
for i, (k, v) in enumerate([('11 000+', 'participants'), ('800+', 'intervenants'), ('19 Mds', 'd’impressions médias')]):
    x = Inches(7.4 + i * 1.9)
    text(s, x, Inches(4.45), Inches(1.8), Inches(1.0), [[(k, {'bold': True, 'size': 24, 'color': BLANC})], [(v, {'size': 12, 'color': GRIS})]])
card(s, Inches(0.6), Inches(5.65), Inches(12.1), Inches(1.15), fill=NUIT)
text(s, Inches(0.9), Inches(5.65), Inches(11.6), Inches(1.15),
     'Ce que cela change : les startups, chercheurs et institutions camerounais qui se distinguent à Yaoundé préparent leur présence à Genève, au cœur du système des Nations Unies.',
     size=15, anchor=MSO_ANCHOR.MIDDLE)
notes(s, 'Positionnement clé : JCIA 2027 = étape camerounaise sur la route du Geneva AI Summit 2027 (Genève, juin 2027). Partenaires associés : UIT (membre de secteur) et Geneva AI Governance Institute (GAIGI).')

# =========================================================
# 9. CINQ OBJECTIFS DU SIDE EVENT
s = new_slide()
eyebrow(s, 'La feuille de route vers Genève')
title(s, 'Cinq objectifs pour l’événement satellite')
objs = [('Préparer', 'Constituer la délégation nationale de haut niveau et ses messages pour Genève.'),
        ('Promouvoir', 'Sélectionner les solutions camerounaises les plus matures pour les espaces de démonstration.'),
        ('Faire rayonner', 'Accroître la visibilité internationale via les médias, le corps diplomatique et l’ONU.'),
        ('Investir', 'Organiser des rencontres qualifiées entre porteurs de projets et investisseurs.'),
        ('Coopérer', 'Faciliter les accords avec des partenaires technologiques étrangers.')]
cols = [ORANGE, TURQ, TERRA, VIOLET2, ORANGE]
for i, (t, d) in enumerate(objs):
    x = Inches(0.6 + i * 2.45)
    card(s, x, Inches(2.2), Inches(2.25), Inches(4.3), top=cols[i])
    text(s, x + Inches(0.25), Inches(2.5), Inches(1.8), Inches(1.0), f'0{i+1}', size=44, bold=True, color=cols[i])
    text(s, x + Inches(0.25), Inches(3.6), Inches(1.8), Inches(2.7), [[(t, {'bold': True, 'size': 18, 'space_after': 8})], [(d, {'size': 13, 'color': GRIS})]], spacing=1.15)
notes(s, 'Les cinq étapes de la trajectoire Yaoundé–Genève, telles que présentées sur jciacm.com.')

# =========================================================
# 10. LES 4 AXES STRATÉGIQUES
s = new_slide()
eyebrow(s, 'Les axes stratégiques')
title(s, 'Quatre enjeux, quatre réponses concrètes')
axes = [('Visibilité', 'Une vitrine', 'Le Salon National 100 % IA : 150+ exposants, démonstrations en continu.'),
        ('Financement', 'Un pont', 'Startup Pitch Competition, rencontres investisseurs et sponsors, B2B et B2G.'),
        ('Structuration', 'Un outil', 'L’Annuaire national des acteurs de l’IA : 1 000+ acteurs recensés et vérifiés.'),
        ('Projection internationale', 'Un tremplin', 'Side event du AI for Good Global Summit et délégation camerounaise à Genève.')]
for i, (t, k, d) in enumerate(axes):
    x = Inches(0.6 + i * 3.07)
    card(s, x, Inches(2.2), Inches(2.87), Inches(4.35), top=ENJEUX[i])
    text(s, x + Inches(1.6), Inches(2.3), Inches(1.15), Inches(1.0), f'0{i+1}', size=48, bold=True, color=ENJEUX[i], align=PP_ALIGN.RIGHT)
    text(s, x + Inches(0.3), Inches(3.35), Inches(2.35), Inches(3.1), [
        [('L’enjeu de la', {'size': 12, 'color': GRIS})],
        [(t, {'bold': True, 'size': 20, 'space_after': 14})],
        [(k.upper(), {'bold': True, 'size': 12, 'color': ENJEUX[i]})],
        [(d, {'size': 13, 'color': BLANC})]], spacing=1.15)
notes(s, 'Les quatre enjeux de la charte JCIA, chacun associé à un dispositif concret de l’édition 2027.')

# =========================================================
# 11. PROGRAMME JOUR 1
s = new_slide()
eyebrow(s, 'Programme · Jour 1 · Mardi 27 avril 2027')
title(s, 'Ouverture, plénières et inauguration du Salon', h=Inches(0.8))
j1 = [('08h00', 'Accueil et enregistrement', 'Visite libre des stands en pré-ouverture'),
      ('09h45', 'Arrivée des officiels', 'Gouvernement, corps diplomatique, invités de marque'),
      ('10h00', 'Cérémonie officielle d’ouverture', 'Allocutions de l’IAC/CAIPI, des partenaires et des autorités'),
      ('11h00', 'Inauguration du Salon National 100 % IA', 'Visite guidée des stands, point de presse'),
      ('12h00', 'Plénière 1 · Souveraineté numérique et modèles d’IA africains', '« Bâtir des systèmes ancrés dans nos langues, nos données et nos valeurs »'),
      ('13h00', 'Plénière 2 · Financer l’excellence', 'Capital, calcul et talents pour faire émerger des champions africains'),
      ('13h45', 'Déjeuner de réseautage', 'Déjeuner VIP Gouvernement – diplomatie – sponsors'),
      ('15h00', 'Démonstrations et rencontres d’affaires', 'B2B et B2G programmées, présentations éclairs des exposants')]
for i, (h, t, d) in enumerate(j1):
    col, row = i // 4, i % 4
    x = Inches(0.6 + col * 6.15); y = Inches(1.8 + row * 1.17)
    rect(s, x, y, Inches(5.95), Inches(1.08), CARTE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x + Inches(0.25), y, Inches(1.0), Inches(1.08), h, size=16, bold=True, color=ORANGE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(1.3), y, Inches(4.5), Inches(1.08), [[(t, {'bold': True, 'size': 14})], [(d, {'size': 12, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(0.6), Inches(6.85) - Inches(0.25), Inches(10), Inches(0.3), 'Horaires : 08h00 – 18h00. Programme communiqué sous réserve de modifications.', size=11, color=GRIS, italic=True)
notes(s, 'Jour 1 : réflexion stratégique et démonstration. Source : jciacm.com/programme.')

# =========================================================
# 12. PROGRAMME JOUR 2
s = new_slide()
eyebrow(s, 'Programme · Jour 2 · Mercredi 28 avril 2027')
title(s, 'Compétences, mise en relation et gala des Awards', h=Inches(0.8))
text(s, Inches(0.6), Inches(1.9), Inches(6), Inches(0.4), '09H00 – 12H00 · QUATRE MASTERCLASSES AVEC ATTESTATION', size=12, bold=True, color=TURQ)
mc = [('IA générative & administration publique', 'Cadres des administrations'),
      ('IA & santé', 'Professionnels de santé, startups'),
      ('IA, agriculture intelligente & sécurité alimentaire', 'Agronomes, coopératives, agritech'),
      ('Cybersécurité, données & gouvernance de l’IA', 'DSI, RSSI, juristes, régulateurs')]
for i, (t, p) in enumerate(mc):
    y = Inches(2.35 + i * 1.08)
    card(s, Inches(0.6), y, Inches(6.0), Inches(0.95))
    rect(s, Inches(0.6), y, Inches(0.09), Inches(0.95), ENJEUX[i])
    text(s, Inches(0.95), y, Inches(5.5), Inches(0.95), [[(t, {'bold': True, 'size': 14})], [(p, {'size': 12, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(7.0), Inches(1.9), Inches(6), Inches(0.4), 'LES TEMPS FORTS', size=12, bold=True, color=TURQ)
tf_ = [('13h30', 'Startup Pitch Competition', 'Devant un panel d’investisseurs'),
       ('15h00', 'Women in AI Forum', 'Leadership féminin et inclusion'),
       ('16h15', 'Young AI Leaders Forum', 'La génération montante et le mentorat'),
       ('Journée', 'AI Career Fair', 'Espace recrutement des talents de l’IA'),
       ('19h30', 'Gala des Cameroon AI Awards', 'Remise des 10 distinctions (sur invitation)')]
for i, (h, t, d) in enumerate(tf_):
    y = Inches(2.35 + i * 0.86)
    text(s, Inches(7.0), y, Inches(1.1), Inches(0.75), h, size=15, bold=True, color=ORANGE)
    text(s, Inches(8.2), y, Inches(4.6), Inches(0.75), [[(t, {'bold': True, 'size': 14})], [(d, {'size': 12, 'color': GRIS})]])
notes(s, 'Jour 2 : 08h30 – 18h00, puis gala à 19h30. Rencontres B2B et B2G planifiées via l’application de l’événement pendant les deux jours.')

# =========================================================
# 13. SALON NATIONAL 100 % IA
s = new_slide()
photo(s, os.path.join(IMG, 'salon_siad.jpg'), Inches(6.9), Inches(0.07), W - Inches(6.9), Inches(6.85))
rect(s, Inches(6.9), Inches(0.07), Inches(0.08), Inches(6.85), ORANGE)
eyebrow(s, 'Axe 01 · Visibilité', color=ORANGE)
title(s, 'Le Salon National 100 % IA, cœur battant des JCIA', w=Inches(6.0), h=Inches(1.3))
text(s, Inches(0.6), Inches(2.3), Inches(6.0), Inches(1.0),
     'La plus grande exposition du Cameroun dédiée exclusivement à l’IA, inaugurée par des membres du Gouvernement, pendant les deux jours, dans les espaces d’exposition du Hilton.',
     size=14, color=GRIS, spacing=1.2)
for i, (k, v) in enumerate([('150+', 'exposants attendus'), ('200', 'solutions présentées')]):
    text(s, Inches(0.6 + i * 3.0), Inches(3.45), Inches(2.8), Inches(1.0), [[(k, {'bold': True, 'size': 34, 'color': ORANGE})], [(v, {'size': 13, 'color': GRIS})]])
for i, t in enumerate(['Démonstrations en continu sur la scène du Salon', 'Application de mise en relation pour planifier ses rendez-vous',
                       'Rencontres B2B : startups, entreprises, investisseurs', 'Rencontres B2G : solutions IA et commande publique innovante']):
    y = Inches(4.75 + i * 0.5)
    rect(s, Inches(0.6), y + Inches(0.08), Inches(0.14), Inches(0.14), ENJEUX[i], shape=MSO_SHAPE.OVAL)
    text(s, Inches(0.9), y, Inches(5.7), Inches(0.45), t, size=13)
notes(s, 'Exposants : startups, entreprises tech, laboratoires, administrations, universités, incubateurs, diaspora, institutions financières. Les 50 projets présélectionnés aux CAIA exposent gratuitement. Photo : Salon 100 % IA, JCIA 2025.')

# =========================================================
# 14. CAMEROON AI AWARDS 2027
s = new_slide()
eyebrow(s, 'Célébrer l’excellence', color=ORANGE)
title(s, 'Cameroon AI Awards 2027 (CAIA)', h=Inches(0.7))
text(s, Inches(0.6), Inches(1.55), Inches(12), Inches(0.5), 'La plus haute distinction nationale des talents de l’IA Made in Cameroun, au pays et dans la diaspora. Sous le patronage du Bureau régional de l’UNESCO pour l’Afrique centrale et du Haut-Commissariat britannique au Cameroun.', size=13, color=GRIS, spacing=1.15)
cats = ['IA pour la santé', 'Agriculture & sécurité alimentaire', 'Éducation & formation', 'Inclusion financière & fintech', 'Administration publique',
        'Cybersécurité', 'Langues nationales, culture & industries créatives', 'Recherche scientifique', 'Femme de l’année en IA', 'Jeune talent / étudiant chercheur']
card(s, Inches(0.6), Inches(2.4), Inches(6.3), Inches(4.3))
text(s, Inches(0.9), Inches(2.6), Inches(5.8), Inches(0.4), '10 CATÉGORIES', size=12, bold=True, color=TURQ)
for i, c in enumerate(cats):
    x = Inches(0.9 + (i // 5) * 3.0); y = Inches(3.05 + (i % 5) * 0.7)
    text(s, x, y, Inches(2.85), Inches(0.65), [[(f'{i+1:02d}  ', {'bold': True, 'color': ORANGE}), (c, {})]], size=13)
text(s, Inches(7.2), Inches(2.45), Inches(5.5), Inches(0.4), 'CALENDRIER', size=12, bold=True, color=TURQ)
cal = [('15 nov. 2026 → 28 fév. 2027', 'Candidatures en ligne, ouvertes et gratuites'),
       ('15 mars 2027', 'Publication des 50 projets présélectionnés'),
       ('20 mars → 15 avril 2027', 'Vote du public (40 % de la note)'),
       ('28 avril 2027', 'Gala et remise des prix (jury : 60 %)')]
for i, (d, t) in enumerate(cal):
    y = Inches(2.9 + i * 0.82)
    rect(s, Inches(7.2), y + Inches(0.05), Inches(0.06), Inches(0.62), ENJEUX[i])
    text(s, Inches(7.45), y, Inches(5.3), Inches(0.75), [[(d, {'bold': True, 'size': 14})], [(t, {'size': 12, 'color': GRIS})]])
text(s, Inches(7.2), Inches(6.25), Inches(5.6), Inches(0.5), 'Récompenses : trophée, mention « UNESCO Award Winner », offres de financement, stages, stand gratuit, préparation à la délégation de Genève.', size=12, color=ORANGE, spacing=1.1)
notes(s, 'Éligibilité : nationalité camerounaise, 18 ans et plus, au Cameroun ou dans la diaspora. Jury de 8 membres indépendants. Termes de référence : jciacm.com/documents/TDR-CAIA-2027.pdf')

# =========================================================
# 15. ANNUAIRE NATIONAL
s = new_slide()
photo(s, os.path.join(IMG, 'salon_gta.jpg'), 0, Inches(0.07), Inches(5.6), Inches(6.85))
rect(s, Inches(5.6), Inches(0.07), Inches(0.08), Inches(6.85), TERRA)
eyebrow(s, 'Axe 03 · Structuration', x=Inches(6.2), color=TERRA)
title(s, 'L’Annuaire national des acteurs de l’IA', x=Inches(6.2), w=Inches(6.6), h=Inches(1.3))
text(s, Inches(6.2), Inches(2.2), Inches(6.5), Inches(1.2),
     'Une première nationale : la base de référence qui recense, de façon structurée et vérifiée, les acteurs clés de l’écosystème camerounais. Édition imprimée de prestige et version consultable en ligne.',
     size=14, color=GRIS, spacing=1.2)
text(s, Inches(6.2), Inches(3.55), Inches(3), Inches(1.0), [[('1 000+', {'bold': True, 'size': 34, 'color': ORANGE})], [('acteurs visés', {'size': 13, 'color': GRIS})]])
text(s, Inches(9.3), Inches(3.55), Inches(3.5), Inches(1.0), [[('catalogue.jcia.cm', {'bold': True, 'size': 18})], [('version en ligne', {'size': 13, 'color': GRIS})]])
for i, (k, v) in enumerate([('Pour l’État', 'Un outil de pilotage de la Stratégie nationale de l’IA'), ('Pour les investisseurs', 'Un répertoire qualifié qui réduit les coûts de prospection'),
                            ('Pour les startups et chercheurs', 'Une visibilité durable, bien au-delà des deux jours'), ('Pour les partenaires internationaux', 'Une porte d’entrée fiable vers l’écosystème')]):
    y = Inches(4.6 + i * 0.56)
    text(s, Inches(6.2), y, Inches(6.6), Inches(0.5), [[(k + ' : ', {'bold': True, 'color': BLANC}), (v, {'color': GRIS})]], size=12)
notes(s, 'Réalisé sous la supervision du Comité scientifique : appel public à inscription, vérification, catégorisation standardisée et mise à jour annuelle. Consentement explicite, droit de rectification et minimisation des données.')

# =========================================================
# 16. PARTENAIRES
s = new_slide()
eyebrow(s, 'Ils portent les JCIA')
title(s, 'Un écosystème de partenaires institutionnels et internationaux', h=Inches(1.3))
p27 = [('Organisateur', 'IAC – CAIPI'), ('Label international', 'Road to Geneva AI Summit'), ('Partenaire stratégique', 'Geneva AI Governance Institute'),
       ('Collaboration sectorielle', 'UIT · Membre de Secteur'), ('Patronage', 'Ministère des Postes et Télécommunications'),
       ('Égide des CAIA 2027', 'Commission nationale pour l’UNESCO'), ('Partenaire académique', 'Université Bordeaux Montaigne')]
text(s, Inches(0.6), Inches(2.2), Inches(6), Inches(0.4), 'ÉDITION 2027', size=12, bold=True, color=TURQ)
for i, (r, n) in enumerate(p27):
    x = Inches(0.6 + (i % 2) * 3.05); y = Inches(2.6 + (i // 2) * 1.0)
    card(s, x, y, Inches(2.9), Inches(0.85))
    text(s, x + Inches(0.2), y, Inches(2.6), Inches(0.85), [[(r.upper(), {'size': 10, 'bold': True, 'color': ORANGE})], [(n, {'size': 13, 'bold': True})]], anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(7.0), Inches(2.2), Inches(6), Inches(0.4), 'ILS NOUS ONT FAIT CONFIANCE EN 2023 ET 2025', size=12, bold=True, color=TURQ)
past = ['Commission nationale UNESCO', 'UIT', 'AI Council for Africa', 'GAIGI', 'AUF', 'Gouvernement du Canada', 'Business France', 'MILA', 'Université Bordeaux Montaigne',
        'ENSPY', 'ESSFAR', 'IRIC', 'NumIAtech', 'Atos', 'Huawei', 'CAMPOST', 'Port Autonome de Kribi', 'SERVOO', 'GTEK']
for i, p in enumerate(past):
    x = Inches(7.0 + (i % 2) * 2.95); y = Inches(2.62 + (i // 2) * 0.42)
    text(s, x, y, Inches(2.9), Inches(0.4), [[('• ', {'color': ORANGE, 'bold': True}), (p, {})]], size=12)
notes(s, 'Médias ayant couvert les JCIA : CRTV, Canal 2 International, Vision 4, Équinoxe TV, Africa 24, BBC Afrique, RFI, Canal +, Cameroon Tribune, EcoMatin, Mutations, Le Jour, entre autres.')

# =========================================================
# 17. DEVENIR PARTENAIRE
s = new_slide()
eyebrow(s, 'Devenir partenaire', color=ORANGE)
title(s, 'Six formules, une ambition commune', h=Inches(0.8))
rows = [('Platinum', '10 000 000', '1', 'Partenaire officiel exclusif · stand 36 m² · allocution de 10 min à l’ouverture · 15 invitations VIP'),
        ('Diamond', '5 000 000', '2', 'Parrainage d’une plénière ou du gala · stand 24 m² · keynote de 15 min · 10 invitations VIP'),
        ('Gold', '3 000 000', '4', 'Parrainage d’une masterclass ou d’un espace · stand 18 m² · présentation de 10 min'),
        ('Silver', '1 000 000', '6', 'Stand 12 m² · présentation de 10 min sur la scène du Salon · 4 invitations VIP'),
        ('Bronze', '500 000', '10', 'Stand 9 m² · logo sur le site, les écrans et le programme · 2 invitations VIP'),
        ('Supporter', '100 000', 'Illimité', 'Stand mutualisé 4 m² · certificat de soutien · ouvert aux PME et startups')]
tbl = s.shapes.add_table(len(rows) + 1, 4, Inches(0.6), Inches(1.9), Inches(12.1), Inches(4.3)).table
widths = [1.8, 1.9, 1.2, 7.2]
for i, wd in enumerate(widths): tbl.columns[i].width = Inches(wd)
hdr = ['Formule', 'FCFA', 'Places', 'Principales contreparties']
for r in range(len(rows) + 1):
    for c in range(4):
        cell = tbl.cell(r, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = ENCRE if r == 0 else (CARTE if r % 2 else SECTION)
        cell.margin_left = Inches(0.15); cell.margin_top = Inches(0.06); cell.margin_bottom = Inches(0.06)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame; tf.paragraphs[0].text = ''
        run = tf.paragraphs[0].add_run(); run.text = hdr[c] if r == 0 else rows[r - 1][c]
        f = run.font; f.name = FONT; f.size = Pt(12 if r == 0 else 13); f.bold = (r == 0 or c == 0)
        f.color.rgb = ORANGE if (r == 0 or (c == 0)) else BLANC
text(s, Inches(0.6), Inches(6.35), Inches(12.1), Inches(0.5),
     'Sponsoring à la carte également possible (stands, prises de parole, parrainages, visibilité). Contributions en nature acceptées. Places limitées : disponibilité confirmée par le secrétariat.',
     size=12, color=GRIS, italic=True)
notes(s, 'Dossier de sponsoring complet : jciacm.com/documents/Dossier-Partenariat-JCIA-2027.pdf — Contact : contact@jciacm.com · +237 699 089 937.')

# =========================================================
# 18. PLAN DE VISIBILITÉ
s = new_slide()
eyebrow(s, 'Stratégie de communication')
title(s, 'Une visibilité mesurable avant, pendant et après', h=Inches(0.8))
phases = [('Avant', ORANGE, ['Conférence de presse de lancement (mars 2027)', 'Communiqués et dossiers de presse', 'Affichage à Yaoundé et Douala', 'Spots TV et radio']),
          ('Pendant', TURQ, ['Une centaine de journalistes accrédités', 'Points de presse quotidiens', 'Plénières et Awards en direct', 'Interviews plateaux']),
          ('Après', VIOLET2, ['Communiqué de clôture et bilan chiffré', 'Film officiel de l’événement', 'Diffusion des recommandations', 'Suivi de la délégation jusqu’à Genève'])]
for i, (t, c, items) in enumerate(phases):
    x = Inches(0.6 + i * 3.0)
    card(s, x, Inches(1.95), Inches(2.8), Inches(4.0), top=c)
    text(s, x + Inches(0.25), Inches(2.2), Inches(2.4), Inches(0.5), [[(f'0{i+1} ', {'color': c}), (t, {})]], size=20, bold=True)
    for j, it in enumerate(items):
        text(s, x + Inches(0.25), Inches(2.9 + j * 0.74), Inches(2.4), Inches(0.7), it, size=13, color=GRIS, spacing=1.1)
card(s, Inches(9.75), Inches(1.95), Inches(2.95), Inches(4.0), fill=SECTION)
for i, (k, v) in enumerate([('2 M+', 'personnes touchées visées'), ('5 M', 'impressions digitales visées'), ('10 000+', 'contacts qualifiés en infolettre')]):
    text(s, Inches(10.05), Inches(2.2 + i * 1.22), Inches(2.5), Inches(1.1), [[(k, {'bold': True, 'size': 28, 'color': ORANGE})], [(v, {'size': 12, 'color': GRIS})]])
text(s, Inches(0.6), Inches(6.15), Inches(12), Inches(0.6), 'Digital : site officiel, LinkedIn, Facebook, X, Instagram, TikTok, YouTube, streaming habillé aux couleurs des sponsors, application de l’événement.', size=12, color=GRIS, italic=True)
notes(s, 'Plan de communication tel que présenté sur la page Partenaires de jciacm.com.')

# =========================================================
# 19. CLÔTURE / CONTACTS
s = new_slide(footer=False, band=False)
photo(s, os.path.join(IMG, 'visite_stand.jpg'), 0, 0, W, H)
rect(s, 0, 0, W, H, NUIT, alpha=0.6)
rect(s, 0, 0, Inches(7.8), H, NUIT, alpha=0.85)
s.shapes.add_picture(LOGO, Inches(0.6), Inches(0.5), width=Inches(3.0))
text(s, Inches(0.6), Inches(2.1), Inches(7), Inches(1.6), 'Rejoignez le mouvement, de Yaoundé à Genève', size=36, bold=True, spacing=1.0)
text(s, Inches(0.6), Inches(3.75), Inches(6.8), Inches(0.9), 'Participez, exposez, candidatez aux Cameroon AI Awards ou devenez partenaire des JCIA 2027.', size=16, color=GRIS, spacing=1.15)
contacts = [('Site', 'www.jciacm.com'), ('E-mail', 'contact@jciacm.com'), ('Téléphone / WhatsApp', '+237 699 089 937 · +237 677 238 022'),
            ('Adresse', 'Immeuble Dangote, 2e étage, Coron, Yaoundé')]
for i, (k, v) in enumerate(contacts):
    y = Inches(4.65 + i * 0.5)
    text(s, Inches(0.6), y, Inches(2.3), Inches(0.45), k.upper(), size=11, bold=True, color=ORANGE)
    text(s, Inches(2.9), y - Inches(0.03), Inches(4.8), Inches(0.45), v, size=14, bold=True)
s.shapes.add_picture(TOGHU, 0, H - bh, width=W)
notes(s, 'Merci. Contacts du secrétariat de l’IAC – CAIPI. Photo : visite officielle du Salon 100 % IA, JCIA 2025.')

prs.save(OUT)
print('slides', len(prs.slides), OUT)
