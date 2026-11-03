#!/usr/bin/env python3
"""Génère les pages statiques du site (python3 tools/build.py).
Édite le contenu ici, puis relance le script : en-tête, pied de page et navigation restent cohérents."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.godotetfils-chartres.fr"
TEL, TEL_HREF = "02 37 83 49 77", "+33237834977"

SERVICES = [
    ("vendre-or.html", "Vendre mon or", "coin-euro", "Faites estimer et rachetez vos objets en or, sans rendez-vous."),
    ("acheter-or.html", "Acheter de l'or", "coins", "Pièces et lingots d'investissement, avec conseil personnalisé."),
    ("numismatique.html", "Numismatique", "medal", "Pièces de collection : valeur du métal et valeur numismatique."),
    ("argent-bijoux.html", "Argent &amp; bijoux", "diamond", "Argenterie, platine et bijoux anciens estimés avec soin."),
    ("change.html", "Bureau de change", "exchange", "Devises étrangères pour vos voyages, achat et vente."),
]
NAV = [(h, t) for h, t, _, _ in SERVICES] + [("la-maison.html", "La maison"), ("contact.html", "Contact")]

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
        ("Faut-il prendre rendez-vous ?", "Non, du lundi au vendredi de 9h30 à 18h00 : venez à l'agence sans rendez-vous. Le samedi matin, l'agence reçoit sur rendez-vous : appelez le 02 37 83 49 77. Pour un lot important, un appel au 02 37 83 49 77 nous permet de mieux vous recevoir."),
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
    ("Numismatique", [
        ("Une pièce rare vaut-elle plus que son poids d'or ?", "Parfois, oui. Au-delà du métal, la valeur numismatique dépend de la rareté (tirage, millésime), de l'état de conservation et de la demande des collectionneurs. Beaucoup de pièces courantes ne valent cependant que leur métal."),
        ("Dois-je nettoyer mes pièces avant de venir ?", "Non, jamais. Le nettoyage raye la surface et peut faire perdre une grande part de la valeur d'une pièce de collection. Apportez-la telle quelle."),
        ("Comment connaître la valeur de ma collection ?", "Apportez vos pièces à l'agence : l'estimation est gratuite et sans engagement. Elle distingue la valeur du métal et, le cas échéant, une valeur de collection."),
        ("Comment tenir et conserver mes pièces ?", "Tenez-les par la tranche, sans toucher les faces, et conservez-les à l'abri de l'humidité dans des capsules ou des écrins adaptés."),
    ]),
    ("Change", [
        ("Puis-je changer des devises à l'agence ?", "Oui, l'agence est aussi bureau de change. Les devises disponibles varient : appelez-nous avant de venir pour confirmer celle dont vous avez besoin."),
    ]),
]

def esc_json(o): return json.dumps(o, ensure_ascii=False, indent=2)

def header(active):
    cur = lambda h: ' aria-current="page"' if h == active else ""
    in_svc = active in [h for h, _, _, _ in SERVICES]
    items = "".join(
        f'<a href="{h}"{cur(h)}>[[icon:{ico}]]<span><strong>{t}</strong><small>{d}</small></span></a>' for h, t, ico, d in SERVICES)
    items += f'<a class="mega-extra" href="faq.html"{cur("faq.html")}>[[icon:zoom-check]]<span><strong>Questions fréquentes</strong><small>Estimation, documents, prix de rachat…</small></span></a>'
    panel = (
        '<div class="container mega-inner">'
        f'<div class="mega-list"><p class="mega-title">Nos services</p><div class="mega-grid">{items}</div></div>'
        '<aside class="mega-aside"><p class="mega-title">Estimation gratuite</p>'
        '<p>Sans rendez-vous du lundi au vendredi, de 9h30 à 18h00. Le samedi matin, sur rendez-vous.</p>'
        f'<a class="btn btn-gold btn-sm" href="tel:{TEL_HREF}">[[icon:phone-call]]<span>{TEL}</span></a>'
        '<a class="link-more" href="contact.html">Venir à l\'agence</a></aside>'
        '</div>')
    dd_cls = " is-current" if in_svc else ""
    return f'''  <a class="skip" href="#contenu">Aller au contenu</a>
  <header class="site-header" id="haut">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Godot &amp; Fils Chartres, accueil">
        <img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils, depuis 1933">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu">
        <span></span><span></span>
      </button>
      <nav id="nav" class="menu" aria-label="Navigation principale">
        <div class="menu-links">
          <span class="menu-glide" aria-hidden="true"></span>
          <div class="menu-dd">
            <button type="button" class="menu-dd-btn{dd_cls}" aria-expanded="false" aria-haspopup="true" aria-controls="menu-panel"><span>Nos services</span>[[icon:chevron-down]]</button>
            <div class="menu-panel" id="menu-panel" role="group" aria-label="Nos services">{panel}</div>
          </div>
          <a href="la-maison.html"{cur("la-maison.html")}>[[icon:building-store]]<span>La maison</span></a>
          <a href="contact.html"{cur("contact.html")}>[[icon:map-pin]]<span>Contact</span></a>
        </div>
        <span class="menu-status" data-open-status data-short><span class="dot"></span><span class="status-text">Horaires d'ouverture</span></span>
        <a class="btn btn-gold btn-sm menu-cta" href="tel:{TEL_HREF}">[[icon:phone-call]]<span>{TEL}</span></a>
        <div class="menu-foot">
          <p>[[icon:map-pin]]<span>23 rue de la Pie, 28000 Chartres</span></p>
          <p>[[icon:clock]]<span>Lun – Ven · 9h30 – 18h00<br>Samedi matin sur rendez-vous</span></p>
        </div>
      </nav>
    </div>
  </header>'''

def cta_band():
    return f'''    <section class="cta-band">
      <div class="container cta-inner">
        <div>
          <h2>Estimation gratuite, sans rendez-vous.</h2>
          <p>Passez nous voir au 23 rue de la Pie, du lundi au vendredi de 9h30 à 18h00, et le samedi matin sur rendez-vous.</p>
        </div>
        <div class="cta-actions">
          <a class="btn btn-gold" href="contact.html">Venir à l'agence</a>
          <a class="btn btn-outline" href="tel:{TEL_HREF}">{TEL}</a>
        </div>
      </div>
    </section>'''

def footer():
    svc = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t, _, _ in SERVICES)
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
          <li>[[icon:clock]]<span>Lun – Ven · 9h30 – 18h00<br>Samedi matin sur rendez-vous</span></li>
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
          <li><button type="button" class="linklike" data-consent-open>Gérer les cookies</button></li>
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
  <script src="assets/js/consent.js" defer></script>
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
  <link rel="preload" href="assets/fonts/josefin-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/josefin-sans-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
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
    html = re.sub(r"\[\[icon:([a-z0-9-]+)(?::(thin))?\]\]", lambda m: ic(m.group(1), m.group(2) or "light"), html)
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
          <li><span class="step-head"><span class="step-num">1</span>[[icon:building-store:thin]]</span><h3>Vous passez à l'agence</h3><p>Sans rendez-vous, du lundi au vendredi, avec vos bijoux, pièces ou lingots.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:scale:thin]]</span><h3>Nous examinons devant vous</h3><p>Contrôle du titre et pesée de chaque objet, sous vos yeux.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:receipt-euro:thin]]</span><h3>Nous vous faisons une offre</h3><p>Une proposition détaillée, fondée sur le cours du jour. Vous restez libre de refuser.</p></li>
          <li><span class="step-head"><span class="step-num">4</span>[[icon:cash-banknote:thin]]</span><h3>Vous êtes payé</h3><p>Si vous acceptez, la transaction est finalisée avec un bordereau d'achat conforme à la réglementation.</p></li>
        </ol>'''

ICON_ALIAS = {'coin-euro': 'currency-eur', 'coins': 'coins', 'diamond': 'sketch-logo', 'diamonds': 'diamonds-four', 'exchange': 'swap', 'medal': 'coin', 'building-store': 'storefront', 'map-pin': 'map-pin', 'phone-call': 'phone-call', 'clock': 'clock', 'id': 'identification-card', 'file-certificate': 'certificate', 'eye-check': 'eye', 'heart-handshake': 'handshake', 'shield-check': 'shield-check', 'scale': 'scales', 'receipt-euro': 'receipt', 'cash-banknote': 'money', 'chart-line': 'chart-line-up', 'plus': 'plus', 'equal': 'equals', 'x': 'x', 'chevron-down': 'caret-down', 'chevron-left': 'caret-left', 'chevron-right': 'caret-right', 'star': 'star', 'zoom-check': 'magnifying-glass', 'world': 'globe-hemisphere-west', 'hourglass': 'hourglass', 'dental': 'tooth', 'tools-kitchen-2': 'fork-knife', 'plane-departure': 'airplane-takeoff', 'plane-arrival': 'airplane-landing', 'star-fill': 'star-fill'}

def ic(name, weight="light", cls="ic"):
    """Inline un SVG Phosphor Icons (assets/icons/, licence MIT). weight : light (défaut) ou thin (grands pictogrammes)."""
    target = ICON_ALIAS[name]
    fname = "star-fill-fill" if target == "star-fill" else f"{target}-{weight}"
    raw = open(os.path.join(ROOT, "assets", "icons", fname + ".svg"), encoding="utf-8").read()
    inner = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")].strip()
    return f'<svg class="{cls}" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{inner}</svg>'

# Dans les gabarits, [[icon:nom]] est remplacé par le SVG correspondant (voir page())
ICON = {"or": "[[icon:coin-euro]]", "pieces": "[[icon:coins]]", "argent": "[[icon:diamond]]", "change": "[[icon:exchange]]"}

# ---------------------------------------------------------------- AVIS GOOGLE
# Les avis viennent de tools/avis.json (à remplir avec de VRAIS avis : copier-coller depuis Google Business Profile).
# Tant que la liste est vide, la section n'est pas générée.
def avis_section():
    path = os.environ.get("AVIS_FILE", os.path.join(ROOT, "tools", "avis.json"))
    if not os.path.exists(path):
        return ""
    data = json.load(open(path, encoding="utf-8"))
    avis = [a for a in data.get("avis", []) if a.get("texte") and a.get("auteur")]
    if not avis:
        return ""
    esc = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    stars = lambda n: "".join(f'<span class="star{" star-on" if i < n else ""}">[[icon:{"star-fill" if i < n else "star"}]]</span>' for i in range(5))
    cards = []
    for a in avis:
        n = max(1, min(5, int(a.get("note", 5))))
        initiale = esc(a["auteur"].strip()[:1].upper())
        meta = " · ".join(x for x in [esc(a["date"]) if a.get("date") else "", "Avis Google"] if x)
        cards.append(
            f'<article class="review"><div class="review-stars" role="img" aria-label="{n} sur 5">{stars(n)}</div>'
            f'<blockquote><p>{esc(a["texte"])}</p></blockquote>'
            f'<footer><span class="review-avatar" aria-hidden="true">{initiale}</span>'
            f'<div><strong>{esc(a["auteur"])}</strong><span>{meta}</span></div></footer></article>')
    note, nb = data.get("note_moyenne"), data.get("nombre_avis")
    resume = ""
    if note:
        n_txt = str(note).replace(".", ",")
        total = f" · {nb} avis Google" if nb else " · avis Google"
        resume = (f'<div class="rating"><strong>{n_txt}</strong><div class="review-stars" role="img" aria-label="Note moyenne {n_txt} sur 5">{stars(round(float(note)))}</div>'
                  f'<span>sur 5{total}</span></div>')
    lien = data.get("lien_google", "https://www.google.com/maps/search/?api=1&query=Godot+et+Fils+Chartres+23+rue+de+la+Pie")
    return f'''    <section class="section" id="avis">
      <div class="container">
        <div class="reviews-head">
          <header class="section-head">
            <p class="eyebrow">Avis clients</p>
            <h2>Ils nous ont fait confiance</h2>
            <p>Les avis de nos clients, publiés sur Google.</p>
          </header>
          {resume}
        </div>
        <div class="reviews" data-reviews>
          <div class="reviews-track" tabindex="0" role="region" aria-label="Avis clients, défilement horizontal">{"".join(cards)}</div>
          <div class="reviews-nav">
            <button type="button" class="round-btn" data-rev="prev" aria-label="Avis précédents">[[icon:chevron-left]]</button>
            <button type="button" class="round-btn" data-rev="next" aria-label="Avis suivants">[[icon:chevron-right]]</button>
            <a class="btn btn-outline btn-sm" href="{lien}" target="_blank" rel="noopener">Voir tous les avis sur Google</a>
          </div>
        </div>
      </div>
    </section>'''

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
FAQ_CLS = "section section-soft" if avis_section() else "section"   # alternance des fonds selon la présence des avis
TICKER = "".join(f"<span>{w}</span>" for w in ["Achat d'or", "Vente de pièces", "Lingots", "Argent", "Bijoux", "Bureau de change", "Depuis 1933"] * 6)
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
            <li><strong data-count="1933" data-from="1900">1933</strong><span>année de fondation</span></li>
            <li><strong>0 €</strong><span>pour une estimation</span></li>
            <li><strong>Sans RDV</strong><span>du lundi au vendredi</span></li>
          </ul>
        </div>
      </div>
    </section>

    <div class="ticker" aria-hidden="true"><div class="ticker-track">{TICKER}</div></div>

    <section class="strip" aria-label="Informations pratiques">
      <div class="container strip-grid">
        <div><span class="strip-label">[[icon:map-pin]]Adresse</span>23 rue de la Pie, 28000 Chartres</div>
        <div><span class="strip-label">[[icon:clock]]Horaires</span>Lun – Ven · 9h30 – 18h00<br>Sam. matin sur RDV</div>
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
        <div class="split-visual" aria-hidden="true"><div class="year-badge"><span>Fondée en</span><strong data-count="1933" data-from="1900">1933</strong></div></div>
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

{avis_section()}

    <section class="{FAQ_CLS}" id="faq">
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

# ================================================================ PAGES SERVICES

def subnav(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>[[icon:{ico}]]<span>{t}</span></a></li>'
        for h, t, ico, _ in SERVICES)
    return f'''    <div class="subnav" aria-label="Nos services">
      <div class="container"><ul>{items}</ul></div>
    </div>'''

def service_hero(crumb, eyebrow, h1, lead, icon, facts):
    fl = "".join(f'<li>[[icon:{i_}:thin]]<div><strong>{big}</strong><span>{small}</span></div></li>' for i_, big, small in facts)
    return f'''    <section class="page-hero service-hero">
      <div class="container service-hero-grid">
        <div>
          <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <span aria-hidden="true">/</span> <span>{crumb}</span></nav>
          <p class="eyebrow">{eyebrow}</p>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="contact.html">Venir à l'agence</a>
            <a class="btn btn-ghost" href="tel:{TEL_HREF}">Appeler l'agence</a>
          </div>
        </div>
        <aside class="facts-card" aria-label="L'essentiel">
          <div class="facts-mark" aria-hidden="true">[[icon:{icon}:thin]]</div>
          <ul>{fl}</ul>
        </aside>
      </div>
    </section>'''

def others(active, cls=""):
    cards = "".join(
        f'<a class="other-card" href="{h}"><span class="card-icon" aria-hidden="true">[[icon:{ico}]]</span><h3>{t}</h3><p>{d}</p><span class="link-more">Découvrir</span></a>'
        for h, t, ico, d in SERVICES if h != active)
    return f'''    <section class="section {cls} others">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Nos autres services</p><h2>Ce que nous pouvons aussi faire pour vous</h2></header>
        <div class="cards cards-auto">{cards}</div>
      </div>
    </section>'''

def feature(icon, title, text):
    return f'<article class="card-row"><span class="card-icon" aria-hidden="true">[[icon:{icon}]]</span><div><h3>{title}</h3><p>{text}</p></div></article>'

def faq_section(title, items, cls="section-soft"):
    return f'''    <section class="section {cls}">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Questions fréquentes</p><h2>{title}</h2></header>
        <div class="faq">
{faq_block(items)}
        </div>
      </div>
    </section>'''

FORMULA = '''        <div class="formula" role="img" aria-label="Poids multiplié par pureté multiplié par cours du jour égale votre offre">
          <div class="f-box">[[icon:scale:thin]]<strong>Poids</strong><span>pesée sur place</span></div>
          <span class="f-op" aria-hidden="true">[[icon:x]]</span>
          <div class="f-box">[[icon:diamond:thin]]<strong>Pureté</strong><span>titre du poinçon</span></div>
          <span class="f-op" aria-hidden="true">[[icon:x]]</span>
          <div class="f-box">[[icon:chart-line:thin]]<strong>Cours du jour</strong><span>au moment de la vente</span></div>
          <span class="f-op" aria-hidden="true">[[icon:equal]]</span>
          <div class="f-box f-result">[[icon:receipt-euro:thin]]<strong>Votre offre</strong><span>détaillée et expliquée</span></div>
        </div>'''

# ---------------------------------------------------------------- VENDRE
vendre = service_hero("Vendre mon or", "Rachat d'or à Chartres", "Vendre mon or à Chartres, au prix du jour.",
    "Bijoux, alliances, or dentaire, pièces, lingots : faites estimer vos objets gratuitement, sous vos yeux, sans rendez-vous et sans engagement.",
    "coin-euro", [("coin-euro", "0 €", "Estimation gratuite"), ("building-store", "Sans RDV", "Du lundi au vendredi"), ("scale", "Sous vos yeux", "Pesée et contrôle du titre")]) + "\n" + subnav("vendre-or.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Ce que nous rachetons</p>
          <h2>Tout objet contenant de l'or</h2>
          <p>L'état n'a pas d'importance : le prix repose sur le poids et la pureté du métal.</p>
        </header>
        <div class="cards-feature">
          {feature("diamond", "Bijoux", "Bagues, colliers, bracelets, chaînes, médailles, boucles d'oreilles, même cassés, démodés ou dépareillés.")}
          {feature("heart-handshake", "Alliances &amp; gourmettes", "Alliances anciennes, bagues de famille, gourmettes et chevalières dont vous n'avez plus l'usage.")}
          {feature("dental", "Or dentaire", "Couronnes, bridges et autres pièces dentaires en or sont estimés selon leur teneur en métal précieux.")}
          {feature("coins", "Pièces d'or", "Napoléon, Souverain, Krugerrand, 50 pesos et autres pièces d'or de collection ou d'investissement.")}
          {feature("scale", "Lingots &amp; lingotins", "Lingots de toutes tailles : estimation au poids et au titre, avec vos justificatifs si vous les avez.")}
          <article class="card-row card-row-accent"><div><h3>Un doute ?</h3><p>Apportez l'objet : nous vous disons gratuitement ce qu'il vaut.</p><a class="link-arrow" href="contact.html">Venir à l'agence</a></div></article>
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
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Comment est fixé le prix</p>
          <h2>Un calcul simple, expliqué avant de décider</h2>
          <p>Le prix de rachat dépend du poids de l'objet, de son titre (la proportion d'or pur, gravée par un poinçon) et du cours de l'or au moment de la transaction.</p>
        </header>
{FORMULA}
        <div class="split split-top">
          <div class="split-copy">
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
      </div>
    </section>

{faq_section("Vendre son or", FAQ[0][1][2:] + FAQ[1][1])}

{others("vendre-or.html")}'''
page("vendre-or.html", "Vendre son or à Chartres — Rachat d'or, bijoux et pièces | Godot &amp; Fils",
     "Vendez votre or à Chartres : bijoux, alliances, or dentaire, pièces et lingots. Estimation gratuite et sans rendez-vous chez Godot & Fils, 23 rue de la Pie.", vendre)

# ---------------------------------------------------------------- ACHETER
COINS = [
    ("20 francs Napoléon", "France", "900 ‰", "5,81"),
    ("Souverain", "Royaume-Uni", "916,7 ‰", "7,32"),
    ("Krugerrand (1 once)", "Afrique du Sud", "916,7 ‰", "31,1"),
    ("Maple Leaf (1 once)", "Canada", "999,9 ‰", "31,1"),
    ("Philharmonique (1 once)", "Autriche", "999,9 ‰", "31,1"),
]
coin_cards = "\n".join(
    f'''          <article class="coin-card"><div class="medal"><strong>{g}</strong><span>g d'or fin</span></div><h3>{n}</h3><dl><div><dt>Origine</dt><dd>{o}</dd></div><div><dt>Titre</dt><dd>{t}</dd></div></dl></article>'''
    for n, o, t, g in COINS)

acheter = service_hero("Acheter de l'or", "Or d'investissement", "Acheter de l'or physique : pièces et lingots.",
    "Une épargne tangible, détenue en main propre. L'agence vous conseille selon votre projet et les disponibilités du moment.",
    "coins", [("coins", "Pièces &amp; lingots", "Selon les disponibilités"), ("shield-check", "Conseil", "Personnalisé, sans pression"), ("phone-call", "Tarif du jour", "Sur simple appel")]) + "\n" + subnav("acheter-or.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Pourquoi de l'or physique</p>
          <h2>Un actif tangible, reconnu partout</h2>
          <p>L'or est un métal que l'on peut détenir, transmettre et revendre. Il se prête à la diversification d'une épargne.</p>
        </header>
        <div class="cards-feature cards-feature-3">
          {feature("coins", "Pièces", "Facilement divisibles, reconnues sur le marché, elles s'adaptent aux petits comme aux grands budgets.")}
          {feature("scale", "Lingots &amp; lingotins", "Du petit lingotin au lingot massif : une prime généralement plus faible par gramme pour les formats importants.")}
          <article class="card-row card-row-accent"><div><h3>Conseil personnalisé</h3><p>Dites-nous votre projet, nous vous orientons vers le produit le plus adapté.</p><a class="link-arrow" href="contact.html">Nous contacter</a></div></article>
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
        <div class="coin-grid">
{coin_cards}
        </div>
        <aside class="notice"><strong>Bon à savoir :</strong> le prix de l'or varie en permanence. Un investissement comporte un risque de perte en capital et la fiscalité de l'or a ses propres règles : renseignez-vous avant d'acheter.</aside>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Comment acheter</p><h2>Simple, sur place</h2></header>
        <ol class="steps steps-3 steps-light">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:phone-call:thin]]</span><h3>Vous nous contactez</h3><p>Par téléphone ou directement à l'agence, pour connaître les produits disponibles et les tarifs du moment.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:shield-check:thin]]</span><h3>Nous vous conseillons</h3><p>Pièces ou lingots, budget, horizon : nous vous aidons à choisir sans pression.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:coins:thin]]</span><h3>Vous repartez avec votre or</h3><p>La transaction est finalisée à l'agence, avec les documents réglementaires. Une pièce d'identité est requise.</p></li>
        </ol>
      </div>
    </section>

{faq_section("Acheter de l'or", FAQ[2][1])}

{others("acheter-or.html")}'''
page("acheter-or.html", "Acheter de l'or à Chartres — Pièces et lingots d'investissement | Godot &amp; Fils",
     "Achetez de l'or physique à Chartres : Napoléon, Souverain, Krugerrand, Maple Leaf, lingots et lingotins. Conseils personnalisés chez Godot & Fils.", acheter)

# ---------------------------------------------------------------- ARGENT & BIJOUX
argent = service_hero("Argent &amp; bijoux", "Argent · Platine · Bijoux", "Argent, platine et bijoux : une expertise pour chaque pièce.",
    "Argenterie, pièces d'argent, platine, bijoux anciens ou démodés : nous les estimons avec soin, gratuitement et sans engagement.",
    "diamond", [("diamond", "Expertise", "Chaque pièce est examinée"), ("coin-euro", "0 €", "Estimation gratuite"), ("id", "Pièce d'identité", "Requise pour vendre")]) + "\n" + subnav("argent-bijoux.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Nos domaines</p>
          <h2>Au-delà de l'or</h2>
          <p>Les autres métaux précieux et les bijoux méritent la même attention.</p>
        </header>
        <div class="cards-feature">
          {feature("tools-kitchen-2", "Argent", "Pièces d'argent, argenterie, couverts, ménagères, objets en argent massif : estimés selon leur poids et leur titre.")}
          {feature("diamonds", "Platine", "Bijoux et lingots de platine, un métal rare et dense, estimés selon leur pureté et le cours du jour.")}
          {feature("diamond", "Bijoux anciens", "Pièces de famille, bijoux démodés ou dépareillés : nous distinguons la valeur du métal de celle de la création.")}
          <article class="card-row card-row-accent"><div><h3>Un objet, un doute ?</h3><p>Montrez-le-nous : l'estimation est gratuite.</p><a class="link-arrow" href="contact.html">Venir à l'agence</a></div></article>
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
      <div class="container">
        <header class="section-head"><p class="eyebrow">Conseils</p><h2>Avant de venir</h2></header>
        <ol class="tips">
          <li><span class="tip-ico">[[icon:diamond]]</span><div><h3>Ne nettoyez pas</h3><p>L'estimation se fait sur l'état d'origine de l'objet.</p></div></li>
          <li><span class="tip-ico">[[icon:coins]]</span><div><h3>Apportez tout</h3><p>Même ce qui est cassé, tordu ou dépareillé.</p></div></li>
          <li><span class="tip-ico">[[icon:file-certificate]]</span><div><h3>Vos justificatifs</h3><p>Factures, certificats ou écrins d'origine, si vous les avez.</p></div></li>
          <li><span class="tip-ico">[[icon:id]]</span><div><h3>Une pièce d'identité</h3><p>En cours de validité, obligatoire pour toute vente.</p></div></li>
        </ol>
      </div>
    </section>

{others("argent-bijoux.html", "section-soft")}'''
page("argent-bijoux.html", "Argent, platine et bijoux à Chartres — Estimation gratuite | Godot &amp; Fils",
     "Faites estimer gratuitement votre argenterie, vos pièces d'argent, votre platine et vos bijoux anciens à Chartres chez Godot & Fils.", argent)

# ---------------------------------------------------------------- CHANGE
change = service_hero("Change", "Bureau de change", "Changer vos devises à Chartres, simplement.",
    "Achat et vente de devises étrangères à l'agence, avant votre départ ou à votre retour de voyage.",
    "exchange", [("exchange", "Devises", "Achat et vente"), ("phone-call", "Appelez d'abord", "Pour confirmer la devise"), ("id", "Pièce d'identité", "À présenter au guichet")]) + "\n" + subnav("change.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Notre service</p>
          <h2>Un change simple, sur place</h2>
          <p>Avant un voyage ou après un séjour à l'étranger, l'agence vous accueille pour changer vos euros en devises, ou vos devises en euros. Les devises disponibles varient selon les périodes.</p>
        </header>
        <div class="cards-feature">
          {feature("plane-departure", "Avant de partir", "Anticipez : certaines devises peuvent nécessiter un délai. Un appel suffit pour vérifier.")}
          {feature("plane-arrival", "Au retour", "Reprenez vos devises restantes en euros, billets de banque étrangers inclus selon disponibilité.")}
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Comment ça marche</p><h2>En trois temps</h2></header>
        <ol class="steps steps-3">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:phone-call:thin]]</span><h3>Vous appelez</h3><p>Pour confirmer que la devise est disponible et connaître le tarif du moment.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:id:thin]]</span><h3>Vous passez à l'agence</h3><p>Du lundi au vendredi, sans rendez-vous, avec une pièce d'identité.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:exchange:thin]]</span><h3>Vous repartez avec vos devises</h3><p>Le taux vous est communiqué avant la transaction.</p></li>
        </ol>
        <p class="mt"><a class="btn btn-gold" href="tel:{TEL_HREF}">Appeler pour une devise</a></p>
      </div>
    </section>

{faq_section("Le change", FAQ[3][1] + FAQ[0][1][:1], cls="")}

{others("change.html", "section-soft")}'''
page("change.html", "Bureau de change à Chartres — Devises | Godot &amp; Fils",
     "Bureau de change à Chartres : achat et vente de devises étrangères chez Godot & Fils, 23 rue de la Pie. Renseignez-vous par téléphone sur la devise souhaitée.", change)

# ---------------------------------------------------------------- NUMISMATIQUE
FORMULA_NUMIS = '''        <div class="formula formula-5" role="img" aria-label="Métal plus rareté plus état plus demande égale valeur">
          <div class="f-box">[[icon:scale:thin]]<strong>Métal</strong><span>poids et titre</span></div>
          <span class="f-op" aria-hidden="true">[[icon:plus]]</span>
          <div class="f-box">[[icon:diamond:thin]]<strong>Rareté</strong><span>tirage, millésime</span></div>
          <span class="f-op" aria-hidden="true">[[icon:plus]]</span>
          <div class="f-box">[[icon:eye-check:thin]]<strong>État</strong><span>grade de conservation</span></div>
          <span class="f-op" aria-hidden="true">[[icon:plus]]</span>
          <div class="f-box">[[icon:chart-line:thin]]<strong>Demande</strong><span>intérêt des collectionneurs</span></div>
          <span class="f-op" aria-hidden="true">[[icon:equal]]</span>
          <div class="f-box f-result">[[icon:medal:thin]]<strong>Valeur</strong><span>métal + prime de collection</span></div>
        </div>'''

GRADES = [("B", "Beau", "Pièce très usée, reliefs presque effacés."),
          ("TB", "Très beau", "Usure nette, mais les détails principaux restent lisibles."),
          ("TTB", "Très très beau", "Légère usure sur les points hauts du relief."),
          ("SUP", "Superbe", "Quelques traces de frottement, brillance d'origine en partie conservée."),
          ("SPL", "Splendide", "Presque neuve, infimes marques de manipulation."),
          ("FDC", "Fleur de coin", "État de frappe, sans aucune usure.")]
grade_rows = "\n".join(
    f'              <tr><th scope="row"><span class="grade">{a}</span></th><td>{n}</td><td>{d}</td></tr>' for a, n, d in GRADES)

numis = service_hero("Numismatique", "Pièces de collection", "Numismatique : quand une pièce vaut plus que son métal.",
    "Napoléon, Hercule, Semeuse, louis d'or… Faites estimer vos pièces de collection : nous distinguons la valeur du métal de la valeur numismatique.",
    "medal", [("medal", "Collection", "Valeur numismatique"), ("coin-euro", "0 €", "Estimation gratuite"), ("scale", "Métal + prime", "Estimation détaillée")]) + "\n" + subnav("numismatique.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Ce qui fait la valeur</p>
          <h2>Au-delà du métal</h2>
          <p>Une pièce de collection vaut d'abord par son métal, puis par ce qui la rend recherchée. Quatre éléments entrent en jeu.</p>
        </header>
{FORMULA_NUMIS}
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Les grandes familles</p>
          <h2>Quelles pièces pouvez-vous nous montrer ?</h2>
          <p>Toutes les pièces sont les bienvenues, des plus courantes aux plus anciennes.</p>
        </header>
        <div class="cards-feature cards-feature-dark">
          {feature("coins", "Pièces d'or françaises", "Napoléon (20 francs or), Coq, Génie, Semeuse et autres pièces d'or de la période du franc.")}
          {feature("diamond", "Pièces d'argent", "Hercule, Semeuse, Turin et autres pièces de 5, 10 ou 50 francs en argent.")}
          {feature("hourglass", "Monnaies anciennes", "Louis d'or, écus et monnaies royales ou impériales.")}
          {feature("exchange", "Pièces étrangères", "Souverain, Krugerrand, 50 pesos et autres pièces d'or ou d'argent du monde entier.")}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container split split-top">
        <div class="split-copy">
          <p class="eyebrow">L'état de conservation</p>
          <h2>Le grade change tout</h2>
          <p>Pour une même pièce, l'écart de prix peut être important entre un exemplaire usé et un exemplaire presque neuf. Les numismates utilisent une échelle de grades, du plus usé au plus beau.</p>
          <aside class="notice notice-light"><strong>Bon à savoir :</strong> la valeur de collection dépend du marché. Pour une pièce très rare, un avis spécialisé complémentaire peut être recommandé.</aside>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <caption>Les grades usuels</caption>
            <thead><tr><th scope="col">Grade</th><th scope="col">Signification</th><th scope="col">Aspect</th></tr></thead>
            <tbody>
{grade_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Conservation</p><h2>Protéger la valeur de vos pièces</h2></header>
        <ol class="tips tips-dark">
          <li><span class="tip-ico">[[icon:eye-check]]</span><div><h3>Ne nettoyez jamais</h3><p>Un nettoyage raye la surface et fait perdre une grande part de la valeur.</p></div></li>
          <li><span class="tip-ico">[[icon:coins]]</span><div><h3>Tenez par la tranche</h3><p>Évitez de toucher les faces : la peau laisse des traces durables.</p></div></li>
          <li><span class="tip-ico">[[icon:shield-check]]</span><div><h3>Protégez-les</h3><p>Capsules ou écrins, à l'abri de l'humidité et des chocs.</p></div></li>
          <li><span class="tip-ico">[[icon:file-certificate]]</span><div><h3>Gardez l'historique</h3><p>Factures, certificats ou notes de famille éclairent l'origine d'une pièce.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Comment ça marche</p><h2>Faire estimer ses pièces</h2></header>
        <ol class="steps steps-3 steps-light">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:coins:thin]]</span><h3>Vous apportez vos pièces</h3><p>À l'agence, telles qu'elles sont : sans les nettoyer.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:scale:thin]]</span><h3>Nous les examinons</h3><p>Identification, pesée, contrôle du titre et appréciation de l'état.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:receipt-euro:thin]]</span><h3>Vous recevez une estimation</h3><p>Valeur du métal et, le cas échéant, valeur de collection. Vous décidez ensuite.</p></li>
        </ol>
      </div>
    </section>

{faq_section("La numismatique", FAQ[4][1])}

{others("numismatique.html")}'''
page("numismatique.html", "Numismatique à Chartres — Estimation de pièces de collection | Godot &amp; Fils",
     "Pièces de collection à Chartres : Napoléon, Hercule, Semeuse, louis d'or. Valeur du métal et valeur numismatique, estimation gratuite chez Godot & Fils.", numis)

# ---------------------------------------------------------------- HISTOIRE (frise chronologique)
# ⚠ Dates et faits issus de sources publiques (sites du réseau, presse spécialisée) : à valider avec l'agence.
TIMELINE = [
    ("1933", "building-store", "Une maison née à Paris",
     "Godot &amp; Fils voit le jour en 1933. Son siège historique se trouve rue Vivienne, dans le quartier de la Bourse, à Paris.", ""),
    ("2017", "heart-handshake", "Le réseau s'ouvre à la proximité",
     "La maison ouvre sa première agence en franchise : son savoir-faire s'installe au plus près de ses clients.", ""),
    ("2020", "map-pin", "Chartres rejoint le réseau",
     "L'agence du 23 rue de la Pie ouvre ses portes, avec le même savoir-faire et un accueil de proximité en centre-ville.", ""),
    ("Aujourd'hui", "world", "Des agences partout en France",
     "De Paris à Marseille, de Lille à Bordeaux : retrouvez l'agence la plus proche de chez vous sur la carte du réseau.",
     '<a class="link-more" href="#reseau">Voir la carte</a>'),
]

def histoire_section():
    items = "".join(
        f'<li class="tl-item"><span class="tl-dot">[[icon:{ico}]]</span>'
        f'<div class="tl-card"><p class="tl-year">{y}</p><h3>{t}</h3><p>{d}</p>{link}</div></li>'
        for y, ico, t, d, link in TIMELINE)
    return f'''    <section class="section" id="histoire">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Notre histoire</p>
          <h2>Près d'un siècle de savoir-faire</h2>
          <p>Fondée en 1933, la maison Godot &amp; Fils s'est imposée comme une référence du négoce de l'or et des métaux précieux. Son réseau d'agences est présent dans de nombreuses villes, de Paris à Versailles en passant par Saint-Germain-en-Laye.</p>
        </header>
        <div class="history-stats">
          <div><strong data-since="1933">90+</strong><span>ans d'expérience</span></div>
          <div><strong>5</strong><span>domaines d'expertise</span></div>
          <div><strong>0 €</strong><span>pour une estimation</span></div>
        </div>
        <ol class="timeline" aria-label="Les grandes dates de la maison">{items}</ol>
        <p class="history-end">À Chartres, l'agence du 23 rue de la Pie perpétue cette tradition : une expertise rigoureuse, des conseils personnalisés et un accueil de proximité, dans le centre de la ville.</p>
      </div>
    </section>'''

# ---------------------------------------------------------------- LA MAISON
maison = hero("La maison", "Depuis 1933", "Une institution du négoce de métaux précieux.",
              "Depuis 1933, la maison Godot & Fils accompagne particuliers et épargnants dans l'achat et la vente d'or, d'argent et de métaux précieux.", actions=False) + '''

''' + histoire_section() + '''

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
               "Du lundi au vendredi, sans rendez-vous ; le samedi matin, sur rendez-vous. Pour un lot important ou une devise précise, un appel nous permet de mieux vous recevoir.", actions=False) + f'''

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
                  <tr data-day="6"><th scope="row">Samedi</th><td>Matin, sur rendez-vous</td></tr>
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
        <div class="map" data-map-consent>
          <iframe title="Plan d'accès à l'agence Godot &amp; Fils Chartres" data-src="https://maps.google.com/maps?q=23%20rue%20de%20la%20Pie%2C%2028000%20Chartres&amp;z=16&amp;output=embed" loading="lazy" hidden></iframe>
          <div class="map-placeholder">
            [[icon:map-pin:thin]]
            <h3>Plan d'accès</h3>
            <p>Le plan est fourni par Google Maps, qui peut déposer des cookies. Il ne s'affiche qu'avec votre accord.</p>
            <div class="hero-actions">
              <button type="button" class="btn btn-gold" data-consent-maps>Afficher le plan</button>
              <a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&amp;query=23+rue+de+la+Pie+28000+Chartres" target="_blank" rel="noopener">Ouvrir dans Google Maps</a>
            </div>
          </div>
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
     "Agence Godot & Fils Chartres : 23 rue de la Pie, 28000 Chartres. Ouvert du lundi au vendredi de 9h30 à 18h00, samedi matin sur rendez-vous. Tél. 02 37 83 49 77.", contact, ld=LD_STORE, cta=False)

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
        <p>Ce site ne collecte aucune donnée personnelle via formulaire et n'utilise aucun cookie de mesure d'audience ni de publicité. Les polices sont hébergées sur le site. Le plan d'accès de la page Contact est fourni par Google Maps, qui peut déposer des cookies : il n'est chargé qu'avec votre accord, que vous pouvez modifier à tout moment via « Gérer les cookies » en bas de page. Votre choix est mémorisé dans le stockage local de votre navigateur pendant 6 mois. Pour toute question relative à vos données, contactez l'agence.</p>
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
