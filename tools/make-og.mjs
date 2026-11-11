// Génère les images de partage (Open Graph, 1200×630) de chaque page : assets/img/og/<page>.jpg
// Usage : cd tools/geo && npm install playwright  (ou tout dossier où « playwright » est installé)  puis  node ../make-og.mjs
// Les polices et photos viennent du dossier assets/ ; aucune requête réseau.
import { createRequire } from "node:module";
import { mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, resolve } from "node:path";

const { chromium } = createRequire(import.meta.url)("playwright");
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const A = (p) => pathToFileURL(resolve(ROOT, "assets", p)).href;

const PAGES = [
  { slug: "index", eyebrow: "Chartres · 23 rue de la Pie", title: "Achat et vente d'or et d'argent à Chartres", sub: "Estimation gratuite, sans engagement et sans rendez-vous", img: "img/devanture.webp", pos: "62% 50%" },
  { slug: "vendre-or", eyebrow: "Rachat à Chartres", title: "Vendre son or et son argent", sub: "Bijoux, pièces, lingots : estimation gratuite sous vos yeux", img: "img/or-pieces-lingots-gros-plan.webp", pos: "50% 50%" },
  { slug: "acheter-or", eyebrow: "Or et argent d'investissement", title: "Acheter pièces et lingots d'or et d'argent", sub: "Napoléon, Krugerrand, Maple Leaf, Philharmonique…", img: "img/or-lingots-pieces.webp", pos: "50% 50%" },
  { slug: "numismatique", eyebrow: "Pièces de collection", title: "Numismatique : faites estimer vos pièces", sub: "Valeur du métal et valeur de collection", img: "img/numismatique-pieces-anciennes.webp", pos: "40% 50%" },
  { slug: "argent-bijoux", eyebrow: "Argent · Platine · Bijoux", title: "Argenterie, platine et bijoux anciens", sub: "Estimation gratuite et sans engagement", img: "img/argent-lingot-100-onces.webp", pos: "50% 50%" },
  { slug: "change", eyebrow: "Bureau de change", title: "Changer vos devises à Chartres", sub: "Achat et vente de devises étrangères", img: "img/change-billets-devises.webp", pos: "50% 50%" },
  { slug: "pourquoi-investir-or", eyebrow: "Information générale", title: "Pourquoi investir dans l'or ?", sub: "Rendements, inflation et risques, chiffres à l'appui", img: "img/or-lingots-gros-plan.webp", pos: "50% 50%" },
  { slug: "comparer", eyebrow: "Comparateur", title: "Comparer l'or, les actions, l'immobilier", sub: "Courbes depuis 2000 et simulateur de capital", img: "img/argent-lingotins.webp", pos: "50% 50%" },
  { slug: "la-maison", eyebrow: "La maison", title: "Godot & Fils, un réseau de 125 agences", sub: "Négoce de métaux précieux", img: "img/agence-facade.webp", pos: "50% 50%" },
  { slug: "faq", eyebrow: "Questions fréquentes", title: "Vous vous posez des questions ?", sub: "Estimation, documents, prix, change", img: "img/agence-accueil.webp", pos: "50% 50%" },
  { slug: "contact", eyebrow: "Contact et accès", title: "Nous rendre visite à Chartres", sub: "23 rue de la Pie · 02 37 83 49 77", img: "img/agence-facade.webp", pos: "50% 50%" },
];

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

const html = (p) => `<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face { font-family: JS; font-weight: 400; src: url("${A("fonts/josefin-sans-latin-400-normal.woff2")}") format("woff2"); }
@font-face { font-family: JS; font-weight: 700; src: url("${A("fonts/josefin-sans-latin-700-normal.woff2")}") format("woff2"); }
* { box-sizing: border-box; margin: 0; }
body { width: 1200px; height: 630px; background: #000; font-family: JS, sans-serif; color: #fff; position: relative; overflow: hidden; }
.photo { position: absolute; top: 0; right: 0; bottom: 0; width: 720px; background: url("${A(p.img)}") ${p.pos} / cover; }
.fade { position: absolute; inset: 0; background: linear-gradient(90deg, #000 0%, #000 34%, rgba(0,0,0,.86) 50%, rgba(0,0,0,.35) 78%, rgba(0,0,0,.25) 100%); }
.frame { position: absolute; inset: 24px; border: 1px solid rgba(226,171,69,.55); }
.logo { position: absolute; left: 72px; top: 64px; width: 250px; }
.copy { position: absolute; left: 72px; top: 196px; width: 640px; }
.eyebrow { font-size: 19px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: #e2ab45; margin-bottom: 22px; }
h1 { font-size: 66px; font-weight: 400; line-height: 1.06; letter-spacing: -0.05em; }
.rule { width: 72px; height: 3px; background: #e2ab45; margin: 30px 0 22px; }
.sub { font-size: 25px; line-height: 1.4; color: rgba(255,255,255,.78); max-width: 560px; }
.url { position: absolute; left: 72px; bottom: 56px; font-size: 18px; letter-spacing: .08em; color: rgba(255,255,255,.6); }
</style></head><body>
<div class="photo"></div><div class="fade"></div><div class="frame"></div>
<img class="logo" src="${A("img/logo-blanc.png")}" alt="">
<div class="copy"><div class="eyebrow">${esc(p.eyebrow)}</div><h1>${esc(p.title)}</h1><div class="rule"></div><div class="sub">${esc(p.sub)}</div></div>
<div class="url">godotetfils-chartres.fr</div>
</body></html>`;

mkdirSync(resolve(ROOT, "assets/img/og"), { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const p of PAGES) {
  const tmp = resolve(tmpdir(), `og-${p.slug}.html`);
  writeFileSync(tmp, html(p));
  await page.goto(pathToFileURL(tmp).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  await page.screenshot({ path: resolve(ROOT, `assets/img/og/${p.slug}.jpg`), type: "jpeg", quality: 86 });
  console.log("OK", p.slug);
}
await browser.close();
