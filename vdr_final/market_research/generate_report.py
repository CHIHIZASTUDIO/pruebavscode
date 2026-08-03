#!/usr/bin/env python3
"""
Market Report Generator
=========================
Generates an HTML market report from comparables.json.

Produces a professional, investor-ready report that can be
incorporated into the VDR or shared standalone.
"""

import json
import os
import sys
from datetime import datetime


def load_comparables(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_html_report(data):
    props = data.get("top_comparables", [])
    summary = data

    rows = ""
    for i, p in enumerate(props):
        rows += f"""
        <tr>
          <td>{i + 1}</td>
          <td>{p.get("name", "—")}</td>
          <td>{p.get("similarity_score", 0)}%</td>
          <td>USD {p.get("adr_usd", 0):,.2f}</td>
          <td>{p.get("occupancy_percent", 0)}%</td>
          <td>{p.get('rating', '—')}</td>
          <td>{p.get('platform', '—')}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Market Intelligence Report — La Nuit</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', -apple-system, sans-serif; background: #0a0a0a; color: #e5e5e5; padding: 2rem; }}
  .container {{ max-width: 900px; margin: 0 auto; }}
  h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
  h2 {{ font-size: 1.2rem; margin: 2rem 0 1rem; border-bottom: 2px solid #f59e0b; padding-bottom: 0.5rem; }}
  h3 {{ font-size: 1rem; margin: 1.5rem 0 0.75rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; margin: 1rem 0; }}
  th, td {{ padding: 0.5rem 0.75rem; border: 1px solid #2a2a2a; text-align: left; }}
  th {{ background: #1a1a1a; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; color: #888; }}
  .metric {{ display: inline-block; background: #141414; border: 1px solid #2a2a2a; border-radius: 8px; padding: 1rem 1.5rem; margin: 0.5rem; text-align: center; }}
  .metric .value {{ font-size: 1.5rem; font-weight: 700; }}
  .metric .label {{ font-size: 0.7rem; text-transform: uppercase; color: #888; margin-top: 0.25rem; }}
  .footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #2a2a2a; font-size: 0.75rem; color: #888; }}
  .highlight {{ background: #1a1a1a; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: 600; }}
</style>
</head>
<body>
<div class="container">
  <h1>Market Intelligence Report</h1>
  <p><strong>Location:</strong> {summary.get('location', 'La Vega, Cundinamarca')}</p>
  <p><strong>Period:</strong> {summary.get('period', 'TTM')}</p>
  <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

  <h2>Market Overview</h2>
  <div>
    <div class="metric"><div class="value">USD {summary.get('market_avg_adr', 0):,.0f}</div><div class="lbl">Avg ADR</div></div>
    <div class="metric"><div class="value">{summary.get('market_avg_occupancy', 0)}%</div><div class="lbl">Avg Occupancy</div></div>
    <div class="metric"><div class="val">{summary.get('total_properties', 0)}</div><div class="lbl">Properties</div></div>
  </div>

  <h2>Top 8 Comparables (Ranked by Similarity)</h2>
  <table>
    <thead><tr><th>#</th><th>Property</th><th>Similarity</th><th>ADR</th><th>Occupancy</th><th>Rating</th><th>Source</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>

  <h2>La Nuit Projection vs Market</h2>
  <table>
    <thead><tr><th>Year</th><th>Projected ADR</th><th>Market Context</th></tr></thead>
    <tbody>
      <tr><td>Year 1</td><td>USD 143</td><td>Below market — new property, no brand recognition</td></tr>
      <tr><td>Year 2</td><td>USD 238</td><td>Approaching market average (USD {summary.get('market_avg_adr', 0):,.0f})</td></tr>
      <tr><td>Year 3</td><td><span class="highlight">USD 357</span></td><td>Within market range — validated by comparables</td></tr>
    </tbody>
  </table>

  <div class="footer">
    <p>Source: AirROI / AirDNA / Booking.com / Airbnb — La Vega, Cundinamarca, Colombia</p>
    <p>Prepared by CHIHIZA Studio for Conrad Pramböck</p>
  </div>
</div>
</body>
</html>"""

    return html


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    comparables_path = os.path.join(base_dir, "output", "comparables.json")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(comparables_path):
        print("Error: comparables.json not found. Run generate_json.py first.")
        sys.exit(1)

    data = load_comparables(comparables_path)
    html = generate_html_report(data)

    output_path = os.path.join(output_dir, "market_report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_path}")
    print(f"Size: {len(html):,} bytes")


if __name__ == "__main__":
    main()