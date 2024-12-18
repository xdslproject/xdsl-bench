#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmarks that measure the time to import `xdsl_opt_main`.

These are are simple example which can be used as a template for more
complex/helpful benchmarks. See "Writing benchmarks" in the asv docs for more
information.
"""

from pathlib import Path

BENCHMARKS_DIR = Path(__file__).parent


def time_import_inspect() -> None:
    """Import benchmark using the default asv mechanism."""
    from xdsl.xdsl_opt_main import xDSLOptMain  # noqa: F401


def timeraw_import_inspect() -> str:
    """Import benchmark using the `raw` asv mechanism."""
    return """
    from xdsl.xdsl_opt_main import xDSLOptMain
    """


if __name__ == "__main__":
    import cProfile
    from pathlib import Path

    test_name = Path(__file__).stem
    output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{test_name}.prof"

    cProfile.run("time_import_inspect()", output_prof)

    print(f"Profile written to '{output_prof}'!")
