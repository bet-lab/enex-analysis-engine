# Deterministic contracts

The `Scientific contracts` workflow adds a scientific verification baseline;
it does not measure or claim a speed improvement over the documentation build.

Run the same installed-package environment and checks locally:

```sh
git submodule update --init --recursive
uv sync --locked --extra dev --no-editable
uv run --no-sync ruff check tests
uv run --no-sync ruff format --check tests
uv run --no-sync mypy --follow-imports=skip tests
uv run --no-sync pytest -q --durations=10 --junitxml=contracts.xml
```

The suite covers fixed-capacity electric-boiler steady snapshots, both output
forms, padded-N TDMA systems against `numpy.linalg.solve`, isolated installed
TMHP imports, and simulation-worker response labels and numerical-error rows.
The numerical properties use deterministic Hypothesis examples. No managed
dependency is replaced by a fake. Pytest returns failure when it collects no
tests; missing embedded TMHP is an import failure, not a skip.

## Known limits found while adding coverage

- `TDMA` documents N-1 off-diagonals, but its only production caller creates
  padded N-element arrays. The tests use that caller's convention: `a[0]` and
  `c[-1]` are unused. This change does not correct the documented convention or
  claim support for compact N-1 inputs.
- `simulate_ashp_step` assigns `Q_iu`, while the real heat-pump classes consume
  `Q_r_int`. Thus a requested load of 0, 100, 5000, or -5000 W leaves the model
  at its default 6000 W load. Even an `Off` response can retain compressor
  power. The returned `E_tot`, `X_in_tot`, and `X_out_tot` also fall back to zero
  because the classes expose differently named totals. The worker tests pin
  response classification and its error envelope only; they do not validate
  requested physical load, Off energy, or those totals. Fixing the adapter's
  physical behavior requires a separate reviewed change.

The documentation workflow, scientific equations, input data, and tolerances
are unchanged. These checks run on pull requests and main pushes, but making
their check name required in branch protection is an owner decision.
