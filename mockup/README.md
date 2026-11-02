# JCIA 2027 — Maquette de l'application mobile

Maquette cliquable de l'app compagnon du site <https://jciacm.com/>.
Elle reproduit les pages et parcours **visibles publiquement** sur le site. Elle ne contient
aucun code, aucune clé et aucune donnée privée du site d'origine.

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
| Plus | Salon 100 % IA, Awards, Annuaire, Participants, Partenaires, FAQ, Contact |

## Ce qui est volontairement factice

- Participants, billet, QR code, paiement : **données fictives**, rien n'est envoyé ni stocké.
- Les boutons marqués « Maquette — … » indiquent une action à brancher (calendrier .ics, WhatsApp, formulaire de candidature, upload photo, PDF).
- Les photos et logos du site ne sont pas copiés (avatars à initiales). Les droits des visuels appartiennent à l'organisateur.

## Pistes pour la vraie app (à valider par l'équipe)

- Données (programme, intervenants, billets) à servir par une API, pas en dur dans le JS.
- Paiement (Mobile Money / Stripe, via le prestataire existant) et QR code à générer côté serveur.
- Liste des participants : afficher uniquement les personnes ayant donné leur consentement ; ne jamais exposer e-mail ni WhatsApp.
- Sections manquantes dans la maquette : espace connecté, matchmaking B2B/B2G, vote du public des Awards, notifications, plan du Salon (annoncés sur le site comme « app événement »).

## Limites du relevé

Réalisé le 2026-11-02 à partir des pages publiques. Le programme du jour 2 est reconstitué à partir de ce qui est publié ;
l'onglet « Participants » du site et les pages légales n'ont pas pu être lus.
