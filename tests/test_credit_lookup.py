"""
Unit tests for credit lookup functionality
"""
import pytest
import json
import sys
import os
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from credit_lookup import CreditLookup, quick_lookup, KNOWN_ENTITIES


class TestCreditLookup:
    """Test the CreditLookup class."""
    
    def test_clean_company_name(self):
        """Test company name cleaning functionality."""
        lookup = CreditLookup()
        
        test_cases = [
            ("Lanceleaf Solar LLC", "Lanceleaf Solar"),
            ("NextEra Energy Inc.", "NextEra Energy"),
            ("Carolina Solar Energy III, LLC", "Carolina Solar Energy III,"),
            ("Some Company Corp", "Some Company"),
            ("Test Corporation", "Test"),
        ]
        
        for input_name, expected in test_cases:
            result = lookup._clean_company_name(input_name)
            assert result == expected, f"Failed for {input_name}: got {result}, expected {expected}"
    
    def test_determine_risk_tier(self):
        """Test risk tier determination logic."""
        lookup = CreditLookup()
        
        # Low risk: public company with 10+ years
        data = {"public_company": True, "years_since_incorp": 15}
        assert lookup._determine_risk_tier(data) == "low"
        
        # Medium risk: 5-10 years
        data = {"public_company": False, "years_since_incorp": 7}
        assert lookup._determine_risk_tier(data) == "medium"
        
        # High risk: new company
        data = {"public_company": False, "years_since_incorp": 3}
        assert lookup._determine_risk_tier(data) == "high"
        
        # High risk: no data
        data = {}
        assert lookup._determine_risk_tier(data) == "high"
    
    def test_get_discount_rate(self):
        """Test discount rate mapping."""
        lookup = CreditLookup()
        
        assert lookup._get_discount_rate("low") == 0.10
        assert lookup._get_discount_rate("medium") == 0.10
        assert lookup._get_discount_rate("high") == 0.10
        assert lookup._get_discount_rate("unknown") == 0.10  # Default
    
    @patch('credit_lookup.requests.get')
    def test_sec_lookup_success(self, mock_get):
        """Test successful SEC lookup."""
        # Mock response with public company indicators
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "10-k filing for test company proxy statement"
        mock_get.return_value = mock_response
        
        lookup = CreditLookup()
        result = lookup._sec_lookup("Test Company")
        
        assert result is not None
        assert result["public_company"] is True
        assert result["years_since_incorp"] == 10
        assert result["state_of_incorp"] == "DE"
    
    @patch('credit_lookup.requests.get')
    def test_sec_lookup_failure(self, mock_get):
        """Test SEC lookup failure handling."""
        # Mock failed request
        mock_get.side_effect = Exception("Network error")
        
        lookup = CreditLookup()
        result = lookup._sec_lookup("Test Company")
        
        assert result is None
    
    @patch('credit_lookup.requests.get')
    def test_sec_lookup_no_public_indicators(self, mock_get):
        """Test SEC lookup with no public company indicators."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "basic company information"
        mock_get.return_value = mock_response
        
        lookup = CreditLookup()
        result = lookup._sec_lookup("Test Company")
        
        assert result is None


class TestQuickLookup:
    """Test the quick lookup functionality."""
    
    def test_known_entities_lookup(self):
        """Test lookup against known entities database."""
        # Test Lanceleaf lookup
        result = quick_lookup("Lanceleaf Solar LLC")
        assert result["risk_tier"] == "medium"
        assert result["recommended_discount"] == 0.10
        assert result["public_company"] is False
        assert "Known Entities DB" in result["data_sources"]
        
        # Test NextEra lookup
        result = quick_lookup("NextEra Energy Partners")
        assert result["risk_tier"] == "low"
        assert result["recommended_discount"] == 0.10
        assert result["public_company"] is True
    
    def test_unknown_company_fallback(self):
        """Test fallback for unknown companies."""
        with patch.object(CreditLookup, 'lookup_company') as mock_lookup:
            mock_lookup.return_value = {
                "company_name": "Unknown Corp",
                "risk_tier": "high",
                "recommended_discount": 0.10
            }
            
            result = quick_lookup("Unknown Corp")
            assert result["risk_tier"] == "high"
            assert result["recommended_discount"] == 0.10
    
    def test_empty_company_name(self):
        """Test handling of empty company name."""
        result = quick_lookup("")
        assert result == {}
        
        result = quick_lookup(None)
        assert result == {}


class TestKnownEntities:
    """Test the known entities database."""
    
    def test_known_entities_structure(self):
        """Test that known entities have required fields."""
        required_fields = ["public_company", "years_since_incorp", "state_of_incorp", "risk_tier"]
        
        for entity_name, data in KNOWN_ENTITIES.items():
            for field in required_fields:
                assert field in data, f"Entity {entity_name} missing field {field}"
            
            # Validate field types
            assert isinstance(data["public_company"], bool)
            assert isinstance(data["years_since_incorp"], int)
            assert isinstance(data["state_of_incorp"], str)
            assert data["risk_tier"] in ["low", "medium", "high"]


class TestIntegration:
    """Test end-to-end credit lookup integration."""
    
    def test_full_lookup_pipeline(self):
        """Test complete lookup pipeline for known entity."""
        result = quick_lookup("Lanceleaf Solar Development LLC")
        
        # Should find Lanceleaf in known entities
        assert "lanceleaf" in result["clean_name"]
        assert result["risk_tier"] == "medium"
        assert result["recommended_discount"] == 0.10
        assert "lookup_timestamp" in result
        assert "company_name" in result
    
    @patch('credit_lookup.CreditLookup.lookup_company')
    def test_sec_api_integration(self, mock_lookup):
        """Test integration with SEC API (mocked)."""
        mock_lookup.return_value = {
            "company_name": "Public Solar Corp",
            "clean_name": "public solar corp",
            "public_company": True,
            "years_since_incorp": 15,
            "state_of_incorp": "DE",
            "risk_tier": "low",
            "recommended_discount": 0.10,
            "data_sources": ["SEC EDGAR"],
            "lookup_timestamp": "2025-07-12T12:00:00"
        }
        
        result = quick_lookup("Public Solar Corp")
        assert result["risk_tier"] == "low"
        assert result["recommended_discount"] == 0.10
        assert "SEC EDGAR" in result["data_sources"]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])