# SpiceFlow Calculator v2 - Instructions

This Markdown report provides a market-competitive valuation tool with size-based pricing and a sensitivity dashboard.

## How to Use
1. Run `python tools/excel/create_calculator_v2.py`.
2. Enter your lease information when prompted:
   - **Annual Base Rent**
   - **Years Remaining**
   - **Annual Escalator (%)**
   - **Risk Tier** – Low, Medium, or High.
3. Review the generated `spiceflow-calculator-v2.md` report.
   - **Buyout Offer** automatically applies size-based percentages and a minimum multiple of 8× annual rent.
   - **Deal Quality Rating** compares the offer to Renewa’s 12.5× benchmark.
4. The report includes a sensitivity section showing NPV outputs across discount rates (6–16%) and buyout percentages (80–95%).

## New Features in v2
- Markdown format with clean tables.
- CLI prompts for risk tier selection.
- **Dynamic pricing formula**:
  - < $100k rent → up to 95% of NPV
  - $100k–$500k rent → up to 90% of NPV
  - > $500k rent → up to 85% of NPV
  - Minimum 8× multiple enforced.
- **Sensitivity** section for quick scenario analysis.

The report is saved at `tools/excel/spiceflow-calculator-v2.md`.
