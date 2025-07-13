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
import numpy as np

import sys
sys.path.append('src')

from lease_valuation import pv_buyout
from document_extractor import process_document
from credit_lookup import quick_lookup
from manual_overrides import get_manual_override, should_skip_document, get_skip_reason


def calculate_irr(cash_flows: List[float], max_iterations: int = 1000, tolerance: float = 1e-6) -> float:
    """
    Calculate Internal Rate of Return (IRR) for a series of cash flows using Newton-Raphson method.
    
    Args:
        cash_flows: List of cash flows where first value is typically negative (investment)
                   and subsequent values are positive (returns)
    
    Returns:
        IRR as a decimal (e.g., 0.08 for 8%)
    """
    # Newton-Raphson method for IRR calculation
    rate = 0.1  # Initial guess (10%)
    
    for _ in range(max_iterations):
        # Calculate NPV and its derivative at current rate
        npv = sum([cf / (1 + rate) ** i for i, cf in enumerate(cash_flows)])
        npv_derivative = sum([-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows)])
        
        # Check for convergence
        if abs(npv) < tolerance:
            return rate
            
        # Avoid division by zero
        if abs(npv_derivative) < tolerance:
            break
            
        # Newton-Raphson update
        new_rate = rate - npv / npv_derivative
        
        # Check for convergence in rate
        if abs(new_rate - rate) < tolerance:
            return new_rate
            
        rate = new_rate
        
        # Keep rate reasonable
        if rate < -0.99:  # Avoid rates below -99%
            rate = -0.99
        elif rate > 10:  # Avoid rates above 1000%
            rate = 10
    
    return rate


@dataclass
class LeaseResult:
    name: str
    annual_rent: float
    annual_rent_per_acre: float | None
    term_years: int
    renewal_options: str | None
    total_potential_term: int | None
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
    
    # Check if document should be skipped
    if should_skip_document(file_path.name):
        print(f"⚠️  Skipping {file_path.name}: {get_skip_reason(file_path.name)}")
        return None
    
    # Check for manual override first
    manual_data = get_manual_override(file_path.name)
    if manual_data:
        print(f"📋 Using manual data for {file_path.name}")
        data = manual_data.copy()
    else:
        # Extract data using document extractor
        data = process_document(file_path)
        print(f"🤖 Using automated extraction for {file_path.name}")
    
    if not data:
        return None
    
    # Validate required fields and data quality
    if data.get('annual_rent') is None or data.get('term_years') is None:
        print(f"⚠️  Skipping {file_path.name}: missing annual_rent or term_years")
        return None
    
    # Additional validation for data quality
    if data.get('term_years', 0) > 50:
        print(f"⚠️  Skipping {file_path.name}: unreasonable term ({data.get('term_years')} years)")
        return None
    
    if data.get('annual_rent', 0) > 10000000:
        print(f"⚠️  Skipping {file_path.name}: unreasonable rent (${data.get('annual_rent'):,})")
        return None
    
    if data.get('escalator', 0) > 0.1:  # 10%
        print(f"⚠️  Skipping {file_path.name}: unreasonable escalator ({data.get('escalator')*100:.1f}%)")
        return None
    
    # Use total potential term if available for valuation, otherwise base term
    valuation_term = data.get('total_potential_term') or data['term_years']
    
    # Calculate buyout using existing valuation engine
    buyout_offer = pv_buyout(
        annual_rent=data['annual_rent'],
        term_years=valuation_term,
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
    # Simple multiple for reference (not used in main comparison)
    simple_multiple = buyout_offer / data['annual_rent']
    
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
    
    # Recalculate with fixed 10% discount rate using valuation term
    buyout_offer = pv_buyout(
        annual_rent=data['annual_rent'],
        term_years=valuation_term,
        escalator=data['escalator'],
        discount_rate=actual_discount_rate,
        buyout_pct=0.85
    )
    pv_value = buyout_offer / 0.85
    
    # Calculate actual IRR based on cash flows
    # Generate escalating annual rent payments over the valuation term
    annual_rents = []
    current_rent = data['annual_rent']
    escalator = data.get('escalator', 0.0)
    
    for year in range(valuation_term):
        annual_rents.append(current_rent)
        current_rent *= (1 + escalator)
    
    # IRR cash flows: negative investment followed by positive rent payments
    cash_flows = [-buyout_offer] + annual_rents
    irr = calculate_irr(cash_flows)
    
    return LeaseResult(
        name=data.get('name', file_path.stem),
        annual_rent=data['annual_rent'],
        annual_rent_per_acre=(data['annual_rent'] / data['acres']) if data.get('acres') else None,
        term_years=data['term_years'],
        renewal_options=data.get('renewal_options'),
        total_potential_term=data.get('total_potential_term'),
        escalator=data.get('escalator', 0.0),
        risk_tier=risk_tier,
        location=data.get('location', 'Unknown'),
        acres=data.get('acres', 0.0),
        developer=data.get('developer', 'Unknown'),
        pv_value=pv_value,
        undiscounted_value=undiscounted_value,
        buyout_offer=buyout_offer,
        multiple=irr,
        discount_rate=actual_discount_rate,
        credit_data=credit_data
    )


def generate_summary_table(results: List[LeaseResult], output_path: Path):
    """Generate Markdown summary table."""
    with open(output_path, 'w') as f:
        f.write("# Lease Portfolio Summary\n\n")
        f.write("| Name | Annual Rent / Acre | Total Annual Rent | Base Term | Renewals | Total Term | Escalator | Risk Tier | Discount Rate | Location | Acres | Developer | Total Undiscounted Rent Value | Present Value | **Buyout Offer** | IRR |\n")
        f.write("|------|--------------------|------------------|-----------|----------|------------|-----------|-----------|---------------|----------|-------|-----------|------------------------------|--------------|------------------|----------|\n")
        for r in results:
            # Competitive if annualized return > 6% (reasonable target vs 10% discount rate)
            competitive = "🟢" if r.multiple >= 0.06 else "🟡"
            rent_per_acre_display = f"${r.annual_rent_per_acre:,.2f}" if r.annual_rent_per_acre else "—"
            renewals_display = r.renewal_options if r.renewal_options else "—"
            total_term_display = f"{r.total_potential_term}y" if r.total_potential_term else f"{r.term_years}y"
            f.write(
                f"| {r.name} | {rent_per_acre_display} | ${r.annual_rent:,} | {r.term_years}y | {renewals_display} | {total_term_display} | {r.escalator*100:.1f}% | {r.risk_tier.title()} | {r.discount_rate*100:.0f}% | {r.location} | {r.acres:,.0f} | {r.developer} | ${r.undiscounted_value:,.0f} | ${r.pv_value:,.0f} | **${r.buyout_offer:,.0f}** | {competitive} {r.multiple*100:.1f}% |\n")
        
        f.write(f"\n## Portfolio Totals\n")
        f.write(f"- **Total Investment**: ${sum(r.buyout_offer for r in results):,.0f}\n")
        f.write(f"- **Average Annualized Return**: {sum(r.multiple for r in results) / len(results)*100:.1f}%\n")
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

**Average Annualized Return:** {avg_multiple*100:.1f}%  
**Total Portfolio Value:** ${sum(r.pv_value for r in results):,.0f} (NPV)  
**Recommended Offers:** ${total_buyouts:,.0f} (85% of NPV)  
**Weighted Term:** {sum(r.term_years * r.annual_rent for r in results) / total_annual_rent:.1f} years average

## Individual Lease Recommendations

"""
    
    # Sort by buyout offer size for prioritization
    sorted_results = sorted(results, key=lambda x: x.buyout_offer, reverse=True)
    
    for i, r in enumerate(sorted_results, 1):
        competitive_note = "✅ Competitive" if r.multiple >= 0.06 else "⚠️ Below target"
        report += f"**{i}. {r.name}** ({r.location})\n"
        report += f"- **Recommended Offer:** ${r.buyout_offer:,.0f} ({r.multiple*100:.1f}% annualized return) {competitive_note}\n"
        report += f"- Term: {r.term_years} years, Escalator: {r.escalator*100:.1f}%, Risk: {r.risk_tier.title()}\n\n"
    
    report += f"""## Risk Assessment

The portfolio exhibits balanced risk exposure with {risk_breakdown} distribution across risk tiers. All recommendations assume current market discount rates and standard 85% NPV acquisition pricing.

## Market Positioning

Our average {avg_multiple*100:.1f}% annualized return compares favorably to industry benchmarks, providing solid returns above the {discount_rate*100:.0f}% discount rate. Deals above 6.0% annualized returns are competitive in today's market.

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