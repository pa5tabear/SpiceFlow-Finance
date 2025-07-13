"""
Manual lease data overrides based on verified analysis
=====================================================

Ground truth data from manual review in lease-analysis.md
Use this to override automated extraction when patterns fail.
"""

# Verified lease data from manual analysis
MANUAL_LEASE_DATA = {
    "Lanceleaf Solar_Land Lease Agreement.pdf": {
        "name": "Lanceleaf Solar Land Lease Agreement",
        "annual_rent": 95680,
        "term_years": 25,  # Base term
        "renewal_options": "4 × 5-yr",
        "total_potential_term": 45,  # 25 + (4 × 5)
        "escalator": 0.025,
        "risk_tier": "medium",
        "location": "Kendall County, Illinois", 
        "acres": 36.8,
        "developer": "Lanceleaf Solar",
        "notes": "Executed; semi-annual payments (Jan 15 / Jul 15)"
    },
    
    "8568.pdf": {
        "name": "Wyoming Laramie Municipal Lease",
        "annual_rent": 230000,
        "term_years": 25,  # Base term
        "renewal_options": "Undisclosed",
        "total_potential_term": 25,  # Unknown renewals
        "escalator": 0.015,
        "risk_tier": "low",  # Municipal lease = lower risk
        "location": "Laramie, Wyoming", 
        "acres": 1150,
        "developer": "Boulevard Associates LLC (NextEra)",
        "notes": "City of Laramie municipal lease; option rent $2.50/acre"
    },
    
    "SOL-KY-03_GROUND_LEASE_SULLIVAN,_RON__GWYNETTE_Redacted.pdf": {
        "name": "Kentucky Carolina Solar Lease",
        "annual_rent": None,  # Redacted
        "term_years": 30,  # Base term: 30.75 rounded
        "renewal_options": "2 × 5-yr",
        "total_potential_term": 40,  # 30 + (2 × 5)
        "escalator": 0.02,  # Average of 1.5% and 2%
        "risk_tier": "medium",
        "location": "Kentucky",
        "acres": 85,
        "developer": "Carolina Solar Energy III, LLC",
        "notes": "Redacted rent; early termination after 15.75 yrs"
    },
    
    "4cd102d0dec45e7e68bf75b37e62955666d69473.pdf": {
        "name": "Project Company Lease Consent",
        "annual_rent": 25607,
        "term_years": None,  # Not specified
        "renewal_options": "Unknown",
        "total_potential_term": None,  # Cannot calculate without base term
        "escalator": 0.01,
        "risk_tier": "high",  # Unknown entity
        "location": "Unknown",
        "acres": None,
        "developer": "Unknown Project Company",
        "notes": "Lease consent mentions rent $25,606.55/yr escalating 1% annually"
    }
}

# Documents that should be skipped (not actual leases)
SKIP_DOCUMENTS = {
    "RR22-0640 Request for Ordinance_Solar IX Land Lease.pdf": "Ordinance request; lease terms not yet executed",
    "lease-option-fawn-meadow---redacted.pdf": "Development-stage option (needs vetting)",
    "25I0955-Ground Lease - final version.pdf": "Per MW capacity basis - needs manual calculation",
    "Enxco-Wind-Farm-Lease.pdf": "Per acre/MW basis - needs manual calculation"
}

def get_manual_override(filename: str) -> dict:
    """Get manual lease data if available."""
    return MANUAL_LEASE_DATA.get(filename, None)

def should_skip_document(filename: str) -> bool:
    """Check if document should be skipped."""
    return filename in SKIP_DOCUMENTS

def get_skip_reason(filename: str) -> str:
    """Get reason for skipping document."""
    return SKIP_DOCUMENTS.get(filename, "Unknown reason")