"""
Unit tests for lease valuation engine
"""
import pytest
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lease_valuation import LeaseParams, generate_cash_flows, present_value, pv_buyout


class TestLeaseParams:
    """Test the LeaseParams dataclass and cash flow generation."""
    
    def test_basic_cash_flows(self):
        """Test basic cash flow generation without escalator."""
        params = LeaseParams(annual_rent=100000, term_years=3, escalator=0.0)
        cash_flows = params.cash_flows()
        expected = np.array([100000, 100000, 100000])
        np.testing.assert_array_equal(cash_flows, expected)
    
    def test_escalated_cash_flows(self):
        """Test cash flow generation with 5% annual escalator."""
        params = LeaseParams(annual_rent=100000, term_years=3, escalator=0.05)
        cash_flows = params.cash_flows()
        expected = np.array([100000, 105000, 110250])
        np.testing.assert_array_almost_equal(cash_flows, expected)
    
    def test_custom_escalators(self):
        """Test custom escalator schedule."""
        params = LeaseParams(
            annual_rent=100000, 
            term_years=3, 
            custom_escalators=[0.02, 0.03, 0.05]
        )
        cash_flows = params.cash_flows()
        # Year 1: 100k * 1.02 = 102k
        # Year 2: 100k * 1.02 * 1.03 = 105.06k  
        # Year 3: 100k * 1.02 * 1.03 * 1.05 = 110.313k
        expected = np.array([102000, 105060, 110313])
        np.testing.assert_array_almost_equal(cash_flows, expected)
    
    def test_balloon_cost(self):
        """Test balloon cost in final year."""
        params = LeaseParams(annual_rent=100000, term_years=2, balloon_cost=50000)
        cash_flows = params.cash_flows()
        expected = np.array([100000, 50000])  # 100k - 50k balloon
        np.testing.assert_array_equal(cash_flows, expected)
    
    def test_custom_escalators_wrong_length(self):
        """Test error handling for mismatched custom escalator length."""
        with pytest.raises(ValueError, match="Length of custom escalators must equal term_years"):
            params = LeaseParams(annual_rent=100000, term_years=3, custom_escalators=[0.02, 0.03])
            params.cash_flows()


class TestPresentValue:
    """Test present value calculations."""
    
    def test_zero_discount_rate(self):
        """Test PV calculation with zero discount rate."""
        cash_flows = np.array([100, 100, 100])
        pv = present_value(cash_flows, 0.0)
        assert pv == 300.0
    
    def test_ten_percent_discount(self):
        """Test PV calculation with 10% discount rate."""
        cash_flows = np.array([100, 100, 100])
        pv = present_value(cash_flows, 0.10)
        # Expected: 100/1.1 + 100/1.21 + 100/1.331 = 248.69
        expected = 100/1.1 + 100/1.21 + 100/1.331
        assert abs(pv - expected) < 0.01
    
    def test_single_payment(self):
        """Test PV with single payment."""
        cash_flows = np.array([1000])
        pv = present_value(cash_flows, 0.10)
        expected = 1000 / 1.10
        assert abs(pv - expected) < 0.01


class TestRealLeaseFixtures:
    """Test with real lease data fixtures."""
    
    def test_illinois_lanceleaf_lease(self):
        """Test Illinois Lanceleaf Solar lease valuation."""
        buyout = pv_buyout(
            annual_rent=95680,
            term_years=23,
            escalator=0.025,
            discount_rate=0.10,
            buyout_pct=0.85
        )
        # Should be reasonable multiple of annual rent
        multiple = buyout / 95680
        assert 6.0 < multiple < 10.0  # Reasonable range
        assert buyout > 500000  # Substantial offer
    
    def test_wyoming_lease(self):
        """Test Wyoming lease valuation."""
        buyout = pv_buyout(
            annual_rent=230000,
            term_years=25,
            escalator=0.015,
            discount_rate=0.10,
            buyout_pct=0.85
        )
        multiple = buyout / 230000
        assert 6.0 < multiple < 10.0
        assert buyout > 1000000
    
    def test_kentucky_lease(self):
        """Test Kentucky lease valuation."""
        buyout = pv_buyout(
            annual_rent=50000,
            term_years=25,
            escalator=0.02,
            discount_rate=0.10,
            buyout_pct=0.85
        )
        multiple = buyout / 50000
        assert 6.0 < multiple < 10.0
        assert buyout > 200000


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_zero_rent(self):
        """Test handling of zero annual rent."""
        buyout = pv_buyout(annual_rent=0, term_years=25, discount_rate=0.10)
        assert buyout == 0.0
    
    def test_one_year_term(self):
        """Test one-year lease term."""
        buyout = pv_buyout(annual_rent=100000, term_years=1, discount_rate=0.10, buyout_pct=0.8)
        expected = (100000 / 1.10) * 0.8
        assert abs(buyout - expected) < 1.0
    
    def test_high_escalator(self):
        """Test high escalator rate."""
        buyout = pv_buyout(annual_rent=100000, term_years=5, escalator=0.20, discount_rate=0.10)
        assert buyout > 100000  # Should be higher than single year rent
    
    def test_negative_balloon_cost(self):
        """Test negative balloon cost (actually a bonus)."""
        buyout = pv_buyout(
            annual_rent=100000, 
            term_years=2, 
            balloon_cost=-25000,  # Bonus payment
            discount_rate=0.10
        )
        normal_buyout = pv_buyout(annual_rent=100000, term_years=2, discount_rate=0.10)
        assert buyout > normal_buyout  # Should be higher with bonus


class TestIntegrationFlow:
    """Test complete workflow integration."""
    
    def test_params_to_buyout_flow(self):
        """Test complete flow from LeaseParams to buyout offer."""
        params = LeaseParams(annual_rent=200000, term_years=20, escalator=0.025)
        cash_flows = generate_cash_flows(params)
        pv = present_value(cash_flows, 0.10)
        buyout = pv * 0.85
        
        # Compare with direct function
        direct_buyout = pv_buyout(
            annual_rent=200000, 
            term_years=20, 
            escalator=0.025, 
            discount_rate=0.10,
            buyout_pct=0.85
        )
        
        assert abs(buyout - direct_buyout) < 1.0  # Should match within rounding


if __name__ == '__main__':
    pytest.main([__file__, '-v'])