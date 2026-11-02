# JCIA 2027 — Maquette minimaliste (2 variantes d'icônes)

Version épurée de l'app compagnon, pensée pour être **comprise au premier coup d'œil** : peu d'écrans, un seul bouton principal par écran,
de grands titres, des gestes simples. La maquette complète précédente reste disponible dans `../index.html`.

| Fichier | Contenu |
|---|---|
| `dist/jcia-minimal-3d.html` | **Icônes 3D** (autonome : s'ouvre d'un double-clic) |
| `dist/jcia-minimal-flat.html` | **Icônes plates** à traits (autonome) |
| `index.html` + `style.css` + `app.js` | Code source lisible, même code pour les deux variantes (`?icons=3d` ou `?icons=flat`) |
| `build.py` | Régénère les deux fichiers de `dist/` : `python3 build.py` |

## Principes de conception

- **Navigation à bulle** (inspirée de votre référence) : l'onglet actif sort de la barre dans une bulle en relief, qui glisse d'un onglet à l'autre. 5 onglets : Accueil, Programme, Billet, Rencontres, Explorer.
- **Écrans d'accueil en 3 étapes** (inspirés de votre seconde référence) : grand visuel coloré, gros titre, une phrase, un bouton, des pastilles d'étape. Rejouable avec `?onboarding=1`.
- **Un seul bouton plein par écran** (charte), libellés simples, vouvoiement, pas de jargon.
- **Accueil réduit à l'essentiel** : compte à rebours, un bouton, 4 accès rapides, une actualité.
- **Billet en 3 étapes** (choisir → informations → payer) avec barre de progression, puis un billet lisible avec QR.
- Nuit / Jour / Auto (suit le téléphone), animations coupées si « réduire les animations », navigation au clavier, feuilles à piège de focus.

## Les deux variantes d'icônes

- **3D** : [Fluent Emoji 3D](https://github.com/microsoft/fluentui-emoji) de Microsoft, **licence MIT** (fichier `assets/3d/LICENSE-fluentui-emoji.txt`). 37 icônes en 160 px. Ce sont des emojis 3D : leur style est celui de Microsoft, pas une identité JCIA sur mesure.
- **Plat** : icônes à traits dessinées dans le code (`FLAT` dans `app.js`).
- Pour une identité 3D propre à la JCIA : faire dessiner un jeu d'icônes sur mesure et remplacer les PNG de `assets/3d/` (mêmes noms de fichiers).

## Ce qui est repris de la maquette complète, et ce qui est laissé de côté

Repris : programme avec favoris et détection des chevauchements, billetterie et paiement simulé, rencontres B2B/B2G, plan indicatif du Salon, Awards et vote (aperçu), intervenants, FAQ, contact, notifications.
Laissés de côté pour rester minimaliste : page Salon, Annuaire national, Participants, Partenaires & sponsors (contenu surtout destiné aux exposants et sponsors).

## À savoir

- Données **fictives** : profils des rencontres, billet, QR, plan du Salon (le plan officiel du Hilton n'est pas publié), finalistes du vote. Rien n'est envoyé : tout reste dans le navigateur (clé `jcia-min-v1`). Explorer → « Réinitialiser la démonstration ».
- Mêmes hypothèses à valider que la maquette complète (règles du vote, créneaux B2B, délais de rappel) : voir `../README.md`.
- Police Sora chargée depuis Google Fonts : à héberger soi-même en production.
- Le logo de la version Jour est une recoloration provisoire du logo de la charte : demander le fichier officiel.
