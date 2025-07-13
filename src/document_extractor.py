#!/usr/bin/env python3
"""
Document Extraction Module for Solar Lease Processing
====================================================

Extracts key lease terms from PDF and Word documents using pattern matching.
Falls back to JSON if available for testing/validation.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import sys

def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from PDF using pdfplumber or fallback to system tools."""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except ImportError:
        # Fallback to system pdftotext if available
        try:
            result = subprocess.run(
                ['pdftotext', str(file_path), '-'], 
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠️  Cannot extract PDF text from {file_path}. Install pdfplumber: pip install pdfplumber")
            return ""

def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from Word document."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        print(f"⚠️  Cannot extract DOCX text from {file_path}. Install python-docx: pip install python-docx")
        return ""

def extract_lease_data_from_text(text: str, filename: str) -> Dict[str, Any]:
    """Extract lease terms from document text using pattern matching."""
    
    # Default values
    lease_data = {
        "name": filename.replace('.pdf', '').replace('.docx', '').replace('_', ' ').title(),
        "annual_rent": None,
        "term_years": None,
        "escalator": 0.0,
        "risk_tier": "medium",
        "location": None,
        "acres": None,
        "developer": None,
        "landowners": None
    }
    
    # Clean text for pattern matching
    text_clean = re.sub(r'\s+', ' ', text.replace('\n', ' ')).lower()
    
    # Extract annual rent - look for dollar amounts with rent context
    rent_patterns = [
        r'annual\s+rental\s+payment[:\s]+\$([0-9,]+)',
        r'annual\s+rent.*?\$([0-9,]+)',
        r'rent.*?\$([0-9,]+).*?per\s+year',
        r'\$([0-9,]+).*?annual',
        r'payment.*?\$([0-9,]+)',
        r'lease\s+payment.*?\$([0-9,]+)',
        r'rent.*?of\s+\$([0-9,]+)',
        r'sum\s+of\s+\$([0-9,]+)',
        r'amount\s+of\s+\$([0-9,]+)',
        r'compensation.*?\$([0-9,]+)',
        r'shall\s+pay.*?\$([0-9,]+)',
        r'per\s+acre.*?\$([0-9,]+)',
        r'\$([0-9,]+).*?per\s+acre',
        r'([0-9,]+)\s+dollars?.*?annual',
        r'total.*?rent.*?\$([0-9,]+)'
    ]
    
    for pattern in rent_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                lease_data["annual_rent"] = int(match.group(1).replace(',', ''))
                break
            except ValueError:
                continue
    
    # Extract term years
    term_patterns = [
        r'for\s+([0-9]+)\s+years?',                 # "for 25 years"
        r'term.*?([0-9]+)\s+years?',
        r'([0-9]+)\s+year\s+term',
        r'lease\s+term.*?([0-9]+)',
        r'initial\s+term.*?([0-9]+)\s+years?',
        r'period\s+of\s+([0-9]+)\s+years?',
        r'for\s+a\s+term\s+of\s+([0-9]+)',
        r'([0-9]+)\s+years?.*?term',
        r'commencing.*?([0-9]+)\s+years?',
        r'lease.*?([0-9]+)\s+years?.*?period',
        r'expires.*?([0-9]+)\s+years?'
    ]
    
    for pattern in term_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                lease_data["term_years"] = int(match.group(1))
                break
            except ValueError:
                continue
    
    # Extract escalator percentage
    escalator_patterns = [
        r'escalat.*?([0-9]+(?:\.[0-9]+)?)\s*%',
        r'increas.*?([0-9]+(?:\.[0-9]+)?)\s*%.*?(?:annual|per\s+year)',  # allow "per year"
        r'([0-9]+(?:\.[0-9]+)?)\s*%.*?escalat',
        r'([0-9]+(?:\.[0-9]+)?)\s*percent.*?(?:annual|per\s+year).*?increas'
    ]
    
    for pattern in escalator_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                lease_data["escalator"] = float(match.group(1)) / 100.0
                break
            except ValueError:
                continue
    
    # Extract acreage
    acres_patterns = [
        r'([0-9,]+(?:\.[0-9]+)?)\s+acres?',  # allow thousands separator
        r'acres?.*?([0-9,]+(?:\.[0-9]+)?)',
        r'([0-9,]+)\s+acres?\s+more\s+or\s+less'
    ]
    
    for pattern in acres_patterns:
        match = re.search(pattern, text_clean)
        if match:
            try:
                lease_data["acres"] = float(match.group(1).replace(',', ''))
                break
            except ValueError:
                continue

    # Check for rent expressed per acre (capture possibly multiple rates) and choose the highest
    per_acre_rates = re.findall(r'\$([0-9]+(?:\.[0-9]+)?)\s+per\s+(?:utilized\s+)?acre', text_clean)
    if per_acre_rates and lease_data.get("acres") and (lease_data.get("annual_rent") is None or lease_data["annual_rent"] <= 1000):
        try:
            rates_float = [float(r.replace(',', '')) for r in per_acre_rates]
            rate = max(rates_float)
            lease_data["annual_rent"] = int(rate * lease_data["acres"])
        except ValueError:
            pass
    
    # Extract location (state patterns)
    state_patterns = [
        r'state\s+of\s+([a-z]+)',                       # "state of Wyoming"
        r'in\s+the\s+state\s+of\s+([a-z]+)',          # "in the state of Wyoming"
        r'([a-z]+)\s+state',                             # "Wyoming state"
        r'county[,\s]+([a-z]+)',                        # trailing after county
        r'within\s+([a-z]+)\s+county',
        r'located\s+in\s+([a-z]+)',
        r'situated\s+in\s+([a-z]+)',
        r'([a-z]+)\s+county'                            # capture county last
    ]
    
    # Combined pattern: "X County, Y" capturing both
    combined_match = re.search(r'([a-z]+)\s+county[\s,]+([a-z]+)', text_clean)
    if combined_match:
        county = combined_match.group(1).title()
        state = combined_match.group(2).title()
        if len(county) > 2 and len(state) > 2:
            lease_data["location"] = f"{county} County, {state}"

    # If not already set, iterate other patterns
    if lease_data["location"] is None:
        for pattern in state_patterns:
            match = re.search(pattern, text_clean)
            if match:
                location = match.group(1).title()
                if len(location) > 2:  # Avoid initials
                    lease_data["location"] = location
                    break
    
    # Extract developer/lessee company names
    company_patterns = [
        r'lessee[:\s]+([a-z\s,\.]+llc)',
        r'lessee[:\s]+([a-z\s,\.]+inc)',
        r'developer[:\s]+([a-z\s,\.]+llc)',
        r'([a-z\s]+solar[a-z\s]*llc)',
        r'([a-z\s]+energy[a-z\s]*llc)',
        r'([a-z\s]+renewable[a-z\s]*llc)'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, text_clean)
        if match:
            company = match.group(1).strip().title()
            if len(company) > 5:  # Reasonable company name length
                lease_data["developer"] = company
                break
    
    return lease_data

def process_document(file_path: Path) -> Optional[Dict[str, Any]]:
    """Process a single document file and extract lease data."""
    
    file_ext = file_path.suffix.lower()
    
    # Handle JSON files (for testing/validation)
    if file_ext == '.json':
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading JSON {file_path}: {e}")
            return None
    
    # Extract text based on file type
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        print(f"⚠️  Unsupported file type: {file_path}")
        return None
    
    if not text.strip():
        print(f"⚠️  No text extracted from {file_path}")
        return None
    
    # Extract lease data from text
    lease_data = extract_lease_data_from_text(text, file_path.stem)
    
    # Validate required fields
    if lease_data["annual_rent"] is None or lease_data["term_years"] is None:
        print(f"⚠️  Missing critical data in {file_path} (rent: {lease_data['annual_rent']}, term: {lease_data['term_years']})")
        # Don't return None - provide what we found for manual review
    
    return lease_data

def main():
    """Test the extraction on sample files."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test document extraction')
    parser.add_argument('file', help='Document file to process')
    args = parser.parse_args()
    
    file_path = Path(args.file)
    result = process_document(file_path)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to extract data")

if __name__ == '__main__':
    main()