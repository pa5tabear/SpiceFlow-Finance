#!/usr/bin/env python3
"""
Credit Risk Lookup Module for Solar Lease Counterparties
========================================================

Quick credit assessment using public data sources:
- SEC EDGAR API for public company status
- Basic entity age and incorporation lookup
- Risk tier mapping for discount rate assignment
"""

import requests
import re
import json
import argparse
from typing import Dict, Optional, Any
from datetime import datetime
import time


class CreditLookup:
    """Credit assessment client for lease counterparties."""
    
    def __init__(self):
        # SEC EDGAR API endpoint (free, no key required)
        self.sec_base_url = "https://data.sec.gov"
        self.headers = {
            "User-Agent": "SpiceFlow Finance (hello@spiceflow.com)",
            "Accept": "application/json"
        }
    
    def lookup_company(self, company_name: str) -> Dict[str, Any]:
        """
        Perform credit lookup for a company name.
        
        Returns:
            Dict with credit assessment data:
            - public_company: bool
            - years_since_incorp: int or None
            - state_of_incorp: str or None  
            - risk_tier: str (low/medium/high)
            - recommended_discount: float
        """
        
        # Clean company name for search
        clean_name = self._clean_company_name(company_name)
        
        # Initialize result structure
        result = {
            "company_name": company_name,
            "clean_name": clean_name,
            "public_company": False,
            "years_since_incorp": None,
            "state_of_incorp": None,
            "risk_tier": "high",  # Default to conservative
            "recommended_discount": 0.10,  # Fixed 10%
            "data_sources": [],
            "lookup_timestamp": datetime.now().isoformat()
        }
        
        # Try SEC lookup for public company status
        sec_data = self._sec_lookup(clean_name)
        if sec_data:
            result.update(sec_data)
            result["data_sources"].append("SEC EDGAR")
        
        # Apply risk tier logic
        result["risk_tier"] = self._determine_risk_tier(result)
        # For now, we always apply a flat 10% discount rate
        result["recommended_discount"] = 0.10
        
        return result
    
    def _clean_company_name(self, name: str) -> str:
        """Clean company name for API searches."""
        if not name:
            return ""
        
        # Remove common suffixes and clean
        name = re.sub(r'\s+(LLC|Inc|Corp|Corporation|Company|Co|LP|LLP|Partnership)\.?\s*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+', ' ', name.strip())
        return name
    
    def _sec_lookup(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Lookup company in SEC EDGAR database."""
        try:
            # SEC company search endpoint
            search_url = f"{self.sec_base_url}/api/xbrl/companyfacts/CIK{self._get_cik_for_name(company_name)}.json"
            
            # For now, use company search endpoint
            search_endpoint = f"{self.sec_base_url}/cgi-bin/browse-edgar"
            params = {
                'company': company_name,
                'match': 'contains',
                'output': 'atom'
            }
            
            response = requests.get(search_endpoint, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse response for public company indicators
                content = response.text.lower()
                
                # Simple heuristics for public company detection
                public_indicators = ['10-k', '10-q', '8-k', 'proxy', 'registration']
                is_public = any(indicator in content for indicator in public_indicators)
                
                if is_public:
                    return {
                        "public_company": True,
                        "years_since_incorp": 10,  # Conservative estimate for established public cos
                        "state_of_incorp": "DE"    # Most public companies incorporate in Delaware
                    }
            
        except Exception as e:
            print(f"SEC lookup failed for {company_name}: {e}")
        
        return None
    
    def _get_cik_for_name(self, company_name: str) -> str:
        """Get CIK number for company name (simplified)."""
        # This would require a more sophisticated mapping
        # For MVP, we'll use heuristics
        return "0000000000"  # Placeholder
    
    def _determine_risk_tier(self, data: Dict[str, Any]) -> str:
        """Determine risk tier based on company data."""
        
        # Public company with long history = low risk
        if data.get("public_company") and data.get("years_since_incorp", 0) >= 10:
            return "low"
        
        # Established private company = medium risk  
        if data.get("years_since_incorp", 0) >= 5:
            return "medium"
        
        # Default to high risk for new/unknown entities
        return "high"
    
    def _get_discount_rate(self, risk_tier: str) -> float:
        """Map risk tier to discount rate."""
        # Currently we ignore risk tier variability and always use 10%
        return 0.10


# Simplified lookup for common solar industry players
KNOWN_ENTITIES = {
    "nextera": {
        "public_company": True,
        "years_since_incorp": 30,
        "state_of_incorp": "FL",
        "risk_tier": "low"
    },
    "enxco": {
        "public_company": False,
        "years_since_incorp": 15,
        "state_of_incorp": "CA", 
        "risk_tier": "medium"
    },
    "lanceleaf": {
        "public_company": False,
        "years_since_incorp": 8,
        "state_of_incorp": "IL",
        "risk_tier": "medium"
    },
    "carolina solar": {
        "public_company": False,
        "years_since_incorp": 6,
        "state_of_incorp": "NC",
        "risk_tier": "medium"
    },
    "nexamp": {
        "public_company": False,
        "years_since_incorp": 12,
        "state_of_incorp": "MA",
        "risk_tier": "medium"
    }
}


def quick_lookup(company_name: str) -> Dict[str, Any]:
    """Quick lookup using known entities database."""
    if not company_name:
        return {}
    
    clean_name = company_name.lower().strip()
    
    # Check against known entities
    for known_key, data in KNOWN_ENTITIES.items():
        if known_key in clean_name:
            result = {
                "company_name": company_name,
                "clean_name": clean_name,
                **data,
                "data_sources": ["Known Entities DB"],
                "lookup_timestamp": datetime.now().isoformat()
            }
            
            # Apply discount rate
            lookup_client = CreditLookup()
            result["recommended_discount"] = lookup_client._get_discount_rate(result["risk_tier"])
            
            return result
    
    # Fall back to full lookup
    lookup_client = CreditLookup()
    return lookup_client.lookup_company(company_name)


def main():
    """CLI interface for credit lookup."""
    parser = argparse.ArgumentParser(description='Credit risk lookup for solar lease counterparties')
    parser.add_argument('company_name', help='Company name to lookup')
    parser.add_argument('--output', choices=['json', 'summary'], default='summary', 
                       help='Output format')
    
    args = parser.parse_args()
    
    # Perform lookup
    result = quick_lookup(args.company_name)
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        # Summary format
        print(f"Credit Assessment: {result.get('company_name', 'Unknown')}")
        print(f"Risk Tier: {result.get('risk_tier', 'unknown').title()}")
        print(f"Recommended Discount Rate: {result.get('recommended_discount', 0.10)*100:.1f}%")
        print(f"Public Company: {'Yes' if result.get('public_company') else 'No'}")
        if result.get('years_since_incorp'):
            print(f"Years Since Incorporation: {result.get('years_since_incorp')}")


if __name__ == '__main__':
    main()