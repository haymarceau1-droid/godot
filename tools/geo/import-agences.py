#!/usr/bin/env python3
"""Régénère tools/geo/agences.json à partir de la liste officielle du réseau.

Usage :
    python3 tools/geo/import-agences.py            # télécharge la liste officielle
    python3 tools/geo/import-agences.py page.html  # ou lit une copie locale
puis :  cd tools/geo && node make-map.mjs && cd ../.. && python3 tools/build.py

Source : https://www.achat-or-et-argent.fr/agences-liste (nom, adresse, téléphone, coordonnées GPS, lien).
Les agences proches (même agglomération) sont regroupées sur un même point de la carte ; l'Île-de-France forme un seul point.
"""
import html
import json
import math
import os
import re
import sys
import urllib.request

URL = "https://www.achat-or-et-argent.fr/agences-liste"
BASE = "https://www.achat-or-et-argent.fr"
HERE = os.path.dirname(os.path.abspath(__file__))
IDF = {"75", "77", "78", "91", "92", "93", "94", "95"}
MERGE_KM = 20          # deux agences à moins de 20 km partagent un point de la carte
METRO = (41.0, 51.5, -5.5, 9.8)  # lat min, lat max, lon min, lon max : métropole + Corse (hors Monaco, traité à part)

TITRES = {  # regroupements : titre affiché selon la ville principale du point
    "Antibes": "Côte d'Azur",
    "Aix-les-Bains": "Chambéry & Aix-les-Bains",
    "Toulon": "Toulon & Hyères",
    "Saint Etienne": "Saint-Étienne",
    "Chalon-sur-Saône": "Chalon-sur-Saône",
}

SMALL = {"de", "du", "des", "la", "le", "les", "sur", "en", "sous", "lès", "d", "l", "et", "aux", "au"}


def fetch():
    if len(sys.argv) > 1:
        return open(sys.argv[1], encoding="utf-8", errors="replace").read()
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (godot-chartres import)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def title_city(s):
    """« AIX-EN-PROVENCE » -> « Aix-en-Provence »."""
    def word(w, first):
        w = w.lower()
        if not first and w in SMALL:
            return w
        return w[:1].upper() + w[1:]
    out, first = [], True
    for token in re.split(r"([ '’-])", s.strip()):
        if token in " '’-":
            out.append(token)
        elif token:
            out.append(word(token, first))
            first = False
    return "".join(out)


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def parse(page):
    m = re.search(r'\{"0":\{"latitude".*?\}\}', page, re.S)
    depth, end = 0, None
    for i, ch in enumerate(page[m.start():]):
        depth += ch == "{"
        depth -= ch == "}"
        if depth == 0:
            end = m.start() + i + 1
            break
    geo = {v["url"]: v for v in json.loads(page[m.start():end]).values()}
    agences, seen = [], set()
    for card in page.split('<div class="col-lg-6 col-12">')[1:]:
        t = re.search(r'<a href="(/agence-[^"]+)" class="stretched-link text-decoration-none">([^<]+)</a>', card)
        if not t or t.group(1) in seen:
            continue
        url, nom = t.group(1), html.unescape(t.group(2)).strip()
        seen.add(url)
        ps = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.findall(r"<p>(.*?)</p>", card, re.S)]
        tel = re.search(r'href="tel:([^"]+)"', card)
        g = geo[url]
        rue, cp_ville = (ps + ["", ""])[:2]
        mm = re.match(r"(\d{4,5})\s+(.*)", cp_ville)
        cp, ville = (mm.group(1), title_city(mm.group(2))) if mm else ("", title_city(cp_ville))
        agences.append({
            "nom": re.sub(r"\s*\(.*?\)\s*", " ", nom).strip(),  # « Paris (Siège, depuis 1933) » -> « Paris »
            "adresse": f"{rue}, {cp} {ville}".strip(", "),
            "tel": tel.group(1).strip() if tel else None,
            "url": BASE + url,
            "ville": ville, "cp": cp,
            "lat": float(g["latitude"]), "lon": float(g["longitude"]),
        })
    return agences


def in_metro(a):
    return len(a["cp"]) == 5 and METRO[0] <= a["lat"] <= METRO[1] and METRO[2] <= a["lon"] <= METRO[3] and not a["cp"].startswith("98")


def main():
    ag = parse(fetch())
    metro = [a for a in ag if in_metro(a)]
    hors = [a for a in ag if not in_metro(a)]

    # regroupement : Île-de-France d'un bloc, sinon liaison simple à moins de MERGE_KM
    parent = list(range(len(metro)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i, a in enumerate(metro):
        for j in range(i):
            b = metro[j]
            same_idf = a["cp"][:2] in IDF and b["cp"][:2] in IDF
            if same_idf or km((a["lat"], a["lon"]), (b["lat"], b["lon"])) < MERGE_KM:
                parent[find(i)] = find(j)
    clusters = {}
    for i, a in enumerate(metro):
        clusters.setdefault(find(i), []).append(a)

    villes = []
    for members in clusters.values():
        villes_noms = []
        for a in members:
            if a["ville"] not in villes_noms:
                villes_noms.append(a["ville"])
        counts = {v: sum(1 for a in members if a["ville"] == v) for v in villes_noms}
        main = max(villes_noms, key=lambda v: (counts[v], -villes_noms.index(v)))
        idf = members[0]["cp"][:2] in IDF
        titre = "Paris & Île-de-France" if idf else TITRES.get(main, main)
        lat = sum(a["lat"] for a in members) / len(members)
        lon = sum(a["lon"] for a in members) / len(members)
        local = any(a["ville"] == "Chartres" for a in members)
        v = {"ville": titre, "lat": round(lat, 4), "lon": round(lon, 4), "agences": []}
        if local:
            v["local"] = True
        for a in sorted(members, key=lambda x: (x["cp"], x["nom"])):
            item = {"nom": a["nom"], "adresse": a["adresse"], "tel": a["tel"], "url": a["url"]}
            if a["ville"] == "Chartres":
                item["url"] = "contact.html"
            v["agences"].append(item)
        villes.append(v)
    villes.sort(key=lambda v: v["ville"].replace("Î", "I"))

    if hors:
        villes.append({"ville": "Monaco, étranger & outre-mer", "nopin": True, "agences": [
            {"nom": a["nom"], "adresse": a["adresse"], "tel": a["tel"], "url": a["url"]} for a in sorted(hors, key=lambda x: x["nom"])]})

    data = {
        "_note": "Réseau Godot & Fils : liste officielle importée par tools/geo/import-agences.py (nom, adresse, téléphone, GPS).",
        "officielle": URL,
        "villes": villes,
    }
    with open(os.path.join(HERE, "agences.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{len(ag)} agences, {len(villes)} points ({len(hors)} hors métropole)")
    for v in villes:
        print(f"  {v['ville']:28s} {len(v['agences'])}")


main()
