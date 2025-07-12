# Sprint 2 Plan - MVP Excel Calculator

**Duration:** 2 days  
**Goal:** Build working Excel calculator using real Illinois Lanceleaf lease data

## Sprint Goal
Create a functional Excel NPV calculator that can generate a buyout offer using our validated real-world lease terms. Must be demo-ready with actual numbers from our Illinois lease example.

## Sprint Rationale (Based on Sprint 1 Learnings)

### Why Excel Calculator Now:
- **We have real data**: Illinois Lanceleaf lease ($2,600/acre, 2.5% escalators)
- **Missing critical tool**: Can't make offers without valuation capability
- **Next logical step**: From research → working model → business process
- **Stakeholder need**: Need demo-ready tool to show progress

### Why Excel (Not Python):
- **Universally accessible**: Any stakeholder can open and modify
- **Transparent calculations**: All formulas visible for validation
- **Rapid iteration**: Faster to build and test than coding
- **Business standard**: Finance industry expects Excel models

## User Stories

### Story 1: Basic NPV Calculator
**As a** SpiceFlow analyst  
**I want** to input lease details and get NPV  
**So that** I can quickly value any solar lease  

**Acceptance Criteria:**
- [ ] Excel file with inputs: Annual Rent, Years Remaining, Escalator %, Discount Rate
- [ ] NPV calculation using standard formula: `=NPV(discount_rate, cash_flows)`
- [ ] Output: Present Value and Max Buyout Offer (80% of PV)
- [ ] Tested with Illinois Lanceleaf data: $95,680/year, 23 years, 2.5% escalators

### Story 2: Escalator Modeling
**As a** SpiceFlow analyst  
**I want** to model annual rent increases  
**So that** my valuations reflect real lease terms  

**Acceptance Criteria:**
- [ ] Escalating cash flow calculations year-by-year
- [ ] Formula: Year N rent = Base Rent × (1 + Escalator)^N
- [ ] Validates against our 3 lease examples (1.5%, 2%, 2.5% escalators)
- [ ] Visual cash flow timeline showing rent growth

### Story 3: Risk-Based Discount Rates
**As a** SpiceFlow analyst  
**I want** to apply different discount rates based on risk  
**So that** my offers reflect deal quality  

**Acceptance Criteria:**
- [ ] Dropdown for Risk Tier: Low (8%), Medium (12%), High (16%)
- [ ] Risk tier descriptions based on our research:
  - Low: Operating project, strong developer (Carolina Solar Energy)
  - Medium: Under construction, mid-tier developer (Lanceleaf Solar)
  - High: Development stage, unknown developer
- [ ] Discount rate automatically updates NPV calculation

### Story 4: Real-World Validation
**As a** SpiceFlow stakeholder  
**I want** to see the calculator tested against our real lease data  
**So that** I trust the model's accuracy  

**Acceptance Criteria:**
- [ ] Test case 1: Illinois Lanceleaf ($2,600/acre, 36.8 acres, 2.5% escalators)
- [ ] Test case 2: Wyoming Laramie ($200/acre, estimated terms, 1.5% escalators)
- [ ] Test case 3: Kentucky (hypothetical rates, 1.5%-2% escalators)
- [ ] Results documented with buyout offers for each scenario

## Sprint Backlog & Time Estimates

### Day 1: Core Calculator (4 hours)
1. **Excel structure setup** (30 min)
   - Input section with clear labels
   - Calculation section with formulas
   - Output section with results
2. **NPV formula implementation** (45 min)
   - Annual cash flow calculations with escalators
   - NPV function with user-defined discount rate
   - Buyout offer calculation (80% of NPV)
3. **Risk tier dropdown** (15 min)
   - Data validation dropdown for Low/Medium/High
   - Linked discount rates (8%/12%/16%)
4. **Test with Illinois data** (30 min)
   - Input: $95,680 annual, 23 years, 2.5% escalator
   - Validate output makes sense vs. industry standards

### Day 2: Validation & Documentation (2 hours)
1. **Multi-scenario testing** (45 min)
   - Test all 3 lease examples
   - Document results and assumptions
2. **Error checking** (15 min)
   - Input validation (no negative numbers, reasonable ranges)
   - Formula verification
3. **Documentation** (30 min)
   - Instructions tab in Excel
   - Assumptions and limitations documented
4. **Demo preparation** (30 min)
   - Save test scenarios as examples
   - Prepare walkthrough narrative

## Definition of Done

### Technical Requirements:
- [ ] Excel file calculates NPV correctly using standard finance formulas
- [ ] All inputs validated (no crashes with bad data)
- [ ] Tested with real lease data from Sprint 1
- [ ] Saved in `/tools/excel/spiceflow-calculator-v1.xlsx`

### Business Requirements:
- [ ] Generates reasonable buyout offers (validate against Renewa 12.5x benchmark)
- [ ] Can process all 3 lease types from our research
- [ ] Demo-ready with sample scenarios
- [ ] Documentation explains assumptions and limitations

### Validation Criteria:
- [ ] Illinois Lanceleaf test: $95,680 annual → reasonable NPV (~$800K-$1.2M range)
- [ ] Wyoming test: $230,000 annual → reasonable NPV (~$2M-$3M range)
- [ ] Results align with industry standards (Renewa pays ~12.5x annual rent)

## Expected Outputs

### Primary Deliverable:
`/tools/excel/spiceflow-calculator-v1.xlsx` with:
- Input sheet for lease parameters
- Calculation engine with NPV formulas
- Results summary with buyout offer
- Test scenarios tab with our 3 real leases

### Secondary Deliverables:
- Documentation of model assumptions
- Test results comparing our outputs to industry benchmarks
- Gap analysis: what's missing for real-world use

## Risk Mitigation

### Technical Risks:
- **Excel formula errors**: Test extensively with known inputs
- **Complex escalator calculations**: Start simple, add complexity incrementally
- **User input errors**: Add data validation and error checking

### Business Risks:
- **Unrealistic outputs**: Validate against industry standards (Renewa, Landmark Dividend)
- **Missing lease complexity**: Document assumptions and limitations clearly
- **Oversimplification**: Focus on 80% use case, note edge cases for future sprints

## Success Criteria

### Sprint Success = Demo-Ready Calculator
- Can input real lease terms and get defensible buyout offer
- Tested against our 3 lease examples with documented results
- Model assumptions clearly stated and reasonable
- Ready to show stakeholders tangible progress

### Sprint Failure = Non-Functional Tool
- Calculator doesn't work with real data
- Outputs are obviously wrong or unrealistic
- No validation against industry benchmarks
- Can't demo with confidence

---

**Next Sprint Preview**: Enhanced features (early termination modeling, sensitivity analysis, professional formatting for stakeholder presentations)

**Key Dependencies**: None - we have all data needed from Sprint 1  
**Stakeholder Demo**: Friday end-of-sprint review with working calculator