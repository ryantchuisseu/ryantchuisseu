# JCIA 2027 — Maquette de l'application mobile

Maquette cliquable de l'app compagnon du site <https://jciacm.com/>.
Elle reproduit les pages et parcours **visibles publiquement** sur le site et applique la charte graphique JCIA 2027.
Elle ne contient aucun code, aucune clé et aucune donnée privée du site d'origine.

## Lancer

Aucune installation. Ouvrir `index.html` dans un navigateur (ou `python3 -m http.server` dans ce dossier).
Sur ordinateur, l'app s'affiche dans un cadre de téléphone ; sur mobile, en plein écran.

## Écrans

| Onglet | Écrans |
|---|---|
| Accueil | Hero, compte à rebours, chiffres, défis, parcours, communauté |
| Programme | Jour 1 / Jour 2, masterclasses |
| Intervenants | Liste + recherche |
| Billets | 5 billets → inscription en 4 étapes → billet (QR fictif) + visuel « I'll be there » |
| Plus | Salon 100 % IA, Awards, Annuaire, Participants, Partenaires, FAQ, Contact, choix Nuit / Jour |

## Charte graphique appliquée (v1.0, octobre 2026)

| Règle de la charte | Dans la maquette |
|---|---|
| Fond nuit `#0E1326`, orange `#F6A343` réservé aux actions et chiffres clés | Variables CSS `:root` en tête de `index.html` |
| Police **Sora** (repli Arial) | Chargée depuis Google Fonts : **à héberger soi-même** en production (confidentialité, hors-ligne) |
| 4 défis = 4 couleurs (orange, turquoise, terracotta, violet), cartes à rayon 22 px, filet de 5 px, numéro en filigrane | Classes `.chal .c1…c4` |
| Bouton pilule dégradé, 44 px mini, **un seul bouton plein par écran** | Classe `.btn` (plein) / `.btn.secondary` (contour) |
| Bande toghu sous l'en-tête | `assets/bande-toghu.png` |
| Carte du Cameroun : une fois par page, jamais derrière un paragraphe | Accueil uniquement, à droite des dates |
| Écriture : vouvoiement, « visés / attendus », pas de places restantes garanties, pas de code PIN | Appliquée aux textes |
| Contraste 4,5:1, jamais l'état par la seule couleur | Onglet actif : couleur + barre ; billet choisi : bordure + « ✓ Sélectionné » |

## Version Jour

Bouton ☀️/🌙 dans l'en-tête, ou Plus → Apparence. Lien direct : `index.html?theme=day`. Le choix est mémorisé dans le navigateur.

- Palette « Jour » de la charte : crème `#FBF6EE` (page), sable `#F4E6D2` (cartes), encre `#19203A` (texte).
- **En-tête et barre d'onglets restent sombres** : le logo a un lettrage blanc, interdit sur fond clair par la charte.
- **Valeurs dérivées, absentes de la charte** (assombries pour tenir le contraste 4,5:1 sur fond clair) : orange de texte `#9A4C07`, gris de texte `#565C75`, chiffres clés `#B8600D` et `#1B7F84`. À faire valider par l'organisateur.
- Implémentation : variables CSS surchargées sous `:root[data-theme="day"]` en tête de `index.html`.

Les trois visuels de `assets/` ont été **extraits du PDF de la charte** : le logo est en 600 px (flou à grande taille).
Demander à l'organisateur le logo en **SVG/PNG haute définition**, la carte et la bande en vectoriel.

## Ce qui est volontairement factice

- Participants, billet, QR code, paiement : **données fictives**, rien n'est envoyé ni stocké.
- Les boutons marqués « Maquette — … » indiquent une action à brancher (calendrier .ics, WhatsApp, formulaire de candidature, upload photo, PDF).
- Photos des intervenants et logos des partenaires : non copiés (avatars à initiales). Les droits appartiennent à l'organisateur.

## Points à trancher avec l'organisateur

- **Adresse du secrétariat** : le site indique « Rue Félicia Hôtel, Coron… », la charte « Rond-point Cami-Toyota, Coron… ». La maquette suit la charte.
- **Téléphones** : la charte autorise 3 numéros (dont +237 222 306 079, absent du site).
- **Intervenants visés** : « 80+ » (page 5 de la charte) contre « 40+ » (page 7 et site). La maquette n'affiche pas ce chiffre.
- **Domaine** : jciacm.com ou jcia.cm (ouvert dans la charte, page 10).
- **Offre −30 %** : fin au 31 décembre 2026, à confirmer.

## Pistes pour la vraie app (à valider par l'équipe)

- Données (programme, intervenants, billets) à servir par une API, pas en dur dans le JS.
- Paiement (Mobile Money / Stripe, via le prestataire existant) et QR code à générer côté serveur.
- Liste des participants : afficher uniquement les personnes ayant donné leur consentement ; ne jamais exposer e-mail ni WhatsApp.
- Sections manquantes dans la maquette : espace connecté, matchmaking B2B/B2G, vote du public des Awards, notifications, plan du Salon (annoncés sur le site comme « app événement »).

## Limites du relevé

Réalisé le 2026-11-02 à partir des pages publiques. Le programme du jour 2 est reconstitué à partir de ce qui est publié ;
l'onglet « Participants » du site et les pages légales n'ont pas pu être lus.
