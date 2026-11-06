# Assistant JCIA : fonctionnalités

Version 1.0, 06/11/2026. Même contenu que le PDF `docs/Assistant-JCIA-maquette-fonctionnalites.pdf`.

Statuts : **Prête** (construite et testée), **Prête, à valider** (à vérifier avec la clé API), **À décider / À fournir** (choix de l'organisateur), **V2** (plus tard).


## Interface

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F01 | Lanceur mascotte | Le chat démarre replié en mascotte, en bas à droite du site, avec « Besoin d’aide ? ». Il peut aussi s’ouvrir au chargement (option). | Prête |
| F02 | En-tête complet | Nom, avatar, statut en ligne, bascule FR/EN, boutons Rafraîchir et Réduire. | Prête |
| F03 | Accueil automatique | Message de bienvenue et séparateur avec la date du jour à chaque ouverture ou rafraîchissement. | Prête |
| F04 | Réponses rapides et suggestion | Trois boutons (Dates et lieu, Devenir partenaire, Contact) et une suggestion (Intervenants), tirés de la FAQ. Modifiables sans toucher au code. | Prête |
| F05 | Bulles et avatars | Bot à gauche (fond sombre, avatar mascotte), visiteur à droite (violet, avatar personne). Défilement automatique vers le dernier message. | Prête |
| F06 | Indicateur « écrit… » | Trois points animés avant chaque réponse du bot. | Prête |
| F07 | Saisie, émojis, envoi | Champ de 600 caractères max, envoi par la touche Entrée ou le bouton avion (seul bouton plein), choix de 12 émojis. | Prête |
| F08 | Cartes d’information | Cartes à filet coloré : dates et lieu, les 4 enjeux, contacts officiels. | Prête |
| F09 | Liens officiels | « En savoir plus » vers la Billetterie, le dossier de sponsoring ou la page Intervenants. Les adresses web dans les réponses sont cliquables. | Prête |
| F10 | Étiquette de source | Sous chaque réponse : FAQ officielle, Réponse IA basée sur la FAQ, ou Contact officiel. | Prête |
| F11 | Rappel de sécurité | Sous la saisie : « Ne partagez jamais de code PIN ni de mot de passe dans ce chat. » | Prête |
| F12 | Rafraîchir et réduire | Rafraîchir efface la conversation. Réduire replie le chat en mascotte ; la touche Échap fait de même. | Prête |

## Réponses

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F13 | FAQ sans IA (couche 1) | 16 questions officielles de jciacm.com/faq, plus Contact et Intervenants, en FR et EN, reprises mot pour mot. Gratuit et instantané. | Prête |
| F14 | Règles locales | Remerciements et messages incompréhensibles traités dans le navigateur, sans appel à l’IA. | Prête |
| F15 | Questions libres par IA (couche 2) | Claude Haiku 5.5 répond en 1 à 4 phrases, à partir de trois sources : FAQ, informations du site (programme, billets, CAIA, annuaire…) et offre de sponsoring. | Prête, à valider |
| F16 | Mémoire de conversation | Le bot tient compte des 8 derniers messages, tant que la page reste ouverte. Rien n’est conservé ensuite. | Prête |
| F17 | Repli humain (couche 3) | Pas d’information, erreur technique ou trop de questions : message clair et carte de contact du secrétariat. | Prête |
| F18 | Bilingue FR / EN | Interface et réponses en français par défaut, anglais en miroir. Le bot répond dans la langue du visiteur. | Prête |

## Mascotte

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F19 | Humeurs réactives | 5 humeurs liées à la situation (tableau page 6), avec une bulle de texte. | Prête |
| F20 | Animations | Saut, hochement, balancement, rebond, ombre au sol. Un clic sur la mascotte la fait réagir. | Prête |
| F21 | Animations réduites | Respect du réglage système « réduire les animations ». | Prête |

## Sécurité et fiabilité

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F22 | Garde-fous de la charte | Pas de sujet de conférence non annoncé, pas de places garanties (billets et sponsoring), pas de promesse d’invitation au gala, jamais de demande de code PIN, de mot de passe ou de données bancaires. Chiffres toujours « attendus ». Recentrage si hors sujet. Refus des tentatives de détournement. | Prête, à valider |
| F23 | Clé API protégée | La clé reste sur le serveur Cloudflare (secret chiffré), jamais dans le site ni dans le navigateur. | Prête |
| F24 | Anti-abus | 20 questions IA maximum par visiteur toutes les 10 minutes. Seuls les sites autorisés (jciacm.com, jcia.cm) peuvent appeler le serveur. | Prête |
| F25 | Statistiques anonymes | Pour chaque réponse IA : langue, type de réponse, jetons utilisés. Aucun contenu ni donnée personnelle. Consultable dans Cloudflare. | Prête |

## Intégration et mise à jour

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F26 | Intégration en une ligne | Une balise script à ajouter au site. Le widget est isolé : son style ne touche pas au site, et inversement. | Prête |
| F27 | Mise à jour du contenu | Modifier 3 fichiers texte (FAQ, infos, sponsoring) puis redéployer : boutons et réponses IA se mettent à jour ensemble. | Prête |
| F28 | Plan B sans le prestataire | Le chatbot peut vivre sur une page à part, reliée au site par un lien « Une question ? ». | Prête |

## À décider ou pour plus tard

| N° | Fonctionnalité | Description | Statut |
|---|---|---|---|
| F29 | Lecture des 2 PDF du site | Dossier de sponsoring et termes de référence CAIA : à fournir pour compléter les sources. | À fournir |
| F30 | Pièces jointes | Bouton retiré de la version réelle : un bouton sans effet donne l’impression d’un bug. À réactiver si un vrai besoin apparaît. | À décider |
| F31 | Formulaire de contact dans le chat | Nom, e-mail, message envoyés au secrétariat sans quitter le chat. | À décider |
| F32 | Historique après la session | Non recommandé tant que la protection des données n’est pas validée par l’organisateur. | À décider |
| F33 | Mascotte identique au site | Reprendre le fichier source de la mascotte déjà utilisée sur jciacm.com. | À fournir |
| F34 | Voix | Écoute et lecture à voix haute (voix du navigateur, puis voix payante si besoin), bouche animée de la mascotte. | V2 |
| F35 | Interactions « glisser » | Tirer pour rafraîchir avec le bras de la mascotte ; glisser une carte (billet, formule) pour l’activer, avec confettis. | V2 |
