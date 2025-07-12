# Sprint 1 Plan - MVP Calculator
**Duration:** 3 days  
**Goal:** Single Excel file that can calculate a buyout offer in under 2 minutes

## Sprint Goal
Create the absolute minimum viable product - one Excel file that takes 3 inputs and produces a buyout offer number that we can test with 1 real landowner.

## User Stories (Sprint 1 Only)

### Story 1: Basic NPV Calculator
**As a** SpiceFlow analyst  
**I want** to input lease details and get an NPV  
**So that** I can quickly estimate what a lease is worth

**Acceptance Criteria:**
- [ ] Excel file with 3 input cells: Annual Rent, Years Remaining, Risk Tier
- [ ] Dropdown for Risk Tier (Low/Medium/High)
- [ ] Automatic discount rate selection (7%/10%/15%)
- [ ] NPV calculation using standard formula
- [ ] Single output: "Maximum Offer" (80% of NPV)

### Story 2: Simple Sensitivity Table
**As a** SpiceFlow analyst  
**I want** to see how discount rates affect the offer  
**So that** I can understand the impact of risk assessment

**Acceptance Criteria:**
- [ ] Data table showing NPV at 6%, 8%, 10%, 12%, 15% discount rates
- [ ] All calculations automatically update when inputs change

## Definition of Done
- [ ] Excel file opens and calculates correctly
- [ ] Can input Missouri lease data and get reasonable output
- [ ] Tested with at least 1 sample calculation
- [ ] File saved in `/tools/excel/` directory

## Sprint Backlog
1. Create Excel file structure (30 min)
2. Build NPV formula with risk-based discount rates (45 min)
3. Add sensitivity analysis table (30 min)
4. Test with sample data (15 min)

## Demo Criteria
- Input: $50K annual rent, 20 years remaining, Medium risk
- Expected Output: ~$426K maximum offer (NPV ~$532K at 10% discount)

## Sprint Review Questions
1. Can we generate a buyout offer in under 2 minutes?
2. Do the numbers feel reasonable compared to industry standards?
3. Is this sufficient for initial landowner conversation?

---
*Next Sprint Preview: Add escalators, create basic LOI template*