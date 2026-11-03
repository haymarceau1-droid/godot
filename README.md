# Godot & Fils Chartres — refonte du site

Site vitrine statique (HTML/CSS/JS, sans dépendance) pour l'agence Godot & Fils de Chartres,
en remplacement de https://www.godotetfils-chartres.fr/.

Design system : voir [`DESIGN.md`](DESIGN.md) (canvas noir, surfaces blanches, or `#d49732`, CTA bleu `#0071e3`, Josefin Sans, rayon 5px, aplats).

## Contenu
- `index.html` — page unique : accueil, services, étapes d'estimation, la maison, FAQ, agence (horaires, carte)
- `mentions-legales.html` — mentions légales (champs à compléter)
- `assets/css/style.css`, `assets/js/main.js`, `assets/img/`

Fonctionnalités : design responsive (menu mobile, bouton d'appel flottant), indicateur
« ouvert / fermé » calculé à l'heure de Paris, jour courant surligné dans les horaires,
données structurées schema.org (SEO local), animations respectant `prefers-reduced-motion`.

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
