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
| Accueil | Hero, compte à rebours, **4 raccourcis**, à propos, chiffres animés, défis, parcours, communauté |
| Programme | Jour 1 / Jour 2 / **Mon programme** (étoile par session, détection des chevauchements, rappels), masterclasses |
| Intervenants | Liste + recherche |
| Billets | 5 billets → inscription en 4 étapes → **attente de paiement** → billet (QR fictif) + visuel « I'll be there » |
| Plus | **Mon programme, Rencontres B2B/B2G, Plan du Salon, Vote des Awards, Notifications**, puis Salon 100 % IA, Awards, Annuaire, Participants, Partenaires, FAQ, Contact ; choix Nuit / Jour ; réinitialisation de la démo |

Les cinq écrans en gras correspondent aux fonctions que le site annonce pour l'« app événement » : programme personnalisé, matchmaking B2B/B2G, notifications, plans du Salon, plus le vote du public des Awards.

## Version 2 : finitions et écrans ajoutés

- **Icônes** : SVG en ligne (`ICONS` dans `index.html`, trait 1,8 px, couleur héritée) à la place des emojis.
- **Animations** : apparition en cascade des écrans, retour tactile sur les boutons, feuille du bas (« bottom sheet »), squelettes de chargement (Annuaire, Participants), écran d'attente de paiement, chiffres clés animés, point pulsant « vous êtes ici » sur le plan. Tout est désactivé si l'utilisateur règle « réduire les animations » (`prefers-reduced-motion`).
- **Accessibilité** : interrupteurs `role="switch"`, feuilles `role="dialog"` avec piège de focus et fermeture par Échap, zones du plan utilisables au clavier (Entrée/Espace) avec liste alternative, texte « Non lue » pour lecteurs d'écran.
- **Données locales** : favoris, votes, demandes de rendez-vous, notifications et préférences sont mémorisés dans le navigateur (clé `jcia-mock-v2`). Plus → « Réinitialiser les données de démonstration » remet tout à zéro.
- **Correctif** : en version Nuit, le logo de la version Jour s'affichait aussi (ordre de règles CSS).

### Hypothèses de la maquette à faire valider

| Sujet | Hypothèse prise | À confirmer |
|---|---|---|
| Vote du public | Un vote par catégorie, modifiable jusqu'au 15 avril ; 5 finalistes fictifs par catégorie | Règles officielles, authentification (billet ? e-mail ?), anti-fraude |
| Rendez-vous B2B/B2G | Créneaux de 20 min le mardi 27, 15:00–18:00 (plage « rencontres » du programme) ; confirmation simulée après 3,5 s | Créneaux du mercredi, qui confirme, lieu exact, billets concernés |
| Compatibilité (%) | Valeur fictive | Algorithme de recommandation, ou on l'enlève |
| Plan du Salon | Plan **fictif** ; zones reprises des espaces cités sur le site | Plan officiel du Hilton |
| Rappels | 15 minutes avant chaque session | Délai souhaité |
| Notifications | 5 types (sessions, rendez-vous, annonces, vote, billet) | Liste réelle, fréquence, textes |
| Durée d'une session sans heure de fin | 45 min (sert à détecter les chevauchements) | Horaires exacts du programme |

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

Modelée sur la version claire observée sur <https://jciacm.com/> (le site suit le réglage du système : `color-scheme: light dark`) et sur la palette « Jour » de la charte.

- **Bascule** : bouton ☀️/🌙 en haut à droite, ou Plus → Apparence. Par défaut, la maquette suit le réglage du téléphone. Lien direct : `index.html?theme=day`. Le choix est mémorisé.
- **Ce qui change** : fond crème `#FBF6EE` avec motif toghu discret, cartes blanches à ombre douce, en-tête clair avec logo à **lettrage sombre**, bande toghu conservée, bouton secondaire gris clair, petits titres en terracotta précédés de trois losanges.
- **Valeurs dérivées, absentes de la charte** (assombries pour le contraste sur fond clair) : terracotta de texte `#B8502A`, dégradé des titres `#D2700F → #B8502A`, gris de texte `#5C617C`, chiffres clés `#D2700F` et `#1B7F84`. À faire valider.
- **Logo jour** (`assets/logo-jcia-jour.png`) : **version provisoire** fabriquée en recolorant le logo de la charte (lettrage blanc → encre). Le site utilise un vrai logo à lettrage sombre : demander le fichier officiel (SVG/PNG).
- La carte du Cameroun reste dans son cadre sombre arrondi (comme dans la charte) : sa version à fond transparent n'est pas disponible.
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
- Notifications : vrais envois push (APNs / FCM) et autorisation demandée au premier lancement ; ici les notifications sont simulées.
- Rendez-vous B2B/B2G et vote : à brancher sur un serveur (authentification, quotas, anti-doublons) ; ici tout est local au navigateur.
- Encore absents de la maquette : espace connecté (compte, connexion), « I'll be there » avec photo réelle et recadrage, version anglaise complète, mode hors-ligne.

## Limites du relevé

Réalisé le 2026-11-02 à partir des pages publiques. Le programme du jour 2 est reconstitué à partir de ce qui est publié ;
l'onglet « Participants » du site et les pages légales n'ont pas pu être lus.
