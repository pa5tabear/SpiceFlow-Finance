# Sprint 3 Plan - Python CLI & Test-Driven Validation

**Duration:** 2 days  
**Goal:** Build production-ready Python valuation CLI with comprehensive testing and automated competitive validation

## Sprint Goal
Leverage the existing `lease_valuation.py` engine to create a professional CLI interface with unit tests and automated validation that generates competitive offers. Replace manual CSV maintenance with programmatic validation.

## Sprint Rationale (Based on Technical Feedback)

### Critical Issues to Address:
- **Escalator formula bug** in CSV calculator (Year 2 = Year 1 instead of proper escalation)
- **Manual validation process**: Hand-maintained `validation_results.csv` prone to errors
- **No unit testing**: Can't verify accuracy or prevent regressions
- **CSV limitations**: No professional UX, error-prone manual updates

### Technical Opportunity:
- **Python engine exists**: `tools/python/lease_valuation.py` is clean, auditable <100 LOC
- **Professional foundation**: Proper NPV calculations, supports custom escalators
- **Automation potential**: CLI interface + batch processing capabilities
- **Testing framework**: Pytest with real lease fixture cases

## User Stories

### Story 1: CLI Valuation Interface
**As a** SpiceFlow analyst  
**I want** to run valuations from command line  
**So that** I can batch process deals and integrate with other tools  

**Acceptance Criteria:**
- [ ] CLI interface: `python -m lease_valuation --annual-rent 95680 --years 23 --escalator 0.025`
- [ ] JSON input support: `python -m lease_valuation --input sample.json`
- [ ] Batch processing: `python -m lease_valuation --batch tests/test_cases.csv`
- [ ] Output formats: JSON, CSV, and human-readable

### Story 2: Comprehensive Unit Testing
**As a** developer maintaining the valuation engine  
**I want** comprehensive test coverage with real lease scenarios  
**So that** I can verify accuracy and prevent regressions  

**Acceptance Criteria:**
- [ ] Pytest test suite covering all functions in `lease_valuation.py`
- [ ] Test fixtures for Illinois, Wyoming, Kentucky lease examples
- [ ] Edge case testing (zero escalators, balloon costs, custom schedules)
- [ ] Automated validation replacing manual `validation_results.csv`

### Story 3: Competitive Pricing Algorithm
**As a** SpiceFlow business manager  
**I want** dynamic pricing that competes with market leaders  
**So that** we win deals while maintaining profitability  

**Acceptance Criteria:**
- [ ] Size-based buyout percentages: 95% for <$100K, 90% for <$500K, 85% for >$500K annual
- [ ] Minimum multiple floors: 8x annual rent baseline regardless of NPV
- [ ] Risk-adjusted pricing by discount rate tier (8%/12%/16%)
- [ ] Profitability safeguard: maintain 15%+ IRR on all offers

### Story 4: Interactive Web Demo (Stretch Goal)
**As a** stakeholder evaluating our tool  
**I want** an interactive web interface  
**So that** I can test scenarios without installing Python  

**Acceptance Criteria:**
- [ ] Streamlit app with input sliders and real-time results
- [ ] Embedded validation against our 3 real lease examples
- [ ] Comparison table vs Renewa 12.5x benchmark
- [ ] Export functionality for calculated scenarios

## Sprint Backlog & Time Estimates

### Day 1: CLI Interface & Unit Testing (6 hours)

#### Morning: CLI Development (3 hours)
1. **Create `__main__.py` module** (1 hour)
   - Command-line argument parsing with argparse
   - Support for individual parameters and JSON input files
   - Batch processing from CSV files
   - Multiple output formats (JSON, CSV, human-readable)

2. **Enhanced competitive pricing logic** (1 hour)
   - Size-based buyout percentage calculation
   - Minimum multiple floor enforcement (8x annual rent)
   - Risk-tier discount rate integration
   - Profitability validation (15% IRR minimum)

3. **JSON configuration system** (1 hour)
   - Sample input files for each lease example
   - Configuration schema for pricing parameters
   - Easy parameter adjustment without code changes

#### Afternoon: Testing Framework (3 hours)
4. **Pytest test suite creation** (2 hours)
   - Test fixtures for Illinois Lanceleaf lease ($95,680 annual)
   - Test fixtures for Wyoming Laramie lease ($230,000 annual)
   - Test fixtures for Kentucky Sullivan lease ($50,000 annual)
   - Edge case tests (zero escalators, balloon costs, custom schedules)
   - Performance tests for large lease portfolios

5. **Automated validation generation** (1 hour)
   - Replace manual `validation_results.csv` with programmatic generation
   - Batch validation script for all test cases
   - Regression testing against known good results

### Day 2: Competitive Enhancement & Demo (4 hours)

#### Morning: Competitive Algorithm (2 hours)
6. **Dynamic pricing implementation** (1 hour)
   - Size-based buyout percentages with smooth transitions
   - Geographic/risk tier adjustments
   - Market benchmark integration (Renewa 12.5x standard)

7. **Business logic validation** (1 hour)
   - Test new pricing against all 3 lease examples
   - Verify 80%+ deals now competitive vs Renewa
   - Document improvement metrics vs Sprint 2 results

#### Afternoon: Documentation & Demo (2 hours)
8. **Professional documentation** (1 hour)
   - README section: CLI usage examples
   - Installation and setup instructions
   - Configuration file documentation
   - Testing and validation procedures

9. **Streamlit demo app (Stretch Goal)** (1 hour)
   - Interactive web interface with input sliders
   - Real-time calculation and results display
   - Embedded test case validation
   - Export functionality for scenarios

## Definition of Done

### Technical Requirements:
- [ ] CLI interface functional with all specified options
- [ ] Pytest test suite with 90%+ code coverage
- [ ] All tests passing with real lease data validation
- [ ] Automated validation replacing manual CSV process

### Business Requirements:
- [ ] 80%+ of test cases competitive vs Renewa (up from 33% in Sprint 2)
- [ ] All deals meet minimum 8x multiple floors
- [ ] Profitability maintained (15%+ IRR on all offers)
- [ ] Size-based pricing implemented and validated

### Documentation Requirements:
- [ ] Complete CLI usage documentation
- [ ] Test execution instructions
- [ ] Configuration file examples
- [ ] Validation procedure documentation

## Validation Targets

### Illinois Lanceleaf Test (Current: 7.3x → Target: 8.5x+)
- Input: $95,680 annual, 23 years, 2.5% escalator, Medium risk (12%)
- New logic: 95% buyout (small deal) + 8x minimum floor
- Expected: ~$850K offer → 8.9x multiple ✅

### Wyoming Laramie Test (Current: 9.4x → Maintain)
- Input: $230,000 annual, 23 years, 1.5% escalator, Low risk (8%)
- New logic: 85% buyout (large deal)
- Expected: Maintain competitiveness at 9.4x multiple ✅

### Kentucky Sullivan Test (Current: 7.2x → Target: 8.0x+)
- Input: $50,000 annual, 25 years, 2.0% escalator, Medium risk (12%)
- New logic: 95% buyout (small deal) + 8x minimum floor
- Expected: ~$400K offer → 8.0x multiple ✅

## Risk Assessment & Mitigation

### Technical Risks:
**Risk**: CLI complexity reduces usability  
**Mitigation**: Provide simple JSON input files for common scenarios

**Risk**: Test fixtures become outdated  
**Mitigation**: Use real lease data as ground truth, update when market changes

### Business Risks:
**Risk**: Higher buyout percentages reduce margins  
**Mitigation**: Maintain 15% IRR minimum, adjust only where profitable

**Risk**: Still can't compete on largest deals  
**Mitigation**: Focus on 80% win rate in our target market segments

## Success Metrics

### Primary Success (Must Achieve):
- **Technical**: Working CLI with comprehensive test coverage
- **Business**: 80%+ competitive rate vs Renewa benchmark
- **Process**: Automated validation replacing manual maintenance

### Stretch Success (Nice to Have):
- **Streamlit demo**: Interactive web interface for stakeholders
- **Market leadership**: Identify deals where we beat Renewa
- **Automation**: Full batch processing for lease portfolio analysis

## Expected Outputs

### Primary Deliverables:
- **Enhanced `lease_valuation.py`** with CLI interface and competitive pricing
- **Comprehensive test suite** with real lease fixtures
- **Automated validation system** generating competitive analysis
- **Professional documentation** for installation and usage

### Secondary Deliverables:
- **Sample JSON input files** for each lease type
- **Batch processing scripts** for portfolio analysis
- **Streamlit web demo** (stretch goal)
- **Updated Sprint 3 review** with quantitative results

## Technical Architecture

### File Structure:
```
tools/python/
├── lease_valuation.py          # Core engine (existing)
├── __main__.py                 # CLI interface (new)
├── competitive_pricing.py      # Business logic (new)
├── tests/
│   ├── test_lease_valuation.py # Unit tests (new)
│   ├── test_cli.py            # CLI tests (new)
│   └── fixtures/               # Test data (new)
│       ├── illinois_lease.json
│       ├── wyoming_lease.json
│       └── kentucky_lease.json
└── examples/
    ├── sample_input.json       # CLI usage examples
    └── batch_test_cases.csv    # Batch processing example
```

---

**Next Sprint Preview**: LOI template creation and landowner outreach automation  
**Key Insight**: Sprint 3 transforms us from "functional prototype" to "production-ready tool"  
**Stakeholder Value**: Professional CLI tool with automated validation and competitive offers
> ⚠️  **Update (2025-07-12):** Excel and Streamlit references below are now out-of-scope.  Transition focus to CLI + JSON pipeline as defined in *Sprint-4 guidance*.