"""Response classification and numerical-error envelopes, not load correctness.

The current runner writes Q_iu while models consume Q_r_int. These tests do not
claim that requested loads or Off energy are physically implemented correctly.
"""

import pytest

from enex_analysis.simulation_runner import simulate_ashp_step


@pytest.mark.parametrize(
    ("load", "mode"),
    [(0.0, "Off"), (99.0, "Off"), (-99.0, "Off"), (100.0, "Cooling"), (-100.0, "Heating")],
)
def test_response_labels_respect_sign_and_deadband(load, mode):
    """The response labels use a strict 100 W deadband and one-based hours."""
    result = simulate_ashp_step((7, load, 20.0))
    assert result["Hour"] == 8
    assert result["Mode"] == mode
    assert "Error" not in result
    assert result["X_Eff_percent"] == pytest.approx(result["X_eff"] * 100)


def test_numerical_failure_returns_error_row():
    """A real nonphysical ambient temperature yields a bounded error response."""
    result = simulate_ashp_step((2, 100.0, -400.0))
    assert result["Hour"] == 3
    assert result["Mode"] == "Cooling"
    assert result["Error"]
    assert result["E_tot"] == 0
