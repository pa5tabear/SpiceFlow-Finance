#!/usr/bin/env python3
"""
SpiceFlow Finance NPV Calculator Generator
Creates Excel file with NPV calculations for solar lease buyouts
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_spiceflow_calculator():
    """Create the Excel NPV calculator"""
    
    # Create empty dataframe for structure
    df = pd.DataFrame()
    
    # Calculator data structure
    calculator_data = {
        'A': [
            'SPICEFLOW FINANCE - SOLAR LEASE NPV CALCULATOR',
            '',
            'INPUT PARAMETERS',
            'Annual Base Rent ($)',
            'Years Remaining', 
            'Annual Escalator (%)',
            'Risk Tier',
            '',
            'RISK TIER LOOKUP',
            'Low Risk (Operating + Strong Dev)',
            'Medium Risk (Construction + Mid-tier)', 
            'High Risk (Development + Weak Dev)',
            '',
            'CASH FLOW PROJECTION',
            'Year',
            *[str(i) for i in range(1, 26)],  # Years 1-25
            '',
            'VALUATION RESULTS',
            'Total Gross Cash Flows',
            'Net Present Value',
            'Buyout Offer (80% of NPV)',
            'Effective Multiple (x Annual Rent)',
            '',
            'VALIDATION BENCHMARKS',
            'Renewa Benchmark (12.5x Annual)',
            'Our Multiple vs Renewa',
            'Deal Quality Rating'
        ],
        'B': [
            '',  # Title
            '',
            '',  # Header
            95680,  # Default: Illinois Lanceleaf
            23,     # Default years
            0.025,  # Default 2.5% escalator
            'Medium', # Default risk tier
            '',
            'Discount Rate',
            '8%',   # Low risk
            '12%',  # Medium risk  
            '16%',  # High risk
            '',
            '',
            'Annual Rent',
            *['=B4*(1+B6)^(A16-1)' for i in range(25)],  # Escalating rent formulas
            '',
            '',
            '=SUM(B16:B40)',  # Total cash flows
            '=NPV(VLOOKUP(B7,B10:C12,2,FALSE),B16:B40)',  # NPV with dynamic discount rate
            '=B44*0.8',  # 80% buyout offer
            '=B45/B4',   # Multiple calculation
            '',
            '',
            '=B4*12.5',  # Renewa benchmark
            '=B46/B49',  # Comparison ratio
            '=IF(B50>=0.8,"Competitive",IF(B50>=0.6,"Fair","Below Market"))'
        ],
        'C': [
            '',  # Title
            '',
            '',  # Header  
            '← Enter lease annual rent',
            '← Enter remaining lease term',
            '← Enter annual escalation %',
            '← Enter: Low, Medium, or High',
            '',
            'Description',
            'Operating project, strong developer',
            'Under construction, mid-tier dev',
            'Development stage, unknown dev', 
            '',
            '',
            'Present Value',
            *[f'=B{16+i}/(1+VLOOKUP(B7,B10:C12,2,FALSE))^A{16+i}' for i in range(25)],  # PV formulas
            '',
            '',
            '',
            '← Net present value of all payments',
            '← Our cash offer to landowner',
            '← Multiple of current annual rent',
            '',
            '',
            '← Industry standard benchmark',
            '← How competitive our offer is',
            '← Deal assessment vs market'
        ]
    }
    
    # Create DataFrame
    max_rows = max(len(calculator_data['A']), len(calculator_data['B']), len(calculator_data['C']))
    
    # Pad shorter columns with empty strings
    for col in ['A', 'B', 'C']:
        while len(calculator_data[col]) < max_rows:
            calculator_data[col].append('')
    
    df = pd.DataFrame(calculator_data)
    
    return df

def create_test_scenarios():
    """Create test scenarios sheet"""
    
    test_data = {
        'Scenario': [
            'Illinois Lanceleaf Solar',
            'Wyoming City of Laramie', 
            'Kentucky Sullivan Family (Est.)',
            '',
            'Expected Results:'
        ],
        'Annual_Rent': [95680, 230000, 50000, '', ''],
        'Years': [23, 23, 25, '', ''],
        'Escalator': ['2.5%', '1.5%', '2.0%', '', ''],
        'Risk_Tier': ['Medium', 'Low', 'Medium', '', ''],
        'Expected_NPV': ['~$866K', '~$2.4M', '~$570K', '', ''],
        'Expected_Offer': ['~$693K', '~$1.9M', '~$456K', '', ''],
        'Notes': [
            'Real executed lease, Kendall County IL',
            'Municipal counterparty, large scale',
            'Family landowner, estimated terms',
            '',
            'Validate outputs against these ranges'
        ]
    }
    
    return pd.DataFrame(test_data)

if __name__ == "__main__":
    # Create calculator
    calculator = create_spiceflow_calculator()
    scenarios = create_test_scenarios()
    
    # Save to Markdown for easier version control
    calculator.to_markdown('tools/excel/spiceflow-calculator-v1.md', index=False)

    scenarios.to_markdown('tools/excel/test-scenarios.md', index=False)
    
    print("✅ SpiceFlow Calculator created successfully!")
    print("📁 Files saved to /tools/excel/")
    print("📊 Open spiceflow-calculator-v1.md to view the table")
    print("🧪 Test with scenarios from test-scenarios.md")