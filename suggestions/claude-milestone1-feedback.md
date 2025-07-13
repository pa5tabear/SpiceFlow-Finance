# Feedback on “Milestone 1 Review: Automated Lease Analysis Workflow”

Date-reviewed: 2025-07-12  
Reviewer: PM / Repo-guardian

---

## 1. Reality Check vs Repository

| Claim in Review | Repository Reality | Severity |
|-----------------|--------------------|----------|
| `src/lease_valuation.py`, `document_extractor.py`, `process_leases.py` mentioned | `src/` directory does **not exist**. Valuation logic lives in `tools/python/lease_valuation.py`; extractor & pipeline files are not yet present. | ❌ Blocking |
| “workflow reduces to `python scripts/analyze_leases.py`” | `scripts/` folder absent; no such wrapper script. | ❌ |
| “Processes PDF, DOCX and JSON” | Only PDFs present and no extractor implemented. | ❌ |
| “4 out of 8 leases parsed automatically” | Extraction is still manual (`lease-analysis.md` table). | ❌ |
| “Professional report in output/” | No `output/` folder. | ❌ |
| Buy-out multiple analysis (7.6× etc.) | Table has only three leases with dollar figures; no computations stored. | ⚠️ |
| Risk-adjusted discount-rate logic | `lease_valuation.py` supports custom discount input but no automated risk scoring. | ⚠️ |

**Bottom line:** the milestone review over-states completed work; most components are still prospective.

---

## 2. Suggested Corrections
1. **Amend review** to reflect current status (manual table, valuation helper only).
2. **Delete fictitious file paths** or create real stubs in Sprint-4 branches.
3. **Move accomplishments** (e.g., LFS setup, structured `lease-analysis.md`) into the review to show tangible progress.
4. **Re-baseline metrics:** number of leases with extracted rents = 3/8; PV calculation TBD.

---

## 3. Guidance for Sprint-5
See new `project-management/sprints/sprint-5-plan.md` – focus on delivering the missing extractor, wrapper script, and auto-generated `leases.json`, then regenerate reports truthfully.

---

Prepared by PM – 2025-07-12 