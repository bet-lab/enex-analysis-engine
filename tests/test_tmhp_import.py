"""Embedded TMHP remains usable without a sibling checkout or PYTHONPATH."""

import subprocess
import sys


def test_embedded_tmhp_imports_in_isolated_interpreter(tmp_path):
    """Installed package initialization exposes both documented import names."""
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import enex_analysis, tmhp; "
            "from enex_analysis.tmhp.calc_util import C2K; "
            "from enex_analysis.electric_boiler import ElectricBoiler; "
            "assert enex_analysis.tmhp is tmhp; "
            "assert C2K(0.0) == 273.15; "
            "assert ElectricBoiler.__name__ == 'ElectricBoiler'",
        ],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
