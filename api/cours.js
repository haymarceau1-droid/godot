// Fonction serverless Vercel : cours spot de l'or et de l'argent, convertis en euros.
// Le navigateur n'appelle que ce site (/api/cours) : aucune requête tierce côté visiteur, aucune clé exposée.
// Sources : gold-api.com (cours XAU/XAG en dollars, sans clé) et Frankfurter / BCE (taux USD→EUR).
const OZ = 31.1034768; // grammes dans une once troy

async function getJson(url, ms = 5000) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(url, { signal: ctl.signal, headers: { accept: 'application/json' } });
    if (!r.ok) throw new Error(url + ' → ' + r.status);
    return await r.json();
  } finally { clearTimeout(t); }
}

async function usdEur() {
  try {
    const d = await getJson('https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR');
    if (d && d.rates && d.rates.EUR > 0) return d.rates.EUR;
  } catch (e) { /* on tente la source de secours */ }
  const d = await getJson('https://open.er-api.com/v6/latest/USD');
  if (d && d.rates && d.rates.EUR > 0) return d.rates.EUR;
  throw new Error('taux USD/EUR indisponible');
}

function metal(usd, rate) {
  const eurOz = usd * rate;
  return { usd_oz: usd, eur_oz: eurOz, eur_g: eurOz / OZ };
}

module.exports = async (req, res) => {
  try {
    const [xau, xag, rate] = await Promise.all([
      getJson('https://api.gold-api.com/price/XAU'),
      getJson('https://api.gold-api.com/price/XAG'),
      usdEur(),
    ]);
    if (!(xau.price > 0) || !(xag.price > 0)) throw new Error('prix invalide');
    res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300');
    res.status(200).json({
      updatedAt: new Date().toISOString(),
      eur_usd: rate,
      or: metal(xau.price, rate),
      argent: metal(xag.price, rate),
    });
  } catch (e) {
    res.setHeader('Cache-Control', 'no-store');
    res.status(502).json({ error: 'Cours momentanément indisponibles' });
  }
};
