export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();
  const { dex_a_price, dex_b_price } = req.body || {};
  const pa = parseFloat(dex_a_price || 1.000);
  const pb = parseFloat(dex_b_price || 1.000);
  const spread_pct = parseFloat((((pb - pa) / pa) * 100).toFixed(3));
  const is_ghost_spread = spread_pct >= 0.20;

  return res.status(200).json({
    spread_pct: spread_pct,
    is_ghost_spread: is_ghost_spread,
    route: is_ghost_spread ? "PRIVATE_FLASHBOTS_BUNDLE" : "NONE"
  });
}
