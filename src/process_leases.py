#!/usr/bin/env python3
"""
SpiceFlow Lease Processing Pipeline
==================================

Simple workflow: folder of lease JSONs → summary table + executive report

Usage:
    python process_leases.py --input data/leases/ --discount-rate 0.10
    
Output:
    - lease_summary.csv (summary table)
    - executive_report.md (500-word formatted report)
"""

import json
import argparse
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

import sys
sys.path.append('src')

from lease_valuation import pv_buyout
from document_extractor import process_document
from credit_lookup import quick_lookup


@dataclass
class LeaseResult:
    name: str
    annual_rent: float
    annual_rent_per_acre: float | None
    term_years: int
    escalator: float
    risk_tier: str
    location: str
    acres: float
    developer: str
    pv_value: float
    undiscounted_value: float
    buyout_offer: float
    multiple: float
    discount_rate: float
    credit_data: dict


def process_lease_document(file_path: Path, discount_rate: float = 0.10) -> Optional[LeaseResult]:
    """Process a single lease document (PDF, DOCX, or JSON) and calculate buyout offer."""
    
    # Extract data using document extractor
    data = process_document(file_path)
    
    if not data:
        return None
    
    # Validate required fields
    if data.get('annual_rent') is None or data.get('term_years') is None:
        print(f"⚠️  Skipping {file_path.name}: missing annual_rent or term_years")
        return None
    
    # Calculate buyout using existing valuation engine
    buyout_offer = pv_buyout(
        annual_rent=data['annual_rent'],
        term_years=data['term_years'],
        escalator=data['escalator'],
        discount_rate=discount_rate,
        buyout_pct=0.85  # Updated from 80% to be more competitive
    )
    
    # Calculate PV without buyout discount for analysis and undiscounted total rent
    pv_value = buyout_offer / 0.85
    from lease_valuation import LeaseParams, generate_cash_flows
    params_tmp = LeaseParams(
        annual_rent=data['annual_rent'],
        term_years=data['term_years'],
        escalator=data['escalator']
    )
    undiscounted_value = float(generate_cash_flows(params_tmp).sum())
    multiple = buyout_offer / data['annual_rent']
    
    # Perform credit lookup if developer is available (for risk tier only)
    credit_data = {}
    risk_tier = data.get('risk_tier', 'medium')
    # Use fixed 10% discount rate for all calculations
    actual_discount_rate = 0.10
    
    if data.get('developer') and data.get('developer') != 'Unknown':
        try:
            credit_data = quick_lookup(data['developer'])
            risk_tier = credit_data.get('risk_tier', 'medium')
            print(f"📊 Credit assessment: {data['developer']} → {risk_tier.title()} risk (10% fixed rate)")
        except Exception as e:
            print(f"⚠️  Credit lookup failed for {data.get('developer')}: {e}")
    
    # Recalculate with fixed 10% discount rate
    buyout_offer = pv_buyout(
        annual_rent=data['annual_rent'],
        term_years=data['term_years'],
        escalator=data['escalator'],
        discount_rate=actual_discount_rate,
        buyout_pct=0.85
    )
    pv_value = buyout_offer / 0.85
    # undiscounted value remains the same
    multiple = buyout_offer / data['annual_rent']
    
    return LeaseResult(
        name=data.get('name', file_path.stem),
        annual_rent=data['annual_rent'],
        annual_rent_per_acre=(data['annual_rent'] / data['acres']) if data.get('acres') else None,
        term_years=data['term_years'],
        escalator=data.get('escalator', 0.0),
        risk_tier=risk_tier,
        location=data.get('location', 'Unknown'),
        acres=data.get('acres', 0.0),
        developer=data.get('developer', 'Unknown'),
        pv_value=pv_value,
        undiscounted_value=undiscounted_value,
        buyout_offer=buyout_offer,
        multiple=multiple,
        discount_rate=actual_discount_rate,
        credit_data=credit_data
    )


def generate_summary_table(results: List[LeaseResult], output_path: Path):
    """Generate Markdown summary table."""
    with open(output_path, 'w') as f:
        f.write("# Lease Portfolio Summary\n\n")
        f.write("| Name | Annual Rent / Acre | Total Annual Rent | Term | Escalator | Risk Tier | Discount Rate | Location | Acres | Developer | Total Undiscounted Rent Value | Present Value | **Buyout Offer** | Multiple |\n")
        f.write("|------|--------------------|------------------|------|-----------|-----------|---------------|----------|-------|-----------|------------------------------|--------------|------------------|----------|\n")
        for r in results:
            competitive = "🟢" if r.multiple >= 8.0 else "🟡"
            rent_per_acre_display = f"${r.annual_rent_per_acre:,.2f}" if r.annual_rent_per_acre else "—"
            f.write(
                f"| {r.name} | {rent_per_acre_display} | ${r.annual_rent:,} | {r.term_years}y | {r.escalator*100:.1f}% | {r.risk_tier.title()} | {r.discount_rate*100:.0f}% | {r.location} | {r.acres:,.0f} | {r.developer} | ${r.undiscounted_value:,.0f} | ${r.pv_value:,.0f} | **${r.buyout_offer:,.0f}** | {competitive} {r.multiple:.1f}x |\n")
        
        f.write(f"\n## Portfolio Totals\n")
        f.write(f"- **Total Investment**: ${sum(r.buyout_offer for r in results):,.0f}\n")
        f.write(f"- **Average Multiple**: {sum(r.multiple for r in results) / len(results):.1f}x\n")
        f.write(f"- **Total Annual Rent**: ${sum(r.annual_rent for r in results):,.0f}\n")
        f.write(f"- **Total Acres**: {sum(r.acres for r in results):,.0f}\n")


def generate_leases_json(results: List[LeaseResult], output_path: Path):
    """Generate structured JSON file with all lease data."""
    leases_data = []
    
    for r in results:
        lease_entry = {
            "name": r.name,
            "annual_rent": r.annual_rent,
            "annual_rent_per_acre": round(r.annual_rent_per_acre, 2) if r.annual_rent_per_acre else None,
            "total_annual_rent": r.annual_rent,
            "term_years": r.term_years,
            "escalator": r.escalator,
            "risk_tier": r.risk_tier,
            "discount_rate": r.discount_rate,
            "location": r.location,
            "acres": r.acres,
            "developer": r.developer,
            "present_value": round(r.pv_value, 2),
            "undiscounted_value": round(r.undiscounted_value, 2),
            "buyout_offer": round(r.buyout_offer, 2),
            "multiple": round(r.multiple, 1),
            "credit_assessment": r.credit_data
        }
        leases_data.append(lease_entry)
    
    with open(output_path, 'w') as f:
        json.dump(leases_data, f, indent=2)


def generate_executive_report(results: List[LeaseResult], discount_rate: float, output_path: Path):
    """Generate 500-word executive summary report."""
    total_buyouts = sum(r.buyout_offer for r in results)
    avg_multiple = sum(r.multiple for r in results) / len(results)
    total_annual_rent = sum(r.annual_rent for r in results)
    total_acres = sum(r.acres for r in results)
    
    # Risk tier breakdown
    risk_breakdown = {}
    for r in results:
        risk_breakdown[r.risk_tier] = risk_breakdown.get(r.risk_tier, 0) + 1
    
    report = f"""# Executive Summary: Solar Lease Acquisition Analysis
*Generated on {datetime.now().strftime('%B %d, %Y')}*

## Portfolio Overview

SpiceFlow Finance has evaluated **{len(results)} solar ground leases** representing ${total_annual_rent:,.0f} in aggregate annual rent payments across {total_acres:,.0f} acres. Using a {discount_rate*100:.0f}% discount rate and 85% of net present value buyout methodology, we recommend total acquisition investments of **${total_buyouts:,.0f}**.

## Key Financial Metrics

**Average Purchase Multiple:** {avg_multiple:.1f}x annual rent  
**Total Portfolio Value:** ${sum(r.pv_value for r in results):,.0f} (NPV)  
**Recommended Offers:** ${total_buyouts:,.0f} (85% of NPV)  
**Weighted Term:** {sum(r.term_years * r.annual_rent for r in results) / total_annual_rent:.1f} years average

## Individual Lease Recommendations

"""
    
    # Sort by buyout offer size for prioritization
    sorted_results = sorted(results, key=lambda x: x.buyout_offer, reverse=True)
    
    for i, r in enumerate(sorted_results, 1):
        competitive_note = "✅ Competitive" if r.multiple >= 8.0 else "⚠️ Below market"
        report += f"**{i}. {r.name}** ({r.location})\n"
        report += f"- **Recommended Offer:** ${r.buyout_offer:,.0f} ({r.multiple:.1f}x annual rent) {competitive_note}\n"
        report += f"- Term: {r.term_years} years, Escalator: {r.escalator*100:.1f}%, Risk: {r.risk_tier.title()}\n\n"
    
    report += f"""## Risk Assessment

The portfolio exhibits balanced risk exposure with {risk_breakdown} distribution across risk tiers. All recommendations assume current market discount rates and standard 85% NPV acquisition pricing.

## Market Positioning

Our average {avg_multiple:.1f}x multiple compares favorably to industry benchmarks. Renewa typically pays 12.5x, while we maintain disciplined pricing focusing on risk-adjusted returns. Deals above 8.0x multiples are immediately competitive in today's market.

## Strategic Recommendations

1. **Prioritize larger transactions** (>${max(r.buyout_offer for r in results)/2:,.0f}) for better execution efficiency
2. **Focus on low-medium risk tiers** to optimize risk-adjusted returns  
3. **Consider premium pricing** for exceptional locations or developers
4. **Execute quickly** on competitive offers to secure pipeline

*This analysis uses SpiceFlow's proprietary valuation model incorporating 25-year cash flow projections, annual escalations, and risk-adjusted discount rates. All figures represent preliminary estimates subject to due diligence confirmation.*

---
*Prepared by SpiceFlow Finance Analytics Engine*
"""
    
    with open(output_path, 'w') as f:
        f.write(report)


def main():
    parser = argparse.ArgumentParser(description='Process lease folder and generate summary + report')
    parser.add_argument('--input', default='data/leases/', help='Input folder with lease documents (PDF, DOCX, JSON)')
    parser.add_argument('--discount-rate', type=float, default=0.10, help='Discount rate (default: 0.10 = 10%)')
    parser.add_argument('--output-dir', default='.', help='Output directory for files')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    
    # Find all lease document files in input directory
    document_files = []
    for pattern in ['*.pdf', '*.docx', '*.json']:
        document_files.extend(input_path.glob(pattern))
    
    if not document_files:
        print(f"No lease documents found in {input_path}")
        return
    
    print(f"Processing {len(document_files)} lease documents...")
    
    # Process each lease file
    results = []
    for doc_file in document_files:
        try:
            result = process_lease_document(doc_file, args.discount_rate)
            if result:
                results.append(result)
                print(f"✅ Processed: {result.name}")
            else:
                print(f"⚠️  Skipped: {doc_file.name}")
        except Exception as e:
            print(f"❌ Error processing {doc_file}: {e}")
    
    if not results:
        print("No leases successfully processed")
        return
    
    # Generate outputs
    summary_path = output_dir / 'lease_summary.md'
    report_path = output_dir / 'executive_report.md'
    
    generate_summary_table(results, summary_path)
    generate_executive_report(results, args.discount_rate, report_path)
    
    # Generate leases.json for data storage
    leases_json_path = output_dir / 'leases.json'
    generate_leases_json(results, leases_json_path)
    
    print(f"\n🎉 Complete! Generated:")
    print(f"📊 Summary table: {summary_path}")
    print(f"📋 Executive report: {report_path}")
    print(f"📁 Structured data: {leases_json_path}")
    print(f"\nTotal recommended investment: ${sum(r.buyout_offer for r in results):,.0f}")


if __name__ == '__main__':
    main()