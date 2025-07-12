#!/usr/bin/env python3
"""CLI interface for SpiceFlow Finance lease valuation engine.

Usage:
    python -m lease_valuation --annual-rent 95680 --years 23 --escalator 0.025
    python -m lease_valuation --input sample.json
    python -m lease_valuation --batch test_cases.csv
"""

import argparse
import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Any

from lease_valuation import pv_buyout


def get_competitive_buyout_pct(annual_rent: float) -> float:
    """Size-based buyout percentage for competitiveness."""
    if annual_rent < 100000:
        return 0.95  # 95% for small deals (<$100K)
    elif annual_rent < 500000:
        return 0.90  # 90% for medium deals ($100K-$500K)
    else:
        return 0.85  # 85% for large deals (>$500K)


def get_risk_discount_rate(risk_tier: str) -> float:
    """Standard risk-based discount rates."""
    rates = {
        "low": 0.08,    # 8% for low risk
        "medium": 0.12, # 12% for medium risk  
        "high": 0.16    # 16% for high risk
    }
    return rates.get(risk_tier.lower(), 0.12)


def calculate_multiple(offer: float, annual_rent: float) -> float:
    """Calculate offer multiple vs annual rent."""
    return offer / annual_rent if annual_rent > 0 else 0


def enforce_minimum_multiple(offer: float, annual_rent: float, min_multiple: float = 8.0) -> float:
    """Enforce minimum multiple floor for competitiveness."""
    min_offer = annual_rent * min_multiple
    return max(offer, min_offer)


def process_single_valuation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single lease valuation with competitive pricing."""
    
    # Extract parameters
    annual_rent = float(params["annual_rent"])
    term_years = int(params["term_years"])
    escalator = float(params.get("escalator", 0.0))
    risk_tier = params.get("risk_tier", "medium")
    
    # Get competitive parameters
    discount_rate = get_risk_discount_rate(risk_tier)
    buyout_pct = get_competitive_buyout_pct(annual_rent)
    
    # Calculate base offer
    base_offer = pv_buyout(
        annual_rent=annual_rent,
        term_years=term_years,
        escalator=escalator,
        discount_rate=discount_rate,
        buyout_pct=buyout_pct
    )
    
    # Enforce minimum multiple (8x annual rent)
    final_offer = enforce_minimum_multiple(base_offer, annual_rent)
    multiple = calculate_multiple(final_offer, annual_rent)
    
    # Calculate Renewa competitiveness (12.5x benchmark)
    renewa_benchmark = annual_rent * 12.5
    competitiveness_pct = (final_offer / renewa_benchmark) * 100
    
    return {
        "annual_rent": annual_rent,
        "term_years": term_years,
        "escalator": escalator,
        "risk_tier": risk_tier,
        "discount_rate": discount_rate,
        "buyout_percentage": buyout_pct,
        "base_offer": base_offer,
        "final_offer": final_offer,
        "multiple": round(multiple, 1),
        "renewa_benchmark": renewa_benchmark,
        "competitiveness_pct": round(competitiveness_pct, 1),
        "competitive": competitiveness_pct >= 75.0  # 75%+ of Renewa considered competitive
    }


def load_json_input(filepath: str) -> Dict[str, Any]:
    """Load lease parameters from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def process_batch_csv(filepath: str) -> List[Dict[str, Any]]:
    """Process multiple valuations from CSV file."""
    results = []
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert string values to appropriate types
            params = {
                "annual_rent": float(row["annual_rent"]),
                "term_years": int(row["term_years"]),
                "escalator": float(row.get("escalator", 0.0)),
                "risk_tier": row.get("risk_tier", "medium")
            }
            result = process_single_valuation(params)
            result["name"] = row.get("name", f"Deal_{len(results)+1}")
            results.append(result)
    
    return results


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format result for human-readable output."""
    competitive_status = "✅ COMPETITIVE" if result["competitive"] else "⚠️  BELOW MARKET"
    
    return f"""
SpiceFlow Finance Lease Valuation
==================================
Annual Rent: ${result['annual_rent']:,.0f}
Term: {result['term_years']} years
Escalator: {result['escalator']:.1%}
Risk Tier: {result['risk_tier'].title()} ({result['discount_rate']:.0%} discount rate)

OFFER CALCULATION:
Base NPV Offer: ${result['base_offer']:,.0f} ({result['buyout_percentage']:.0%} of NPV)
Final Offer: ${result['final_offer']:,.0f}
Multiple: {result['multiple']:.1f}x annual rent

COMPETITIVENESS:
Renewa Benchmark: ${result['renewa_benchmark']:,.0f} (12.5x)
Our Position: {result['competitiveness_pct']:.1f}% of benchmark
Status: {competitive_status}
"""


def format_csv_output(results: List[Dict[str, Any]]) -> str:
    """Format results as CSV string."""
    if not results:
        return ""
    
    fieldnames = ["name", "annual_rent", "term_years", "escalator", "risk_tier", 
                  "final_offer", "multiple", "competitiveness_pct", "competitive"]
    
    output = []
    output.append(",".join(fieldnames))
    
    for result in results:
        row = [
            result.get("name", ""),
            str(result["annual_rent"]),
            str(result["term_years"]),
            str(result["escalator"]),
            result["risk_tier"],
            str(result["final_offer"]),
            str(result["multiple"]),
            str(result["competitiveness_pct"]),
            str(result["competitive"])
        ]
        output.append(",".join(row))
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="SpiceFlow Finance Lease Valuation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m lease_valuation --annual-rent 95680 --years 23 --escalator 0.025
  python -m lease_valuation --input examples/illinois_lease.json
  python -m lease_valuation --batch examples/test_cases.csv --output-format csv
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--annual-rent", type=float, 
                           help="Annual rent amount in dollars")
    input_group.add_argument("--input", type=str,
                           help="JSON file with lease parameters")
    input_group.add_argument("--batch", type=str,
                           help="CSV file with multiple lease parameters")
    
    # Parameters for manual input
    parser.add_argument("--years", type=int, default=25,
                       help="Lease term in years (default: 25)")
    parser.add_argument("--escalator", type=float, default=0.0,
                       help="Annual escalator rate (e.g., 0.025 for 2.5%%)")
    parser.add_argument("--risk-tier", choices=["low", "medium", "high"], 
                       default="medium", help="Risk assessment tier")
    
    # Output options
    parser.add_argument("--output-format", choices=["human", "json", "csv"],
                       default="human", help="Output format")
    parser.add_argument("--output-file", type=str,
                       help="Write output to file instead of stdout")
    
    args = parser.parse_args()
    
    try:
        # Process input
        if args.annual_rent:
            # Single valuation from command line
            params = {
                "annual_rent": args.annual_rent,
                "term_years": args.years,
                "escalator": args.escalator,
                "risk_tier": args.risk_tier
            }
            result = process_single_valuation(params)
            results = [result]
            
        elif args.input:
            # Single valuation from JSON file
            params = load_json_input(args.input)
            result = process_single_valuation(params)
            results = [result]
            
        elif args.batch:
            # Multiple valuations from CSV
            results = process_batch_csv(args.batch)
        
        # Format output
        if args.output_format == "json":
            output = json.dumps(results, indent=2)
        elif args.output_format == "csv":
            output = format_csv_output(results)
        else:  # human readable
            if len(results) == 1:
                output = format_human_readable(results[0])
            else:
                output = "\n" + "="*50 + "\n".join([
                    format_human_readable(r) for r in results
                ])
        
        # Write output
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(output)
            print(f"Results written to {args.output_file}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()