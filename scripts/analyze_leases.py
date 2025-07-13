#!/usr/bin/env python3
"""
SpiceFlow Lease Analyzer - One-Command Workflow
===============================================

Simple usage: python analyze_leases.py

This script:
1. Processes all lease documents (PDF, DOCX, JSON) in data/leases/
2. Generates lease_summary.md 
3. Generates executive_report.md
4. Opens both files for review

For custom discount rate: python analyze_leases.py --rate 0.10
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Default discount rate (fixed at 10% unless overridden)
    discount_rate = 0.10
    
    # Parse simple command line argument
    if len(sys.argv) > 1:
        if sys.argv[1] == '--rate' and len(sys.argv) > 2:
            try:
                discount_rate = float(sys.argv[2])
                print(f"Using custom discount rate: {discount_rate*100:.1f}%")
            except ValueError:
                print("Invalid discount rate. Using default 10%.")
        elif sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            return
    
    print("🚀 SpiceFlow Lease Analyzer")
    print("=" * 40)
    
    # Run the main processing script
    cmd = [
        sys.executable, 
        'src/process_leases.py',
        '--discount-rate', str(discount_rate),
        '--output-dir', 'output'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Check if files were created and offer to open them
        summary_file = Path('output/lease_summary.md')
        report_file = Path('output/executive_report.md')
        
        if summary_file.exists() and report_file.exists():
            print("\n📁 Files created successfully!")
            print("💡 Next steps:")
            print("   - View summary: open output/lease_summary.md")  
            print("   - Read report: open output/executive_report.md")
            print("   - Edit discount rate: python scripts/analyze_leases.py --rate 0.10")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running analysis: {e}")
        print("Error output:", e.stderr)
    except FileNotFoundError:
        print("❌ Could not find src/process_leases.py - run from repo root directory")

if __name__ == '__main__':
    main()