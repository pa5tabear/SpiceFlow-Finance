# Feedback on *Sprint 3 Plan – Python Valuation Engine & Testing*

> Goal of this note: make sure Sprint 3 stays laser-focused on the **minimal “PDF → buy-out number” pipeline** with transparent math and defensible sources.  Anything that looks like polish, adjacent products, or premature optimization can wait.

---

## 1. Summary Assessment

| Section | Status | Rationale |
|---------|--------|-----------|
| **CLI valuation engine** | ✅ Keep | Essential for batch runs & automation; aligns with transparency goal. |
| **Comprehensive unit tests** | ✅ Keep | Guarantees math remains correct as logic evolves. |
| **Competitive pricing algorithm (size-based %s, IRR check, optimisation)** | ⚠️  De-scope for now | Adds business strategy complexity; not required to go from PDF → number. Recommend postponing to Sprint 4+. |
| **Interactive web demo (Streamlit)** | ❌ Remove | Nice but non-essential UI; wastes capacity. Stakeholders can read JSON/CSV or a simple CLI output. |
| **Excel native file + professional formatting** | ❌ Remove | Directly contradicts move away from CSV/Excel; introduces dual code paths. |
| **Sensitivity dashboard & charts** | ❌ Remove | Good future enhancement; not needed for MVP calculation. |
| **Market research time-box** | ⚠️  Cut to 30 min sanity-check | A quick benchmark refresh is fine; deep research belongs in a separate spike. |

---

## 2. Lean Sprint 3 Backlog (Suggested)

1. **CLI Wrapper & Batch Mode (core)**  
   • `python -m lease_valuation --json path/to/lease.json`  
   • `python -m lease_valuation --batch leases/*.json`  
   • Output: human-readable summary + machine-readable JSON.
2. **Unit Tests**  
   • Pytest fixtures for the three real leases.  
   • Edge-case tests (zero escalator, negative balloon, 1-year term).
3. **PDF→JSON Extraction Prototype** *(critical path)*  
   • Minimal parser (e.g., regex or manual mapping) that converts a single PDF’s key terms to JSON accepted by the valuation engine.  
   • Document extraction steps so process is transparent.  
   • Hard-code field mapping for one lease; generalisation can follow later.
4. **Documentation**  
   • Update README: sample PDF → extracted JSON → CLI output.  
   • Explain formulae (escalator, discount factors) inline.
5. **Automated Validation Script**  
   • Generates a CSV report comparing engine outputs with manual calculations (sanity-check).  
   • Runs in CI (`pytest && python validate.py`).

_Note: Stretch goals like size-based pricing or Streamlit demo can be listed but explicitly **out of scope** for Sprint 3._

---

## 3. Revised Definition of Done

1. A **single command** converts a prepared JSON term sheet into a buy-out offer, printing PV, offer amount, and effective multiple.
2. All core functions covered by unit tests (≥ 90 % coverage target).
3. At least one real lease PDF successfully parsed into JSON with documented methodology.
4. README contains step-by-step reproduction guide (no proprietary tools needed).

---

## 4. Why This Trimmed Scope Meets Stakeholder Needs

• **Speed**: Delivers tangible, end-to-end pipeline in two days.  
• **Transparency**: Math lives in a plain-text Python file under version control; sources referenced in JSON.  
• **Extensibility**: Once PDF→JSON and valuation are rock-solid, adding GUIs or dynamic pricing is straightforward and low-risk.

---

Prepared by: AI code-review assistant – 2025-07-12 