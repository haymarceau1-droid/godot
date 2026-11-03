// Génère tools/geo/france-map.json : contour SVG de la France métropolitaine + position (x, y) des villes.
// Usage : cd tools/geo && npm install && node make-map.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { feature } from "topojson-client";
import { geoConicConformal, geoPath } from "d3-geo";

const topo = JSON.parse(readFileSync("node_modules/world-atlas/countries-10m.json", "utf8"));
const france = feature(topo, topo.objects.countries).features.find((f) => f.properties.name === "France");

// On ne garde que la métropole + Corse (le contour « France » de Natural Earth inclut l'outre-mer)
const inMetro = ([lon, lat]) => lon > -6 && lon < 10 && lat > 41 && lat < 52;
const polys = france.geometry.coordinates.filter((p) => p[0].some(inMetro));
const metro = { type: "Feature", geometry: { type: "MultiPolygon", coordinates: polys } };

const W = 800, H = 800;
const projection = geoConicConformal().parallels([44, 49]).rotate([-3, 0]).fitExtent([[20, 20], [W - 20, H - 20]], metro);
const path = geoPath(projection).digits(1);

const data = JSON.parse(readFileSync("agences.json", "utf8"));
const villes = data.villes.map((v) => {
  if (v.nopin) return v; // Monaco, étranger, outre-mer : listés sans point sur la carte
  const [x, y] = projection([v.lon, v.lat]);
  return { ...v, x: +x.toFixed(1), y: +y.toFixed(1) };
});

writeFileSync("france-map.json", JSON.stringify({
  viewBox: `0 0 ${W} ${H}`,
  path: path(metro),
  officielle: data.officielle,
  villes,
}));
console.log("OK :", villes.length, "villes,", villes.reduce((n, v) => n + v.agences.length, 0), "agences");
