#!/usr/bin/env python3
"""Génère les pages statiques du site (python3 tools/build.py).
Édite le contenu ici, puis relance le script : en-tête, pied de page et navigation restent cohérents."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.godotetfils-chartres.fr"
TEL, TEL_HREF = "02 37 83 49 77", "+33237834977"

NAV = [
    ("vendre-or.html", "Vendre mon or"),
    ("acheter-or.html", "Acheter de l'or"),
    ("argent-bijoux.html", "Argent &amp; bijoux"),
    ("change.html", "Change"),
    ("la-maison.html", "La maison"),
    ("contact.html", "Contact"),
]

LD_STORE = {
    "@context": "https://schema.org", "@type": "JewelryStore",
    "name": "Godot & Fils Chartres",
    "description": "Achat et vente d'or, d'argent, de pièces, de lingots et de bijoux. Bureau de change.",
    "url": SITE + "/", "telephone": TEL_HREF, "foundingDate": "1933",
    "logo": SITE + "/assets/img/logo-noir.png",
    "address": {"@type": "PostalAddress", "streetAddress": "23 rue de la Pie", "postalCode": "28000",
                "addressLocality": "Chartres", "addressCountry": "FR"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:30", "closes": "18:00"}],
}

FAQ = [
    ("Avant de venir", [
        ("Faut-il prendre rendez-vous ?", "Non. Vous pouvez venir à l'agence sans rendez-vous, du lundi au vendredi de 9h30 à 18h00. Pour un lot important, un appel au 02 37 83 49 77 nous permet de mieux vous recevoir."),
        ("L'estimation est-elle vraiment gratuite ?", "Oui. L'estimation et les conseils sont gratuits et sans engagement : vous êtes libre d'accepter ou non notre offre."),
        ("Quels documents dois-je apporter ?", "Une pièce d'identité en cours de validité, obligatoire pour toute vente de métaux précieux. Pour les pièces et lingots, apportez aussi les factures ou certificats d'achat si vous en avez : ils peuvent avoir une incidence sur la fiscalité applicable."),
    ]),
    ("Vendre", [
        ("Comment est calculé le prix de rachat ?", "Le prix dépend du poids, du titre (pureté) du métal et du cours de l'or ou de l'argent au jour de la transaction. Pour certaines pièces de collection, la valeur numismatique peut également être prise en compte."),
        ("Rachetez-vous l'or cassé ou abîmé ?", "Oui. Bijoux cassés, chaînes emmêlées, boucles d'oreilles orphelines, or dentaire : tout est estimé selon sa teneur en métal précieux."),
        ("Que se passe-t-il si je refuse l'offre ?", "Rien : vous repartez avec vos objets, sans frais. L'estimation est faite devant vous, la décision vous appartient."),
        ("Mes bijoux sont-ils fondus ?", "Les bijoux rachetés pour leur métal sont généralement destinés au recyclage. Si vous souhaitez conserver une pièce de valeur, dites-le lors de l'estimation."),
    ]),
    ("Acheter", [
        ("Puis-je acheter de l'or pour investir ?", "Oui. Nous proposons des pièces et des lingots d'investissement. Contactez l'agence pour connaître les disponibilités et les tarifs du moment."),
        ("Les prix changent-ils dans la journée ?", "Oui. Les prix de l'or et de l'argent suivent les marchés : le tarif applicable est celui du moment de la transaction."),
        ("Quelle différence entre une pièce et un lingot ?", "Les pièces sont facilement divisibles et reconnues sur le marché ; les lingots, plus massifs, portent généralement une prime plus faible par gramme. Nous vous aidons à choisir selon votre projet."),
    ]),
    ("Change", [
        ("Puis-je changer des devises à l'agence ?", "Oui, l'agence est aussi bureau de change. Les devises disponibles varient : appelez-nous avant de venir pour confirmer celle dont vous avez besoin."),
    ]),
]

def esc_json(o): return json.dumps(o, ensure_ascii=False, indent=2)

def header(active):
    links = "\n".join(
        f'        <a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''  <a class="skip" href="#contenu">Aller au contenu</a>
  <header class="site-header" id="haut">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Godot &amp; Fils Chartres, accueil">
        <img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils, depuis 1933">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
      <nav id="nav" class="nav" aria-label="Navigation principale">
{links}
        <a class="btn btn-gold btn-sm" href="tel:{TEL_HREF}">{TEL}</a>
      </nav>
    </div>
  </header>'''

def cta_band():
    return f'''    <section class="cta-band">
      <div class="container cta-inner">
        <div>
          <h2>Estimation gratuite, sans rendez-vous.</h2>
          <p>Passez nous voir au 23 rue de la Pie, du lundi au vendredi de 9h30 à 18h00.</p>
        </div>
        <div class="cta-actions">
          <a class="btn btn-dark" href="contact.html">Venir à l'agence</a>
          <a class="btn btn-outline" href="tel:{TEL_HREF}">{TEL}</a>
        </div>
      </div>
    </section>'''

def footer():
    svc = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in NAV[:4])
    return f'''  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <a class="brand brand-footer" href="index.html">
          <img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils, depuis 1933">
        </a>
        <p>Achat et vente d'or, d'argent et de métaux précieux. Bureau de change.</p>
      </div>
      <div>
        <h3>Agence</h3>
        <ul class="foot-lines">
          <li>[[icon:map-pin]]<span>23 rue de la Pie<br>28000 Chartres</span></li>
          <li>[[icon:phone-call]]<a href="tel:{TEL_HREF}">{TEL}</a></li>
          <li>[[icon:clock]]<span>Lun – Ven · 9h30 – 18h00</span></li>
        </ul>
      </div>
      <div>
        <h3>Nos services</h3>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h3>Informations</h3>
        <ul>
          <li><a href="la-maison.html">La maison</a></li>
          <li><a href="faq.html">Questions fréquentes</a></li>
          <li><a href="contact.html">Contact &amp; accès</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>© <span data-year>2026</span> Godot &amp; Fils Chartres. Tous droits réservés.</p>
    </div>
  </footer>
  <a class="call-fab" href="tel:{TEL_HREF}" aria-label="Appeler l'agence au {TEL}">
    [[icon:phone-call]]
  </a>
  <script src="assets/js/main.js" defer></script>'''

def page(slug, title, desc, body, ld=None, cta=True, noindex=False):
    active = slug
    ld_tag = f'\n  <script type="application/ld+json">\n{esc_json(ld)}\n  </script>' if ld else ""
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canon = "" if noindex else f'\n  <link rel="canonical" href="{SITE}/{"" if slug == "index.html" else slug}">'
    html = f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{canon}{robots}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:locale" content="fr_FR">
  <meta name="theme-color" content="#000000">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400;700&display=swap" rel="stylesheet">
  <script>document.documentElement.className+=" js"</script>
  <link rel="stylesheet" href="assets/css/style.css">{ld_tag}
</head>
<body>
{header(active)}

  <main id="contenu">
{body}
{cta_band() if cta else ""}
  </main>

{footer()}
</body>
</html>
'''
    html = re.sub(r"\[\[icon:([a-z0-9-]+)\]\]", lambda m: ic(m.group(1)), html)
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(html)
    print("écrit", slug)

def hero(crumb, eyebrow, h1, lead, actions=True):
    act = f'''
        <div class="hero-actions">
          <a class="btn btn-gold" href="contact.html">Venir à l'agence</a>
          <a class="btn btn-ghost" href="tel:{TEL_HREF}">Appeler l'agence</a>
        </div>''' if actions else ""
    return f'''    <section class="page-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <span aria-hidden="true">/</span> <span>{crumb}</span></nav>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>{act}
      </div>
    </section>'''

def faq_block(items):
    return "\n".join(f"          <details>\n            <summary>{q}</summary>\n            <p>{a}</p>\n          </details>" for q, a in items)

def steps_block():
    return '''        <ol class="steps">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:building-store]]</span><h3>Vous passez à l'agence</h3><p>Sans rendez-vous, du lundi au vendredi, avec vos bijoux, pièces ou lingots.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:scale]]</span><h3>Nous examinons devant vous</h3><p>Contrôle du titre et pesée de chaque objet, sous vos yeux.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:receipt-euro]]</span><h3>Nous vous faisons une offre</h3><p>Une proposition détaillée, fondée sur le cours du jour. Vous restez libre de refuser.</p></li>
          <li><span class="step-head"><span class="step-num">4</span>[[icon:cash-banknote]]</span><h3>Vous êtes payé</h3><p>Si vous acceptez, la transaction est finalisée avec un bordereau d'achat conforme à la réglementation.</p></li>
        </ol>'''

def ic(name, cls="ic"):
    """Inline un SVG Tabler Icons (assets/icons/<name>.svg, licence MIT)."""
    raw = open(os.path.join(ROOT, "assets", "icons", name + ".svg"), encoding="utf-8").read()
    inner = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")]
    inner = inner.replace('<path stroke="none" d="M0 0h24v24H0z" fill="none"/>', "")
    inner = " ".join(l.strip() for l in inner.strip().splitlines())
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')

# Dans les gabarits, [[icon:nom]] est remplacé par le SVG correspondant (voir page())
ICON = {"or": "[[icon:coin-euro]]", "pieces": "[[icon:coins]]", "argent": "[[icon:diamond]]", "change": "[[icon:exchange]]"}

# ---------------------------------------------------------------- RÉSEAU (carte de France)
import unicodedata
def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")

GROUP_TITLES = {"Île-de-France": "Paris &amp; Île-de-France", "Hauts-de-France": "Hauts-de-France", "Savoie": "Savoie"}

def reseau_section():
    m = json.load(open(os.path.join(ROOT, "tools", "geo", "france-map.json"), encoding="utf-8"))
    groups = {}
    for v in m["villes"]:
        key = v.get("pin", v["ville"])
        g = groups.setdefault(key, {"titre": GROUP_TITLES.get(key, key), "x": v["x"], "y": v["y"], "local": False, "agences": []})
        g["local"] = g["local"] or v.get("local", False)
        g["agences"] += v["agences"]
    n_ag = sum(len(g["agences"]) for g in groups.values())
    n_vi = len(m["villes"])
    pins, chips, panels = [], [], []
    for key, g in sorted(groups.items(), key=lambda kv: kv[1]["titre"].replace("Î", "I")):
        sid, n = "p-" + slug(key), len(g["agences"])
        r = min(6 + (n - 1) * 1.1, 12)
        cls = "pin pin-local" if g["local"] else "pin"
        label = f'{g["titre"]}, {n} agence{"s" if n > 1 else ""}'.replace("&amp;", "et")
        pins.append(f'''          <g class="{cls}" data-target="{sid}" tabindex="0" role="button" aria-label="{label}" transform="translate({g["x"]} {g["y"]})">
            <circle class="pin-hit" r="18"/><circle class="pin-halo" r="{r + 5:.1f}"/><circle class="pin-dot" r="{r:.1f}"/>
            <title>{g["titre"]}</title>
          </g>''')
        chips.append(f'<li><button type="button" class="chip{" chip-local" if g["local"] else ""}" data-target="{sid}">{g["titre"]}</button></li>')
        items = []
        for a in g["agences"]:
            adr = a.get("adresse") or "Adresse à confirmer auprès de l'agence"
            adr = adr.replace("&", "&amp;")
            tel = f'<a href="tel:+33{a["tel"].replace(" ", "")[1:]}">{a["tel"]}</a>' if a.get("tel") else ""
            ext = a.get("url")
            link = ""
            if ext:
                ext_attr = "" if ext.endswith(".html") and not ext.startswith("http") else ' target="_blank" rel="noopener"'
                link = f'<a class="text-link-light" href="{ext}"{ext_attr}>Voir l\'agence</a>'
            items.append(f'<li><strong>{a["nom"]}</strong><span>{adr}</span>{(" " + tel) if tel else ""}{link}</li>')
        badge = '<p class="panel-badge">Notre agence</p>' if g["local"] else ""
        panels.append(f'''        <div class="panel" id="{sid}">
          {badge}<h3>{g["titre"]}</h3>
          <p class="panel-count">{n} agence{"s" if n > 1 else ""}</p>
          <ul class="agences">{"".join(items)}</ul>
        </div>''')
    local_id = next("p-" + slug(k) for k, g in groups.items() if g["local"])
    return f'''    <section class="section section-dark" id="reseau" data-default="{local_id}">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Notre réseau</p>
          <h2>Des agences partout en France</h2>
          <p>Godot &amp; Fils, ce sont des agences de proximité reliées par une même exigence. Cliquez sur une ville pour découvrir l'agence la plus proche de vous.</p>
        </header>
        <div class="network">
          <div class="map-france">
            <svg viewBox="{m["viewBox"]}" role="group" aria-label="Carte de France des agences Godot &amp; Fils">
              <path class="fr-land" d="{m["path"]}"/>
              <g class="pins">
{chr(10).join(pins)}
              </g>
            </svg>
            <p class="map-legend"><span class="legend-dot"></span> Agence &nbsp;·&nbsp; <span class="legend-dot legend-local"></span> Chartres, notre agence</p>
          </div>
          <div class="network-side">
            <div class="panels" aria-live="polite">
{chr(10).join(panels)}
            </div>
          </div>
        </div>
        <h3 class="chips-title">Toutes les villes</h3>
        <ul class="chips">
{chr(10).join(chips)}
        </ul>
        <p class="map-note">{n_vi} villes et {n_ag} agences référencées. Liste établie à partir de sources publiques : le réseau évolue, retrouvez la <a class="text-link-light" href="{m["officielle"]}" target="_blank" rel="noopener">liste officielle des agences</a>.</p>
      </div>
    </section>'''

# ---------------------------------------------------------------- ACCUEIL
home = f'''    <section class="hero hero-photo">
      <div class="container hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Or · Argent · Pièces · Lingots · Bijoux · Change</p>
          <h1>Votre or estimé à sa <em>juste valeur</em>, au cœur de Chartres.</h1>
          <p class="lead">Achat et vente de métaux précieux par une maison fondée en 1933. Estimation gratuite, sans engagement et sans rendez-vous.</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="contact.html">Venir à l'agence</a>
            <a class="btn btn-ghost" href="tel:{TEL_HREF}">Appeler l'agence</a>
          </div>
          <ul class="hero-proof" aria-label="Nos engagements">
            <li><strong>1933</strong><span>année de fondation</span></li>
            <li><strong>0 €</strong><span>pour une estimation</span></li>
            <li><strong>Sans RDV</strong><span>du lundi au vendredi</span></li>
          </ul>
        </div>
      </div>
    </section>

    <section class="strip" aria-label="Informations pratiques">
      <div class="container strip-grid">
        <div><span class="strip-label">[[icon:map-pin]]Adresse</span>23 rue de la Pie, 28000 Chartres</div>
        <div><span class="strip-label">[[icon:clock]]Horaires</span>Lun – Ven · 9h30 – 18h00</div>
        <div><span class="strip-label">[[icon:phone-call]]Téléphone</span><a href="tel:{TEL_HREF}">{TEL}</a></div>
        <div class="strip-status" data-open-status><span class="dot"></span><span class="status-text">Horaires d'ouverture</span></div>
      </div>
    </section>

    <section class="section" id="services">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Nos services</p>
          <h2>Tout ce qui brille, et bien plus encore.</h2>
          <p>Que vous souhaitiez vendre des bijoux hérités, investir dans l'or physique ou préparer un voyage, l'agence vous reçoit et vous conseille.</p>
        </header>
        <div class="cards cards-4">
          <article class="card"><div class="card-icon" aria-hidden="true">{ICON["or"]}</div><h3>Vendre mon or</h3><p>Bijoux, débris, alliances, chaînes, or dentaire, pièces et lingots : nous rachetons votre or, quel que soit son état.</p><a class="link-more" href="vendre-or.html">Vendre mon or</a></article>
          <article class="card"><div class="card-icon" aria-hidden="true">{ICON["pieces"]}</div><h3>Acheter de l'or</h3><p>Napoléon, Souverain, Krugerrand, lingots et lingotins : constituez une épargne tangible, conseillé par des spécialistes.</p><a class="link-more" href="acheter-or.html">Acheter de l'or</a></article>
          <article class="card"><div class="card-icon" aria-hidden="true">{ICON["argent"]}</div><h3>Argent &amp; bijoux</h3><p>Argenterie, pièces d'argent, platine, bijoux anciens ou démodés : une expertise attentive pour chaque pièce.</p><a class="link-more" href="argent-bijoux.html">Argent &amp; bijoux</a></article>
          <article class="card"><div class="card-icon" aria-hidden="true">{ICON["change"]}</div><h3>Bureau de change</h3><p>Achat et vente de devises étrangères pour vos voyages ou au retour : un service simple, sur place.</p><a class="link-more" href="change.html">Bureau de change</a></article>
        </div>
      </div>
    </section>

    <section class="section section-dark" id="estimation">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Comment ça marche</p>
          <h2>Vendre votre or en quatre étapes</h2>
          <p>Un parcours transparent, en face à face, pour que vous décidiez en toute sérénité.</p>
        </header>
{steps_block()}
        <aside class="notice"><strong>À prévoir :</strong> une pièce d'identité en cours de validité est obligatoire pour toute vente de métaux précieux.</aside>
      </div>
    </section>

    <section class="section" id="maison">
      <div class="container split">
        <div class="split-visual" aria-hidden="true"><div class="year-badge"><span>Fondée en</span><strong>1933</strong></div></div>
        <div class="split-copy">
          <p class="eyebrow">La maison</p>
          <h2>Une institution du négoce de métaux précieux</h2>
          <p>Fondée en 1933, la maison Godot &amp; Fils s'est imposée comme une référence du négoce de l'or et des métaux précieux. Son réseau d'agences est présent dans de nombreuses villes, de Paris à Versailles en passant par Saint-Germain-en-Laye.</p>
          <p>À Chartres, notre agence perpétue ce savoir-faire : une expertise rigoureuse, des conseils personnalisés et un accueil de proximité.</p>
          <ul class="checks">
            <li>Expertise réalisée sur place, sous vos yeux</li>
            <li>Offre fondée sur le cours du jour</li>
            <li>Confidentialité et transactions sécurisées</li>
            <li>Conseils pour l'investissement dans l'or physique</li>
          </ul>
          <p class="mt"><a class="btn btn-outline" href="la-maison.html">Découvrir la maison</a></p>
        </div>
      </div>
    </section>

{reseau_section()}

    <section class="section" id="faq">
      <div class="container narrow">
        <header class="section-head">
          <p class="eyebrow">Questions fréquentes</p>
          <h2>Vous vous posez des questions ?</h2>
        </header>
        <div class="faq">
{faq_block(FAQ[0][1] + FAQ[1][1][:1])}
        </div>
        <p class="mt"><a class="btn btn-ghost" href="faq.html">Toutes les questions</a></p>
      </div>
    </section>'''
page("index.html", "Godot &amp; Fils Chartres — Achat et vente d'or, d'argent et de métaux précieux",
     "Agence Godot & Fils à Chartres, 23 rue de la Pie : achat et vente d'or, d'argent, de pièces, de lingots et de bijoux, bureau de change. Estimation gratuite, sans engagement et sans rendez-vous.",
     home, ld=LD_STORE)

# ---------------------------------------------------------------- VENDRE
vendre = hero("Vendre mon or", "Rachat d'or à Chartres", "Vendre mon or à Chartres, au meilleur prix du jour.",
              "Bijoux, alliances, or dentaire, pièces, lingots : faites estimer vos objets gratuitement, sous vos yeux, sans rendez-vous et sans engagement.") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Ce que nous rachetons</p>
          <h2>Tout objet contenant de l'or</h2>
          <p>L'état n'a pas d'importance : le prix repose sur le poids et la pureté du métal.</p>
        </header>
        <div class="cards">
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:diamond]]</div><h3>Bijoux</h3><p>Bagues, colliers, bracelets, chaînes, médailles, boucles d'oreilles, même cassés, démodés ou dépareillés.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:heart-handshake]]</div><h3>Alliances &amp; gourmettes</h3><p>Alliances anciennes, bagues de famille, gourmettes et chevalières dont vous n'avez plus l'usage.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:dental]]</div><h3>Or dentaire</h3><p>Couronnes, bridges et autres pièces dentaires en or sont estimés selon leur teneur en métal précieux.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:coins]]</div><h3>Pièces d'or</h3><p>Napoléon, Souverain, Krugerrand, 50 pesos et autres pièces d'or de collection ou d'investissement.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:scale]]</div><h3>Lingots &amp; lingotins</h3><p>Lingots de toutes tailles : estimation au poids et au titre, avec vos justificatifs si vous les avez.</p></article>
          <article class="card card-accent"><h3>Un doute ?</h3><p>Apportez l'objet : nous vous disons gratuitement ce qu'il vaut.</p><a class="link-arrow" href="contact.html">Venir à l'agence</a></article>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Comment ça marche</p>
          <h2>Quatre étapes, en face à face</h2>
          <p>Un parcours transparent pour que vous décidiez en toute sérénité.</p>
        </header>
{steps_block()}
        <aside class="notice"><strong>À prévoir :</strong> une pièce d'identité en cours de validité est obligatoire pour toute vente de métaux précieux.</aside>
      </div>
    </section>

    <section class="section">
      <div class="container split">
        <div class="split-copy">
          <p class="eyebrow">Comment est fixé le prix</p>
          <h2>Poids, pureté et cours du jour</h2>
          <p>Le prix de rachat dépend de trois éléments : le <strong>poids</strong> de l'objet, son <strong>titre</strong> (la proportion d'or pur, gravée par un poinçon) et le <strong>cours de l'or</strong> au moment de la transaction.</p>
          <p>Les pièces de collection peuvent en plus avoir une valeur numismatique. Toutes ces informations vous sont expliquées avant que vous décidiez.</p>
          <ul class="checks">
            <li>Pesée et contrôle du titre devant vous</li>
            <li>Offre détaillée et expliquée</li>
            <li>Aucune obligation d'accepter</li>
          </ul>
        </div>
        <div>
          <div class="table-wrap">
            <table class="data-table">
              <caption>Les titres de l'or les plus courants</caption>
              <thead><tr><th scope="col">Carats</th><th scope="col">Titre (pureté)</th><th scope="col">Teneur en or</th></tr></thead>
              <tbody>
                <tr><th scope="row">24 carats</th><td>999 ‰</td><td>99,9 %</td></tr>
                <tr><th scope="row">18 carats</th><td>750 ‰</td><td>75 %</td></tr>
                <tr><th scope="row">14 carats</th><td>585 ‰</td><td>58,5 %</td></tr>
                <tr><th scope="row">9 carats</th><td>375 ‰</td><td>37,5 %</td></tr>
              </tbody>
            </table>
          </div>
          <p class="note">En France, l'or 18 carats (750 ‰) est le plus répandu en bijouterie.</p>
        </div>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Questions fréquentes</p><h2>Vendre son or</h2></header>
        <div class="faq">
{faq_block(FAQ[0][1][2:] + FAQ[1][1])}
        </div>
      </div>
    </section>'''
page("vendre-or.html", "Vendre son or à Chartres — Rachat d'or, bijoux et pièces | Godot &amp; Fils",
     "Vendez votre or à Chartres : bijoux, alliances, or dentaire, pièces et lingots. Estimation gratuite et sans rendez-vous chez Godot & Fils, 23 rue de la Pie.", vendre)

# ---------------------------------------------------------------- ACHETER
acheter = hero("Acheter de l'or", "Or d'investissement", "Acheter de l'or physique : pièces et lingots.",
               "Une épargne tangible, détenue en main propre. L'agence vous conseille selon votre projet et les disponibilités du moment.") + '''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Pourquoi de l'or physique</p>
          <h2>Un actif tangible, reconnu partout</h2>
          <p>L'or est un métal que l'on peut détenir, transmettre et revendre. Il se prête à la diversification d'une épargne.</p>
        </header>
        <div class="cards">
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:coins]]</div><h3>Pièces</h3><p>Facilement divisibles, reconnues sur le marché, elles s'adaptent aux petits comme aux grands budgets.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">[[icon:scale]]</div><h3>Lingots &amp; lingotins</h3><p>Du petit lingotin au lingot massif : une prime généralement plus faible par gramme pour les formats importants.</p></article>
          <article class="card card-accent"><h3>Conseil personnalisé</h3><p>Dites-nous votre projet, nous vous orientons vers le produit le plus adapté.</p><a class="link-arrow" href="contact.html">Nous contacter</a></article>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Les pièces d'investissement</p>
          <h2>Les références du marché</h2>
          <p>Caractéristiques indicatives. Les disponibilités et les tarifs varient : appelez l'agence pour les connaître.</p>
        </header>
        <div class="table-wrap table-dark">
          <table class="data-table">
            <thead><tr><th scope="col">Pièce</th><th scope="col">Origine</th><th scope="col">Titre</th><th scope="col">Poids d'or fin</th></tr></thead>
            <tbody>
              <tr><th scope="row">20 francs Napoléon</th><td>France</td><td>900 ‰</td><td>≈ 5,81 g</td></tr>
              <tr><th scope="row">Souverain</th><td>Royaume-Uni</td><td>916,7 ‰</td><td>≈ 7,32 g</td></tr>
              <tr><th scope="row">Krugerrand (1 once)</th><td>Afrique du Sud</td><td>916,7 ‰</td><td>31,1 g</td></tr>
              <tr><th scope="row">Maple Leaf (1 once)</th><td>Canada</td><td>999,9 ‰</td><td>31,1 g</td></tr>
              <tr><th scope="row">Philharmonique (1 once)</th><td>Autriche</td><td>999,9 ‰</td><td>31,1 g</td></tr>
            </tbody>
          </table>
        </div>
        <aside class="notice"><strong>Bon à savoir :</strong> le prix de l'or varie en permanence. Un investissement comporte un risque de perte en capital et la fiscalité de l'or a ses propres règles : renseignez-vous avant d'acheter.</aside>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Comment acheter</p><h2>Simple, sur place</h2></header>
        <ol class="steps steps-3 steps-light">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:phone-call]]</span><h3>Vous nous contactez</h3><p>Par téléphone ou directement à l'agence, pour connaître les produits disponibles et les tarifs du moment.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:shield-check]]</span><h3>Nous vous conseillons</h3><p>Pièces ou lingots, budget, horizon : nous vous aidons à choisir sans pression.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:coins]]</span><h3>Vous repartez avec votre or</h3><p>La transaction est finalisée à l'agence, avec les documents réglementaires. Une pièce d'identité est requise.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Questions fréquentes</p><h2>Acheter de l'or</h2></header>
        <div class="faq">
''' + faq_block(FAQ[2][1]) + '''
        </div>
      </div>
    </section>'''
page("acheter-or.html", "Acheter de l'or à Chartres — Pièces et lingots d'investissement | Godot &amp; Fils",
     "Achetez de l'or physique à Chartres : Napoléon, Souverain, Krugerrand, Maple Leaf, lingots et lingotins. Conseils personnalisés chez Godot & Fils.", acheter)

# ---------------------------------------------------------------- ARGENT & BIJOUX
argent = hero("Argent &amp; bijoux", "Argent · Platine · Bijoux", "Argent, platine et bijoux : une expertise pour chaque pièce.",
              "Argenterie, pièces d'argent, platine, bijoux anciens ou démodés : nous les estimons avec soin, gratuitement et sans engagement.") + '''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Nos domaines</p>
          <h2>Au-delà de l'or</h2>
          <p>Les autres métaux précieux et les bijoux méritent la même attention.</p>
        </header>
        <div class="cards">
          <article class="card"><div class="card-icon" aria-hidden="true">''' + "[[icon:tools-kitchen-2]]" + '''</div><h3>Argent</h3><p>Pièces d'argent, argenterie, couverts, ménagères, objets en argent massif : estimés selon leur poids et leur titre.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">''' + "[[icon:diamonds]]" + '''</div><h3>Platine</h3><p>Bijoux et lingots de platine, un métal rare et dense, estimés selon leur pureté et le cours du jour.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">''' + "[[icon:diamond]]" + '''</div><h3>Bijoux anciens</h3><p>Pièces de famille, bijoux démodés ou dépareillés : nous distinguons la valeur du métal de celle de la création.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container split">
        <div class="split-copy">
          <p class="eyebrow">Les titres courants</p>
          <h2>Reconnaître l'argent et le platine</h2>
          <p>Comme l'or, l'argent et le platine portent un poinçon indiquant leur pureté. Ce titre, avec le poids et le cours du jour, détermine la valeur du métal.</p>
          <p>Un bijou peut aussi valoir plus que son métal : signature, époque, pierres. N'hésitez pas à nous le montrer avant toute décision.</p>
        </div>
        <div class="table-wrap table-dark">
          <table class="data-table">
            <caption>Titres courants</caption>
            <thead><tr><th scope="col">Métal</th><th scope="col">Titre</th><th scope="col">Usage courant</th></tr></thead>
            <tbody>
              <tr><th scope="row">Argent 925</th><td>925 ‰</td><td>Bijoux, argenterie</td></tr>
              <tr><th scope="row">Argent 800</th><td>800 ‰</td><td>Argenterie, pièces</td></tr>
              <tr><th scope="row">Platine 950</th><td>950 ‰</td><td>Bijouterie</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Conseils</p><h2>Avant de venir</h2></header>
        <ul class="checks checks-lg">
          <li>Ne nettoyez pas vos objets : l'estimation se fait sur l'état d'origine.</li>
          <li>Apportez tout, même ce qui est cassé, tordu ou dépareillé.</li>
          <li>Si vous les avez, apportez les factures, certificats ou écrins d'origine.</li>
          <li>Pensez à votre pièce d'identité en cours de validité.</li>
        </ul>
      </div>
    </section>'''
page("argent-bijoux.html", "Argent, platine et bijoux à Chartres — Estimation gratuite | Godot &amp; Fils",
     "Faites estimer gratuitement votre argenterie, vos pièces d'argent, votre platine et vos bijoux anciens à Chartres chez Godot & Fils.", argent)

# ---------------------------------------------------------------- CHANGE
change = hero("Change", "Bureau de change", "Changer vos devises à Chartres, simplement.",
              "Achat et vente de devises étrangères à l'agence, avant votre départ ou à votre retour de voyage.") + '''

    <section class="section">
      <div class="container split">
        <div class="split-copy">
          <p class="eyebrow">Notre service</p>
          <h2>Un change simple, sur place</h2>
          <p>Avant un voyage ou après un séjour à l'étranger, l'agence vous accueille pour changer vos euros en devises, ou vos devises en euros.</p>
          <p>Les devises disponibles varient selon les périodes : appelez-nous avant de venir pour confirmer celle dont vous avez besoin et le tarif du moment.</p>
          <ul class="checks">
            <li>Service au guichet, sans rendez-vous</li>
            <li>Taux communiqué avant la transaction</li>
            <li>Pièce d'identité à présenter</li>
          </ul>
          <p class="mt"><a class="btn btn-gold" href="tel:''' + TEL_HREF + '''">Appeler pour une devise</a></p>
        </div>
        <div class="cards cards-1">
          <article class="card"><div class="card-icon" aria-hidden="true">''' + "[[icon:plane-departure]]" + '''</div><h3>Avant de partir</h3><p>Anticipez : certaines devises peuvent nécessiter un délai. Un appel suffit pour vérifier.</p></article>
          <article class="card"><div class="card-icon" aria-hidden="true">''' + "[[icon:plane-arrival]]" + '''</div><h3>Au retour</h3><p>Reprenez vos devises restantes en euros, billets de banque étrangers inclus selon disponibilité.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Questions fréquentes</p><h2>Le change</h2></header>
        <div class="faq">
''' + faq_block(FAQ[3][1] + FAQ[0][1][:1]) + '''
        </div>
      </div>
    </section>'''
page("change.html", "Bureau de change à Chartres — Devises | Godot &amp; Fils",
     "Bureau de change à Chartres : achat et vente de devises étrangères chez Godot & Fils, 23 rue de la Pie. Renseignez-vous par téléphone sur la devise souhaitée.", change)


# ---------------------------------------------------------------- LA MAISON
maison = hero("La maison", "Depuis 1933", "Une institution du négoce de métaux précieux.",
              "Depuis 1933, la maison Godot & Fils accompagne particuliers et épargnants dans l'achat et la vente d'or, d'argent et de métaux précieux.", actions=False) + '''

    <section class="section">
      <div class="container split">
        <div class="split-visual" aria-hidden="true"><div class="year-badge"><span>Fondée en</span><strong>1933</strong></div></div>
        <div class="split-copy">
          <p class="eyebrow">Notre histoire</p>
          <h2>Près d'un siècle de savoir-faire</h2>
          <p>Fondée en 1933, la maison Godot &amp; Fils s'est imposée comme une référence du négoce de l'or et des métaux précieux. Son réseau d'agences est présent dans de nombreuses villes, de Paris à Versailles en passant par Saint-Germain-en-Laye.</p>
          <p>À Chartres, l'agence du 23 rue de la Pie perpétue cette tradition : une expertise rigoureuse, des conseils personnalisés et un accueil de proximité, dans le centre de la ville.</p>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Nos engagements</p>
          <h2>Ce qui guide chaque estimation</h2>
        </header>
        <div class="cards">
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:eye-check]]</div><h3>Transparence</h3><p>Pesée, contrôle du titre et calcul du prix se font devant vous. Chaque offre est expliquée.</p></article>
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:shield-check]]</div><h3>Liberté</h3><p>L'estimation est gratuite et sans engagement. Vous repartez avec vos objets si l'offre ne vous convient pas.</p></article>
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:map-pin]]</div><h3>Proximité</h3><p>Une agence ouverte du lundi au vendredi, sans rendez-vous, avec une équipe qui prend le temps de vous conseiller.</p></article>
        </div>
      </div>
    </section>

''' + reseau_section() + '''

    <section class="section">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Ce que nous faisons</p><h2>Un seul interlocuteur pour vos métaux précieux</h2></header>
        <ul class="checks checks-lg">
          <li><a class="text-link" href="vendre-or.html">Rachat d'or</a> : bijoux, or dentaire, pièces et lingots</li>
          <li><a class="text-link" href="acheter-or.html">Vente d'or d'investissement</a> : pièces et lingots</li>
          <li><a class="text-link" href="argent-bijoux.html">Argent, platine et bijoux</a> : estimation et rachat</li>
          <li><a class="text-link" href="change.html">Bureau de change</a> : devises étrangères</li>
        </ul>
      </div>
    </section>'''
page("la-maison.html", "La maison Godot &amp; Fils — Négoce de métaux précieux depuis 1933",
     "Godot & Fils, institution du négoce d'or et de métaux précieux depuis 1933. Découvrez l'histoire, les engagements et l'agence de Chartres.", maison)

# ---------------------------------------------------------------- FAQ
faq_sections = "\n".join(f'''    <section class="section{" section-soft" if i % 2 else ""}">
      <div class="container narrow">
        <header class="section-head"><h2>{t}</h2></header>
        <div class="faq">
{faq_block(items)}
        </div>
      </div>
    </section>''' for i, (t, items) in enumerate(FAQ))
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, items in FAQ for q, a in items]}
page("faq.html", "Questions fréquentes — Godot &amp; Fils Chartres",
     "Toutes les réponses à vos questions sur la vente d'or, l'achat de pièces et lingots, l'estimation gratuite et le bureau de change à Chartres.",
     hero("Questions fréquentes", "FAQ", "Vous vous posez des questions ?",
          "Estimation, documents, prix de rachat, investissement, change : retrouvez ici les réponses les plus courantes.", actions=False) + "\n\n" + faq_sections,
     ld=faq_ld)

# ---------------------------------------------------------------- CONTACT
contact = hero("Contact", "Votre agence", "Nous rendre visite à Chartres.",
               "Du lundi au vendredi, sans rendez-vous. Pour un lot important ou une devise précise, un appel nous permet de mieux vous recevoir.", actions=False) + f'''

    <section class="section">
      <div class="container contact-grid">
        <div class="contact-card">
          <h2>Godot &amp; Fils Chartres</h2>
          <dl class="contact-list">
            <div><dt>[[icon:map-pin]]Adresse</dt><dd>23 rue de la Pie<br>28000 Chartres</dd></div>
            <div><dt>[[icon:phone-call]]Téléphone</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a></dd></div>
            <div>
              <dt>[[icon:clock]]Horaires</dt>
              <dd>
                <p class="open-line" data-open-status><span class="dot"></span><span class="status-text">Horaires d'ouverture</span></p>
                <table class="hours"><tbody>
                  <tr data-day="1"><th scope="row">Lundi</th><td>9h30 – 18h00</td></tr>
                  <tr data-day="2"><th scope="row">Mardi</th><td>9h30 – 18h00</td></tr>
                  <tr data-day="3"><th scope="row">Mercredi</th><td>9h30 – 18h00</td></tr>
                  <tr data-day="4"><th scope="row">Jeudi</th><td>9h30 – 18h00</td></tr>
                  <tr data-day="5"><th scope="row">Vendredi</th><td>9h30 – 18h00</td></tr>
                  <tr data-day="6"><th scope="row">Samedi</th><td>Fermé</td></tr>
                  <tr data-day="0"><th scope="row">Dimanche</th><td>Fermé</td></tr>
                </tbody></table>
              </dd>
            </div>
          </dl>
          <div class="hero-actions">
            <a class="btn btn-gold" href="tel:{TEL_HREF}">Appeler</a>
            <a class="btn btn-outline" href="https://www.google.com/maps/search/?api=1&amp;query=23+rue+de+la+Pie+28000+Chartres" target="_blank" rel="noopener">Itinéraire</a>
          </div>
        </div>
        <div class="map">
          <iframe title="Plan d'accès à l'agence Godot &amp; Fils Chartres" src="https://maps.google.com/maps?q=23%20rue%20de%20la%20Pie%2C%2028000%20Chartres&amp;z=16&amp;output=embed" loading="lazy"></iframe>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Avant de venir</p><h2>Ce qu'il faut apporter</h2></header>
        <div class="cards">
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:id]]</div><h3>Une pièce d'identité</h3><p>En cours de validité, obligatoire pour toute vente de métaux précieux.</p></article>
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:diamond]]</div><h3>Vos objets</h3><p>Bijoux, pièces, lingots, argenterie : même cassés ou abîmés, sans les nettoyer.</p></article>
          <article class="card card-dark"><div class="card-icon" aria-hidden="true">[[icon:file-certificate]]</div><h3>Vos justificatifs</h3><p>Factures, certificats ou écrins d'origine, si vous les avez. Ils peuvent faciliter la transaction.</p></article>
        </div>
      </div>
    </section>'''
page("contact.html", "Contact et accès — Godot &amp; Fils Chartres, 23 rue de la Pie",
     "Agence Godot & Fils Chartres : 23 rue de la Pie, 28000 Chartres. Ouvert du lundi au vendredi de 9h30 à 18h00. Tél. 02 37 83 49 77.", contact, ld=LD_STORE, cta=False)

# ---------------------------------------------------------------- MENTIONS LÉGALES
legal = '''    <section class="legal">
      <div class="container narrow">
        <h1>Mentions légales</h1>
        <h2>Éditeur du site</h2>
        <p>Godot &amp; Fils Chartres — 23 rue de la Pie, 28000 Chartres — Tél. ''' + TEL + '''<br>
        Raison sociale : <span class="todo">à compléter</span> · SIRET : <span class="todo">à compléter</span> · RCS : <span class="todo">à compléter</span><br>
        Directeur de la publication : <span class="todo">à compléter</span></p>
        <h2>Hébergement</h2>
        <p><span class="todo">Nom, adresse et téléphone de l'hébergeur à compléter.</span></p>
        <h2>Propriété intellectuelle</h2>
        <p>L'ensemble des contenus de ce site (textes, visuels, logos) est protégé par le droit de la propriété intellectuelle. Toute reproduction sans autorisation préalable est interdite.</p>
        <h2>Données personnelles</h2>
        <p>Ce site ne collecte aucune donnée personnelle via formulaire. La carte d'accès intégrée à la page Contact est fournie par un service tiers susceptible de déposer des cookies. Pour toute question relative à vos données, contactez l'agence.</p>
      </div>
    </section>'''
page("mentions-legales.html", "Mentions légales — Godot &amp; Fils Chartres", "Mentions légales du site Godot & Fils Chartres.", legal, cta=False, noindex=True)

# ---------------------------------------------------------------- sitemap / robots
pages = ["index.html"] + [h for h, _ in NAV] + ["faq.html"]
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages:
        f.write(f"  <url><loc>{SITE}/{'' if p == 'index.html' else p}</loc></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
