"""
Unit tests for document extraction functionality
"""
import pytest
import json
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_extractor import extract_lease_data_from_text, process_document


class TestTextExtraction:
    """Test lease data extraction from text."""
    
    def test_annual_rent_extraction(self):
        """Test various annual rent pattern matching."""
        test_cases = [
            ("The annual rent shall be $95,680 per year", 95680),
            ("Lessee agrees to pay $230,000 annually", 230000),
            ("Annual payment of $50,000", 50000),
            ("rent in the amount of $125,500", 125500),
            ("compensation shall be $75,000 per annum", 75000),
        ]
        
        for text, expected_rent in test_cases:
            result = extract_lease_data_from_text(text, "test")
            assert result["annual_rent"] == expected_rent, f"Failed for: {text}"
    
    def test_term_years_extraction(self):
        """Test lease term extraction."""
        test_cases = [
            ("The lease term shall be 25 years", 25),
            ("initial term of 30 years", 30),
            ("for a period of 20 years", 20),
            ("lease expires after 15 years", 15),
        ]
        
        for text, expected_term in test_cases:
            result = extract_lease_data_from_text(text, "test")
            assert result["term_years"] == expected_term, f"Failed for: {text}"
    
    def test_escalator_extraction(self):
        """Test escalator percentage extraction."""
        test_cases = [
            ("rent shall escalate 2.5% annually", 0.025),
            ("increase of 3.0% per year", 0.030),
            ("annual escalation of 1.5%", 0.015),
            ("2 percent annual increase", 0.02),
        ]
        
        for text, expected_escalator in test_cases:
            result = extract_lease_data_from_text(text, "test")
            assert abs(result["escalator"] - expected_escalator) < 0.001, f"Failed for: {text}"
    
    def test_acres_extraction(self):
        """Test acreage extraction."""
        test_cases = [
            ("The property consists of 36.8 acres", 36.8),
            ("located on 150 acres more or less", 150.0),
            ("encompassing 82.33 acres", 82.33),
        ]
        
        for text, expected_acres in test_cases:
            result = extract_lease_data_from_text(text, "test")
            assert result["acres"] == expected_acres, f"Failed for: {text}"
    
    def test_location_extraction(self):
        """Test location/state extraction."""
        test_cases = [
            ("located in Kendall County, Illinois", "Kendall"),
            ("situated in Albany County", "Albany"),
            ("within the state of Wyoming", "Wyoming"),
        ]
        
        for text, expected_location in test_cases:
            result = extract_lease_data_from_text(text, "test")
            assert expected_location.lower() in result["location"].lower(), f"Failed for: {text}"
    
    def test_company_extraction(self):
        """Test developer/company name extraction."""
        test_cases = [
            ("Lessee: Lanceleaf Solar LLC", "Lanceleaf Solar Llc"),
            ("Developer: Carolina Solar Energy III, LLC", "Carolina Solar Energy Iii, Llc"),
            ("NextEra Energy Partners LLC", "Nextera Energy Partners Llc"),
        ]
        
        for text, expected_company in test_cases:
            result = extract_lease_data_from_text(text, "test")
            if result["developer"]:
                assert expected_company.lower() in result["developer"].lower(), f"Failed for: {text}"
    
    def test_missing_data_handling(self):
        """Test handling of missing critical data."""
        # Text with no rent information
        text_no_rent = "This is a lease for 25 years with 2% escalation on 100 acres"
        result = extract_lease_data_from_text(text_no_rent, "test")
        assert result["annual_rent"] is None
        assert result["term_years"] == 25
        
        # Text with no term information  
        text_no_term = "Annual rent of $100,000 with 2% escalation"
        result = extract_lease_data_from_text(text_no_term, "test")
        assert result["annual_rent"] == 100000
        assert result["term_years"] is None
    
    def test_default_values(self):
        """Test default value assignment."""
        text = "Simple lease document"
        result = extract_lease_data_from_text(text, "test_lease")
        
        assert result["name"] == "Test Lease"
        assert result["risk_tier"] == "medium"
        assert result["escalator"] == 0.0
        assert result["annual_rent"] is None
        assert result["term_years"] is None


class TestJSONProcessing:
    """Test JSON file processing."""
    
    def test_json_file_processing(self):
        """Test processing of JSON lease files."""
        # Use existing test fixtures if available
        fixtures_dir = Path("tools/python/tests/fixtures")
        if fixtures_dir.exists():
            json_files = list(fixtures_dir.glob("*.json"))
            
            for json_file in json_files:
                result = process_document(json_file)
                assert result is not None
                assert "annual_rent" in result
                assert "term_years" in result
                
                # Validate required fields exist
                if result["annual_rent"] and result["term_years"]:
                    assert result["annual_rent"] > 0
                    assert result["term_years"] > 0


class TestFileTypeHandling:
    """Test different file type handling."""
    
    def test_unsupported_file_type(self):
        """Test handling of unsupported file types."""
        fake_path = Path("test.txt")
        result = process_document(fake_path)
        assert result is None
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent files."""
        fake_path = Path("nonexistent.json")
        result = process_document(fake_path)
        assert result is None


class TestIntegrationPatterns:
    """Test realistic extraction patterns."""
    
    def test_lanceleaf_style_lease(self):
        """Test pattern similar to Lanceleaf Solar lease."""
        text = """
        SOLAR GROUND LEASE AGREEMENT
        
        This lease is for a term of 25 years commencing on the effective date.
        The annual rent shall be $95,680 payable semi-annually.
        Rent shall escalate at 2.5% annually.
        The leased premises consist of approximately 36.8 acres
        located in Kendall County, Illinois.
        Lessee: Lanceleaf Solar LLC
        """
        
        result = extract_lease_data_from_text(text, "lanceleaf_test")
        assert result["annual_rent"] == 95680
        assert result["term_years"] == 25
        assert abs(result["escalator"] - 0.025) < 0.001
        assert result["acres"] == 36.8
        assert "kendall" in result["location"].lower()
    
    def test_wyoming_style_lease(self):
        """Test pattern similar to Wyoming municipal lease."""
        text = """
        GROUND LEASE AGREEMENT
        
        The City hereby leases to Lessee approximately 1,150 acres
        for a term of 25 years.
        Annual rental payment: $230,000
        Rent escalation: 1.5% per annum
        Located in Albany County, Wyoming
        Lessee: Boulevard Associates LLC
        """
        
        result = extract_lease_data_from_text(text, "wyoming_test")
        assert result["annual_rent"] == 230000
        assert result["term_years"] == 25
        assert abs(result["escalator"] - 0.015) < 0.001
        assert result["acres"] == 1150
        assert "wyoming" in result["location"].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])