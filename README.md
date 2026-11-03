# Godot & Fils Chartres — refonte du site

Site vitrine statique (HTML/CSS/JS, sans dépendance) pour l'agence Godot & Fils de Chartres,
en remplacement de https://www.godotetfils-chartres.fr/.

Design system : voir [`DESIGN.md`](DESIGN.md) (canvas noir, surfaces blanches, or `#d49732`, CTA or, Josefin Sans, rayon 5px, aplats).

## Pages
| Fichier | Contenu |
|---|---|
| `index.html` | Accueil : services, étapes, la maison, FAQ |
| `vendre-or.html` | Rachat d'or : objets acceptés, calcul du prix, titres de l'or |
| `acheter-or.html` | Or d'investissement : pièces, lingots, tableau des références |
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

Fonctionnalités : responsive (menu burger sous 1100px, bouton d'appel flottant), indicateur « ouvert / fermé » à l'heure de Paris,
données structurées schema.org, animations respectant `prefers-reduced-motion`.

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
