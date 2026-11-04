# Energy-Exergy Analysis Engine

**Comprehensive thermodynamic modeling for diverse energy systems through unified energy-exergy analysis**

A Python library that enables simultaneous energy (first-law) and exergy (second-law) analysis of various energy conversion systems. Built for researchers, engineers, and educators who need to understand not just how much energy flows through a system, but also the quality and potential of that energy.

---

## Why Energy-Exergy Analysis?

Traditional energy analysis tells you _how much_ energy is used, but not _how well_ it's used. Exergy analysis reveals the true thermodynamic efficiency by accounting for energy quality and identifying where irreversibilities occur. Together, energy-exergy analysis provides:

- **Complete thermodynamic picture**: Understand both quantity (energy) and quality (exergy) of energy flows
- **Inefficiency identification**: Pinpoint where exergy is consumed through irreversible processes while energy is conserved
- **Technology comparison**: Fair comparison between different energy conversion technologies
- **Optimization guidance**: Identify the most promising areas for system improvement

This library makes energy-exergy analysis accessible by providing ready-to-use models for common energy systems, with automatic calculation of energy, entropy, and exergy balances.

---

## Core Capabilities

### Unified Balance Calculations

Every component model automatically calculates three balances:

1. **Energy Balance** (First Law of Thermodynamics): Identifies energy flows and losses
2. **Entropy Balance** (Second Law of Thermodynamics): Quantifies irreversibilities
3. **Exergy Balance** (Both First and Second Law of Thermodynamics): Reveals thermodynamic inefficiencies

These balances are calculated consistently across all components, enabling system-level analysis and comparison.

### Analysis Features

- **Automatic balance calculation**: Set parameters, run `system_update()`, get all balances
- **Steady-State & Dynamic Simulation**: Advanced models support `analyze_steady()` and `analyze_dynamic()` with schedules
- **Optimal Operation Search**: Built-in optimization algorithms to find optimal operating conditions
- **Subsystem-level analysis**: Detailed balances for each subsystem (e.g., combustion chamber, heat exchanger, mixing valve)
- **Performance metrics**: Exergy efficiency, COP, and other key performance indicators
- **Visualization support**: Built-in functions for displaying balance results
- **Unit conversion utilities**: Comprehensive unit conversion functions for all common physical quantities

---

## Energy Systems Supported

The library provides models for a wide range of energy conversion systems, organized by application:

### Domestic Hot Water (DHW) Systems

- **`ElectricBoiler`**: Electric resistance heating system with hot water storage tank
- **`GasBoiler`**: Advanced natural gas combustion boiler (supports dynamic schedules)
- **`AirSourceHeatPumpBoiler`**: Air-source heat pump for hot water production (features CoolProp integration and optimal operation search)
- **`SolarAssistedGasBoiler`**: Hybrid system combining solar thermal collectors with gas backup
- **`GroundSourceHeatPumpBoiler`**: Ground-source heat pump for hot water production (features g-function borehole model)

### Heat Pump Systems

- **`AirSourceHeatPump_cooling`**: Air-source heat pump in cooling mode
- **`AirSourceHeatPump_heating`**: Air-source heat pump in heating mode
- **`GroundSourceHeatPump_cooling`**: Ground-source heat pump in cooling mode
- **`GroundSourceHeatPump_heating`**: Ground-source heat pump in heating mode

### Renewable Energy Systems

- **`PV_to_Converter`**: Photovoltaic system with charge controller, battery, and DC/AC converter

### Dynamic System Models

- **`ElectricHeater`**: Dynamic heat transfer analysis for electric heating elements
- **`StratifiedTankTDMA`**: 1D Stratified hot-water tank model using TDMA and effective thermal conductivity

### Auxiliary Components

- **`Fan`**: Air handling fan with performance curves
- **`Pump`**: Fluid circulation pump with efficiency curves

---

## API entry points

The installed Python namespace is **`enex_analysis`**, while the distribution name is `enex-analysis-engine`. The package initializer exposes the embedded TMHP package; it does not re-export component classes or `print_balance`.

- [ElectricBoiler implementation](src/enex_analysis/electric_boiler.py): `enex_analysis.electric_boiler.ElectricBoiler`. Construction requires explicit heater, tank, temperature and flow parameters. `analyze_steady(T_tank_w, T0, Q_heat_target, return_dict=True)` returns a dictionary, or a one-row DataFrame when `return_dict=False`; dynamic operation uses `analyze_dynamic`.
- [Balance formatter](src/enex_analysis/enex_functions.py): `enex_analysis.enex_functions.print_balance(balance, decimal=2)` accepts a balance mapping. It is not a top-level export.
- [System models](src/enex_analysis/enex_engine.py) contain the cooling/heating classes listed above; follow the actual module and method signatures.

### Electric-boiler steady snapshot

After preparing the checkout and environment below:

```python
from enex_analysis.electric_boiler import ElectricBoiler

boiler = ElectricBoiler(
    heater_capacity=6000.0,
    V_tank_full=0.2,
    T_sup_w_C=10.0,
    T_tank_w_lower_bound_C=50.0,
    T_tank_w_upper_bound_C=60.0,
    T_tank_w_in_C=10.0,
    T_mix_w_out_C=45.0,
    dV_mix_w_out_max=0.0001,
)
result = boiler.analyze_steady(T_tank_w=55.0, T0=10.0, Q_heat_target=4000.0)
print(result["E_heater [W]"])  # 6000.0
```

The constructor uses heater power in W, tank volume in m³, the explicitly named temperatures in °C, and maximum mixed-water volumetric flow in m³/s. In `analyze_steady`, **`Q_heat_target > 0` switches the fixed-capacity heater on**; it does not modulate heater power to the requested target. Thus this snapshot reports 6000 W with a 4000 W target. It does not solve a transient tank balance, and the steady path sets tank loss to zero.

This is a synthetic interface example, not a validated operating point or annual calculation. The older zero-argument `ElectricBoiler()` / `system_update()` example does not describe this class. Component imports load shared helpers from the pinned TMHP submodule; this example does not establish compatibility or physical validity of every other model. Consult the source and [I/O guide](docs/source/guides/io-guide.md) before adapting a study.

---

## Installation

### Requirements

- Python >= 3.10
- `uv` package manager

### Checkout and install

Clone the current repository with its embedded TMHP submodule:

```bash
git clone --recurse-submodules https://github.com/bet-lab/enex-analysis-engine.git
cd enex-analysis-engine
uv sync
```

For an existing checkout, run `git submodule update --init --recursive` before `uv sync`. The submodule is located at `src/enex_analysis/tmhp` and uses its own `src/tmhp` layout; package initialization adds that embedded source to the import path. Do not substitute an unrelated TMHP revision without checking API compatibility. Dependency installation requires access to the Git source configured for dartwork-mpl.

---

## Documentation

Comprehensive documentation is available:

- **[Documentation source](docs/source/index.rst)**: Sphinx API reference and user guide
- **[IO_DOCS.md](IO_DOCS.md)**: Complete input/output interface documentation for all components
- **[EXAMPLES.md](EXAMPLES.md)**: Additional usage examples and tutorials (Korean)

Source documentation includes [installation](docs/source/getting-started/installation.rst), the [user guide](docs/source/guides/user-guide.rst), [core API](docs/source/api/core.rst), [engine API](docs/source/api/engines.rst) and [generated module reference](docs/source/api/generated/modules.rst). Source signatures take precedence when an older tutorial uses a different class interface.

---

## Source map

- [Package initializer](src/enex_analysis/__init__.py): embedded TMHP import aliases.
- [Electric boiler](src/enex_analysis/electric_boiler.py), [gas boiler](src/enex_analysis/gas_boiler.py) and [system engines](src/enex_analysis/enex_engine.py): system calculations.
- [Shared functions](src/enex_analysis/enex_functions.py): balance formatting and shared calculations.
- [Stratified storage](src/enex_analysis/tank_stratification_model.py): tank model.
- [Documentation sources](docs/source/), [project configuration](pyproject.toml) and [submodule configuration](.gitmodules): environment and interface reference.

The heat-pump cycle implementation is embedded under `src/enex_analysis/tmhp`; preserve its submodule identity and its model-specific units, reference-state and balance conventions when comparing systems.
