"""Pin the padded-N coefficient convention used by the stratified-tank caller."""

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from enex_analysis.tdma import TDMA


@settings(max_examples=40, derandomize=True, deadline=None)
@given(
    n=st.integers(min_value=2, max_value=8),
    seed=st.integers(min_value=0, max_value=2**32 - 1),
)
def test_padded_diagonals_match_independent_linear_solve(n, seed):
    """Random diagonally dominant systems retain every interior coefficient."""
    rng = np.random.default_rng(seed)
    lower = rng.uniform(-2.0, 2.0, size=n - 1)
    upper = rng.uniform(-2.0, 2.0, size=n - 1)
    main = np.full(n, 6.0)
    rhs = rng.uniform(-10.0, 10.0, size=n)
    matrix = np.diag(main) + np.diag(lower, -1) + np.diag(upper, 1)
    expected = np.linalg.solve(matrix, rhs)
    # The sole production caller passes N entries, with unused boundary slots.
    actual = TDMA(np.r_[123.0, lower], main, np.r_[upper, -456.0], rhs)
    np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(matrix @ actual, rhs, rtol=1e-12, atol=1e-12)
