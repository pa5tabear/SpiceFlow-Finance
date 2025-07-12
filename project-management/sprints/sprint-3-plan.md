# Sprint 3 Plan - Competitive Calculator Enhancement

**Duration:** 2 days  
**Goal:** Make our buyout offers competitive vs Renewa while maintaining profitability

## Sprint Goal
Transform our Excel calculator from "functional but uncompetitive" to "market-leading tool" that can generate offers competitive with Renewa's 12.5x standard while preserving business margins.

## Sprint Rationale (Based on Sprint 2 Learnings)

### Critical Issues to Address:
- **Only 33% competitive** vs Renewa benchmark (1 out of 3 deals)
- **Small deals non-competitive**: 7.2x-7.3x vs Renewa's 12.5x
- **CSV format unprofessional** for stakeholder presentations
- **No sensitivity analysis** to optimize deal parameters

### Strategic Opportunity:
- **Large deals already work**: Wyoming at 9.4x is competitive  
- **Foundation is solid**: Calculator math is correct, just needs tuning
- **Market gap identified**: Size-based pricing could be our advantage
- **Tool sophistication**: Professional Excel will build credibility

## User Stories

### Story 1: Market-Competitive Buyout Offers
**As a** SpiceFlow analyst  
**I want** to generate offers that compete with Renewa  
**So that** landowners choose us over the market leader  

**Acceptance Criteria:**
- [ ] Adjust buyout percentage from 80% to dynamic range (85-95% of NPV)
- [ ] Add minimum multiple floor (8x annual rent regardless of NPV)
- [ ] Implement size-based pricing: Higher percentages for smaller deals
- [ ] Test: 80%+ of our 3 lease examples now competitive vs Renewa

### Story 2: Professional Excel Native File
**As a** stakeholder reviewing our tool  
**I want** a professional-looking Excel file with proper formatting  
**So that** I trust the sophistication of our business  

**Acceptance Criteria:**
- [ ] Convert from CSV to native Excel (.xlsx) format
- [ ] Add data validation dropdowns for Risk Tier selection
- [ ] Professional color scheme and formatting
- [ ] Input cells clearly marked with borders/highlighting
- [ ] Results section formatted as executive summary

### Story 3: Sensitivity Analysis Dashboard
**As a** SpiceFlow analyst  
**I want** to see how different assumptions affect our offers  
**So that** I can optimize deal parameters in real-time  

**Acceptance Criteria:**
- [ ] Data table showing NPV at different discount rates (6%-16%)
- [ ] Buyout percentage slider/scenarios (80%-95%)
- [ ] Minimum multiple impact analysis
- [ ] "Sweet spot" identification for maximum competitiveness

### Story 4: Deal Optimization Engine
**As a** SpiceFlow business manager  
**I want** automated recommendations for optimal offer structure  
**So that** every deal is priced for maximum win probability  

**Acceptance Criteria:**
- [ ] Algorithm that suggests optimal buyout percentage by deal size
- [ ] Risk-adjusted minimum multiples (Low: 8x, Medium: 9x, High: 10x)
- [ ] Competitiveness score vs Renewa benchmark
- [ ] Profitability check (minimum 15% IRR maintained)

## Sprint Backlog & Time Estimates

### Day 1: Competitiveness Overhaul (6 hours)
1. **Market research validation** (1 hour)
   - Research Renewa's cost of capital and margins
   - Validate why they can pay 12.5x consistently
   - Identify our competitive advantages (speed, specialization, etc.)

2. **Dynamic pricing algorithm** (2 hours)
   - Size-based buyout percentages: 
     - <$100K annual: 90-95% of NPV
     - $100K-$500K annual: 85-90% of NPV  
     - >$500K annual: 80-85% of NPV
   - Minimum multiple floors by risk tier
   - Profitability safeguards (max 95% of NPV)

3. **Enhanced calculation engine** (2 hours)
   - Implement new pricing logic
   - Add optimization algorithms
   - Create competitiveness scoring
   - Test against our 3 lease examples

4. **Initial validation** (1 hour)
   - Run all test cases with new pricing
   - Verify 80%+ now competitive vs Renewa
   - Document improvement metrics

### Day 2: Professional Presentation & Analysis (4 hours)
1. **Excel native file creation** (2 hours)
   - Convert to .xlsx format with proper formatting
   - Add data validation dropdowns
   - Professional color scheme and layout
   - Input/output section organization

2. **Sensitivity analysis dashboard** (1.5 hours)
   - Multi-variable data tables
   - Visual indicators for optimal scenarios
   - Competitive positioning charts
   - Risk/return trade-off analysis

3. **Documentation and demo prep** (30 min)
   - Update instructions for new features
   - Create demo script for stakeholders
   - Package deliverables for presentation

## Definition of Done

### Competitiveness Requirements:
- [ ] 80%+ of test cases competitive vs Renewa (up from 33%)
- [ ] All deals meet minimum multiple floors
- [ ] Profitability maintained (15%+ IRR preserved)
- [ ] Size-based pricing implemented and tested

### Professional Tool Requirements:
- [ ] Native Excel file (.xlsx) with proper formatting
- [ ] Data validation dropdowns working
- [ ] Sensitivity analysis functional
- [ ] Demo-ready for stakeholder presentation

### Validation Criteria:
**Illinois Lanceleaf Test (Current: 7.3x → Target: 8.5x+)**
- Input: $95,680 annual, 23 years, 2.5% escalator, Medium risk
- Expected: 90% buyout percentage → ~$788K offer → 8.2x multiple

**Wyoming Laramie Test (Current: 9.4x → Maintain)**
- Input: $230,000 annual, 23 years, 1.5% escalator, Low risk  
- Expected: 85% buyout percentage → maintain competitiveness

**Kentucky Sullivan Test (Current: 7.2x → Target: 8.0x+)**
- Input: $50,000 annual, 25 years, 2.0% escalator, Medium risk
- Expected: 95% buyout percentage → ~$429K offer → 8.6x multiple

## Risk Assessment & Mitigation

### Business Risks:
**Risk**: Higher buyout percentages reduce our margins
**Mitigation**: Maintain 15% IRR minimum, adjust only where profitable

**Risk**: Complex pricing confuses users
**Mitigation**: Automated recommendations with clear explanations

**Risk**: Still can't compete on largest deals
**Mitigation**: Focus on 80% win rate, not 100% - identify our sweet spot

### Technical Risks:
**Risk**: Excel file becomes too complex
**Mitigation**: Keep core calculator simple, add analysis as separate tabs

**Risk**: Formula errors in new pricing logic
**Mitigation**: Extensive testing with known scenarios before deployment

## Success Metrics

### Primary Success (Must Achieve):
- **Competitiveness**: 80%+ of deals competitive vs Renewa
- **Tool Quality**: Professional Excel file ready for stakeholder demo
- **Business Viability**: Maintain 15%+ IRR on all competitive offers

### Stretch Success (Nice to Have):
- **Market Leadership**: Identify deals where we can beat Renewa 
- **Optimization**: Algorithm suggests optimal pricing automatically
- **Sophistication**: Sensitivity analysis rivals industry standards

## Expected Outputs

### Primary Deliverable:
`/tools/excel/spiceflow-calculator-v2.xlsx` with:
- Dynamic size-based pricing engine
- Professional formatting and dropdowns
- Sensitivity analysis dashboard  
- Competitiveness scoring vs benchmarks

### Secondary Deliverables:
- Updated validation results showing improved competitiveness
- Demo script for stakeholder presentation
- Business case documentation for pricing strategy

---

**Next Sprint Preview**: LOI template creation and landowner presentation materials  
**Key Insight**: Sprint 3 transforms us from "functional tool" to "competitive business weapon"  
**Stakeholder Value**: Professional-grade calculator that can win deals against market leaders