#!/usr/bin/env python3
"""Generate a Markdown report with dynamic pricing and sensitivity analysis."""
from __future__ import annotations

import numpy as np
import pandas as pd

RISK_TIERS = {"Low": 0.08, "Medium": 0.12, "High": 0.16}


def cash_flows(annual_rent: float, years: int, escalator: float) -> np.ndarray:
    years_arr = np.arange(years)
    return annual_rent * (1 + escalator) ** years_arr


def present_value(cash_flows: np.ndarray, rate: float) -> float:
    factors = 1 / (1 + rate) ** np.arange(1, len(cash_flows) + 1)
    return float(np.sum(cash_flows * factors))


def dynamic_buyout(npv: float, annual_rent: float) -> tuple[float, float]:
    if annual_rent < 100_000:
        pct = 0.95
    elif annual_rent < 500_000:
        pct = 0.90
    else:
        pct = 0.85
    offer = npv * pct
    floor = annual_rent * 8
    return max(offer, floor), pct


def build_report(annual_rent: float, years: int, escalator: float, risk: str) -> str:
    rate = RISK_TIERS[risk]
    cf = cash_flows(annual_rent, years, escalator)
    npv = present_value(cf, rate)
    offer, pct = dynamic_buyout(npv, annual_rent)
    multiple = offer / annual_rent

    # Sensitivity table
    rows = []
    buyout_pcts = [0.80, 0.85, 0.90, 0.95]
    for dr in [0.06, 0.08, 0.10, 0.12, 0.14, 0.16]:
        row = {"Discount Rate": f"{dr:.0%}"}
        for bp in buyout_pcts:
            pv = present_value(cf, dr)
            row[f"{int(bp*100)}%"] = f"${pv * bp:,.0f}"
        rows.append(row)
    sens_df = pd.DataFrame(rows)

    lines = ["# SpiceFlow Calculator v2 Report", ""]
    lines.append("## Input Parameters")
    lines.append(f"- Annual Base Rent: ${annual_rent:,}")
    lines.append(f"- Years Remaining: {years}")
    lines.append(f"- Annual Escalator: {escalator:.1%}")
    lines.append(f"- Risk Tier: {risk} ({rate:.0%} discount)")
    lines.append("")
    lines.append("## Valuation Results")
    lines.append(f"- Net Present Value: ${npv:,.0f}")
    lines.append(f"- Buyout Offer ({pct*100:.0f}% of NPV, 8x floor): ${offer:,.0f}")
    lines.append(f"- Effective Multiple: {multiple:.1f}x annual rent")
    lines.append("")
    lines.append("## Sensitivity Analysis")
    lines.append(sens_df.to_markdown(index=False))
    lines.append("")
    return "\n".join(lines)


def main(path: str = "tools/excel/spiceflow-calculator-v2.md") -> None:
    try:
        annual_rent = float(input("Annual Base Rent ($): "))
        years = int(input("Years Remaining: "))
        escalator = float(input("Annual Escalator (% decimal e.g. 0.025): "))
        risk = input("Risk Tier [Low/Medium/High]: ").title()
    except KeyboardInterrupt:
        print("\nCancelled")
        return

    report = build_report(annual_rent, years, escalator, risk)
    with open(path, "w") as f:
        f.write(report)
    print(f"✅ Markdown report saved to {path}")


if __name__ == "__main__":
    import sys
    output_path = sys.argv[1] if len(sys.argv) > 1 else "tools/excel/spiceflow-calculator-v2.md"
    main(output_path)
