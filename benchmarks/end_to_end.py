#!/usr/bin/env python3
"""Benchmark running xDSL opt end-to-end on MLIR files."""

from pathlib import Path

from xdsl.xdsl_opt_main import xDSLOptMain

BENCHMARKS_DIR = Path(__file__).parent
RAW_TEST_MLIR_DIR = BENCHMARKS_DIR / "resources" / "raw_test_mlir"
EXTRA_MLIR_DIR = BENCHMARKS_DIR / "resources" / "extra_mlir"
MLIR_FILES: dict[str, Path] = {
    "empty_program": RAW_TEST_MLIR_DIR / "xdsl_opt__empty_program.mlir",
    "constant_folding": EXTRA_MLIR_DIR / "program_20.mlir"
    # "constant_folding": RAW_TEST_MLIR_DIR / "xdsl_opt__not_module_with_module.mlir"
}

def time_end_to_end_opt__empty_program() -> None:
    """Time running the empty program."""
    runner = xDSLOptMain(args=[
        str(MLIR_FILES["empty_program"]),
        "-p", "constant-fold-interp"
    ])
    runner.run()


def time_end_to_end_opt__constant_folding() -> None:
    """Time running a constant folding example."""
    runner = xDSLOptMain(args=[
        str(MLIR_FILES["constant_folding"]),
        "-p", "canonicalize"
    ])
    runner.run()


if __name__ == "__main__":
    import cProfile
    import timeit

    from viztracer import VizTracer

    TEST_NAME = Path(__file__).stem
    MLIR_NAME = "constant_folding"

    # Time optimising .mlir files for a single number on performance.
    print(
        "Empty program optimised in "
        f"{timeit.timeit(time_end_to_end_opt__empty_program, number=1)}s"
    )
    print(
        "Many ones optimised in "
        f"{timeit.timeit(time_end_to_end_opt__constant_folding, number=1)}s"
    )

    # Profile end-to-end optimising the constant folding example with cProfile
    output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}.prof"
    cProfile.run(f"time_end_to_end_opt__{MLIR_NAME}()", output_prof)
    print(f"cProfile written to '{output_prof}'!")

    # Profile end-to-end optimising the constant folding example with VizTracer
    output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}.json"
    with VizTracer(output_file=output_prof):
        time_end_to_end_opt__constant_folding()
    print(f"VizTracer profile written to '{output_prof}'!")
