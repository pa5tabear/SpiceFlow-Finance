# SpiceFlow Finance NPV Calculator - Instructions

## File: spiceflow-calculator-v1.md

This Markdown file can be viewed in any text editor or GitHub viewer.

## How to Use:

### Step 1: View the Markdown table
1. Generate the file using `create_calculator.py`
2. Open `spiceflow-calculator-v1.md` in your editor or browser

### Step 2: Input Your Lease Data
**Cell B4**: Annual Base Rent (in dollars)
- Example: 95680 (for Illinois Lanceleaf lease)

**Cell B5**: Years Remaining on Lease
- Example: 23 (typical remaining term)

**Cell B6**: Annual Escalator Percentage
- Example: 2.5% (Illinois Lanceleaf rate)
- Format as a percentage if editing manually

**Cell B7**: Risk Tier (Manual Selection)
- Type: "Low", "Medium", or "High"
- This determines discount rate used in NPV calculation

### Step 3: Review Results
The calculator will automatically show:
- **Net Present Value** (Cell B41): Total value of lease payments
- **Buyout Offer** (Cell B42): 80% of NPV (our offer to landowner)
- **Effective Multiple** (Cell B43): Multiple of annual rent we're paying
- **Benchmark Comparison** (Cell B47): How we compare to Renewa's 12.5x standard

## Risk Tier Guide:

### Low Risk (8% discount rate):
- Operating solar project (generating power)
- Strong developer (NextEra, First Solar, etc.)
- Long-term PPA with strong utility
- Clear title, no environmental issues

### Medium Risk (12% discount rate):
- Project under construction or recently operational
- Mid-tier developer with decent track record
- Medium-term PPA or strong regional utility
- Minor title/environmental issues

### High Risk (16% discount rate):
- Development stage (not yet built)
- Weak developer or frequent ownership changes  
- Merchant power or short-term contracts
- Significant regulatory/environmental risks

## Test Cases:

### Illinois Lanceleaf Solar:
- Annual Rent: $95,680
- Years: 23
- Escalator: 2.5%
- Risk: Medium
- Expected NPV: ~$866K
- Expected Offer: ~$693K

### Wyoming City of Laramie:
- Annual Rent: $230,000
- Years: 23
- Escalator: 1.5%
- Risk: Low (government counterparty)
- Expected NPV: ~$2.4M
- Expected Offer: ~$1.9M

## Manual Discount Rate Update:
Currently, you need to manually change the discount rate in the formulas if you change risk tiers:
- Low: Replace 12% with 8% in all formulas (column D)
- High: Replace 12% with 16% in all formulas (column D)

## Validation:
- Check that Effective Multiple (B43) is reasonable (8x-15x annual rent)
- Compare to Renewa benchmark (they pay ~12.5x annual rent)
- Our offers should be 70-85% of gross lease value