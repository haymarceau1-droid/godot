# Godot & Fils Chartres — refonte du site

Site vitrine statique (HTML/CSS/JS, sans dépendance) pour l'agence Godot & Fils de Chartres,
en remplacement de https://www.godotetfils-chartres.fr/.

Design system : voir [`DESIGN.md`](DESIGN.md) (canvas noir, surfaces blanches, or `#e2ab45`, CTA or, Josefin Sans, rayon 5px, aplats).

## Pages
| Fichier | Contenu |
|---|---|
| `index.html` | Accueil : services, étapes, la maison, FAQ |
| `vendre-or.html` | Rachat d'or : objets acceptés, calcul du prix, titres de l'or |
| `acheter-or.html` | Or d'investissement : pièces, lingots, fiches des références |
| `numismatique.html` | Pièces de collection : ce qui fait la valeur, grades, conservation |
| `argent-bijoux.html` | Argent, platine et bijoux |
| `change.html` | Bureau de change |
| `la-maison.html` | Histoire et engagements (depuis 1933) |
| `faq.html` | Questions fréquentes (données structurées FAQPage) |
| `contact.html` | Adresse, horaires, statut ouvert/fermé, carte |
| `mentions-legales.html` | Mentions légales (champs à compléter) |

Les pages sont **générées** par `tools/build.py` (en-tête, pied de page, navigation, SEO communs).
Pour modifier un texte ou ajouter une page : éditer `tools/build.py`, puis lancer
```bash
python3 tools/build.py
```
`sitemap.xml` et `robots.txt` sont régénérés au passage. Styles : `assets/css/style.css`, script : `assets/js/main.js`.

Fonctionnalités : responsive (méga menu « Nos services » sur ordinateur, panneau plein écran sous 1220px, bouton d'appel flottant), indicateur « ouvert / fermé » à l'heure de Paris,
données structurées schema.org, animations respectant `prefers-reduced-motion`.

## Avis Google (accueil)
La section est alimentée par `tools/avis.json` (format dans `tools/avis.exemple.json`) : prénom/nom, note, date et texte **réels** copiés depuis Google. Tant que `avis` est vide, rien ne s'affiche. Après modification : `python3 tools/build.py`. Ne jamais inventer d'avis.

## Frise « Notre histoire »
Les dates de la page « La maison » sont dans `TIMELINE` (`tools/build.py`). Elles viennent de sources publiques : à valider avec l'agence (1933, 2017, 2020).

## Cookies et vie privée
Le site n'utilise aucun cookie de suivi et héberge sa police (`assets/fonts/`). Seul le plan Google Maps de la page Contact est soumis à consentement : bannière dans `assets/js/consent.js`, choix mémorisé 6 mois dans le navigateur, réouvrable via « Gérer les cookies » en bas de page.

## Animations
Apparitions au défilement, barre de progression, bandeau défilant, carte animée : `assets/js/main.js` + fin de `assets/css/style.css`. Tout est désactivé si l'utilisateur a demandé « réduire les animations ».

## Icônes
[Tabler Icons](https://tabler.io/icons) (licence MIT, copiée dans `assets/icons/LICENSE-tabler-icons.txt`). Pour en ajouter une : copier le SVG dans `assets/icons/` puis écrire `[[icon:nom-du-fichier]]` dans `tools/build.py`.

## Photo du hero
Le hero de l'accueil attend la photo de la devanture dans `assets/img/devanture.webp` (ou `devanture.jpg`), recouverte d'un dégradé horizontal plus foncé côté texte. Sans fichier, le hero reste noir.

## Carte des agences
La carte de la page « La maison » est générée depuis `tools/geo/agences.json` (liste des villes, coordonnées, adresses) :
```bash
cd tools/geo && npm install && node make-map.mjs && cd ../.. && python3 tools/build.py
```

## Aperçu local
```bash
python3 -m http.server 8000
```
puis ouvrir http://localhost:8000

## À valider / compléter
- Horaires : lundi–vendredi 9h30–18h00 (samedi indiqué fermé — à confirmer)
- Adresse e-mail de l'agence (non affichée pour l'instant)
- Logo officiel et photos réelles de l'agence (le « G » doré est provisoire)
- Liste exacte des pièces et lingots proposés, devises disponibles au change
- Mentions légales : raison sociale, SIRET, hébergeur, directeur de la publication
