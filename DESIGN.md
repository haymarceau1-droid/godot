# Design System — Godot & Fils Chartres

Système de référence appliqué au site (`assets/css/style.css`). Les tokens proviennent de
l'extraction du site d'origine ; les sections d'analyse en décrivent l'usage.

## 1. Visual Theme & Atmosphere

Une vitrine de joaillier, la nuit : un **canvas noir** qui joue le rôle de l'écrin de velours,
sur lequel l'**or (`#d49732`)** est la seule couleur chaude — il désigne ce qui a de la valeur
(chiffres clés, labels, numéros d'étape, année de fondation). Les **surfaces blanches**
alternent avec le noir pour donner du rythme et de la lisibilité aux contenus longs
(services, la maison, agence). Le ton est sobre, rassurant, patrimonial — une maison de 1933 —
sans ostentation : pas de dégradés, pas d'effets brillants, l'or est un aplat.

Métaphores : écrin (noir), métal (or), confiance institutionnelle (noir profond `#111111`),
action claire (boutons or pleins, texte noir).

## 2. Color Palette & Roles

### Primary
- **Canvas Background** `#000000` — fond de page, en-tête, hero, étapes, pied de page
- **Secondary Surface** `#ffffff` — sections de contenu, cartes, carte agence

### Accent & Interactive
- **Primary Accent** `#d49732` — boutons principaux (texte noir), bouton d'appel flottant,
  soulignement des liens d'action, focus. *Aucun bleu n'est utilisé sur le site.*

### Text & Neutrals
- **Text Tier 1** `#ffffff` — texte sur fond noir / noir profond
- **Text Tier 2** `#000000` — texte sur fond blanc
- **Text Tier 3** `#d49732` — or : labels (eyebrows), chiffres, numéros, icônes, survols de nav
- **Text Tier 4** `#111111` — noir profond (remplace le noir profond `#111111`) : titres sur fond blanc, bandeau infos, section FAQ

Les variantes « muted » sont des opacités de ces tokens (72 % blanc, 72 % noir),
jamais de nouvelles teintes.

## 3. Typography Rules

| Rôle | Police | Taille | Graisse | Interligne |
|---|---|---|---|---|
| Hero (h1) | Josefin Sans | 67px | 400 | 1 (67px) |
| Chiffres clés / numéros d'étape | Josefin Sans | 47px | 400 | 1 (47px) |
| Titre de section (h2) | Josefin Sans | 38px | 700 | 1.45 (55px) |
| Titre de carte (h3), questions FAQ | Josefin Sans | 19.2px | 700 | 1.3 |
| Corps | Josefin Sans | 16px | 400 | 24px |
| Corps secondaire (cartes, pied) | Josefin Sans | 14px | 400 | 21px |
| Liens utilitaires (pied de page) | Montserrat | 13px | 400 | normal |
| Labels / eyebrows | Josefin Sans | 12px | 700 | normal |

- Les grandes tailles (hero, chiffres) sont en **graisse 400** : élégance par la taille,
  pas par le poids. Les titres de section et de carte passent en **700**.
- **Capitales + interlettrage large** (0.16–0.22em) pour les labels, la navigation et les
  intitulés de pied de page ; jamais pour le corps de texte.
- Josefin Sans a une ligne de base haute : compenser de 2–4px en haut dans les pastilles.

## 4. Component Stylings

- **Rayon `5px`** pour cartes, encadrés, carte, FAQ. **Boutons, pastilles de villes et badges
  entièrement arrondis (pilule, `999px`)**. Éléments circulaires : badge 1933, bouton d'appel flottant.
- **Bouton principal** : fond or `#d49732`, texte noir 700, hauteur ≥ 48px, padding 0.85em 1.6em.
- **Bouton secondaire** : contour 2px blanc (sur noir) ou noir (sur blanc), inversion au survol.
- **Carte** : fond blanc, bordure 1px noir à 14 %, padding 32px ; au survol la bordure
  passe à l'or. Icône dans une pastille noire 52px, trait or.
- **Carte accent** : fond noir, titre or, lien souligné or.
- **Encadré « À prévoir »** : bordure 1px or, fond transparent.
- **FAQ** : `details` sur fond noir, bordure 1px blanc à 14 %, bordure or quand ouvert, « + » or.

## 5. Layout Principles

- Conteneur max **1170px**, gouttière latérale **16px** minimum ; texte long limité à 820px.
- Grilles : 3 colonnes (services), 4 (étapes, bandeau infos), 2 asymétriques (la maison,
  agence : 0.9fr / 1.1fr).
- Espacement **aéré** : 64–96px de padding vertical par section, 20px entre cartes.
- Alternance des fonds : noir (hero) → noir profond (bandeau) → blanc (services) → noir (étapes)
  → blanc (maison) → noir profond (FAQ) → blanc (agence) → noir (pied).

## 6. Depth & Elevation

| Niveau | Traitement | Usage |
|---|---|---|
| 0 | Aplat | Toutes les surfaces |
| 1 | Bordure 1px (14 % d'opacité) | Cartes, FAQ, étapes |
| 2 | Bordure or | Survol / état ouvert |

**Aucune ombre portée, aucun dégradé.** La profondeur vient uniquement du contraste
noir / blanc et des bordures.

## 7. Do's and Don'ts

- **Do** réserver les boutons or pleins (texte noir) aux actions principales.
- **Do** utiliser l'or pour signaler la valeur : labels, chiffres, icônes — et en fond des seuls boutons d'action.
- **Do** écrire labels et navigation en capitales interlettrées.
- **Don't** utiliser de bleu, d'ombres, ni de dégradés (sauf le voile horizontal du hero photo) ; rayons : 5px (blocs) ou pilule (boutons).
- **Don't** introduire de nouvelles teintes : les nuances sont des opacités des tokens.

## 8. Responsive Behavior

- **≥ 1025px** : grilles complètes, visuel lingots/pièces dans le hero.
- **≤ 1024px** : services et étapes en 2 colonnes, bandeau infos 2×2, visuel du hero masqué.
- **≤ 860px** : menu burger (panneau noir plein largeur), sections en 1 colonne, bouton
  d'appel flottant or 56px en bas à droite.
- **≤ 560px** : tout en 1 colonne, boutons du hero pleine largeur.
- Cibles tactiles ≥ 48px (boutons, liens de menu mobile, bouton d'appel).

## 9. Agent Prompt Guide

### Reference Tokens
- **Primary CTA** `#d49732` (texte `#000000`) · **Canvas** `#000000` · **Surface** `#ffffff`
- **Text** `#ffffff` / `#000000` · **Gold** `#d49732` · **Noir profond** `#111111`
- **Font** Josefin Sans (400/700), Montserrat 13px pour liens utilitaires · **Radius** 5px

### Exemples de prompts
1. « Crée une section "Cours de l'or" sur fond noir `#000000` : label en capitales or `#d49732`
   12px interlettré 0.2em, titre Josefin Sans 38px 700 blanc, trois cartes blanches à bordure
   1px `rgba(0,0,0,.14)` et rayon 5px affichant un prix en Josefin Sans 47px 400 or. Pas
   d'ombre ni de dégradé. »
2. « Génère un formulaire de prise de contact sur surface blanche : libellés en capitales or
   12px, champs bordés 1px noir profond `#111111` à 14 %, rayon 5px, hauteur 48px, focus contour
   2px or `#d49732` ; bouton d'envoi plein or `#d49732` texte noir 700. »
3. « Ajoute un bandeau d'avis clients sur fond noir profond `#111111` : citations en Josefin Sans
   19.2px 400 blanc, nom du client en capitales or 12px, séparateurs 1px blanc à 14 %, grille
   3 colonnes repliée en 1 colonne sous 860px. »
