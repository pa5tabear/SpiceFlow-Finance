"""Light-weight valuation helpers for solar ground-lease buyouts.

Usage
-----
>>> from lease_valuation import pv_buyout
>>> pv_buyout(
...     annual_rent=95680,
...     term_years=23,
...     escalator=0.025,
...     discount_rate=0.12,
...     buyout_pct=0.80,
... )
800123.42

The module is intentionally <100 lines so it can be audited quickly.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np

__all__ = [
    "LeaseParams",
    "generate_cash_flows",
    "present_value",
    "pv_buyout",
]


@dataclass
class LeaseParams:
    """Basic parameters that define a ground-lease cash-flow stream."""

    annual_rent: float  # current rent in dollars
    term_years: int  # whole years remaining
    escalator: float = 0.0  # e.g. 0.025 for 2.5 % p.a.
    custom_escalators: Sequence[float] | None = None  # per-year overrides
    balloon_cost: float = 0.0  # one-off cost in final year (e.g., decommissioning)

    def cash_flows(self) -> np.ndarray:
        """Return an array of yearly cash flows (positive = inflow)."""
        years = np.arange(self.term_years)
        if self.custom_escalators is not None:
            if len(self.custom_escalators) != self.term_years:
                raise ValueError("Length of custom escalators must equal term_years")
            escalators = np.array(self.custom_escalators)
            rents = self.annual_rent * np.cumprod(1 + escalators)
        else:
            rents = self.annual_rent * (1 + self.escalator) ** years
        rents[-1] += -self.balloon_cost  # subtract cost in final year if any
        return rents


def generate_cash_flows(params: LeaseParams) -> np.ndarray:
    """Wrapper to produce cash-flows given LeaseParams instance."""

    return params.cash_flows()


def present_value(cash_flows: np.ndarray, discount_rate: float) -> float:
    """Compute NPV of a series of annual cash flows.

    Parameters
    ----------
    cash_flows
        1-D array where index 0 is first year’s cash flow.
    discount_rate
        Decimal discount rate (e.g. 0.12 for 12 %).
    """
    years = np.arange(1, len(cash_flows) + 1)
    discount_factors = 1 / (1 + discount_rate) ** years
    return float((cash_flows * discount_factors).sum())


def pv_buyout(
    *,
    annual_rent: float,
    term_years: int,
    escalator: float = 0.0,
    discount_rate: float = 0.12,
    buyout_pct: float = 0.80,
    custom_escalators: Sequence[float] | None = None,
    balloon_cost: float = 0.0,
) -> float:
    """Convenience wrapper to output a cash offer based on PV * percentage."""

    params = LeaseParams(
        annual_rent=annual_rent,
        term_years=term_years,
        escalator=escalator,
        custom_escalators=custom_escalators,
        balloon_cost=balloon_cost,
    )
    cf = generate_cash_flows(params)
    pv = present_value(cf, discount_rate)
    return round(pv * buyout_pct, 2) 