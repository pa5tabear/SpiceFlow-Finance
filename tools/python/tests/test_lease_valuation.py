"""Unit tests for lease_valuation.py module."""

import pytest
import numpy as np
from pathlib import Path

from lease_valuation import LeaseParams, generate_cash_flows, present_value, pv_buyout


class TestLeaseParams:
    """Test LeaseParams dataclass functionality."""
    
    def test_basic_cash_flows(self):
        """Test cash flow generation with fixed escalator."""
        params = LeaseParams(annual_rent=100000, term_years=3, escalator=0.10)
        flows = params.cash_flows()
        
        expected = np.array([100000, 110000, 121000])
        np.testing.assert_array_almost_equal(flows, expected)
    
    def test_zero_escalator(self):
        """Test cash flows with no escalation."""
        params = LeaseParams(annual_rent=50000, term_years=5, escalator=0.0)
        flows = params.cash_flows()
        
        expected = np.array([50000, 50000, 50000, 50000, 50000])
        np.testing.assert_array_almost_equal(flows, expected)
    
    def test_custom_escalators(self):
        """Test cash flows with custom per-year escalators."""
        params = LeaseParams(
            annual_rent=100000, 
            term_years=3,
            custom_escalators=[0.05, 0.10, 0.15]
        )
        flows = params.cash_flows()
        
        # Year 1: 100k * 1.05 = 105k
        # Year 2: 105k * 1.10 = 115.5k  
        # Year 3: 115.5k * 1.15 = 132.825k
        expected = np.array([105000, 115500, 132825])
        np.testing.assert_array_almost_equal(flows, expected)
    
    def test_balloon_cost(self):
        """Test cash flows with decommissioning cost in final year."""
        params = LeaseParams(
            annual_rent=100000,
            term_years=3,
            escalator=0.0,
            balloon_cost=50000
        )
        flows = params.cash_flows()
        
        expected = np.array([100000, 100000, 50000])  # Final year reduced by balloon cost
        np.testing.assert_array_almost_equal(flows, expected)
    
    def test_custom_escalators_wrong_length(self):
        """Test error handling for mismatched escalator length."""
        with pytest.raises(ValueError, match="Length of custom escalators must equal term_years"):
            params = LeaseParams(
                annual_rent=100000,
                term_years=3,
                custom_escalators=[0.05, 0.10]  # Only 2 values for 3 years
            )
            params.cash_flows()


class TestPresentValue:
    """Test NPV calculation functionality."""
    
    def test_simple_present_value(self):
        """Test NPV calculation with simple cash flows."""
        cash_flows = np.array([100, 100, 100])
        discount_rate = 0.10
        
        # Manual calculation: 100/1.1 + 100/1.1^2 + 100/1.1^3
        expected = 100/1.1 + 100/1.21 + 100/1.331
        result = present_value(cash_flows, discount_rate)
        
        assert abs(result - expected) < 0.01
    
    def test_zero_discount_rate(self):
        """Test NPV with zero discount rate (sum of cash flows)."""
        cash_flows = np.array([100, 200, 300])
        result = present_value(cash_flows, 0.0)
        
        assert result == 600  # Simple sum when no discounting
    
    def test_single_cash_flow(self):
        """Test NPV with single cash flow."""
        cash_flows = np.array([1000])
        result = present_value(cash_flows, 0.12)
        
        expected = 1000 / 1.12
        assert abs(result - expected) < 0.01


class TestPvBuyout:
    """Test complete buyout calculation workflow."""
    
    def test_basic_buyout_calculation(self):
        """Test standard buyout offer calculation."""
        result = pv_buyout(
            annual_rent=100000,
            term_years=10,
            escalator=0.02,
            discount_rate=0.10,
            buyout_pct=0.80
        )
        
        # Should return 80% of the NPV of escalating cash flows
        assert isinstance(result, float)
        assert result > 0
        assert result < 100000 * 10  # Sanity check: less than undiscounted total
    
    def test_buyout_with_balloon_cost(self):
        """Test buyout calculation with decommissioning costs."""
        result_no_balloon = pv_buyout(
            annual_rent=100000,
            term_years=5,
            discount_rate=0.12,
            buyout_pct=1.0
        )
        
        result_with_balloon = pv_buyout(
            annual_rent=100000,
            term_years=5,
            discount_rate=0.12,
            buyout_pct=1.0,
            balloon_cost=200000
        )
        
        # Balloon cost should reduce the buyout offer
        assert result_with_balloon < result_no_balloon
    
    def test_buyout_percentage_scaling(self):
        """Test that buyout percentage correctly scales the offer."""
        base_result = pv_buyout(
            annual_rent=100000,
            term_years=10,
            discount_rate=0.10,
            buyout_pct=1.0
        )
        
        scaled_result = pv_buyout(
            annual_rent=100000,
            term_years=10,
            discount_rate=0.10,
            buyout_pct=0.75
        )
        
        assert abs(scaled_result - base_result * 0.75) < 0.01


class TestRealLeaseExamples:
    """Test calculations against our real lease examples."""
    
    def test_illinois_lanceleaf_lease(self):
        """Test Illinois Lanceleaf Solar lease valuation."""
        # $95,680 annual, 23 years, 2.5% escalator, medium risk (12%)
        result = pv_buyout(
            annual_rent=95680,
            term_years=23,
            escalator=0.025,
            discount_rate=0.12,
            buyout_pct=0.80
        )
        
        # Should be reasonable offer for this lease size
        assert 600000 < result < 900000
        multiple = result / 95680
        assert 6.0 < multiple < 10.0  # Reasonable multiple range
    
    def test_wyoming_sailor_lease(self):
        """Test Wyoming Sailor Solar lease valuation."""
        # $230,000 annual, 25 years, 1.5% escalator, low risk (8%)
        result = pv_buyout(
            annual_rent=230000,
            term_years=25,
            escalator=0.015,
            discount_rate=0.08,
            buyout_pct=0.80
        )
        
        # Should be substantial offer for large municipal lease
        assert 2000000 < result < 3000000
        multiple = result / 230000
        assert 8.0 < multiple < 13.0  # Should be competitive with Renewa
    
    def test_kentucky_sullivan_lease(self):
        """Test Kentucky Sullivan lease valuation."""
        # $50,000 annual, 25 years, 2% escalator, medium risk (12%)
        result = pv_buyout(
            annual_rent=50000,
            term_years=25,
            escalator=0.02,
            discount_rate=0.12,
            buyout_pct=0.80
        )
        
        # Should be reasonable for smaller rural lease
        assert 300000 < result < 500000
        multiple = result / 50000
        assert 6.0 < multiple < 10.0


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_zero_annual_rent(self):
        """Test handling of zero annual rent."""
        result = pv_buyout(
            annual_rent=0,
            term_years=10,
            buyout_pct=0.80
        )
        assert result == 0
    
    def test_zero_term_years(self):
        """Test handling of zero term."""
        result = pv_buyout(
            annual_rent=100000,
            term_years=0,
            buyout_pct=0.80
        )
        assert result == 0
    
    def test_very_high_discount_rate(self):
        """Test with extremely high discount rate."""
        result = pv_buyout(
            annual_rent=100000,
            term_years=25,
            discount_rate=0.50,  # 50% discount rate
            buyout_pct=0.80
        )
        
        # Should be very low due to high discounting
        assert result < 200000
    
    def test_negative_escalator(self):
        """Test with declining rent (negative escalator)."""
        result = pv_buyout(
            annual_rent=100000,
            term_years=10,
            escalator=-0.02,  # Rent decreases 2% annually
            discount_rate=0.10,
            buyout_pct=0.80
        )
        
        # Should be positive but lower than flat rent
        assert result > 0
        
        flat_result = pv_buyout(
            annual_rent=100000,
            term_years=10,
            escalator=0.0,
            discount_rate=0.10,
            buyout_pct=0.80
        )
        
        assert result < flat_result


class TestGenerateCashFlows:
    """Test the generate_cash_flows wrapper function."""
    
    def test_generate_cash_flows_wrapper(self):
        """Test that wrapper function works correctly."""
        params = LeaseParams(annual_rent=100000, term_years=3, escalator=0.05)
        
        direct_flows = params.cash_flows()
        wrapper_flows = generate_cash_flows(params)
        
        np.testing.assert_array_equal(direct_flows, wrapper_flows)