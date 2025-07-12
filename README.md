# SpiceFlow Finance

**Land-Based Solar Lease Monetization Platform**

A systematic approach to acquiring and monetizing existing solar ground leases, providing immediate liquidity to landowners while generating returns through long-term cash flows.

## 🎯 Project Overview

SpiceFlow Finance specializes in purchasing existing solar ground leases from landowners, offering immediate cash payments in exchange for future rental income streams. This creates win-win scenarios where landowners receive liquidity today while we capture long-term stable returns.

## 📋 Complete Task Framework

### Phase 0: Foundation (One-Time Setup - PRIORITY)

**Outcome**: Lightweight but repeatable deal-evaluation stack

- [ ] **Excel Cash-Flow Model**
  - Build single-table lease NPV calculator
  - Inputs: remaining term, escalator rates, discount rate
  - Output: Current value and maximum offer price
  
- [ ] **Python Analysis Toolkit** 
  - 300-line Jupyter notebook for automated underwriting
  - API integration for county tax rolls & GIS parcel data
  - GPT-powered lease document parsing (using Pydantic schemas)
  - NPV calculation and "max offer" suggestions
  
- [ ] **Deal Tracking Database**
  - Notion/Airtable setup: Parcel → Status → Offer Value
  - Integration with Python outputs
  - Pipeline tracking and reporting

### Phase 1: Pre-Landowner Meeting (T-7 → T-1 days)

**Outcome**: Clear narrative + defendable first-pass pricing

- [ ] **Property Analysis**
  - Run target parcel through Python underwriting script
  - Compare against neighboring comps for sanity check
  - Pull satellite & GIS overlays (wetlands, flood zones, transmission lines)
  
- [ ] **Landowner Materials**
  - Create "Why Cash Beats 30 Years of Rent" explainer
  - Include IRR comparison tables (Excel → PDF export)
  - Prepare customizable LOI template with $ blanks for real-time editing

### Phase 2: Landowner Meeting (Day 0)

**Outcome**: Win trust; secure verbal agreement to move to LOI

- [ ] **Meeting Strategy**
  - Open with empathetic positioning ("I develop projects too; understand long-tail rent pain")
  - Demo NPV spreadsheet on iPad with sensitivity analysis
  - Address title/liens questions with written follow-up promise
  
- [ ] **Real-Time Negotiation**
  - Live-edit LOI draft during meeting
  - Agree on headline price & exclusivity window
  - Secure list of required documents (original lease, survey, mortgage payoff)

### Phase 3: Post-Meeting → Signed LOI (Day 1-7)

**Outcome**: Binding (but non-final) commitment

- [ ] **Document Execution**
  - Send e-signature LOI within 24 hours (DocuSign)
  - Launch GPT-powered document intake bot
  - Order title search via API integration
  
- [ ] **Due Diligence Updates**  
  - Update Excel model with any discovered lease amendments
  - Weekly polite follow-ups on outstanding documents
  - Mark LOI "executed" once countersigned

### Phase 4: Bank/Warehouse Capital Prep (Parallel from Day 0)

**Outcome**: Credit partner ready to fund at closing

- [ ] **Credit Package**
  - Draft 2-page credit memo (auto-filled from underwriting DB)
  - Include: asset summary, counterparties, cash flows, security package
  
- [ ] **Data Room Assembly**
  - Populate with: LOI, lease, title, environmental screen, parcel map
  - Generate Excel → PDF cash-flow waterfall with DSCR charts
  
- [ ] **Bank Engagement**
  - Schedule 30-min presentation call
  - Send materials 48 hours prior
  - Capture feedback and tighten model assumptions

### Phase 5: Full Diligence & Definitive Docs (Week 2-5)

**Outcome**: Risk cleared; transition LOI → Purchase Agreement

- [ ] **Environmental & Legal**
  - Commission Phase I ESA desktop review (API ordering)
  - Use GPT to scrape key findings and flag red lines
  - Engage local counsel for deed-of-trust drafting
  - Pull UCC searches on developer tenant
  
- [ ] **Final Documentation**
  - Iterate Python model to final price (include financing costs & margin)
  - Draft Purchase & Assignment Agreement
  - Obtain bank internal credit approval
  - Draft funding schedule

### Phase 6: Closing (Week 6-8)

**Outcome**: Cash wired; liens perfected

- [ ] **Transaction Execution**
  - Execute definitive documents via DocuSign
  - Record deed-of-trust/assignment with county e-filing
  - Trigger bank draw and confirm wire receipt
  
- [ ] **Post-Closing**
  - Update database status → "Closed"
  - Auto-generate Closing Binder PDF via Python (pypdf)
  - Send thank-you package to landowner & broker

## 🛠 Technology Stack & Tooling Decisions

### Current Recommendations

| Need | Tool Now | When to Upgrade |
|------|----------|-----------------|
| Financial Modeling | Excel (universal access) | Python + xlwings at 20+ deals/month |
| Bulk Data Processing | Python + Jupyter | Airflow + PostGIS at 100+ parcels/week |
| Document Extraction | GPT-4 via LangChain | Fine-tuned model after 1,000 parsed leases |
| CRM/Pipeline | Notion + Zapier | HubSpot/DealCloud when team > 5 |
| Reporting | Weekly Slack/email | Auto-generated charts when KPIs stable |

### AI Automation Impact

| Task | Manual Time | AI-Assisted | Time Savings |
|------|-------------|-------------|--------------|
| Lease clause extraction | 45 min/lease | GPT + validators | 40 min → 5 min |
| LOI drafting | 30 min | GPT + templates | 27 min → 3 min |
| Title/ESA review | 1 hr/report | GPT risk scoring | 50 min → 10 min |
| Weekly KPI charts | 15 min | Python automation | 14 min → 1 min |

## 🚀 This Week's Sprint (Priority Actions)

- [ ] **Stand up parcel-NPV notebook** (import Missouri leases as test data)
- [ ] **Create landowner explainer PDF** (copy tables from notebook; design in Google Slides)
- [ ] **Customize LOI template** (pre-fill boilerplate clauses)
- [ ] **Identify 3 priority landowners** (book initial meetings)
- [ ] **Draft credit memo skeleton** (placeholder numbers for banks)

## 📁 Repository Structure

```
SpiceFlow Finance/
├── models/
│   ├── excel/           # Financial models and calculators
│   ├── python/          # Jupyter notebooks and scripts
│   └── templates/       # LOI, credit memo, agreement templates
├── data/
│   ├── parcels/         # Property and GIS data
│   ├── leases/          # Lease documents and extracts
│   └── market/          # Comparable sales and market data
├── documents/
│   ├── marketing/       # Landowner presentation materials
│   ├── legal/           # Agreement templates and legal docs
│   └── closing/         # Transaction closing documents
└── tools/
    ├── apis/            # County data and GIS integrations
    ├── ai/              # GPT document processing scripts
    └── automation/      # Zapier workflows and automations
```

## 📈 Success Metrics

- **Deal Velocity**: Target 2-3 LOIs/month initially
- **Conversion Rate**: 60%+ LOI → Closed deals
- **Time to Close**: <60 days from first meeting
- **Cost Efficiency**: <5% of deal value in acquisition costs
- **AI Utilization**: 80%+ document processing automated

## 🔗 Key Integrations

- **DocuSign**: Contract execution and e-signatures
- **County APIs**: Tax roll and parcel data
- **OpenAI GPT-4**: Document analysis and extraction
- **Banking APIs**: Title searches and credit reporting
- **GIS Platforms**: Property mapping and environmental overlays

---

*Last Updated: July 2025*
*Status: Foundation Phase - Setting Up Core Infrastructure*

## Push test line
