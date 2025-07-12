# Feedback on *Sprint 2 Review – Excel NPV Calculator Development*

> File reviewed: `project-management/sprint-reviews/sprint-2-review.md`
>
> Review date: $(auto-generated)

---

## 1. Accuracy Check

| Claim in Review | Reality | Suggested Fix |
|-----------------|---------|---------------|
| **All 7 deliverable files exist under `/tools/excel/`** | ✅ True – verified. | — |
| **Calculator validated against 3 lease examples** | ⚠️ Partly – worksheet formulas reference Illinois values; Wyoming & Kentucky numbers are in *validation_results.csv* but not embedded in the model. | Embed the two extra test cases in a separate **“Scenarios”** tab.
| **Competitive multiples quoted** | ⚠️ Uses fixed 12.5× benchmark; industry multiples vary (9–14×). | Document data source for benchmark or add range sensitivity. |
| **Risk-tier lookup fully automated** | ⚠️ Requires manual Risk string entry (no dropdown). | Implement a data-validation dropdown and lock the lookup table. |
| **Buy-out “7.3× multiple” for Illinois** | ❓ Re-run once escalator bug (see §2) is fixed – value likely changes. | Recalculate & update narrative. |

---

## 2. Technical Improvement Opportunities

1. **Escalator Formula Bug**  
   Current CSV uses `=B4*(1+B6)^(A16-1)` for *every* year, so Year 2 equals Year 1. Formula should reference each row’s year index:  
   `Rent_n = Rent_0 × (1+Esc)^(n-1)` → in Excel `=$B$4*(1+$B$6)^(A16-1)` then drag-fill.
2. **NPV vs XNPV**  
   `NPV()` assumes *end-of-period* cash flows and ignores period 0. Consider `XNPV()` with explicit dates, or add Rent for Year 0 if payment due immediately.
3. **CSV ➜ XLSX Migration**  
   Dropdowns, conditional formatting, and charts require an `.xlsx`. Use **openpyxl** or just save manually.
4. **Formatting & UX**  
   • Freeze header row, format currency and percentages.  
   • Conditional colour-coding for Competitive/Fair/Below Market.  
   • Protect formula cells to prevent accidental edits.
5. **Parameter Table**  
   Centralise constants (buy-out %; benchmark multiple) so stakeholders can tweak without touching formulas.

---

## 3. Business & Strategy Observations

1. **Multiple Floors**  
   Adopt a minimum offer multiple (e.g., 8× rent) to stay competitive on small deals.
2. **Dynamic Buy-out %**  
   Instead of a flat 80 %, scale with deal size or risk tier.
3. **Market Benchmark Sources**  
   Validate Renewa 12.5× figure with at least two additional acquirers (e.g., Landmark Dividend, SolRiver Capital).
4. **Deal Profitability Model**  
   Add an internal IRR calculation to see if higher offers are still profitable under exit assumptions.

---

## 4. Recommended Actions for Sprint 3

1. **Convert calculator to `.xlsx` with full UX polish.**
2. **Fix escalator and NPV mechanics, then re-run validation.**
3. **Embed multi-scenario tests inside the workbook (Scenarios tab).**
4. **Enhance documentation**: add a *Model Assumptions* section and unit-test sheet.
5. **Re-write business narrative in Sprint-2 Review** after recalculation.

---

*Prepared by: AI code-review assistant* 