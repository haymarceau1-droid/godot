// Fonction serverless Vercel : cours spot de l'or et de l'argent, convertis en euros, avec historique.
// Le navigateur n'appelle que ce site (/api/cours?range=1m|1y|5y) : aucune requête tierce côté visiteur, aucune clé exposée.
// Sources (gratuites, sans clé) :
//   - cours instantané : gold-api.com (XAU / XAG en dollars)
//   - historique quotidien : Stooq (xauusd / xagusd), secours Yahoo Finance (GC=F / SI=F)
//   - taux USD→EUR : Frankfurter / BCE (instantané et historique), secours open.er-api.com
const OZ = 31.1034768; // grammes dans une once troy
const DAYS = { '1m': 31, '1y': 366, '5y': 1827 };
const MAX_POINTS = 120;

async function get(url, ms = 6000, text = false) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(url, { signal: ctl.signal, headers: { accept: text ? 'text/csv,*/*' : 'application/json', 'user-agent': 'Mozilla/5.0 (compatible; godot-cours/1.0)' } });
    if (!r.ok) throw new Error(url + ' → ' + r.status);
    return text ? await r.text() : await r.json();
  } finally { clearTimeout(t); }
}

const ymd = (d) => d.toISOString().slice(0, 10);

async function usdEur() {
  try {
    const d = await get('https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR');
    if (d && d.rates && d.rates.EUR > 0) return d.rates.EUR;
  } catch (e) { /* secours */ }
  const d = await get('https://open.er-api.com/v6/latest/USD');
  if (d && d.rates && d.rates.EUR > 0) return d.rates.EUR;
  throw new Error('taux USD/EUR indisponible');
}

// Taux USD→EUR quotidiens sur la période, reportés sur les week-ends et jours fériés.
async function fxSeries(from, to) {
  const d = await get(`https://api.frankfurter.dev/v1/${ymd(from)}..${ymd(to)}?base=USD&symbols=EUR`, 8000);
  const days = Object.keys(d.rates || {}).sort();
  const map = new Map(days.map((k) => [k, d.rates[k].EUR]));
  return (date) => {
    let k = ymd(date);
    for (let i = 0; i < 10; i++) {
      if (map.has(k)) return map.get(k);
      const prev = new Date(k + 'T00:00:00Z'); prev.setUTCDate(prev.getUTCDate() - 1); k = ymd(prev);
    }
    return days.length ? map.get(days[0]) : null;
  };
}

// Historique quotidien en dollars : [[timestampSecondes, prixUsdOnce], ...]
async function usdHistory(stooq, yahoo, from, to) {
  try {
    const csv = await get(`https://stooq.com/q/d/l/?s=${stooq}&d1=${ymd(from).replace(/-/g, '')}&d2=${ymd(to).replace(/-/g, '')}&i=d`, 8000, true);
    const rows = csv.trim().split('\n').slice(1).map((l) => l.split(','));
    const out = rows.map((r) => [Date.parse(r[0] + 'T12:00:00Z') / 1000, parseFloat(r[4])]).filter((p) => p[0] && p[1] > 0);
    if (out.length > 5) return out;
  } catch (e) { if (process.env.COURS_DEBUG) console.error('stooq', e.message); }
  const y = await get(`https://query1.finance.yahoo.com/v8/finance/chart/${yahoo}?period1=${Math.floor(from / 1000)}&period2=${Math.floor(to / 1000)}&interval=1d`, 8000);
  const r = y.chart.result[0], close = r.indicators.quote[0].close;
  return r.timestamp.map((t, i) => [t, close[i]]).filter((p) => p[1] > 0);
}

function sample(points) {
  if (points.length <= MAX_POINTS) return points;
  const step = (points.length - 1) / (MAX_POINTS - 1);
  const out = [];
  for (let i = 0; i < MAX_POINTS; i++) out.push(points[Math.round(i * step)]);
  return out;
}

async function history(stooq, yahoo, range, rate, livePerG, now) {
  const from = new Date(now - DAYS[range] * 864e5);
  const usd = await usdHistory(stooq, yahoo, from, new Date(now));
  const pts = usd.map(([t, p]) => [t, (p * rate(new Date(t * 1000))) / OZ]).filter((p) => p[1] > 0);
  const out = sample(pts);
  if (out.length) out[out.length - 1] = [Math.floor(now / 1000), livePerG]; // la courbe se termine sur le cours instantané
  return out;
}

module.exports = async (req, res) => {
  const range = DAYS[req.query && req.query.range] ? req.query.range : '1m';
  try {
    const [xau, xag, rate] = await Promise.all([
      get('https://api.gold-api.com/price/XAU'),
      get('https://api.gold-api.com/price/XAG'),
      usdEur(),
    ]);
    if (!(xau.price > 0) || !(xag.price > 0)) throw new Error('prix invalide');
    const now = Date.now();
    const m = (usd) => ({ usd_oz: usd, eur_oz: usd * rate, eur_g: (usd * rate) / OZ });
    const or = m(xau.price), argent = m(xag.price);

    // L'historique est facultatif : s'il échoue, les prix s'affichent quand même.
    let hist = { or: null, argent: null };
    try {
      const rateAt = await fxSeries(new Date(now - DAYS[range] * 864e5), new Date(now));
      const [h1, h2] = await Promise.all([
        history('xauusd', 'GC=F', range, rateAt, or.eur_g, now).catch((e) => { if (process.env.COURS_DEBUG) console.error(e); return null; }),
        history('xagusd', 'SI=F', range, rateAt, argent.eur_g, now).catch(() => null),
      ]);
      hist = { or: h1, argent: h2 };
    } catch (e) { /* pas de courbe */ }

    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300');
    res.status(200).json({ updatedAt: new Date(now).toISOString(), range, eur_usd: rate, or, argent, history: hist });
  } catch (e) {
    res.setHeader('Cache-Control', 'no-store');
    if (process.env.COURS_DEBUG) console.error(e);
    res.status(502).json({ error: 'Cours momentanément indisponibles' });
  }
};
