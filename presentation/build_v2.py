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
TOTAL = 13
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
# 01 — COUVERTURE
s = slide(chrome=False, notes='Journées Camerounaises de l’Intelligence Artificielle, 3e édition, 27 et 28 avril 2027, Hilton Hotel de Yaoundé. Événement satellite du Geneva AI Summit 2027. Photo : JCIA 2025.')
photo(s, 'public_salle', 0, 0, W, H)
gradient(s, 0, 0, W, H, [(0, 97), (45, 88), (100, 25)], 0)
gradient(s, 0, Inches(4.5), W, Inches(3.0), [(0, 0), (100, 85)], 90)
s.shapes.add_picture(LOGO, M, Inches(0.6), width=Inches(2.9))
label(s, M, Inches(2.95), '3e édition  ·  De Yaoundé à Genève')
tx(s, M, Inches(3.35), Inches(11), Inches(2.0), [
    [('Penser l’IA au Cameroun,', {})],
    [('pour le Cameroun.', {'color': ORANGE})]], font=F_DISPLAY, size=48, spacing=0.98)
tx(s, M, Inches(5.25), Inches(8), Inches(0.9), [
    [('Journées Camerounaises de l’Intelligence Artificielle', {'font': F_SEMI})],
    [('27 & 28 avril 2027  ·  Hilton Hotel, Yaoundé', {'color': GRIS})]], font=F_LIGHT, size=16, spacing=1.3)
toghu(s, height=Inches(0.62))

# =============================================================
# 02 — DE YAOUNDÉ À GENÈVE
s = slide(notes='Message clé : les JCIA 2027 sont l’événement satellite (side event) préparatoire du Geneva AI Summit 2027 et la porte d’entrée nationale vers le AI for Good Global Summit de l’UIT. Label international « Road to Geneva AI Summit ».')
pic = s.shapes.add_picture(CARTE, Inches(8.4), Inches(0.55), height=Inches(6.6)); fade_pic(pic, 55)
label(s, M, Inches(2.05), 'Positionnement')
tx(s, M, Inches(2.45), Inches(9), Inches(2.8), [[('De Yaoundé', {})], [('à Genève.', {'color': ORANGE})]], font=F_DISPLAY, size=80, spacing=0.92)
tx(s, M, Inches(5.15), Inches(6.6), Inches(1.0),
   'Les JCIA 2027 sont l’événement satellite du Geneva AI Summit 2027 : l’étape camerounaise sur la route du sommet mondial de l’IA.',
   font=F_LIGHT, size=18, color=GRIS, spacing=1.3)

# =============================================================
# 03 — LE CHIFFRE
s = slide(notes='Objectifs 2027 : 7 000+ participants en présentiel, 5 000+ en ligne, 150+ startups et exposants, 40+ intervenants de haut niveau, 20+ délégations diplomatiques, 500+ rencontres B2B et B2G, 2 millions de personnes touchées. Toujours parler de chiffres « attendus ».')
label(s, M, Inches(1.55), 'Changement d’échelle  ·  objectifs 2027')
tx(s, M, Inches(1.9), Inches(8), Inches(2.6), '7 000+', font=F_DISPLAY, size=150, color=ORANGE, spacing=0.9)
tx(s, M, Inches(4.45), Inches(6.8), Inches(0.9), 'participants attendus au Hilton de Yaoundé, et plus de 5 000 en ligne.', font=F_LIGHT, size=22, color=BLANC, spacing=1.25)
stats = [('150+', 'startups et exposants'), ('40+', 'intervenants de haut niveau'), ('20+', 'délégations diplomatiques')]
for i, (k, v) in enumerate(stats):
    y = Inches(1.95 + i * 1.45)
    box(s, Inches(8.9), y, Inches(3.7), Pt(1), LIGNE)
    tx(s, Inches(8.9), y + Inches(0.22), Inches(3.7), Inches(1.1), [[(k, {'font': F_DISPLAY, 'size': 34})], [(v, {'font': F_LIGHT, 'size': 14, 'color': GRIS})]], spacing=1.1)

# =============================================================
# 04 — TRAJECTOIRE
s = slide(notes='2023 : 1re édition à l’IRIC et l’ENSPY (décembre), 1 000+ participants, 17 intervenants. 2025 : 2e édition au Hilton, ENSPY et IRIC (avril), 5 000 participants + 2 000 en ligne, ~100 startups, 60+ organisations, 1ers Cameroon AI Awards (53 projets), 1er Salon 100 % IA. 2027 : 3e édition, side event du AI for Good, lancement de l’Annuaire national, délégation à Genève.')
label(s, M, Inches(1.35), 'Notre trajectoire')
tx(s, M, Inches(1.7), Inches(11), Inches(1.0), 'Trois éditions, une ambition qui grandit.', font=F_DISPLAY, size=36)
eds = [('2023', '1 000+', 'participants · l’acte fondateur', FANTOME, GRIS),
       ('2025', '7 000', 'participants dont 2 000 en ligne · l’étape décisive', FANTOME, GRIS),
       ('2027', 'Genève', 'l’étape camerounaise du sommet mondial', ORANGE, ORANGE)]
cw = (W - 2 * M) / 3
box(s, M, Inches(4.12), W - 2 * M, Pt(1), LIGNE)
for i, (yr, k, v, cy, ck) in enumerate(eds):
    x = int(M + cw * i)
    tx(s, x, Inches(2.75), int(cw), Inches(1.3), yr, font=F_DISPLAY, size=72, color=cy)
    box(s, x, Inches(4.02), Inches(0.2), Inches(0.2), ck, MSO_SHAPE.OVAL)
    tx(s, x, Inches(4.55), int(cw) - Inches(0.4), Inches(1.6), [[(k, {'font': F_DISPLAY, 'size': 30, 'color': BLANC})], [(v, {'font': F_LIGHT, 'size': 15, 'color': GRIS})]], spacing=1.2)

# =============================================================
# 05 — JCIA 2025 EN IMAGES
s = slide(notes='Retour sur la 2e édition (avril 2025, Hilton Hotel de Yaoundé) : cérémonie, panels, Salon National 100 % IA. 5 000 participants sur place, 2 000 en ligne, ~100 startups, 60+ organisations, 53 projets aux premiers Cameroon AI Awards.')
photo(s, 'pupitre_hilton', 0, 0, Inches(7.6), H, 0.3)
gradient(s, Inches(5.6), 0, Inches(2.0), H, [(0, 0), (100, 100)], 0)
label(s, Inches(8.1), Inches(1.4), 'Ce que nous avons déjà bâti')
tx(s, Inches(8.1), Inches(1.75), Inches(4.6), Inches(1.0), 'JCIA 2025', font=F_DISPLAY, size=44)
for i, (k, v) in enumerate([('5 000', 'participants sur place'), ('2 000', 'participants en ligne'), ('53', 'projets aux 1ers Cameroon AI Awards')]):
    y = Inches(2.85 + i * 0.82)
    tx(s, Inches(8.1), y, Inches(4.6), Inches(0.8), [[(k + '   ', {'font': F_DISPLAY, 'size': 26, 'color': ORANGE}), (v, {'font': F_LIGHT, 'size': 15, 'color': GRIS})]], anchor=MSO_ANCHOR.MIDDLE)
photo(s, 'salon_echange', Inches(8.1), Inches(5.45), Inches(2.2), Inches(1.45))
photo(s, 'panel_intervenante', Inches(10.45), Inches(5.45), Inches(2.15), Inches(1.45))

# =============================================================
# 06 — THÈME
s = slide(notes='Thème officiel de la 3e édition. Quatre piliers : innovation souveraine (technologies, données, modèles, compétences) ; excellence camerounaise ; solutions locales (langues nationales, agriculture, santé communautaire, services publics) ; influence mondiale (de Yaoundé à Genève, gouvernance de l’IA).')
s.shapes.add_picture(CARTE, Inches(8.55), Inches(0.45), height=Inches(6.7))
label(s, M, Inches(1.6), 'Thème 2027  ·  L’IA Made in Cameroun')
tx(s, M, Inches(2.0), Inches(7.6), Inches(3.2), [[('« Penser l’intelligence artificielle ', {}), ('au Cameroun, pour le Cameroun', {'color': ORANGE}), (' »', {})]],
   font=F_DISPLAY, size=42, spacing=1.02)
pil = ['Souveraineté', 'Excellence', 'Solutions locales', 'Influence mondiale']
for i, p in enumerate(pil):
    x = M + Inches((i % 2) * 3.0); yy = 5.25 + (i // 2) * 0.55
    box(s, x, Inches(yy + 0.12), Inches(0.12), Inches(0.12), AXES[i], MSO_SHAPE.OVAL)
    tx(s, x + Inches(0.25), Inches(yy), Inches(2.6), Inches(0.4), p, font=F_SEMI, size=13, color=BLANC)

# =============================================================
# 07 — GENÈVE : L'ÉVÉNEMENT SATELLITE
s = slide(notes='Le AI for Good Global Summit est organisé par l’UIT avec plus de 50 agences des Nations Unies : 11 000+ participants, 800+ intervenants, 19 milliards d’impressions médias. Cinq objectifs du side event : préparer la délégation nationale, promouvoir les solutions les plus matures, faire rayonner le Cameroun, organiser des rencontres avec les investisseurs, faciliter la coopération technologique.')
label(s, M, Inches(1.45), 'Événement satellite')
tx(s, M, Inches(1.8), Inches(6.4), Inches(2.4), 'La route du Geneva AI Summit 2027 passe par Yaoundé.', font=F_DISPLAY, size=38, spacing=1.0)
tx(s, M, Inches(4.25), Inches(5.9), Inches(1.2), 'Les talents qui se distinguent aux JCIA préparent leur présence à Genève, au cœur du système des Nations Unies.', font=F_LIGHT, size=17, color=GRIS, spacing=1.3)
pill = box(s, M, Inches(5.65), Inches(3.6), Inches(0.46), NUIT, MSO_SHAPE.ROUNDED_RECTANGLE)
pill.adjustments[0] = 0.5; pill.line.color.rgb = ORANGE; pill.line.width = Pt(1)
tx(s, M, Inches(5.65), Inches(3.6), Inches(0.46), 'ROAD TO GENEVA AI SUMMIT', font=F_SEMI, size=11, color=ORANGE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, track=200)
# la route
rx = Inches(8.2)
box(s, rx + Inches(0.115), Inches(1.95), Pt(2), Inches(2.25), LIGNE)
for i, (city, date, c, y) in enumerate([('Yaoundé', '27 & 28 avril 2027', ORANGE, 1.75), ('Genève', 'juin 2027', TURQ, 3.95)]):
    box(s, rx, Inches(y + 0.08), Inches(0.26), Inches(0.26), c, MSO_SHAPE.OVAL)
    tx(s, rx + Inches(0.6), Inches(y - 0.05), Inches(4), Inches(0.9), [[(city, {'font': F_DISPLAY, 'size': 28})], [(date, {'font': F_LIGHT, 'size': 14, 'color': c})]], spacing=1.1)
box(s, rx, Inches(5.25), Inches(4.4), Pt(1), LIGNE)
label(s, rx, Inches(5.45), 'AI for Good Global Summit · UIT', color=GRIS)
for i, (k, v) in enumerate([('11 000+', 'participants'), ('800+', 'intervenants'), ('50+', 'agences ONU')]):
    tx(s, rx + Inches(i * 1.5), Inches(5.85), Inches(1.45), Inches(0.9), [[(k, {'font': F_DISPLAY, 'size': 22})], [(v, {'font': F_LIGHT, 'size': 12, 'color': GRIS})]], spacing=1.1)

# =============================================================
# 08 — QUATRE AXES
s = slide(notes='Quatre enjeux de l’écosystème camerounais de l’IA, quatre réponses : visibilité avec le Salon National 100 % IA ; financement avec le Startup Pitch, les investisseurs et sponsors ; structuration avec l’Annuaire national des acteurs de l’IA (1 000+ acteurs visés) ; projection internationale avec le side event du AI for Good et la délégation camerounaise à Genève.')
label(s, M, Inches(1.35), 'Axes stratégiques')
tx(s, M, Inches(1.7), Inches(11), Inches(1.0), 'Quatre enjeux, une réponse intégrée.', font=F_DISPLAY, size=36)
axes = [('Visibilité', 'Le Salon National 100 % IA'), ('Financement', 'Startup Pitch et investisseurs'),
        ('Structuration', 'L’Annuaire national des acteurs de l’IA'), ('Rayonnement', 'Une délégation camerounaise à Genève')]
cw = (W - 2 * M - Inches(0.9)) / 4
for i, (t, d) in enumerate(axes):
    x = int(M + i * (cw + Inches(0.3)))
    box(s, x, Inches(3.05), int(cw), Inches(0.06), AXES[i])
    tx(s, x, Inches(3.35), int(cw), Inches(1.0), f'0{i+1}', font=F_DISPLAY, size=54, color=AXES[i])
    tx(s, x, Inches(4.55), int(cw), Inches(1.9), [[(t, {'font': F_DISPLAY, 'size': 22, 'after': 8})], [(d, {'font': F_LIGHT, 'size': 15, 'color': GRIS})]], spacing=1.2)

# =============================================================
# 09 — DEUX JOURS
s = slide(notes='Jour 1 (08h00–18h00) : accueil, arrivée des officiels, cérémonie d’ouverture, inauguration du Salon, plénière « Souveraineté numérique et modèles d’IA africains », plénière « Financer l’excellence », déjeuner VIP, démos et rencontres B2B/B2G. Jour 2 (08h30–18h00) : 4 masterclasses avec attestation (IA générative & administration, santé, agriculture, cybersécurité), Startup Pitch 13h30, Women in AI Forum 15h00, Young AI Leaders Forum 16h15, AI Career Fair, gala des Awards 19h30 sur invitation.')
label(s, M, Inches(1.35), 'Programme')
tx(s, M, Inches(1.7), Inches(11), Inches(1.0), 'Deux jours intensifs.', font=F_DISPLAY, size=36)
days = [('Mardi 27 avril', [('10h00', 'Cérémonie officielle d’ouverture'), ('12h00', 'Plénières : souveraineté et financement'), ('15h00', 'Démos et rencontres B2B / B2G')]),
        ('Mercredi 28 avril', [('09h00', 'Quatre masterclasses certifiantes'), ('13h30', 'Startup Pitch Competition'), ('19h30', 'Gala des Cameroon AI Awards')])]
for i, (d, items) in enumerate(days):
    x = M + Inches(i * 6.1)
    tx(s, x, Inches(2.95), Inches(5.6), Inches(0.5), d, font=F_SEMI, size=15, color=ORANGE, track=100)
    box(s, x, Inches(3.5), Inches(5.5), Pt(1), LIGNE)
    for j, (h, t) in enumerate(items):
        y = Inches(3.75 + j * 0.95)
        tx(s, x, y, Inches(1.2), Inches(0.6), h, font=F_LIGHT, size=18, color=GRIS)
        tx(s, x + Inches(1.3), y, Inches(4.3), Inches(0.8), t, font=F_SEMI, size=19, color=BLANC, spacing=1.1)

# =============================================================
# 10 — SALON (photo plein cadre)
s = slide(notes='Salon National 100 % IA : la plus grande exposition du Cameroun dédiée à l’IA, inaugurée par des membres du Gouvernement, pendant les deux jours. Démos en continu, application de mise en relation, rencontres B2B et B2G. Les 50 projets présélectionnés aux CAIA exposent gratuitement. Réserver un stand : contact@jciacm.com. Photo : visite officielle des stands, JCIA 2025.')
photo(s, 'visite_officielle', 0, 0, W, H, 0.35)
gradient(s, 0, Inches(2.2), W, H - Inches(2.2), [(0, 0), (55, 80), (100, 97)], 90)
gradient(s, 0, 0, W, Inches(1.4), [(0, 70), (100, 0)], 90)
label(s, M, Inches(4.55), 'Axe 01  ·  Visibilité')
tx(s, M, Inches(4.9), Inches(11.5), Inches(1.0), 'Le Salon National 100 % IA', font=F_DISPLAY, size=44)
for i, (k, v) in enumerate([('150+', 'exposants'), ('200', 'solutions'), ('2', 'jours de démos')]):
    tx(s, M + Inches(i * 2.4), Inches(5.95), Inches(2.3), Inches(0.9), [[(k + ' ', {'font': F_DISPLAY, 'size': 28, 'color': ORANGE}), (v, {'font': F_LIGHT, 'size': 15, 'color': BLANC})]])

# =============================================================
# 11 — CAMEROON AI AWARDS
s = slide(notes='Cameroon AI Awards 2027 : concours national ouvert et gratuit, au Cameroun et dans la diaspora (18 ans et plus). 10 catégories : santé, agriculture, éducation, fintech, administration publique, cybersécurité, langues nationales et culture, recherche, Femme de l’année en IA, Jeune talent. Note finale : jury 60 %, vote du public 40 %. Patronage : Bureau régional de l’UNESCO pour l’Afrique centrale et Haut-Commissariat britannique. Termes de référence sur jciacm.com.')
tx(s, M - Inches(0.1), Inches(1.0), Inches(5), Inches(4.2), '10', font=F_DISPLAY, size=260, color=ORANGE, spacing=0.85)
tx(s, M, Inches(4.75), Inches(4.8), Inches(1.2), 'prix pour récompenser l’IA Made in Cameroun.', font=F_LIGHT, size=20, color=BLANC, spacing=1.25)
label(s, Inches(6.6), Inches(1.45), 'Cameroon AI Awards 2027')
tx(s, Inches(6.6), Inches(1.8), Inches(6), Inches(1.0), 'L’excellence, célébrée.', font=F_DISPLAY, size=36)
cal = [('15 nov. 2026', 'Ouverture des candidatures'), ('28 fév. 2027', 'Clôture des candidatures'), ('20 mars → 15 avril', 'Vote du public'), ('28 avril 2027', 'Gala et remise des prix')]
box(s, Inches(6.7), Inches(3.1), Pt(1.5), Inches(3.05), LIGNE)
for i, (d, t) in enumerate(cal):
    y = Inches(2.95 + i * 0.85); last = i == 3
    box(s, Inches(6.62), y + Inches(0.12), Inches(0.18), Inches(0.18), ORANGE if last else GRIS, MSO_SHAPE.OVAL)
    tx(s, Inches(7.1), y, Inches(5.5), Inches(0.8), [[(d, {'font': F_SEMI, 'size': 17, 'color': ORANGE if last else BLANC})], [(t, {'font': F_LIGHT, 'size': 14, 'color': GRIS})]], spacing=1.1)

# =============================================================
# 12 — PARTENAIRES (escalier des formules)
s = slide(notes='Six formules : Platinum 10 000 000 FCFA (1 place, partenaire officiel exclusif, stand 36 m², allocution d’ouverture, 15 invitations VIP) ; Diamond 5 000 000 (2 places) ; Gold 3 000 000 (4) ; Silver 1 000 000 (6) ; Bronze 500 000 (10) ; Supporter 100 000 (illimité). Sponsoring à la carte possible, contributions en nature acceptées. Places limitées : disponibilité confirmée par le secrétariat. Dossier : jciacm.com/documents/Dossier-Partenariat-JCIA-2027.pdf')
label(s, M, Inches(1.35), 'Devenir partenaire')
tx(s, M, Inches(1.7), Inches(11.8), Inches(1.0), 'Associez votre marque à la route vers Genève.', font=F_DISPLAY, size=30)
tiers = [('Supporter', '100 000'), ('Bronze', '500 000'), ('Silver', '1 M'), ('Gold', '3 M'), ('Diamond', '5 M'), ('Platinum', '10 M')]
gap = Inches(0.22); bw = (W - 2 * M - gap * 5) / 6
base = Inches(6.55)
for i, (n, p) in enumerate(tiers):
    x = int(M + i * (bw + gap)); hh = Inches(0.7 + i * 0.42)
    top = i == 5
    box(s, x, base - hh, int(bw), hh, ORANGE if top else SURF)
    tx(s, x, base - hh - Inches(0.95), int(bw), Inches(0.9), [[(n, {'font': F_SEMI, 'size': 15, 'color': ORANGE if top else BLANC})], [(p + ' FCFA', {'font': F_LIGHT, 'size': 13, 'color': GRIS})]], spacing=1.1)
tx(s, M, Inches(6.72), Inches(11), Inches(0.3), 'Formules à la carte et contributions en nature possibles. Dossier de sponsoring complet sur jciacm.com.', font=F_LIGHT, size=12, color=GRIS)

# =============================================================
# 13 — CLÔTURE
s = slide(chrome=False, notes='Merci. Contacts du secrétariat : contact@jciacm.com, +237 699 089 937 (WhatsApp), +237 677 238 022. Site : www.jciacm.com. Photo : JCIA 2025.')
photo(s, 'public_proche', 0, 0, W, H, 0.35)
gradient(s, 0, 0, W, H, [(0, 92), (100, 92)], 0)
s.shapes.add_picture(LOGO, int((W - Inches(3.0)) / 2), Inches(0.9), width=Inches(3.0))
tx(s, 0, Inches(2.75), W, Inches(1.4), 'Rendez-vous à Yaoundé.', font=F_DISPLAY, size=60, align=PP_ALIGN.CENTER)
tx(s, 0, Inches(3.95), W, Inches(0.6), '27 & 28 avril 2027  ·  Hilton Hotel', font=F_LIGHT, size=22, color=ORANGE, align=PP_ALIGN.CENTER, track=50)
tx(s, 0, Inches(5.1), W, Inches(0.5), [[('www.jciacm.com', {'font': F_SEMI}), ('     ·     contact@jciacm.com     ·     +237 699 089 937', {})]], font=F_LIGHT, size=15, color=BLANC, align=PP_ALIGN.CENTER)
toghu(s, height=Inches(0.62))

# repères (au-dessus de tout)
for sl in prs.slides:
    if getattr(sl, '_chrome', True): pass
for i, sl in enumerate(prs.slides):
    if i not in (0, TOTAL - 1):
        st['n'] = i + 1; chrome(sl)

prs.save(OUT)
print('ok', len(prs.slides))
