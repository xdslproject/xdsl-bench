#!/usr/bin/env python3
"""Benchmark running xDSL opt end-to-end on MLIR files."""

from pathlib import Path
from argparse import Namespace

from xdsl.xdsl_opt_main import xDSLOptMain

BENCHMARKS_DIR = Path(__file__).parent
MLIR_FILES: dict[str, Path] = {
    "empty_program": Path(
        "xdsl/tests/xdsl_opt/empty_program.mlir"
    ),
    "constant_folding": Path(
        "xdsl/tests/filecheck/dialects/arith/arith_constant_fold_interp.mlir"
    ),
}


def time_empty_program() -> None:
    """Time running the empty program."""
    runner = xDSLOptMain(args=[
        str(MLIR_FILES["empty_program"]),
        "-p", "constant-fold-interp"
    ])
    runner.run()


def time_many_ones_sum() -> None:
    """Time running a programming summing many ones."""
    runner = xDSLOptMain(args=[
        str(MLIR_FILES["constant_folding"]),
        "-p", "constant-fold-interp"
    ])
    runner.run()


if __name__ == "__main__":
    import timeit

    print(
        "Empty program optimised in "
        f"{timeit.timeit(time_empty_program, number=1)}s"
    )
    print(
        "Many ones optimised in "
        f"{timeit.timeit(time_many_ones_sum, number=1)}s"
    )
