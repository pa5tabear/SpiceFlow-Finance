# Sprint 1 Plan - Find Real Solar Lease Document
**Duration:** 1 day  
**Goal:** Download and analyze SEC filing ground lease agreement (real public company deal)

## Sprint Goal
Find and download a real-world solar ground lease document (not a template) that we can use to understand actual lease terms and build our valuation model from reality.

## Single User Story

### Story 1: Real Lease Document Acquisition
**As a** SpiceFlow analyst  
**I want** to find and download an actual executed solar ground lease  
**So that** I can build my valuation model based on real-world terms instead of guessing

**Acceptance Criteria:**
- [ ] Find actual executed solar lease document (county records, SEC filing, or court case)
- [ ] Download PDF/document file to `/docs/lease-samples/` directory
- [ ] Extract key financial terms: annual rent, lease duration, escalators, termination clauses
- [ ] Document source and credibility of the lease agreement
- [ ] Create summary of terms for model building

## Search Strategy
1. **County deed records** - Look for recorded solar lease agreements
2. **SEC filings** - Public company exhibits with real lease agreements  
3. **Court cases** - Litigation often includes full lease documents as exhibits
4. **State/federal land leases** - BLM, state land board executed agreements
5. **Municipal records** - City/county solar projects with public lease agreements

## Definition of Done
- [ ] One real solar lease document downloaded and saved
- [ ] Key terms extracted and documented
- [ ] Source credibility verified
- [ ] File properly organized in project structure

## Success Criteria
We have an actual lease document (not a template) that shows:
- Specific dollar amounts for annual rent
- Actual lease duration and escalation terms
- Real developer/landowner names (can be redacted)
- Executed signatures or evidence of being a final agreement

---
*Next Sprint: Build Excel calculator using the real lease terms we find*