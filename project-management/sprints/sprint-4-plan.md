# Sprint 4 Plan – Automated PDF → JSON → PV Pipeline

**Duration:** 3 days (Mon–Wed)
**Sprint Goal:** Produce a command-line toolchain that converts at least three real lease PDFs into structured JSON, feeds each JSON into `lease_valuation.py`, and appends the results to `leases.json` for immediate tabular visualisation.

---

## Why This Sprint?
* We now have seven real leases (and counting) but term extraction is manual.
* Stakeholders want a reproducible, transparent “folder of leases → buy-out table” workflow.
* Eliminates Excel/CSV legacy, cementing the Python-only direction.

---

## User Stories

### Story 1 – Minimal PDF Extractor (CORE)
**As a** data analyst  
**I want** to run `python extract.py lease.pdf -o lease.json`  
**So that** I get structured terms without manual copy-paste.

*Acceptance Criteria*
- CLI accepts single PDF path and output JSON path.
- Extracts (at minimum) `annual_rent`, `acres`, `escalator_pct`, `term_years`.
- **No hallucination:** if a field is not present verbatim in the document, it must be omitted or set to `null`—never estimated or back-filled.
- Accuracy within ±1 % of hand-checked values.

---

### Story 2 – Batch Extraction & Validation
**As a** power user  
**I want** to process all PDFs in `data/leases/` with one command  
**So that** new leases are ingested in seconds.

*Acceptance Criteria*
- `python extract.py data/leases/*.pdf --out-dir extracted` emits one JSON per lease.
- Skips files whose filename or analysis table is marked `TBD`.
- Emits a summary report: processed ✓ / skipped ⚠️ / errors ❌.

---

### Story 3 – Valuation Glue
**As a** acquisitions associate  
**I want** a single command to compute buy-out offers  
**So that** I can share a clean table with management.

*Acceptance Criteria*
- `python value.py extracted/*.json --append leases.json` computes PV via `lease_valuation.py` and appends/updates rows.
- Outputs Markdown table to stdout (fits directly into `lease-analysis.md`).

---

### Story 4 – Unit Tests & CI
**As a** dev lead  
**I want** automated tests  
**So that** future changes don’t break extraction accuracy.

*Acceptance Criteria*
- Pytest fixture JSON for IL, KY, WY leases.
- ≥90 % coverage on extraction + valuation modules.
- GitHub Action runs `pytest` + `ruff` lint on every PR.

---

### Stretch A – Interactive Demo (optional)
- Simple Streamlit page that uploads a PDF and displays JSON + buy-out.

### Stretch B – Credit-Risk Quick-Score (optional)
- Bash/python script `credit_lookup.py lessee_name` that:
   1. Performs a quick web search (SEC, state corp filings) for the lessee entity.
   2. Returns simple heuristic flags: *public-company*, *SPV age*, presence of *parent guarantee* keywords.
- Result stored as `credit_score` field in the JSON (null if not found).

---

## Backlog & Time Estimates
| Day | Task | Est. hrs |
|-----|------|----------|
| Mon AM | Build `extract.py` regex for Lanceleaf (IL) | 2 |
| Mon PM | Generalise regex & parse KY + WY | 2 |
| Tue AM | Batch mode + summary reporting | 1.5 |
| Tue Mid | `value.py` glue + update `leases.json` | 1.5 |
| Tue PM | Unit tests & fixtures | 2 |
| Wed AM | GitHub Action + docs | 1 |
| Wed PM | Buffer / stretch goal | 2 |

---

## Definition of Done
- `extract.py` & `value.py` runnable from repo root with `--help` flags.
- Three real leases parsed; JSON files stored in `extracted/` (git-ignored).
- `leases.json` updated and renders correctly with pandas snippet.
- Tests pass locally and in CI; ≥90 % coverage.
- No Excel/CSV/UI dependencies introduced.

---

## Out-of-Scope (Explicit)
- Advanced NLP or ML extraction.
- Web dashboards or Excel exports.
- Dynamic pricing optimisation – schedule for Sprint 5.

---

Prepared by PM – 2025-07-12 