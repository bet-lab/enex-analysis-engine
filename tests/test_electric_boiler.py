"""Steady snapshots obey the documented fixed-capacity electrical contract."""

import pandas as pd
from hypothesis import given, settings
from hypothesis import strategies as st

from enex_analysis.electric_boiler import ElectricBoiler


def boiler(capacity: float) -> ElectricBoiler:
    """Build a real boiler with nonzero losses to distinguish steady handling."""
    return ElectricBoiler(
        heater_capacity=capacity,
        V_tank_full=0.2,
        T_sup_w_C=15.0,
        T_tank_w_lower_bound_C=50.0,
        T_tank_w_upper_bound_C=60.0,
        T_tank_w_in_C=15.0,
        T_mix_w_out_C=40.0,
        dV_mix_w_out_max=0.0001,
        UA_tank=7.0,
    )


@settings(max_examples=40, derandomize=True, deadline=None)
@given(
    capacity=st.floats(min_value=1.0, max_value=100_000.0),
    target=st.floats(min_value=-100_000.0, max_value=100_000.0),
)
def test_steady_switches_full_capacity_only_for_positive_target(capacity, target):
    """A demand switches rated power; it does not modulate power to the target."""
    result = boiler(capacity).analyze_steady(55.0, 20.0, target)
    expected_power = capacity if target > 0 else 0.0
    assert result["heater_is_on"] == (target > 0)
    assert result["E_heater [W]"] == expected_power
    assert result["E_tot [W]"] == expected_power
    assert result["Q_tank_loss [W]"] == 0.0
    assert result["tank_level [-]"] == 1.0


def test_steady_zero_target_is_off_and_dataframe_matches_dict():
    """The zero boundary is off, and both public output forms carry one snapshot."""
    model = boiler(3000.0)
    result = model.analyze_steady(55.0, 20.0, 0.0)
    frame = model.analyze_steady(55.0, 20.0, 0.0, return_dict=False)
    assert result["heater_is_on"] is False
    assert result["E_tot [W]"] == 0.0
    assert result["T_tank_w [°C]"] == 55.0
    assert result["T0 [°C]"] == 20.0
    pd.testing.assert_frame_equal(frame, pd.DataFrame([result]))
