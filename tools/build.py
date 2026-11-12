#!/usr/bin/env python3
"""Génère les pages statiques du site (python3 tools/build.py).
Édite le contenu ici, puis relance le script : en-tête, pied de page et navigation restent cohérents."""
import datetime, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.godotetfils-chartres.fr"
# Mode test : tant que INDEXABLE est False, aucune page n'est indexable (meta noindex, robots.txt, en-tête X-Robots-Tag, pas de sitemap).
# Pour ouvrir le site aux moteurs de recherche : passer INDEXABLE à True et relancer python3 tools/build.py.
INDEXABLE = False

import hashlib
def _asset_version():
    h = hashlib.md5()
    for rel in ("assets/css/style.css", "assets/js/main.js", "assets/js/consent.js"):
        h.update(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel), "rb").read())
    return h.hexdigest()[:8]

ASSET_V = _asset_version()

TEL, TEL_HREF = "02 37 83 49 77", "+33237834977"

SERVICES = [
    ("vendre-or.html", "Vendre or &amp; argent", "coin-euro", "Faites estimer et rachetez vos objets en or et en argent, sans rendez-vous."),
    ("acheter-or.html", "Acheter or &amp; argent", "coins", "Pièces et lingots d'or et d'argent, avec conseil personnalisé."),
    ("numismatique.html", "Numismatique", "medal", "Pièces de collection : valeur du métal et valeur numismatique."),
    ("argent-bijoux.html", "Argenterie &amp; bijoux", "diamond", "Argenterie, platine et bijoux anciens estimés avec soin."),
    ("change.html", "Bureau de change", "exchange", "Devises étrangères pour vos voyages, achat et vente."),
]
NAV = [(h, t) for h, t, _, _ in SERVICES] + [("la-maison.html", "La maison"), ("contact.html", "Contact")]

LD_STORE = {
    "@context": "https://schema.org", "@type": "JewelryStore", "@id": SITE + "/#agence",
    "name": "Godot & Fils Chartres", "image": SITE + "/assets/img/og-agence.jpg",
    "geo": {"@type": "GeoCoordinates", "latitude": 48.4456, "longitude": 1.4884},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=Godot+et+Fils+Chartres+23+rue+de+la+Pie",
    "areaServed": {"@type": "City", "name": "Chartres"},
    "description": "Achat et vente d'or, d'argent, de pièces, de lingots et de bijoux. Bureau de change.",
    "url": SITE + "/", "telephone": TEL_HREF, "foundingDate": "2020",
    "logo": SITE + "/assets/img/logo-noir.png",
    "address": {"@type": "PostalAddress", "streetAddress": "23 rue de la Pie", "postalCode": "28000",
                "addressLocality": "Chartres", "addressCountry": "FR"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:30", "closes": "18:00"}],
}

FAQ_G = {
 "avant": [
  ("Faut-il prendre rendez-vous ?", "Non, du lundi au vendredi de 9h30 à 18h00 : venez à l'agence sans rendez-vous. Le samedi matin, l'agence reçoit sur rendez-vous : appelez le 02 37 83 49 77. Pour un lot important, un appel au 02 37 83 49 77 nous permet de mieux vous recevoir."),
  ("L'estimation est-elle vraiment gratuite ?", "Oui. L'estimation et les conseils sont gratuits et sans engagement : vous êtes libre d'accepter ou non notre offre."),
  ("Quels documents dois-je apporter ?", "Une pièce d'identité en cours de validité, obligatoire pour toute vente de métaux précieux. Pour les pièces et lingots, apportez aussi les factures ou certificats d'achat si vous en avez : ils peuvent avoir une incidence sur la fiscalité applicable."),
 ],
 "vendre": [
  ("Comment est calculé le prix de rachat ?", "Le prix dépend du poids, du titre (pureté) du métal et du cours de l'or ou de l'argent au jour de la transaction. Les prix sont affichés en agence, avant même toute proposition. Pour certaines pièces de collection, la valeur numismatique peut également être prise en compte."),
  ("Rachetez-vous l'or et l'argent cassés ou abîmés ?", "Oui. Bijoux cassés, chaînes emmêlées, boucles d'oreilles orphelines, or dentaire, argenterie bosselée : tout est estimé selon sa teneur en métal précieux."),
  ("Puis-je vendre des lingots et des pièces d'investissement ?", "Oui. Les lingots, lingotins et pièces (Napoléon, Souverain, Krugerrand, Maple Leaf…) sont estimés au poids et au titre. Apportez vos justificatifs d'achat si vous les avez."),
  ("Que se passe-t-il si je refuse l'offre ?", "Rien : vous repartez avec vos objets, sans frais. L'estimation est faite devant vous, la décision vous appartient."),
  ("Mes bijoux sont-ils fondus ?", "Les bijoux rachetés pour leur métal sont généralement destinés au recyclage. Si vous souhaitez conserver une pièce de valeur, dites-le lors de l'estimation."),
 ],
 "acheter": [
  ("Puis-je acheter de l'or ou de l'argent pour investir ?", "Oui. Nous proposons des pièces et des lingots d'investissement en or et en argent. Contactez l'agence pour connaître les disponibilités et les tarifs du moment."),
  ("Quelle différence entre une pièce et un lingot ?", "Les pièces sont facilement divisibles et reconnues sur le marché ; les lingots, plus massifs, portent généralement une prime plus faible par gramme. Nous vous aidons à choisir selon votre projet."),
  ("Or ou argent : que choisir ?", "L'argent coûte moins cher au gramme, ce qui permet de démarrer avec un petit budget, mais son prix est en général plus volatil que celui de l'or. Les deux peuvent se combiner : nous vous conseillons selon votre projet."),
  ("Les prix changent-ils dans la journée ?", "Oui. Les prix de l'or et de l'argent suivent les marchés : le tarif applicable est celui du moment de la transaction. Les prix sont affichés en agence, avant même toute proposition ; vous pouvez aussi appeler pour connaître le tarif du jour."),
  ("Puis-je revendre mes pièces ou lingots plus tard ?", "Oui : l'or et l'argent physiques se revendent, au cours du moment. Conservez vos factures et certificats d'achat : ils peuvent avoir une incidence sur la fiscalité, dont les règles sont spécifiques."),
 ],
 "argent": [
  ("Rachetez-vous l'argenterie, même bosselée ou dépareillée ?", "Oui. Couverts, ménagères, plateaux et objets en argent massif sont estimés selon leur poids et leur titre, quel que soit leur état."),
  ("Comment savoir si mon objet est en argent massif ou en métal argenté ?", "Cherchez les poinçons : un titre (925 ou 800 par exemple) indique de l'argent massif. Un objet en « métal argenté » n'est qu'une fine couche d'argent sur un autre métal et vaut très peu pour son métal. En cas de doute, apportez-le : le contrôle est gratuit."),
  ("Estimez-vous aussi le platine ?", "Oui. Le platine est estimé comme les autres métaux précieux : au poids, au titre et au cours du jour."),
  ("Mon bijou n'a pas de poinçon, peut-il être estimé ?", "Oui. Le titre est contrôlé sur place, sous vos yeux, avant toute proposition."),
  ("Mes bijoux sont-ils fondus ?", "Les bijoux rachetés pour leur métal sont généralement destinés au recyclage. Si vous souhaitez conserver une pièce de valeur ou ancienne, dites-le lors de l'estimation."),
 ],
 "numis": [
  ("Une pièce rare vaut-elle plus que son poids d'or ?", "Parfois, oui. Au-delà du métal, la valeur numismatique dépend de la rareté (tirage, millésime), de l'état de conservation et de la demande des collectionneurs. Beaucoup de pièces courantes ne valent cependant que leur métal."),
  ("Dois-je nettoyer mes pièces avant de venir ?", "Non, jamais. Le nettoyage raye la surface et peut faire perdre une grande part de la valeur d'une pièce de collection. Apportez-la telle quelle."),
  ("Comment connaître la valeur de ma collection ?", "Apportez vos pièces à l'agence : l'estimation est gratuite et sans engagement. Elle distingue la valeur du métal et, le cas échéant, une valeur de collection."),
  ("Comment tenir et conserver mes pièces ?", "Tenez-les par la tranche, sans toucher les faces, et conservez-les à l'abri de l'humidité dans des capsules ou des écrins adaptés."),
 ],
 "change": [
  ("Puis-je changer des devises à l'agence ?", "Oui, l'agence est aussi bureau de change : achat et vente de devises étrangères, avant votre départ comme à votre retour de voyage."),
  ("Quelles devises sont disponibles ?", "Les devises disponibles varient : appelez-nous avant de venir pour confirmer celle dont vous avez besoin, au 02 37 83 49 77."),
  ("Quel taux de change appliquez-vous ?", "Les taux suivent les marchés et évoluent. Ils sont affichés en agence, avant même toute proposition ; vous pouvez aussi appeler l'agence pour connaître le taux du jour avant de vous déplacer."),
  ("Faut-il une pièce d'identité pour changer ?", "Oui, une pièce d'identité est à présenter au guichet."),
 ],
 "investir": [
  ("Vos informations constituent-elles un conseil en investissement ?", "Non, jamais. Les textes, chiffres, graphiques et simulations de ce site sont des informations générales à visée pédagogique : ce ne sont ni des conseils en investissement, ni des recommandations personnalisées, ni des offres d'achat ou de vente. Ils ne tiennent pas compte de votre situation. Investir comporte un risque de perte en capital et les performances passées ne préjugent pas des performances futures. Avant toute décision, rapprochez-vous d'un professionnel qualifié et indépendant."),
  ("Quel est le rendement annuel moyen de l'or ?", "Entre 2000 et 2025, le prix moyen de l'once a progressé d'environ 10,6 % par an en dollars (environ 8,5 % par an depuis 1971). Ce rendement varie fortement selon la période (environ +3,8 % par an entre 2010 et 2020), il ne tient compte ni des frais ni de la fiscalité, et les performances passées ne préjugent pas des performances futures."),
  ("L'or protège-t-il vraiment de l'inflation ?", "Sur le long terme, son prix a nettement dépassé l'inflation : en euros, l'once a été multipliée par environ 7 entre 2000 et 2024, contre ×1,5 pour les prix en France. Ce n'est pourtant pas vrai chaque année : en 2022, l'inflation a atteint 5,2 % alors que l'or est resté stable en dollars. Les performances passées ne préjugent pas des performances futures."),
  ("L'or est-il un placement sans risque ?", "Non. Son prix fluctue et peut stagner ou reculer pendant des années ; il ne verse ni dividende ni intérêt, et un investissement comporte un risque de perte en capital. Cette page est une information générale, pas un conseil en investissement."),
  ("Puis-je acheter de l'or physique à Chartres ?", "Oui. L'agence propose des pièces et des lingots d'investissement, selon les disponibilités : contactez-nous pour connaître les tarifs du moment."),
 ],
 "comparer": [
  ("Pourquoi déduire l'inflation ?", "Les prix augmentent d'année en année : 1 € d'aujourd'hui n'achète plus ce qu'il achetait en 2000. En déduisant l'inflation (indice des prix de l'Insee), on mesure l'évolution du pouvoir d'achat, et pas seulement du prix. L'option est décochée par défaut : cochez-la pour lire les rendements réels."),
  ("Comment est calculé le rendement annuel moyen ?", "C'est le taux de croissance annualisé sur la période choisie : le taux constant qui, appliqué chaque année, donnerait le même résultat final que les rendements réellement observés."),
  ("Pourquoi l'échelle logarithmique ?", "Elle rend lisibles des courbes très différentes sur un même graphique : à chaque graduation, la valeur double ou presque. Vous pouvez repasser en échelle linéaire à tout moment."),
  ("Ces résultats sont-ils garantis ?", "Non. Le simulateur applique un rendement moyen constant, ce qui ne se produit jamais en réalité : les bonnes et les mauvaises années alternent. Les performances passées ne préjugent pas des performances futures, et cet outil n'est pas un conseil en investissement."),
  ("D'où viennent les données ?", "Des sources citées en bas de page (LBMA, Insee, Notaires-Insee, Euronext…). Certaines séries (immobilier, Livret A, CAC 40 de 2002 à 2007) sont des estimations arrondies, signalées par le signe ≈."),
 ],
}
FAQ = [
    ("Avant de venir", FAQ_G["avant"]),
    ("Vendre", FAQ_G["vendre"]),
    ("Acheter", FAQ_G["acheter"]),
    ("Argenterie et bijoux", FAQ_G["argent"]),
    ("Numismatique", FAQ_G["numis"]),
    ("Change", FAQ_G["change"]),
    ("Investir et comparer", FAQ_G["investir"] + FAQ_G["comparer"][:2]),
]

def esc_json(o): return json.dumps(o, ensure_ascii=False, indent=2)

def header(active):
    cur = lambda h: ' aria-current="page"' if h == active else ""
    in_svc = active in [h for h, _, _, _ in SERVICES]
    items = "".join(
        f'<a href="{h}"{cur(h)}>[[icon:{ico}]]<span><strong>{t}</strong><small>{d}</small></span></a>' for h, t, ico, d in SERVICES)
    items += f'<a href="comparer.html"{cur("comparer.html")}>[[icon:scale]]<span><strong>Comparer les placements</strong><small>Or, actions, immobilier, Livret A : courbes et simulateur</small></span></a>'
    panel = (
        '<div class="container mega-inner">'
        f'<div class="mega-list"><p class="mega-title">Nos services</p><div class="mega-grid">{items}</div></div>'
        '<aside class="mega-aside"><p class="mega-title">Estimation gratuite</p>'
        '<p>Sans rendez-vous du lundi au vendredi, de 9h30 à 18h00. Le samedi matin, sur rendez-vous.</p>'
        f'<a class="btn btn-gold btn-sm" href="tel:{TEL_HREF}"><span>{TEL}</span></a>'
        '<a class="link-more" href="contact.html">Venir à l\'agence</a></aside>'
        '</div>')
    dd_cls = " is-current" if in_svc else ""
    return f'''  <a class="skip" href="#contenu">Aller au contenu</a>
  <header class="site-header" id="haut">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Godot &amp; Fils Chartres, accueil">
        <img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils">
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
          <a href="pourquoi-investir-or.html"{cur("pourquoi-investir-or.html")}>[[icon:chart-line]]<span>Pourquoi investir ?</span></a>
          <a href="la-maison.html"{cur("la-maison.html")}>[[icon:building-store]]<span>La maison</span></a>
          <a href="contact.html"{cur("contact.html")}>[[icon:map-pin]]<span>Contact</span></a>
        </div>
        <span class="menu-status" data-open-status data-short><span class="dot"></span><span class="status-text">Horaires d'ouverture</span></span>
        <a class="btn btn-gold btn-sm menu-cta" href="tel:{TEL_HREF}"><span>{TEL}</span></a>
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

_ref_path = os.path.join(ROOT, "tools", "references.json")
REFERENCES = json.load(open(_ref_path, encoding="utf-8")) if os.path.exists(_ref_path) else []
SOCIAL = [("facebook", "Facebook", "https://www.facebook.com/profile.php?id=100063818612511"),
          ("instagram", "Instagram", "https://www.instagram.com/godot.chartres/"),
          ("youtube", "YouTube", "https://www.youtube.com/channel/UCN-FwhVlacmvbK8Yno6wCug")]

def footer():
    refs = ""
    if REFERENCES:
        tiles = "".join(f'<li><img src="assets/img/references/{r["file"]}.webp" width="350" height="250" loading="lazy" decoding="async" alt="{r["alt"]}"></li>' for r in REFERENCES)
        refs = f'''
    <div class="container footer-refs" aria-label="Monnaies, institutions et moyens de paiement">
      <h3>Monnaies, institutions et moyens de paiement</h3>
      <ul>{tiles}</ul>
      <p>Les logos et marques cités appartiennent à leurs titulaires respectifs.</p>
    </div>'''
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener" aria-label="{n} (nouvelle fenêtre)">[[icon:{i}]]</a></li>' for i, n, u in SOCIAL)
    svc = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t, _, _ in SERVICES)
    return f'''  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <a class="brand brand-footer" href="index.html">
          <img src="assets/img/logo-blanc.png" width="650" height="133" alt="Godot &amp; Fils">
        </a>
        <p>Achat et vente d'or, d'argent et de métaux précieux. Bureau de change.</p>
        <ul class="social">{social}</ul>
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
          <li><a href="pourquoi-investir-or.html">Pourquoi investir dans l'or</a></li>
          <li><a href="comparer.html">Comparer les placements</a></li>
          <li><a href="faq.html">Questions fréquentes</a></li>
          <li><a href="contact.html">Contact &amp; accès</a></li>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><button type="button" class="linklike" data-consent-open>Gérer les cookies</button></li>
        </ul>
      </div>
    </div>
    {refs}
    <div class="container footer-bottom">
      <p>© <span data-year>2026</span> Godot &amp; Fils Chartres. Tous droits réservés.</p>
      <p class="footer-legal">Les informations de ce site sont données à titre indicatif et ne constituent jamais un conseil en investissement. Investir comporte un risque de perte en capital.</p>
    </div>
    <div class="credit-band"><p>Site designé et développé par <a href="https://oswaldsolutions.fr" target="_blank" rel="noopener">oswaldsolutions.fr</a></p></div>
  </footer>
  <a class="call-fab" href="tel:{TEL_HREF}" aria-label="Appeler l'agence au {TEL}">Appeler</a>
  <script src="assets/js/consent.js?v={ASSET_V}" defer></script>
  <script src="assets/js/main.js?v={ASSET_V}" defer></script>'''

SEO = {   # titres (≤ ~60 caractères) et descriptions (≤ ~155) par page ; "service" ajoute le balisage Service
    "index.html": ("Godot &amp; Fils Chartres | Achat et vente d'or et d'argent",
        "Agence Godot &amp; Fils à Chartres, 23 rue de la Pie : achat et vente d'or, d'argent, pièces, lingots et bijoux. Estimation gratuite, sans rendez-vous.", None),
    "vendre-or.html": ("Vendre son or et son argent à Chartres | Godot &amp; Fils",
        "Vendez or, argent, bijoux, pièces et lingots à Chartres. Estimation gratuite sous vos yeux, sans rendez-vous, prix affichés en agence. 23 rue de la Pie.", "Rachat d'or et d'argent"),
    "acheter-or.html": ("Acheter or et argent à Chartres : pièces, lingots | Godot &amp; Fils",
        "Achetez pièces et lingots d'or et d'argent à Chartres : Napoléon, Souverain, Krugerrand, Maple Leaf, Philharmonique. Conseils et prix en agence.", "Vente de pièces et lingots d'or et d'argent"),
    "numismatique.html": ("Numismatique à Chartres : estimation de pièces | Godot &amp; Fils",
        "Faites estimer vos pièces de collection à Chartres (Napoléon, Hercule, Semeuse, louis d'or) : valeur du métal et valeur numismatique. Gratuit.", "Estimation de pièces de collection"),
    "argent-bijoux.html": ("Argenterie, platine et bijoux à Chartres | Godot &amp; Fils",
        "Rachat d'argenterie, de pièces d'argent, de platine et de bijoux anciens à Chartres. Estimation gratuite et sans engagement chez Godot &amp; Fils.", "Rachat d'argenterie, platine et bijoux"),
    "change.html": ("Bureau de change à Chartres | Godot &amp; Fils",
        "Bureau de change à Chartres : achat et vente de devises étrangères avant ou après votre voyage. Taux affichés en agence, 23 rue de la Pie.", "Bureau de change"),
    "pourquoi-investir-or.html": ("Pourquoi investir dans l'or ? Rendements et risques | Godot &amp; Fils",
        "Rendement annuel moyen de l'or depuis 2000, effet de l'inflation, valeur refuge et risques. Information générale, jamais un conseil en investissement.", None),
    "comparer.html": ("Comparer or, actions, immobilier, Livret A | Godot &amp; Fils",
        "Comparez l'or, le S&amp;P 500, le CAC 40, l'immobilier et le Livret A depuis 2000 et simulez votre capital. Information générale, pas un conseil.", None),
    "la-maison.html": ("La maison Godot &amp; Fils : histoire et réseau d'agences",
        "Découvrez l'histoire de la maison Godot &amp; Fils, ses engagements, son réseau de 125 agences et l'agence de Chartres, 23 rue de la Pie.", None),
}
CRUMB = {"vendre-or.html": "Vendre or et argent", "acheter-or.html": "Acheter or et argent", "numismatique.html": "Numismatique",
         "argent-bijoux.html": "Argenterie et bijoux", "change.html": "Bureau de change", "pourquoi-investir-or.html": "Pourquoi investir dans l'or",
         "comparer.html": "Comparer les placements", "la-maison.html": "La maison", "contact.html": "Contact", "faq.html": "Questions fréquentes"}
OG_IMG = SITE + "/assets/img/og-agence.jpg"

def page(slug, title, desc, body, ld=None, cta=True, noindex=False):
    active = slug
    service = None
    if slug in SEO:
        title, desc, service = SEO[slug]
    lds = [ld] if ld else []
    if not noindex and slug != "index.html" and slug in CRUMB:
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": CRUMB[slug], "item": f"{SITE}/{slug}"}]})
    if service:
        lds.append({"@context": "https://schema.org", "@type": "Service", "name": service, "serviceType": service,
                    "provider": {"@id": SITE + "/#agence"}, "areaServed": {"@type": "City", "name": "Chartres"},
                    "url": f"{SITE}/{slug}", "description": re.sub(r"&amp;", "&", desc)})
    _og = os.path.join(ROOT, "assets", "img", "og", slug.replace(".html", "") + ".jpg")
    og_img = f"{SITE}/assets/img/og/{slug.replace('.html', '')}.jpg" if os.path.exists(_og) else OG_IMG
    ld_tag = "".join(f'\n  <script type="application/ld+json">\n{esc_json(x)}\n  </script>' for x in lds)
    noindex = noindex or not INDEXABLE
    robots = '\n  <meta name="robots" content="noindex, nofollow">' if noindex else ""
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
  <meta property="og:site_name" content="Godot &amp; Fils Chartres">
  <meta property="og:url" content="{SITE}/{"" if slug == "index.html" else slug}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{title}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og_img}">
  <meta name="theme-color" content="#000000">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/josefin-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/josefin-sans-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <script>document.documentElement.className+=" js"</script>
  <link rel="stylesheet" href="assets/css/style.css?v={ASSET_V}">{ld_tag}
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
    _wm = [0]
    def _wm_cls(m):
        _wm[0] += 1
        return f'<section class="{m.group(1)} wm-{"r" if _wm[0] % 2 else "l"}"'
    html = re.sub(r'<section class="([^"]*\bsection-dark\b[^"]*)"', _wm_cls, html)
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

STEPS_TIMELINE = '''        <ol class="tsteps">
          <li><span class="ts-label">Étape 1</span><h3>Vous passez à l'agence</h3><p>Sans rendez-vous, du lundi au vendredi, avec vos bijoux, pièces ou lingots.</p></li>
          <li><span class="ts-label">Étape 2</span><h3>Nous examinons devant vous</h3><p>Contrôle du titre et pesée de chaque objet, sous vos yeux.</p></li>
          <li><span class="ts-label">Étape 3</span><h3>Nous vous faisons une offre</h3><p>Une proposition détaillée, fondée sur le cours du jour. Vous restez libre de refuser.</p></li>
          <li><span class="ts-label">Étape 4</span><h3>Vous êtes payé</h3><p>Si vous acceptez, la transaction est finalisée avec un bordereau d'achat conforme à la réglementation.</p></li>
        </ol>'''

def steps_block(timeline=False):
    if timeline:
        return STEPS_TIMELINE
    return '''        <ol class="steps">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:building-store:thin]]</span><h3>Vous passez à l'agence</h3><p>Sans rendez-vous, du lundi au vendredi, avec vos bijoux, pièces ou lingots.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:scale:thin]]</span><h3>Nous examinons devant vous</h3><p>Contrôle du titre et pesée de chaque objet, sous vos yeux.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:receipt-euro:thin]]</span><h3>Nous vous faisons une offre</h3><p>Une proposition détaillée, fondée sur le cours du jour. Vous restez libre de refuser.</p></li>
          <li><span class="step-head"><span class="step-num">4</span>[[icon:cash-banknote:thin]]</span><h3>Vous êtes payé</h3><p>Si vous acceptez, la transaction est finalisée avec un bordereau d'achat conforme à la réglementation.</p></li>
        </ol>'''

ICON_ALIAS = {'facebook': 'facebook-logo', 'instagram': 'instagram-logo', 'youtube': 'youtube-logo', 'coin-euro': 'currency-eur', 'coins': 'coins', 'diamond': 'sketch-logo', 'diamonds': 'diamonds-four', 'exchange': 'swap', 'medal': 'coin', 'building-store': 'storefront', 'map-pin': 'map-pin', 'phone-call': 'phone-call', 'clock': 'clock', 'id': 'identification-card', 'file-certificate': 'certificate', 'eye-check': 'eye', 'heart-handshake': 'handshake', 'shield-check': 'shield-check', 'scale': 'scales', 'receipt-euro': 'receipt', 'cash-banknote': 'money', 'chart-line': 'chart-line-up', 'plus': 'plus', 'equal': 'equals', 'x': 'x', 'chevron-down': 'caret-down', 'chevron-left': 'caret-left', 'chevron-right': 'caret-right', 'star': 'star', 'zoom-check': 'magnifying-glass', 'world': 'globe-hemisphere-west', 'hourglass': 'hourglass', 'dental': 'tooth', 'tools-kitchen-2': 'fork-knife', 'plane-departure': 'airplane-takeoff', 'plane-arrival': 'airplane-landing', 'star-fill': 'star-fill'}

def ic(name, weight="light", cls="ic"):
    """Inline un SVG Phosphor Icons (assets/icons/, licence MIT). weight : light (défaut) ou thin (grands pictogrammes)."""
    target = ICON_ALIAS[name]
    fname = "star-fill-fill" if target == "star-fill" else f"{target}-{weight}"
    raw = open(os.path.join(ROOT, "assets", "icons", fname + ".svg"), encoding="utf-8").read()
    inner = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")].strip()
    return f'<svg class="{cls}" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{inner}</svg>'

# Dans les gabarits, [[icon:nom]] est remplacé par le SVG correspondant (voir page())
ICON = {"or": "[[icon:coin-euro]]", "pieces": "[[icon:coins]]", "argent": "[[icon:diamond]]", "change": "[[icon:exchange]]"}

# ---------------------------------------------------------------- GALERIE DE L'AGENCE
PHOTOS = [
    ("agence-facade.webp", 819, 610, "Devanture de l'agence Godot & Fils au 23 rue de la Pie à Chartres, avec ses pièces et lingots en vitrine",
     "La devanture, 23 rue de la Pie"),
    ("agence-accueil.webp", 820, 610, "Hall d'accueil de l'agence Godot & Fils : guichet vitré, diplômes encadrés et plante verte",
     "Le hall d'accueil et son guichet vitré"),
    ("agence-salon.webp", 820, 610, "Espace d'attente de l'agence Godot & Fils avec fauteuils blancs et table basse",
     "L'espace d'attente"),
]

def agence_gallery(dark=True):
    esc = lambda t: t.replace("&", "&amp;")
    figs = "".join(
        f'<figure class="g-item{" g-main" if i == 0 else ""}"><button type="button" class="g-btn" data-lightbox="assets/img/{f}" '
        f'data-alt="{esc(alt)}" data-caption="{esc(cap)}" aria-label="Agrandir la photo : {esc(cap)}">'
        f'<img src="assets/img/{f}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async"></button>'
        f'<figcaption>{esc(cap)}</figcaption></figure>'
        for i, (f, w, h, alt, cap) in enumerate(PHOTOS))
    return f'''    <section class="section{" section-dark" if dark else ""}" id="agence">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">L'agence</p>
          <h2>Une agence sécurisée, au cœur de Chartres</h2>
          <p>Du lundi au vendredi, sans rendez-vous : un hall d'accueil, un guichet vitré et un espace d'attente. Agence sécurisée et télésurveillée.</p>
        </header>
        <div class="gallery">{figs}</div>
      </div>
    </section>'''

# ---------------------------------------------------------------- AVIS GOOGLE
# Les avis viennent de tools/avis.json (à remplir avec de VRAIS avis : copier-coller depuis Google Business Profile).
# Tant que la liste est vide, la section n'est pas générée.
G_LOGO = ('<svg class="review-g" viewBox="0 0 48 48" role="img" aria-label="Google" width="22" height="22">'
          '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
          '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
          '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
          '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>')

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
            f'<article class="review"><div class="review-top"><div class="review-stars" role="img" aria-label="{n} sur 5">{stars(n)}</div>{G_LOGO}</div>'
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

def tel_href(t):
    d = re.sub(r"[^\d+]", "", t)
    if d.startswith("+"):
        return d
    if d.startswith("00"):
        return "+" + d[2:]
    if d.startswith(("0590", "0690", "0694", "0596", "0262", "0692")):   # outre-mer : numérotation nationale
        return d
    return "+33" + d[1:] if d.startswith("0") else d

def reseau_section():
    m = json.load(open(os.path.join(ROOT, "tools", "geo", "france-map.json"), encoding="utf-8"))
    groups = {}
    for v in m["villes"]:
        key = v.get("pin", v["ville"])
        g = groups.setdefault(key, {"titre": GROUP_TITLES.get(key, key).replace("&amp;", "&").replace("&", "&amp;"), "x": v.get("x"), "y": v.get("y"), "local": False, "agences": []})
        g["local"] = g["local"] or v.get("local", False)
        g["agences"] += v["agences"]
    n_ag = sum(len(g["agences"]) for g in groups.values())
    n_vi = len([v for v in m["villes"] if not v.get("nopin")])
    pins, chips, panels = [], [], []
    for key, g in sorted(groups.items(), key=lambda kv: kv[1]["titre"].replace("Î", "I")):
        sid, n = "p-" + slug(key), len(g["agences"])
        r = min(6 + (n - 1) * 1.1, 12)
        cls = "pin pin-local" if g["local"] else "pin"
        label = f'{g["titre"]}, {n} agence{"s" if n > 1 else ""}'.replace("&amp;", "et")
        if g["x"] is not None: pins.append(f'''          <g class="{cls}" data-target="{sid}" tabindex="0" role="button" aria-label="{label}" transform="translate({g["x"]} {g["y"]})">
            <circle class="pin-hit" r="18"/><circle class="pin-halo" r="{r + 5:.1f}"/><circle class="pin-dot" r="{r:.1f}"/>
            <title>{g["titre"]}</title>
          </g>''')
        chips.append(f'<li><button type="button" class="chip{" chip-local" if g["local"] else ""}" data-target="{sid}">{g["titre"]}</button></li>')
        items = []
        for a in g["agences"]:
            adr = a.get("adresse") or "Adresse à confirmer auprès de l'agence"
            adr = adr.replace("&", "&amp;")
            tel = f'<a href="tel:{tel_href(a["tel"])}">{a["tel"]}</a>' if a.get("tel") else ""
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
        <p class="map-note">{n_ag} agences du réseau, regroupées en {n_vi} points. Liste issue de la <a class="text-link-light" href="{m["officielle"]}" target="_blank" rel="noopener">liste officielle des agences</a> : le réseau évolue, consultez-la pour les dernières ouvertures.</p>
      </div>
    </section>'''

# ---------------------------------------------------------------- ACCUEIL
FAQ_CLS = "section"   # alternance des fonds selon la présence des avis
TICKER = "".join(f"<span>{w}</span>" for w in ["Achat d'or", "Vente de pièces", "Lingots", "Argent", "Bijoux", "Bureau de change"] * 6)
home = f'''    <section class="hero hero-photo">
      <picture class="hero-bg" aria-hidden="true">
        <img src="assets/img/devanture.webp" srcset="assets/img/devanture-1280.webp 1280w, assets/img/devanture.webp 1920w" sizes="100vw" width="1920" height="800" alt="" fetchpriority="high" decoding="async">
      </picture>
      <div class="hero-shade" aria-hidden="true"></div>
      <div class="container hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Or · Argent · Pièces · Lingots · Bijoux · Change</p>
          <h1>Votre or et votre argent estimés à leur <em>juste valeur</em>, au cœur de Chartres.</h1>
          <p class="lead">Achat et vente d'or, d'argent et de métaux précieux à Chartres. Estimation gratuite, sans engagement et sans rendez-vous.</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="contact.html">Venir à l'agence</a>
            <a class="btn btn-ghost" href="tel:{TEL_HREF}">Appeler l'agence</a>
          </div>
          <ul class="hero-proof" aria-label="Nos engagements">
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
          <p>Que vous souhaitiez vendre des bijoux hérités, investir dans l'or et l'argent physiques ou préparer un voyage, l'agence vous reçoit et vous conseille.</p>
        </header>
        <div class="bento">
          <a class="bento-card bento-vendre" href="vendre-or.html">
            <img class="bento-img" src="assets/img/or-pieces-lingots-gros-plan.webp" alt="" width="1000" height="667" loading="lazy" decoding="async">
            <span class="bento-body">
              <span class="bento-top"><span class="bento-num" aria-hidden="true">01</span><span class="bento-ic" aria-hidden="true">{ICON["or"]}</span></span>
              <h3>Vendre or &amp; argent</h3>
              <p>Bijoux, débris, alliances, chaînes, argenterie, pièces et lingots : nous rachetons votre or et votre argent, quel que soit leur état.</p>
              <span class="bento-more">Découvrir</span>
            </span>
          </a>
          <a class="bento-card bento-acheter" href="acheter-or.html">
            <img class="bento-img" src="assets/img/or-lingots-pieces.webp" alt="" width="1000" height="667" loading="lazy" decoding="async">
            <span class="bento-body">
              <span class="bento-top"><span class="bento-num" aria-hidden="true">02</span><span class="bento-ic" aria-hidden="true">{ICON["pieces"]}</span></span>
              <h3>Acheter or &amp; argent</h3>
              <p>Napoléon, Souverain, Krugerrand, Maple Leaf argent, lingots et lingotins : constituez une épargne tangible, conseillé par des spécialistes.</p>
              <span class="bento-more">Découvrir</span>
            </span>
          </a>
          <a class="bento-card bento-argent" href="argent-bijoux.html">
            <img class="bento-img" src="assets/img/argent-lingot-100-onces.webp" alt="" width="1000" height="667" loading="lazy" decoding="async">
            <span class="bento-body">
              <span class="bento-top"><span class="bento-num" aria-hidden="true">03</span><span class="bento-ic" aria-hidden="true">{ICON["argent"]}</span></span>
              <h3>Argenterie &amp; bijoux</h3>
              <p>Argenterie, pièces d'argent, platine, bijoux anciens ou démodés : une expertise attentive pour chaque pièce.</p>
              <span class="bento-more">Découvrir</span>
            </span>
          </a>
          <a class="bento-card bento-change" href="change.html">
            <img class="bento-img" src="assets/img/change-billets-devises.webp" alt="" width="1000" height="667" loading="lazy" decoding="async">
            <span class="bento-body">
              <span class="bento-top"><span class="bento-num" aria-hidden="true">04</span><span class="bento-ic" aria-hidden="true">{ICON["change"]}</span></span>
              <h3>Bureau de change</h3>
              <p>Achat et vente de devises étrangères pour vos voyages ou au retour : un service simple, sur place.</p>
              <span class="bento-more">Découvrir</span>
            </span>
          </a>
        </div>
      </div>
    </section>

    <section class="section section-dark" id="estimation">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Comment ça marche</p>
          <h2>Vendre votre or ou votre argent en quatre étapes</h2>
          <p>Un parcours transparent, en face à face, pour que vous décidiez en toute sérénité.</p>
        </header>
{steps_block(True)}
        <p class="steps-note"><strong>À prévoir :</strong> une pièce d'identité en cours de validité est obligatoire pour toute vente de métaux précieux.</p>
      </div>
    </section>

    <section class="section" id="maison">
      <div class="container split">
        <figure class="split-photo"><img src="assets/img/agence-facade.webp" width="819" height="610" alt="Devanture de l'agence Godot &amp; Fils au 23 rue de la Pie à Chartres" loading="lazy" decoding="async"></figure>
        <div class="split-copy">
          <p class="eyebrow">La maison</p>
          <h2>Une institution du négoce de métaux précieux</h2>
          <p>La maison Godot &amp; Fils s'est imposée comme une référence du négoce de l'or, de l'argent et des métaux précieux. Son réseau d'agences est présent dans de nombreuses villes, de Paris à Versailles en passant par Saint-Germain-en-Laye.</p>
          <p>À Chartres, notre agence perpétue ce savoir-faire : une expertise rigoureuse, des conseils personnalisés et un accueil de proximité.</p>
          <ul class="checks">
            <li>Expertise réalisée sur place, sous vos yeux</li>
            <li>Offre fondée sur le cours du jour</li>
            <li>Confidentialité et transactions sécurisées</li>
            <li>Conseils pour l'investissement dans l'or et l'argent physiques</li>
          </ul>
          <p class="mt"><a class="btn btn-outline" href="la-maison.html">Découvrir la maison</a></p>
        </div>
      </div>
    </section>

{reseau_section()}

{avis_section()}

    <section class="section section-dark prices" id="cours" aria-labelledby="cours-title" data-prices hidden>
      <div class="container">
        <header class="prices-head">
          <div>
            <p class="eyebrow">Cours en direct</p>
            <h2 id="cours-title">L'or et l'argent aujourd'hui</h2>
            <p class="prices-live"><span class="dot" aria-hidden="true"></span><span data-prices-time>Mise à jour…</span></p>
          </div>
          <div class="seg" role="group" aria-label="Période de la courbe">
            <button type="button" data-range="1d" aria-pressed="false">1 j</button>
            <button type="button" data-range="7d" aria-pressed="false">7 j</button>
            <button type="button" data-range="1m" aria-pressed="false">1 mois</button>
            <button type="button" data-range="1y" aria-pressed="false">1 an</button>
            <button type="button" data-range="5y" class="is-on" aria-pressed="true">5 ans</button>
          </div>
        </header>
        <div class="prices-grid" aria-live="polite">
          <article class="price-card" data-metal="or">
            <h3><span class="sw" style="--c:#e2ab45"></span>Or</h3>
            <p class="price-main"><strong data-p="or-g">—</strong><span>€ / gramme</span><em class="price-var" data-var="or"></em></p>
            <p class="price-sub"><span data-p="or-oz">—</span> € l'once troy</p>
            <div class="price-chart" data-pchart="or" role="img" aria-label="Évolution du cours de l'or"></div>
          </article>
          <article class="price-card" data-metal="argent">
            <h3><span class="sw" style="--c:#cfd3d8"></span>Argent</h3>
            <p class="price-main"><strong data-p="argent-g">—</strong><span>€ / gramme</span><em class="price-var" data-var="argent"></em></p>
            <p class="price-sub"><span data-p="argent-oz">—</span> € l'once troy</p>
            <div class="price-chart" data-pchart="argent" role="img" aria-label="Évolution du cours de l'argent"></div>
          </article>
        </div>
        <p class="price-source" data-source>Source : cours instantané gold-api.com · historique Stooq / Yahoo Finance · taux de change BCE (Frankfurter).</p>
        <div class="price-cta">
          <p>Pour estimer vos bijoux, pièces ou lingots, ce sont le poids, le titre et le cours du moment qui comptent.</p>
          <a class="btn btn-gold" href="vendre-or.html">Faire estimer mon or ou mon argent</a>
        </div>
        <p class="note prices-note">Cours spot indicatif des marchés internationaux (métal pur, hors frais et primes), converti en euros. Ce n'est pas le prix de rachat ou de vente de l'agence : le tarif applicable est celui du moment de la transaction. Les prix et les taux sont affichés en agence, avant même toute proposition. Ces cours sont donnés à titre purement informatif : ils ne constituent ni un conseil en investissement, ni une recommandation, ni une offre d'achat ou de vente. Les performances passées ne préjugent pas des performances futures.</p>
      </div>
    </section>

    <section class="{FAQ_CLS}" id="faq">
      <div class="container narrow">
        <header class="section-head">
          <p class="eyebrow">Questions fréquentes</p>
          <h2>Vous vous posez des questions ?</h2>
        </header>
        <div class="faq">
{faq_block(FAQ_G["avant"] + FAQ_G["vendre"][:1])}
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

HERO_IMG = {
    "Vendre or &amp; argent": ("or-pieces-lingots-gros-plan", "Lingots et pièces d'or : Krugerrand, Philharmonique et lingots d'un kilo", "50% 55%"),
    "Acheter or &amp; argent": ("or-lingots-pieces", "Tas de lingots d'or d'un kilo et de pièces d'investissement sur fond noir", "45% 55%"),
    "Argenterie &amp; bijoux": ("argent-lingot-100-onces", "Lingot d'argent pur de 100 onces posé sur des lingots d'argent bruts", "45% 50%"),
    "Pourquoi investir dans l'or": ("or-lingots-gros-plan", "Gros plan sur des lingots d'or fin 999,9", "50% 50%"),
    "Change": ("change-billets-devises", "Billets de nombreuses devises étrangères : dollars, pesos, yuans, roupies", "50% 50%"),
    "Numismatique": ("numismatique-pieces-anciennes", "Pièces anciennes de collection en argent, bronze et cuivre posées sur du bois", "40% 50%"),
    "Comparer les placements": ("argent-lingotins", "Lingots et lingotins d'argent fin de plusieurs formats", "50% 50%"),
}

def service_hero(crumb, eyebrow, h1, lead, icon, facts):
    fl = "".join(f'<li>[[icon:{i_}:thin]]<div><strong>{big}</strong><span>{small}</span></div></li>' for i_, big, small in facts)
    if crumb in HERO_IMG:
        f_, alt, pos = HERO_IMG[crumb]
        side = (f'<figure class="facts-photo" style="--pos:{pos}"><img src="assets/img/{f_}.webp" width="1000" height="667" alt="{alt}" decoding="async" fetchpriority="high">'
                f'<figcaption class="facts-over"><ul>{fl}</ul></figcaption></figure>')
    else:
        side = f'''<aside class="facts-card" aria-label="L'essentiel">
          <div class="facts-mark" aria-hidden="true">[[icon:{icon}:thin]]</div>
          <ul>{fl}</ul>
        </aside>'''
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
        {side}
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
vendre = service_hero("Vendre or &amp; argent", "Rachat d'or et d'argent à Chartres", "Vendre mon or et mon argent à Chartres, au prix du jour.",
    "Bijoux, alliances, or dentaire, argenterie, pièces, lingots : faites estimer vos objets gratuitement, sous vos yeux, sans rendez-vous et sans engagement.",
    "coin-euro", [("coin-euro", "0 €", "Estimation gratuite"), ("building-store", "Sans RDV", "Du lundi au vendredi"), ("scale", "Sous vos yeux", "Pesée et contrôle du titre")]) + "\n" + subnav("vendre-or.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Ce que nous rachetons</p>
          <h2>Tout objet contenant de l'or ou de l'argent</h2>
          <p>L'état n'a pas d'importance : le prix repose sur le poids et la pureté du métal.</p>
        </header>
        <div class="cards-feature">
          {feature("diamond", "Bijoux", "Bagues, colliers, bracelets, chaînes, médailles, boucles d'oreilles, même cassés, démodés ou dépareillés.")}
          {feature("heart-handshake", "Alliances &amp; gourmettes", "Alliances anciennes, bagues de famille, gourmettes et chevalières dont vous n'avez plus l'usage.")}
          {feature("dental", "Or dentaire", "Couronnes, bridges et autres pièces dentaires en or sont estimés selon leur teneur en métal précieux.")}
          {feature("coins", "Pièces d'or &amp; d'argent", "Napoléon, Souverain, Krugerrand, 50 pesos, Hercule, Semeuse et autres pièces d'or ou d'argent de collection ou d'investissement.")}
          {feature("tools-kitchen-2", "Argenterie", "Couverts, ménagères, plateaux et objets en argent massif, même bosselés ou dépareillés.")}
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
          <p>Le prix de rachat dépend du poids de l'objet, de son titre (la proportion de métal pur, gravée par un poinçon) et du cours de l'or ou de l'argent au moment de la transaction. Les prix et les taux sont affichés en agence, avant même toute proposition.</p>
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
                <caption>Les titres de l'or et de l'argent les plus courants</caption>
                <thead><tr><th scope="col">Métal</th><th scope="col">Titre (pureté)</th><th scope="col">Teneur en métal pur</th></tr></thead>
                <tbody>
                  <tr><th scope="row">24 carats</th><td>999 ‰</td><td>99,9 %</td></tr>
                  <tr><th scope="row">18 carats</th><td>750 ‰</td><td>75 %</td></tr>
                  <tr><th scope="row">14 carats</th><td>585 ‰</td><td>58,5 %</td></tr>
                  <tr><th scope="row">9 carats</th><td>375 ‰</td><td>37,5 %</td></tr>
                  <tr><th scope="row">Argent 925</th><td>925 ‰</td><td>92,5 % d'argent</td></tr>
                  <tr><th scope="row">Argent 800</th><td>800 ‰</td><td>80 % d'argent</td></tr>
                </tbody>
              </table>
            </div>
            <p class="note">En France, l'or 18 carats (750 ‰) est le plus répandu en bijouterie, et l'argent 925 (« sterling ») en argenterie et en bijoux.</p>
          </div>
        </div>
      </div>
    </section>

{faq_section("Vendre son or et son argent", FAQ_G["avant"][:1] + FAQ_G["avant"][2:] + FAQ_G["vendre"])}

{others("vendre-or.html")}'''
page("vendre-or.html", "Vendre son or et son argent à Chartres — Rachat d'or, d'argent, bijoux et pièces | Godot &amp; Fils",
     "Vendez votre or et votre argent à Chartres : bijoux, alliances, or dentaire, argenterie, pièces et lingots. Estimation gratuite et sans rendez-vous chez Godot & Fils, 23 rue de la Pie.", vendre)

# ---------------------------------------------------------------- ACHETER
COINS = [
    ("20 francs Napoléon", "France", "900 ‰", "5,81"),
    ("Souverain", "Royaume-Uni", "916,7 ‰", "7,32"),
    ("Krugerrand (1 once)", "Afrique du Sud", "916,7 ‰", "31,1"),
    ("Maple Leaf (1 once)", "Canada", "999,9 ‰", "31,1"),
    ("Philharmonique (1 once)", "Autriche", "999,9 ‰", "31,1"),
]
COINS_AG = [
    ("Maple Leaf argent (1 once)", "Canada", "999,9 ‰", "31,1"),
    ("Philharmonique argent (1 once)", "Autriche", "999 ‰", "31,1"),
    ("Silver Eagle (1 once)", "États-Unis", "999 ‰", "31,1"),
    ("Britannia argent (1 once)", "Royaume-Uni", "999 ‰", "31,1"),
]
COIN_IMG = {"20 francs Napoléon": "napoleon-20-francs", "Souverain": "souverain", "Krugerrand (1 once)": "krugerrand",
            "Philharmonique (1 once)": "philharmonique", "Maple Leaf argent (1 once)": "maple-leaf-argent",
            "Silver Eagle (1 once)": "silver-eagle", "Britannia argent (1 once)": "britannia-argent"}
_cred_path = os.path.join(ROOT, "tools", "pieces-credits.json")
COIN_CREDITS = json.load(open(_cred_path, encoding="utf-8")) if os.path.exists(_cred_path) else {}

def coin_card(n, o, t, g, metal):
    slug = COIN_IMG.get(n)
    if slug and os.path.exists(os.path.join(ROOT, "assets", "img", "pieces", slug + ".webp")):
        visual = (f'<div class="coin-photo"><img src="assets/img/pieces/{slug}.webp" width="360" height="360" loading="lazy" decoding="async" '
                  f'alt="Pièce {n}"></div>')
    else:
        visual = f'<div class="medal"><strong>{g}</strong><span>g {metal} fin</span></div>'
    return (f'          <article class="coin-card">{visual}<h3>{n}</h3><dl><div><dt>Origine</dt><dd>{o}</dd></div>'
            f'<div><dt>Titre</dt><dd>{t}</dd></div><div><dt>Métal fin</dt><dd>{g} g</dd></div></dl></article>')

coin_cards = "\n".join(coin_card(n, o, t, g, m) for m, lst in (("d'or", COINS), ("d'argent", COINS_AG)) for n, o, t, g in lst)

CLASSIQUES_OR = ["Pièces Napoléon 20 F or (effigies Napoléon ou Marianne-Coq)",
                 "Lingots et lingotins des fondeurs suisses : 5 g, 10 g, 20 g, 50 g, 100 g, 250 g, 500 g et 1 kg",
                 "Pièce Krugerrand 1 once", "Pièce Souverain britannique", "Pièce Croix Suisse", "Pièce Union Latine",
                 "Pièces 20 dollars US, 10 dollars US", "Maple Leaf, once moderne neuve", "Philharmonique, once moderne neuve",
                 "… et bien d'autres"]
CLASSIQUES_AG = ["Pièces françaises : Semeuse 1 F, 2 F, 5 F, Hercule 10 F, 50 F, Turin, moderne 100 F",
                 "Maple Leaf, once moderne neuve", "Philharmonique, once moderne neuve", "Silver Eagle, once moderne neuve",
                 "Lingots 500 g et 1 kg"]

def classiques():
    li = lambda items: "".join(f"<li>{t}</li>" for t in items)
    return f'''<div class="classics">
          <h3 class="classics-title">Tous les classiques de l'or et de l'argent « boursables »</h3>
          <div class="classics-grid">
            <div class="classics-col"><h4><span class="sw" style="--c:#e2ab45"></span>L'or</h4><ul class="checks">{li(CLASSIQUES_OR)}</ul></div>
            <div class="classics-col"><h4><span class="sw" style="--c:#cfd3d8"></span>L'argent</h4><ul class="checks">{li(CLASSIQUES_AG)}</ul></div>
          </div>
        </div>'''

def coin_credits():
    if not COIN_CREDITS:
        return ""
    items = []
    for slug, c in COIN_CREDITS.items():
        lic = f'<a href="{c["licurl"]}" target="_blank" rel="noopener">{c["license"]}</a>' if c.get("licurl") else c["license"]
        artist = (c["artist"] or "auteur inconnu").replace("&", "&amp;")
        items.append(f'<li><a href="{c["page"]}" target="_blank" rel="noopener">{c["titre"].rsplit(".", 1)[0]}</a> : {artist}, {lic}</li>')
    return ('<details class="photo-credits"><summary>Crédits des photos</summary><ul>' + "".join(items) +
            '</ul><p>Photographies Wikimedia Commons, utilisées selon leurs licences ; certaines ont été recadrées.</p></details>')

acheter = service_hero("Acheter or &amp; argent", "Or &amp; argent d'investissement", "Acheter de l'or et de l'argent physiques : pièces et lingots.",
    "Une épargne tangible, détenue en main propre. L'agence vous conseille selon votre projet et les disponibilités du moment.",
    "coins", [("coins", "Pièces &amp; lingots", "Selon les disponibilités"), ("shield-check", "Conseil", "Personnalisé, sans pression"), ("phone-call", "Tarif du jour", "Sur simple appel")]) + "\n" + subnav("acheter-or.html") + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Pourquoi de l'or et de l'argent physiques</p>
          <h2>Un actif tangible, reconnu partout</h2>
          <p>L'or et l'argent sont des métaux que l'on peut détenir, transmettre et revendre. Ils se prêtent à la diversification d'une épargne.</p>
          <p><a class="text-link" href="pourquoi-investir-or.html">Pourquoi investir dans l'or ? Rendements, inflation, risques</a></p>
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
        {classiques()}
        {coin_credits()}
        <aside class="notice"><strong>Bon à savoir :</strong> les prix de l'or et de l'argent varient en permanence et sont affichés en agence, avant même toute proposition. Un investissement comporte un risque de perte en capital et la fiscalité des métaux précieux a ses propres règles : renseignez-vous avant d'acheter. Les informations de ce site ne constituent jamais un conseil en investissement ni une recommandation personnalisée.</aside>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head"><p class="eyebrow">Comment acheter</p><h2>Simple, sur place</h2></header>
        <ol class="steps steps-3 steps-light">
          <li><span class="step-head"><span class="step-num">1</span>[[icon:phone-call:thin]]</span><h3>Vous nous contactez</h3><p>Par téléphone ou directement à l'agence, pour connaître les produits disponibles et les tarifs du moment.</p></li>
          <li><span class="step-head"><span class="step-num">2</span>[[icon:shield-check:thin]]</span><h3>Nous vous conseillons</h3><p>Pièces ou lingots, budget, horizon : nous vous aidons à choisir sans pression.</p></li>
          <li><span class="step-head"><span class="step-num">3</span>[[icon:coins:thin]]</span><h3>Vous repartez avec votre or ou votre argent</h3><p>La transaction est finalisée à l'agence, avec les documents réglementaires. Une pièce d'identité est requise.</p></li>
        </ol>
      </div>
    </section>

{faq_section("Acheter or et argent", FAQ_G["acheter"] + FAQ_G["avant"][2:])}

{others("acheter-or.html")}'''
page("acheter-or.html", "Acheter or et argent à Chartres — Pièces et lingots d'investissement | Godot &amp; Fils",
     "Achetez de l'or et de l'argent physiques à Chartres : Napoléon, Souverain, Krugerrand, Maple Leaf, Silver Eagle, lingots et lingotins. Conseils personnalisés chez Godot & Fils.", acheter)

# ---------------------------------------------------------------- ARGENT & BIJOUX
argent = service_hero("Argenterie &amp; bijoux", "Argent · Platine · Bijoux", "Argent, platine et bijoux : une expertise pour chaque pièce.",
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

{faq_section("Argenterie, platine et bijoux", FAQ_G["argent"], cls="section-dark")}

{others("argent-bijoux.html")}'''
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
          <p>Avant un voyage ou après un séjour à l'étranger, l'agence vous accueille pour changer vos euros en devises, ou vos devises en euros. Les devises disponibles varient selon les périodes. Les prix et les taux sont affichés en agence, avant même toute proposition.</p>
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

{faq_section("Le change", FAQ_G["change"] + FAQ_G["avant"][:1], cls="")}

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

{faq_section("La numismatique", FAQ_G["numis"] + FAQ_G["avant"][:1])}

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
          <p>Fondée en 1933, la maison Godot &amp; Fils s'est imposée comme une référence du négoce de l'or, de l'argent et des métaux précieux. Son réseau d'agences est présent dans de nombreuses villes, de Paris à Versailles en passant par Saint-Germain-en-Laye.</p>
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

# ---------------------------------------------------------------- POURQUOI INVESTIR DANS L'OR
# Données : prix moyen annuel de l'once d'or (fixing LBMA PM, USD, arrondi) — LBMA / NMA / MetalCharts.
# Inflation : INSEE (coefficients de transformation de l'euro, base 2025 : 66,08 en 2000, 99,07 en 2024 -> ×1,50).
GOLD_AVG = {2000: 279, 2001: 271, 2002: 310, 2003: 363, 2004: 410, 2005: 445, 2006: 603, 2007: 695, 2008: 872,
            2009: 972, 2010: 1225, 2011: 1572, 2012: 1669, 2013: 1411, 2014: 1266, 2015: 1160, 2016: 1251,
            2017: 1257, 2018: 1269, 2019: 1393, 2020: 1770, 2021: 1799, 2022: 1801, 2023: 1941, 2024: 2386, 2025: 3432}
EVENTS = [(2008, "Crise financière", "L'or termine l'année en hausse (+5,6 % en dollars) alors que les marchés d'actions s'effondrent."),
          (2011, "Crise de la dette en zone euro", "L'once atteint alors un sommet : la moyenne annuelle dépasse 1 500 $."),
          (2020, "Pandémie de Covid-19", "Hausse de +25,1 % en dollars sur l'année."),
          (2022, "Poussée d'inflation", "L'inflation atteint +5,2 % en France, mais l'or reste stable en dollars (−0,4 %) : il ne suit pas l'inflation année après année."),
          (2025, "Année exceptionnelle", "Hausse d'environ +64 % à +67 % selon les sources ; record historique en janvier 2026, puis net repli.")]

def fr_num(n):
    return f"{n:,}".replace(",", "&nbsp;")

def gold_chart():
    W, H, ml, mr, mt, mb = 900, 400, 70, 24, 28, 46
    ymax = 4000
    px = lambda yr: ml + (yr - 2000) / 25 * (W - ml - mr)
    py = lambda v: mt + (1 - v / ymax) * (H - mt - mb)
    grid = "".join(
        f'<line class="ch-grid" x1="{ml}" x2="{W - mr}" y1="{py(v):.1f}" y2="{py(v):.1f}"/>'
        f'<text class="ch-ylab" x="{ml - 10}" y="{py(v) + 4:.1f}" text-anchor="end">{fr_num(v)}</text>' for v in range(0, 4001, 1000))
    xlab = "".join(f'<text class="ch-xlab" x="{px(y):.1f}" y="{H - mb + 24}" text-anchor="middle">{y}</text>' for y in range(2000, 2026, 5))
    pts = [(y, v) for y, v in GOLD_AVG.items()]
    line = "M" + " L".join(f"{px(y):.1f} {py(v):.1f}" for y, v in pts)
    area = line + f" L{px(2025):.1f} {py(0):.1f} L{px(2000):.1f} {py(0):.1f} Z"
    ev_years = {e[0]: i + 1 for i, e in enumerate(EVENTS)}
    dots = ""
    for y, v in pts:
        n = ev_years.get(y)
        label = f"{y} : {fr_num(v)} $ l'once (moyenne annuelle)"
        dots += (f'<g class="ch-pt{" ch-ev" if n else ""}" tabindex="0" data-label="{label}" transform="translate({px(y):.1f} {py(v):.1f})">'
                 f'<circle class="ch-hit" r="14"/><circle class="ch-dot" r="{10 if n else 3.5}"/>'
                 + (f'<text class="ch-num" y="4" text-anchor="middle">{n}</text>' if n else "") + '</g>')
    svg = (f'<svg class="gold-chart" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Courbe du prix moyen annuel de l\'once d\'or en dollars, de 279 $ en 2000 à 3 432 $ en 2025">'
           f'{grid}{xlab}<path class="ch-area" d="{area}"/><path class="ch-line" d="{line}" pathLength="1"/>{dots}</svg>')
    legend = "".join(f'<li><span class="ev-n">{i + 1}</span><div><strong>{y} · {t}</strong><span>{d}</span></div></li>' for i, (y, t, d) in enumerate(EVENTS))
    rows = "".join(f"<tr><th scope=\"row\">{y}</th><td>{fr_num(v)} $</td></tr>" for y, v in pts)
    return f'''<div class="chart-card" data-chart>
          <div class="chart-head"><strong>Prix moyen annuel de l'once d'or</strong><span>en dollars américains · 2000 – 2025</span></div>
          <div class="chart-wrap">{svg}<div class="chart-tip" role="status" aria-live="polite" hidden></div></div>
          <ol class="events">{legend}</ol>
          <details class="chart-data"><summary>Voir les données du graphique</summary>
            <div class="table-wrap table-dark"><table class="data-table"><thead><tr><th scope="col">Année</th><th scope="col">Prix moyen de l'once</th></tr></thead><tbody>{rows}</tbody></table></div>
          </details>
        </div>'''

# ---------------------------------------------------------------- AVERTISSEMENT (information financière)
LEGAL_BANNER = '''
    <section class="legal-banner" aria-label="Avertissement">
      <div class="container">
        <p>[[icon:shield-check]]<span><strong>Information générale, jamais un conseil en investissement.</strong> Le contenu de cette page est purement informatif et pédagogique : il ne constitue ni un conseil en investissement, ni une recommandation personnalisée, ni une offre ou une sollicitation d'achat ou de vente, et ne tient pas compte de votre situation personnelle. Investir comporte un risque de perte en capital. <a href="#avertissement">Lire l'avertissement complet</a></span></p>
      </div>
    </section>'''

LEGAL_FULL = '''    <section class="section" id="avertissement">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Avertissement</p><h2>À lire avant toute décision</h2></header>
        <ul class="legal-points">
          <li><strong>Pas un conseil en investissement.</strong> Les informations, chiffres, graphiques, simulations et textes de ce site sont fournis à titre purement informatif et pédagogique. Ils ne constituent en aucun cas un conseil en investissement, une recommandation personnalisée, une offre, une incitation ou une sollicitation d'achat ou de vente d'un produit ou d'un instrument, ni un conseil juridique, fiscal ou comptable.</li>
          <li><strong>Aucune prise en compte de votre situation.</strong> Ces informations sont générales et identiques pour tous les visiteurs : elles ne tiennent compte ni de vos objectifs, ni de votre horizon de placement, ni de votre patrimoine, ni de votre tolérance au risque.</li>
          <li><strong>Risque de perte en capital.</strong> Le prix de l'or, de l'argent, des actions, de l'immobilier et de tout autre placement peut baisser, parfois fortement et durablement. Aucun rendement n'est garanti. L'or et l'argent physiques ne versent ni intérêt ni dividende.</li>
          <li><strong>Les performances passées ne préjugent pas des performances futures.</strong> Les rendements affichés sont des données historiques. Les simulations appliquent un rendement moyen constant à titre d'illustration : ce n'est ni une prévision, ni une projection, ni un engagement.</li>
          <li><strong>Données indicatives.</strong> Les données proviennent de sources tierces citées sur la page ; certaines sont arrondies ou estimées. Leur exactitude, leur exhaustivité et leur actualité ne sont pas garanties. Les chiffres ne tiennent compte ni des frais, ni des primes, ni de la fiscalité, ni des variations de change. Les cours affichés ne sont pas les prix de rachat ou de vente de l'agence.</li>
          <li><strong>Fiscalité.</strong> Les règles fiscales applicables à l'or, à l'argent et aux autres placements sont spécifiques et peuvent évoluer. Renseignez-vous auprès de l'administration fiscale ou d'un professionnel.</li>
          <li><strong>Votre décision vous appartient.</strong> Avant tout investissement, évaluez votre situation personnelle et, si nécessaire, consultez un professionnel qualifié et indépendant (conseiller en investissements financiers, notaire, expert-comptable). Godot &amp; Fils Chartres ne fournit pas de conseil en investissement : l'agence achète et vend des métaux précieux et en explique le fonctionnement, sans recommander de placement.</li>
        </ul>
      </div>
    </section>'''

pourquoi = service_hero("Pourquoi investir dans l'or", "Or d'investissement", "Pourquoi investir dans l'or ?",
    "Valeur refuge, protection du pouvoir d'achat, rendement annuel moyen : les chiffres depuis 2000, l'effet de l'inflation, et les points à connaître avant d'acheter.",
    "chart-line", [("shield-check", "Valeur refuge", "Réputée en période d'incertitude"), ("chart-line", "+10,6 %/an", "Rendement annuel moyen depuis 2000"), ("scale", "Aussi des risques", "L'or fluctue, parfois fortement")]) + LEGAL_BANNER + f'''

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Les chiffres clés</p>
          <h2>Ce que montrent les données</h2>
          <p>Quelques repères issus de sources publiques (LBMA, INSEE, World Gold Council). Les performances passées ne préjugent pas des performances futures.</p>
        </header>
        <div class="stat-grid">
          <div class="stat"><strong>×8,5</strong><span>Prix moyen de l'once d'or entre 2000 (279 $) et 2024 (2 386 $)</span></div>
          <div class="stat"><strong>×1,5</strong><span>Hausse des prix à la consommation en France sur la même période (INSEE)</span></div>
          <div class="stat"><strong>+5,6 %</strong><span>Performance de l'or en 2008, année de la crise financière (en dollars)</span></div>
          <div class="stat"><strong>≈ +8,6 %/an</strong><span>Rendement annuel moyen de l'or en euros entre 2000 et 2024, contre +1,7 %/an pour l'inflation</span></div>
        </div>

        <header class="section-head sub-head">
          <p class="eyebrow">Rendement annuel moyen</p>
          <h2>Combien l'or a-t-il rapporté, en moyenne, chaque année ?</h2>
          <p>Le rendement annuel moyen lisse les hauts et les bas pour comparer des périodes de durées différentes. Il est calculé ici à partir des prix moyens annuels de l'once, en dollars.</p>
        </header>
        <div class="compare" data-compare>
          <div class="cmp-row"><div class="cmp-label"><strong>Depuis 2000</strong><span>2000 → 2025 · 279 $ → 3 432 $</span></div><div class="cmp-bar"><i style="--k:.6625"></i><b>+10,6 %/an</b></div></div>
          <div class="cmp-row"><div class="cmp-label"><strong>Depuis 1971</strong><span>1971 → 2025 · 41 $ → 3 432 $</span></div><div class="cmp-bar"><i style="--k:.534"></i><b>+8,5 %/an</b></div></div>
          <div class="cmp-row"><div class="cmp-label"><strong>2000 → 2010</strong><span>279 $ → 1 225 $</span></div><div class="cmp-bar"><i style="--k:.996"></i><b>+15,9 %/an</b></div></div>
          <div class="cmp-row"><div class="cmp-label"><strong>2010 → 2020</strong><span>1 225 $ → 1 770 $</span></div><div class="cmp-bar cmp-bar-grey"><i style="--k:.234"></i><b>+3,8 %/an</b></div></div>
          <div class="cmp-row"><div class="cmp-label"><strong>2020 → 2025</strong><span>1 770 $ → 3 432 $</span></div><div class="cmp-bar"><i style="--k:.885"></i><b>+14,2 %/an</b></div></div>
        </div>

        <h3 class="sub-title">En euros, une fois l'inflation déduite (2000 → 2024)</h3>
        <div class="stat-grid stat-grid-3">
          <div class="stat"><strong>≈ +8,6 %/an</strong><span>Or en euros (≈ 302 € → ≈ 2 205 € l'once)</span></div>
          <div class="stat stat-grey"><strong>+1,7 %/an</strong><span>Inflation en France (INSEE)</span></div>
          <div class="stat"><strong>≈ +6,8 %/an</strong><span>Rendement « réel » : ce que l'or a rapporté au-dessus de l'inflation</span></div>
        </div>
        <aside class="notice notice-light"><strong>Comment lire ces chiffres :</strong> le rendement dépend beaucoup de la période choisie (+15,9 %/an entre 2000 et 2010, mais +3,8 %/an entre 2010 et 2020). Il est calculé sur des prix moyens annuels, ne tient compte ni des frais d'achat et de revente, ni de la conservation, ni de la fiscalité, et l'or ne verse aucun revenu. Les performances passées ne préjugent pas des performances futures.</aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Depuis l'an 2000</p>
          <h2>Un quart de siècle de hausse… avec des à-coups</h2>
          <p>Passez la souris sur la courbe (ou naviguez au clavier) pour lire le prix de chaque année. Les points numérotés correspondent aux événements ci-dessous.</p>
        </header>
        {gold_chart()}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Or et inflation</p>
          <h2>Préserver son pouvoir d'achat sur le long terme</h2>
          <p>L'inflation grignote la valeur de l'épargne en euros : 1 € de 2000 ne vaut plus que l'équivalent d'environ 0,67 € en 2024. Sur la même période, l'once d'or a nettement mieux résisté.</p>
        </header>
        <div class="compare" data-compare>
          <div class="cmp-row"><div class="cmp-label"><strong>Prix de l'once d'or en euros</strong><span>≈ 302 € en 2000 → ≈ 2 205 € en 2024</span></div>
            <div class="cmp-bar"><i style="--k:1"></i><b>×7,3</b></div></div>
          <div class="cmp-row"><div class="cmp-label"><strong>Prix à la consommation en France</strong><span>indice 100 en 2000 → 150 en 2024</span></div>
            <div class="cmp-bar cmp-bar-grey"><i style="--k:.205"></i><b>×1,5</b></div></div>
        </div>
        <p class="note">Or en euros : prix moyen LBMA en dollars converti au taux de change moyen annuel de la BCE (calcul indicatif). Inflation : coefficients de l'INSEE (66,08 en 2000 ; 99,07 en 2024).</p>
        <aside class="notice notice-light"><strong>Le point de départ compte :</strong> l'année 2000 correspond à un point bas de l'or. Choisir une autre période donne un autre résultat, d'où l'intérêt de raisonner sur le long terme et de ne pas investir à court terme.</aside>
        <div class="table-wrap table-mt">
          <table class="data-table">
            <caption>Or et inflation ces dernières années</caption>
            <thead><tr><th scope="col">Année</th><th scope="col">Or (en dollars)</th><th scope="col">Inflation en France</th></tr></thead>
            <tbody>
              <tr><th scope="row">2022</th><td>−0,4 %</td><td>+5,2 %</td></tr>
              <tr><th scope="row">2023</th><td>+13,2 %</td><td>+4,9 %</td></tr>
              <tr><th scope="row">2024</th><td>+27,2 %</td><td>+2,0 %</td></tr>
              <tr><th scope="row">2025</th><td>≈ +64 % à +67 %</td><td>+0,9 %</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Pourquoi les investisseurs en détiennent</p>
          <h2>Quatre raisons souvent avancées</h2>
        </header>
        <div class="cards-feature cards-feature-dark">
          {feature("shield-check", "Une valeur refuge", "Dans les périodes de crise ou d'incertitude, beaucoup d'investisseurs se tournent vers l'or, reconnu partout dans le monde.")}
          {feature("scale", "Un actif sans émetteur", "L'or n'est la dette de personne : il ne dépend ni d'une entreprise, ni d'un État, ni d'une banque.")}
          {feature("coins", "Une diversification", "Il évolue différemment des actions et des obligations : il peut équilibrer un patrimoine, sans le remplacer.")}
          {feature("chart-line", "Un recours contre l'érosion monétaire", "Sur le long terme, son prix a dépassé l'inflation, même si ce n'est pas vrai chaque année.")}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Avant d'acheter</p>
          <h2>Ce qu'il faut savoir aussi</h2>
          <p>L'or n'est pas un placement sans risque. Voici les points à avoir en tête.</p>
        </header>
        <div class="cards-feature">
          {feature("chart-line", "Un prix qui fluctue", "L'or peut stagner ou reculer pendant des années (environ +3,8 %/an seulement entre 2010 et 2020) et, après un record historique fin janvier 2026 (au-dessus de 5 500 $ l'once), il a nettement reculé.")}
          {feature("cash-banknote", "Aucun revenu", "Contrairement à une action ou une obligation, l'or ne verse ni dividende ni intérêt : le gain ne vient que de la hausse du prix.")}
          {feature("receipt-euro", "Des frais", "L'écart entre prix d'achat et prix de revente, les éventuels frais de conservation et l'assurance pèsent sur le rendement.")}
          {feature("file-certificate", "Une fiscalité spécifique", "La vente d'or d'investissement est soumise à des règles particulières : renseignez-vous avant d'acheter, et conservez vos justificatifs.")}
        </div>
        <aside class="notice notice-light"><strong>Information générale :</strong> cette page ne constitue ni un conseil en investissement ni une recommandation personnalisée. Investir comporte un risque de perte en capital. L'or est généralement envisagé comme une poche de diversification, et non comme la totalité d'un patrimoine.</aside>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Passer à l'action</p><h2>Acheter or et argent à Chartres</h2></header>
        <p class="lead-dark">Pièces d'investissement (Napoléon, Souverain, Krugerrand, Maple Leaf…) ou lingots : l'agence vous renseigne sur les disponibilités et le tarif du jour, sans engagement.</p>
        <div class="hero-actions">
          <a class="btn btn-gold" href="acheter-or.html">Découvrir pièces et lingots</a>
          <a class="btn btn-ghost" href="comparer.html">Comparer à d'autres placements</a>
          <a class="btn btn-ghost" href="contact.html">Nous contacter</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Sources</p><h2>D'où viennent ces chiffres</h2></header>
        <ul class="sources">
          <li>Prix moyens annuels de l'once : <a href="https://www.lbma.org.uk/prices-and-data/lbma-annual-precious-metals-forecast-survey" target="_blank" rel="noopener">LBMA</a>, <a href="https://nma.org/resources/historical-gold-prices-1833-to-present/" target="_blank" rel="noopener">NMA (série historique)</a>, <a href="https://metalcharts.org/gold-price-history" target="_blank" rel="noopener">MetalCharts</a>.</li>
          <li>Performances annuelles de l'or : données du <a href="https://www.gold.org/goldhub/data/gold-prices" target="_blank" rel="noopener">World Gold Council</a> relayées par <a href="https://chartrow.com/gold/returns" target="_blank" rel="noopener">Chartrow</a>.</li>
          <li>Inflation en France : <a href="https://www.insee.fr/fr/statistiques/serie/011813530" target="_blank" rel="noopener">INSEE, coefficients de transformation de l'euro</a> et <a href="https://www.insee.fr/fr/statistiques/8726461" target="_blank" rel="noopener">prix à la consommation 2025</a>.</li>
          <li>Les valeurs sont arrondies et peuvent différer de quelques dollars selon les sources. Dernière vérification des données : novembre 2026.</li>
        </ul>
      </div>
    </section>

{LEGAL_FULL}

{faq_section("Investir dans l'or", FAQ_G["investir"], cls="section-soft")}'''
page("pourquoi-investir-or.html", "Pourquoi investir dans l'or ? Rendements historiques, inflation, risques | Godot &amp; Fils Chartres",
     "Pourquoi investir dans l'or : rendement annuel moyen, évolution du prix de l'once depuis 2000, comparaison avec l'inflation en France, valeur refuge, risques et fiscalité. Information générale.", pourquoi)

# ---------------------------------------------------------------- COMPARER LES PLACEMENTS
# Séries annuelles 2001-2025 (base 100 à fin 2000). Voir les sources en bas de la page.
#  - Or : prix de fin d'année, fixing LBMA PM, en dollars (variation d'une fin d'année à l'autre)
#  - S&P 500 : rendement total (dividendes réinvestis), en dollars
#  - Immobilier : indice Notaires-Insee des logements anciens, France (variations annuelles arrondies, ≈)
#  - Livret A : taux moyen annuel, intérêts réinvestis (≈, arrondi)
#  - Inflation : prix à la consommation, moyenne annuelle (INSEE)
from math import prod
CMP_YEARS = list(range(2001, 2026))
_GOLD_YE = {2000: 273.65, 2001: 276.50, 2002: 347.20, 2003: 416.25, 2004: 435.60, 2005: 513.00, 2006: 632.00, 2007: 833.75,
            2008: 878.00, 2009: 1087.50, 2010: 1405.50, 2011: 1531.00, 2012: 1657.50, 2013: 1204.50, 2014: 1206.00, 2015: 1060.00,
            2016: 1145.90, 2017: 1291.00, 2018: 1279.00, 2019: 1515.50, 2020: 1887.60, 2021: 1805.85, 2022: 1812.35,
            2023: 2062.40, 2024: 2624.50, 2025: 4368.00}
CMP_SERIES = [
    {"id": "or", "label": "Or", "sub": "en dollars · prix de fin d'année (LBMA)", "color": "#e2ab45", "approx": False,
     "returns": [round(100 * (_GOLD_YE[y] / _GOLD_YE[y - 1] - 1), 2) for y in CMP_YEARS]},
    {"id": "sp", "label": "S&P 500", "sub": "actions américaines · dividendes réinvestis · en dollars", "color": "#4fb583", "approx": False,
     "returns": [-11.89, -22.10, 28.68, 10.88, 4.91, 15.79, 5.49, -37.00, 26.46, 15.06, 2.11, 16.00, 32.39, 13.69, 1.38,
                 11.96, 21.83, -4.38, 31.49, 18.40, 28.71, -18.11, 26.29, 25.02, 17.88]},
    {"id": "cac", "label": "CAC 40", "sub": "actions françaises · dividendes réinvestis · en euros (2002-2007 estimés)", "color": "#e07a9b", "approx": True,
     "returns": [-19.8, -32.0, 19.12, 10.3, 26.3, 20.53, 4.51, -40.3, 27.58, 0.55, -13.39, 20.37, 22.22, 2.71, 11.94, 8.88, 12.73, -8.0, 30.45, -4.96, 31.88, -6.68, 20.14, 0.92, 14.28]},
    {"id": "immo", "label": "Immobilier ancien", "sub": "France · indice Notaires-Insee · valeurs arrondies (≈)", "color": "#d98a63", "approx": True,
     "returns": [7.8, 8.3, 11.7, 15.2, 15.3, 12.1, 6.6, 1.2, -7.1, 6.3, 1.3, -1.3, -2.8, -1.6, 0.4, 2.7, 3.4, 3.3, 3.6,
                 5.7, 6.4, 4.7, -4.2, -2.1, 1.1]},
    {"id": "livret", "label": "Livret A", "sub": "taux moyen annuel · intérêts réinvestis (≈)", "color": "#c58ad6", "approx": True,
     "returns": [3.0, 3.0, 2.6, 2.25, 2.1, 2.44, 2.85, 3.67, 1.7, 1.5, 2.1, 2.0, 1.5, 1.1, 0.9, 0.75, 0.75, 0.75, 0.75,
                 0.55, 0.5, 1.4, 2.9, 3.0, 2.2]},
    {"id": "infl", "label": "Inflation", "sub": "prix à la consommation en France (INSEE)", "color": "#9a9a9a", "approx": False, "ref": True,
     "returns": [1.6, 1.9, 2.1, 2.1, 1.7, 1.7, 1.5, 2.8, 0.1, 1.5, 2.1, 2.0, 0.9, 0.5, 0.0, 0.2, 1.0, 1.8, 1.1, 0.5, 1.6,
                 5.2, 4.9, 2.0, 0.9]},
]
CMP_WINDOWS = [(25, "25 ans · 2001–2025"), (15, "15 ans · 2011–2025"), (10, "10 ans · 2016–2025"), (5, "5 ans · 2021–2025")]

def cmp_cagr(returns, n):
    return prod(1 + x / 100 for x in returns[-n:]) ** (1 / n) - 1

def pct_fr(x, plus=True):
    s = f"{x * 100:+.1f}" if plus else f"{x * 100:.1f}"
    return s.replace(".", ",").replace("-", "−") + "&nbsp;%"

def eur_fr(v):
    return f"{round(v):,}".replace(",", "&#8239;") + "&nbsp;€"

def _infl():
    return next(s for s in CMP_SERIES if s.get("ref"))

def asset_series():
    return [s for s in CMP_SERIES if not s.get("ref")]

def real_returns(returns, infl_returns):
    return [((1 + r / 100) / (1 + i / 100) - 1) * 100 for r, i in zip(returns, infl_returns)]

def sim_rows(amount, years, window, real=True):
    infl = _infl()["returns"]
    ig = cmp_cagr(infl, window)
    rows = []
    for s in asset_series():
        nom = cmp_cagr(s["returns"], window)
        rr = (1 + nom) / (1 + ig) - 1
        val = amount * (1 + (rr if real else nom)) ** years
        rets = real_returns(s["returns"], infl) if real else s["returns"]
        rows.append((s, nom, rr, val, min(rets[-window:])))
    return sorted(rows, key=lambda r: -r[3])

def sim_table_html(amount=10000, years=10, window=25, real=False):
    rows = sim_rows(amount, years, window, real)
    top = max(r[3] for r in rows)
    out = []
    for s, nom, rr, val, worst in rows:
        approx = ' <abbr title="Estimation arrondie">≈</abbr>' if s["approx"] else ""
        out.append(
            f'<tr class="sim-row"><th scope="row"><span class="sw" style="--c:{s["color"]}"></span>{s["label"]}{approx}</th>'
            f'<td data-label="Avant inflation" class="{"" if real else "on"}">{pct_fr(nom)}<small>/an</small></td>'
            f'<td data-label="Après inflation" class="{"on" if real else ""}">{pct_fr(rr)}<small>/an</small></td>'
            f'<td data-label="Valeur finale"><strong>{eur_fr(val)}</strong><span class="mini-bar"><i style="--w:{val / top * 100:.1f}%;--c:{s["color"]}"></i></span></td>'
            f'<td data-label="Gain">{"+" if val - amount >= 0 else "−"}{eur_fr(abs(val - amount))}</td>'
            f'<td data-label="Pire année">{pct_fr(worst / 100)}</td></tr>')
    return "".join(out)

def matrix_html(real=False):
    infl = _infl()["returns"]
    head = "".join(f'<th scope="col">{lab}</th>' for _, lab in CMP_WINDOWS)
    rate = lambda s, n: ((1 + cmp_cagr(s["returns"], n)) / (1 + cmp_cagr(infl, n)) - 1) if real else cmp_cagr(s["returns"], n)
    best = {n: max(asset_series(), key=lambda s: rate(s, n))["id"] for n, _ in CMP_WINDOWS}
    rows = ""
    for s in asset_series():
        cells = "".join(f'<td class="{"best" if best[n] == s["id"] else ""}">{pct_fr(rate(s, n))}</td>' for n, _ in CMP_WINDOWS)
        approx = " ≈" if s["approx"] else ""
        rows += f'<tr><th scope="row"><span class="sw" style="--c:{s["color"]}"></span>{s["label"]}{approx}</th>{cells}</tr>'
    foot = "".join(f'<td>{pct_fr(cmp_cagr(infl, n))}</td>' for n, _ in CMP_WINDOWS)
    label = "Rendement annuel moyen après inflation" if real else "Rendement annuel moyen avant inflation"
    flab = "Inflation moyenne (déjà déduite)" if real else "Pour mémoire : inflation moyenne"
    return (f'<thead><tr><th scope="col" data-matrix-title>{label}</th>{head}</tr></thead><tbody>{rows}</tbody>'
            f'<tfoot><tr class="ref"><th scope="row" data-matrix-foot>{flab}</th>{foot}</tr></tfoot>')

_cmp_json = json.dumps({"years": CMP_YEARS, "series": CMP_SERIES,
                        "windows": [{"n": n, "label": lab} for n, lab in CMP_WINDOWS]}, ensure_ascii=False)
_legend = "".join(
    f'<li><button type="button" class="chip cmp-chip" data-series="{s["id"]}" aria-pressed="true"><span class="sw" style="--c:{s["color"]}"></span>{s["label"]}</button></li>'
    for s in asset_series())
_sub = "".join(f'<li><span class="sw" style="--c:{s["color"]}"></span><div><strong>{s["label"]}</strong><span>{s["sub"]}</span></div></li>' for s in asset_series())
_win_opts = "".join(f'<option value="{n}"{" selected" if n == 25 else ""}>{lab}</option>' for n, lab in CMP_WINDOWS)
_infl25 = cmp_cagr(_infl()["returns"], 25)

comparer = service_hero("Comparer les placements", "Comparateur", "Comparer l'or aux autres placements.",
    "Or, actions américaines et françaises, immobilier et Livret A : leurs courbes depuis 2000, avec l'option « inflation déduite » pour lire le pouvoir d'achat réel, et ce que deviendrait votre capital selon le rendement annuel moyen de chacun.",
    "chart-line", [("chart-line", "5 placements", "Or, S&P 500, CAC 40, immobilier, Livret A"), ("coin-euro", "Option inflation", "Voir le pouvoir d'achat réel"), ("scale", "Votre capital", "Simulez avec votre montant")]) + LEGAL_BANNER + f'''

    <section class="section section-dark" id="courbes">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Les courbes</p>
          <h2>25 ans de placements, côte à côte</h2>
          <p>Chaque courbe part de 100 au point de départ choisi : on lit directement de combien un placement a progressé. Passez la souris sur le graphique pour comparer année par année.</p>
        </header>
        <div class="cmp" data-cmp>
          <div class="cmp-controls">
            <label class="field"><span>Base 100 en</span>
              <select data-cmp-start aria-label="Année de départ">
                <option value="2000" selected>2000</option><option value="2005">2005</option><option value="2010">2010</option><option value="2015">2015</option><option value="2020">2020</option>
              </select></label>
            <div class="seg" role="group" aria-label="Échelle du graphique">
              <button type="button" class="is-on" data-cmp-scale="log" aria-pressed="true">Échelle logarithmique</button>
              <button type="button" data-cmp-scale="lin" aria-pressed="false">Échelle linéaire</button>
            </div>
            <label class="switch"><input type="checkbox" role="switch" data-real><span class="sw-track" aria-hidden="true"></span><span>Inflation déduite</span></label>
          </div>
          <ul class="cmp-legend" aria-label="Séries affichées">{_legend}</ul>
          <div class="cmp-chart-wrap">
            <div class="cmp-chart" data-cmp-chart role="img" aria-label="Courbes comparées de l'or, du S&amp;P 500, du CAC 40, de l'immobilier et du Livret A depuis 2000"></div>
            <div class="chart-tip cmp-tip" role="status" aria-live="polite" hidden></div>
          </div>
          <noscript><p class="note">Le graphique interactif nécessite JavaScript. Les rendements annuels moyens figurent dans le tableau plus bas.</p></noscript>
          <p class="note cmp-hint">« Inflation déduite » : chaque courbe est divisée par l'indice des prix à la consommation (Insee). Elle mesure alors l'évolution du pouvoir d'achat, et non plus seulement du prix. Cochez « Inflation déduite » pour la prendre en compte ; par défaut, les valeurs sont brutes.</p>
          <p class="note cmp-hint">L'échelle logarithmique rend lisibles des courbes très différentes : à chaque graduation, la valeur double ou presque.</p>
          <ul class="cmp-sub">{_sub}</ul>
        </div>
        <script type="application/json" id="cmp-data">{_cmp_json}</script>
      </div>
    </section>

    <section class="section" id="simulateur">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">Simulateur</p>
          <h2>Que deviendrait votre capital ?</h2>
          <p>Saisissez un montant et une durée : le tableau applique à votre capital le rendement annuel moyen historique de chaque placement, sur la période de référence choisie. Cochez « Déduire l'inflation » pour lire le pouvoir d'achat réel.</p>
        </header>
        <form class="sim" data-sim onsubmit="return false">
          <label class="field"><span>Capital investi</span><span class="input-wrap"><input type="number" inputmode="numeric" min="100" max="10000000" step="100" value="10000" data-sim-amount aria-label="Capital investi en euros"><b>€</b></span></label>
          <label class="field"><span>Durée du placement</span><span class="input-wrap"><input type="number" inputmode="numeric" min="1" max="50" step="1" value="10" data-sim-years aria-label="Durée en années"><b>ans</b></span></label>
          <label class="field"><span>Rendements moyens calculés sur</span><select data-sim-window aria-label="Période de référence">{_win_opts}</select></label>
          <label class="switch sim-switch"><input type="checkbox" role="switch" data-real><span class="sw-track" aria-hidden="true"></span><span>Déduire l'inflation</span></label>
        </form>
        <p class="sim-caption" data-sim-caption>Avec 10&nbsp;000&nbsp;€ placés pendant 10&nbsp;ans, au rendement annuel moyen des 25 dernières années, avant inflation.</p>
        <div class="table-wrap">
          <table class="data-table sim-table">
            <caption class="sr-only">Valeur du capital selon le placement</caption>
            <thead><tr><th scope="col">Placement</th><th scope="col">Rendement annuel moyen<br><small>avant inflation</small></th><th scope="col">Rendement annuel moyen<br><small>après inflation</small></th><th scope="col" data-sim-th-val>Valeur finale<br><small>en euros courants</small></th><th scope="col">Gain</th><th scope="col" data-sim-th-worst>Pire année<br><small>avant inflation</small></th></tr></thead>
            <tbody data-sim-body>{sim_table_html()}</tbody>
          </table>
        </div>
        <p class="sim-infl" data-sim-infl>Valeurs en euros courants, <strong>sans déduire l'inflation</strong> ({pct_fr(_infl25)}/an en moyenne sur cette période) : le pouvoir d'achat réel est plus faible. Cochez « Déduire l'inflation » pour le voir.</p>
        <aside class="notice notice-light"><strong>À lire avant d'interpréter :</strong> c'est une simulation à rendement constant, ce qui ne correspond jamais à la réalité : une année sur deux peut être négative. Les résultats passés ne préjugent pas des résultats futurs, et les chiffres ne tiennent compte ni des frais, ni de la fiscalité, ni des droits de mutation ou de l'entretien pour l'immobilier. L'or et le S&amp;P 500 sont exprimés en dollars : pour un investisseur en euros, les variations du change modifient le résultat.</aside>
      </div>
    </section>

    <section class="section section-dark">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">À retenir</p>
          <h2>Le classement change avec la période</h2>
          <p>Le meilleur placement d'une période n'est pas celui de la suivante. La case dorée indique le meilleur rendement annuel moyen de chaque période ; l'interrupteur « Inflation déduite » du graphique ou du simulateur permet de lire les rendements réels.</p>
        </header>
        <div class="table-wrap table-dark">
          <table class="data-table matrix" data-matrix>{matrix_html()}</table>
        </div>
        <div class="cards-feature cards-feature-dark takeaways">
          {feature("scale", "Un classement qui bouge", "L'or domine sur 25, 10 et 5 ans, mais les actions américaines passent devant sur 15 ans, le CAC 40 restant en retrait : le résultat dépend de la période choisie.")}
          {feature("chart-line", "Le risque n'est pas le même", "Les actions ont connu des années à −37 % (2008) ; l'or des années à −27 % (2013) ; le Livret A, jamais négatif en euros courants mais souvent négatif une fois l'inflation déduite (2022 : environ −3,6 %).")}
          {feature("diamond", "L'immobilier, un cas à part", "Il est peu liquide, nécessite souvent un emprunt et génère des frais, des charges et des loyers qui ne figurent pas ici.")}
          {feature("coins", "Se diversifier", "Aucun placement n'est le meilleur chaque année. Beaucoup d'épargnants répartissent leur patrimoine entre plusieurs supports.")}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container narrow">
        <header class="section-head"><p class="eyebrow">Sources et méthode</p><h2>D'où viennent ces données</h2></header>
        <ul class="sources">
          <li><strong>Or :</strong> prix de fin d'année du fixing LBMA PM, en dollars (variation d'une fin d'année à l'autre). Voir la page <a href="pourquoi-investir-or.html">Pourquoi investir dans l'or</a> et les sources <a href="https://www.lbma.org.uk/prices-and-data/lbma-annual-precious-metals-forecast-survey" target="_blank" rel="noopener">LBMA</a> et <a href="https://www.gold.org/goldhub/data/gold-prices" target="_blank" rel="noopener">World Gold Council</a>. Les écarts avec d'autres sources sont de l'ordre d'un point par an.</li>
          <li><strong>S&amp;P 500 :</strong> rendement total annuel dividendes réinvestis, en dollars, d'après <a href="https://smartasset.com/investing/sp-500-average-annual-return" target="_blank" rel="noopener">SmartAsset</a> et <a href="https://www.slickcharts.com/sp500/returns/details" target="_blank" rel="noopener">Slickcharts</a>.</li>
          <li><strong>CAC 40 :</strong> rendement annuel dividendes réinvestis (CAC 40 GR), en euros : valeurs publiées pour 2001 et 2008-2025 (<a href="https://www.zonebourse.com/cours/indice/CAC-40-DIVIDENDES-REINVES-3869660/cotations/" target="_blank" rel="noopener">Zonebourse</a>, <a href="https://live.euronext.com/sites/default/files/documentation/index-fact-sheets/CAC_40_Index_Factsheet.pdf" target="_blank" rel="noopener">Euronext</a>) ; pour 2002-2007, variation du cours de clôture augmentée d'un rendement du dividende estimé à environ 3 % (≈).</li>
          <li><strong>Immobilier :</strong> variations annuelles arrondies de l'indice Notaires-Insee des logements anciens en France (<a href="https://www.insee.fr/fr/statistiques/5371271" target="_blank" rel="noopener">Insee</a>). Estimation à ± 1 ou 2 points selon les années : à utiliser comme un ordre de grandeur.</li>
          <li><strong>Livret A :</strong> taux moyen de chaque année (<a href="https://mes-livrets.fr/guides/historique-taux-livret-a/" target="_blank" rel="noopener">historique des taux</a>), arrondi, intérêts réinvestis. Estimation.</li>
          <li><strong>Inflation (déduite des rendements) :</strong> moyenne annuelle des prix à la consommation, <a href="https://www.insee.fr/fr/statistiques/serie/011813530" target="_blank" rel="noopener">Insee</a>.</li>
          <li>Rendement annuel moyen = taux de croissance annualisé sur la période. Données arrêtées à fin 2025 (S&amp;P 500 et or), mises à jour en novembre 2026. Ce comparateur est une information générale, pas un conseil en investissement ; investir comporte un risque de perte en capital.</li>
        </ul>
        <div class="hero-actions">
          <a class="btn btn-gold" href="pourquoi-investir-or.html">Pourquoi investir dans l'or</a>
          <a class="btn btn-outline" href="acheter-or.html">Acheter or &amp; argent</a>
        </div>
      </div>
    </section>

{LEGAL_FULL}

{faq_section("Comparer les placements", FAQ_G["comparer"], cls="section-soft")}'''
page("comparer.html", "Comparer l'or, les actions, l'immobilier et le Livret A | Godot &amp; Fils Chartres",
     "Comparateur de placements : courbes de l'or, du S&P 500, de l'immobilier, du Livret A et de l'inflation depuis 2000, et simulateur de capital selon le rendement annuel moyen historique.", comparer)

# ---------------------------------------------------------------- LA MAISON
maison = hero("La maison", "Négoce de métaux précieux", "Une institution du négoce de métaux précieux.",
              "La maison Godot & Fils accompagne particuliers et épargnants dans l'achat et la vente d'or, d'argent et de métaux précieux.", actions=False) + '''

''' + histoire_section() + '\n\n' + agence_gallery(True) + '''

    <section class="section">
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
          <li><a class="text-link" href="vendre-or.html">Rachat d'or et d'argent</a> : bijoux, argenterie, pièces et lingots</li>
          <li><a class="text-link" href="acheter-or.html">Vente d'or et d'argent d'investissement</a> : pièces et lingots</li>
          <li><a class="text-link" href="argent-bijoux.html">Argent, platine et bijoux</a> : estimation et rachat</li>
          <li><a class="text-link" href="change.html">Bureau de change</a> : devises étrangères</li>
        </ul>
      </div>
    </section>'''
page("la-maison.html", "La maison Godot &amp; Fils — Négoce de métaux précieux",
     "Godot & Fils, institution du négoce d'or et de métaux précieux. Découvrez l'histoire, les engagements et l'agence de Chartres.", maison)

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
     "Toutes les réponses à vos questions sur la vente d'or et d'argent, l'achat de pièces et lingots, l'estimation gratuite et le bureau de change à Chartres.",
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
                <p class="note hours-note">L'agence est fermée les jours fériés.</p>
                <p class="note hours-note hours-today" data-holiday-note hidden></p>
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
     "Agence Godot & Fils Chartres : 23 rue de la Pie, 28000 Chartres. Ouvert du lundi au vendredi de 9h30 à 18h00, samedi matin sur rendez-vous. Tél. 02 37 83 49 77.", contact + agence_gallery(False), ld=LD_STORE, cta=False)

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
        <h2>Avertissement : informations financières</h2>
        <p>Les informations, chiffres, graphiques et simulations présentés sur ce site (notamment les pages « Pourquoi investir dans l'or », « Comparer les placements » et les cours affichés) sont fournis à titre purement informatif et pédagogique. Ils ne constituent en aucun cas un conseil en investissement, une recommandation personnalisée, ni une offre ou une sollicitation d'achat ou de vente. Ils ne tiennent pas compte de la situation personnelle du visiteur. Tout investissement comporte un risque de perte en capital ; les performances passées ne préjugent pas des performances futures. Les données proviennent de sources tierces dont l'exactitude n'est pas garantie. Avant toute décision, consultez un professionnel qualifié et indépendant.</p>
        <h2>Propriété intellectuelle</h2>
        <p>L'ensemble des contenus de ce site (textes, visuels, logos) est protégé par le droit de la propriété intellectuelle. Toute reproduction sans autorisation préalable est interdite.</p>
        <h2>Données personnelles</h2>
        <p>Ce site ne collecte aucune donnée personnelle via formulaire et n'utilise aucun cookie de mesure d'audience ni de publicité. Les polices sont hébergées sur le site. Le plan d'accès de la page Contact est fourni par Google Maps, qui peut déposer des cookies : il n'est chargé qu'avec votre accord, que vous pouvez modifier à tout moment via « Gérer les cookies » en bas de page. Votre choix est mémorisé dans le stockage local de votre navigateur pendant 6 mois. Pour toute question relative à vos données, contactez l'agence.</p>
      </div>
    </section>'''
page("mentions-legales.html", "Mentions légales — Godot &amp; Fils Chartres", "Mentions légales du site Godot & Fils Chartres.", legal, cta=False, noindex=True)

# ---------------------------------------------------------------- sitemap / robots
pages = ["index.html"] + [h for h, _ in NAV] + ["pourquoi-investir-or.html", "comparer.html", "faq.html"]
if INDEXABLE:
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in pages:
            f.write(f"  <url><loc>{SITE}/{'' if p == 'index.html' else p}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n")
        f.write("</urlset>\n")
    robots_txt = f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {SITE}/sitemap.xml\n"
else:
    if os.path.exists(os.path.join(ROOT, "sitemap.xml")):
        os.remove(os.path.join(ROOT, "sitemap.xml"))
    robots_txt = "User-agent: *\nDisallow: /\n"
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(robots_txt)

# En-têtes Vercel (sécurité + X-Robots-Tag tant que le site est en test)
headers = [{"key": "X-Content-Type-Options", "value": "nosniff"},
           {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
           {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
           {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]
if not INDEXABLE:
    headers.append({"key": "X-Robots-Tag", "value": "noindex, nofollow, noarchive"})
with open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8") as f:
    json.dump({"headers": [{"source": "/(.*)", "headers": headers},
                           {"source": "/assets/(css|js)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]},
                           {"source": "/assets/(img|fonts|icons)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]}]}, f, indent=2)
    f.write("\n")
