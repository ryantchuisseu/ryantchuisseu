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

## Expérience « wouah » (utile, sans manipulation)

| Fonction | Ce qu'elle apporte | Où |
|---|---|---|
| **Billet 3D** | S'incline au doigt ou en penchant le téléphone, reflet lumineux ; **mode scan** (QR plein écran, écran maintenu allumé) | Billet |
| **Visuel « Je serai là »** | Photo (recadrage au doigt + zoom), nom, rôle, couleur du billet ; **partage** natif ou téléchargement PNG 1080×1350. La photo ne quitte pas le téléphone | Billet → Créer mon visuel |
| **Mode « En direct »** | Le jour J, l'accueil montre la session en cours (barre d'avancement), la suivante et un bouton **« M'y emmener »** vers la salle sur le plan ; « En cours » dans le programme | Accueil, Programme |
| **Préparation** | Checklist de 4 étapes avec anneau de progression ; elle **se termine**, est célébrée une fois, puis disparaît | Accueil |
| **Personnalisation** | 4e étape d'accueil : profil + 4 thèmes → cartes « Pour vous », badges dans le programme, rencontres classées par thème | Accueil, Explorer → Mes thèmes |
| **Calendrier** | Vrais fichiers `.ics` (favoris ou événement), fuseau de Yaoundé | Programme, Billet |
| **Recherche** | Sessions, intervenants, questions, en direct | Loupe en haut |
| **Retours sensoriels** | Confettis aux réussites, étincelles sur les favoris, bulle « gélatine », vibrations (désactivables), sons (désactivés par défaut) | Partout · Explorer |

**Mode démonstration** (Explorer) : simule « mardi 12:10 » ou « mercredi 15:05 » pour montrer le mode direct avant l'événement.

**Choix éthiques assumés** : pas de récompense aléatoire, pas de série à perdre, pas de classement public, pas de pression pour revenir. La préparation est finie, les sons sont désactivés par défaut, et tout effet de mouvement est coupé si l'utilisateur réduit les animations.

**Limites** : l'export du visuel ne fonctionne pas depuis `index.html` ouvert en local (sécurité du navigateur) : utiliser les fichiers de `dist/` ou un petit serveur. Le partage natif dépend du téléphone (sinon, téléchargement). L'inclinaison au gyroscope demande une autorisation sur iPhone (au premier toucher du billet).

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
