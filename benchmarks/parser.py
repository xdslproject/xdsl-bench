#!/usr/bin/env python3
"""Benchmark the xDSL parser on MLIR files."""

from pathlib import Path

from xdsl.context import MLContext
from xdsl.parser import Parser


BENCHMARKS_DIR = Path(__file__).parent
GENERIC_TEST_MLIR_DIR = BENCHMARKS_DIR / "resources" / "generic_test_mlir"
MLIR_FILES: dict[str, Path] = {
    "apply_pdl_extra_file": GENERIC_TEST_MLIR_DIR / "apply_pdl_extra_file.mlir",
    "add": GENERIC_TEST_MLIR_DIR / "add.mlir"
}

CTX = MLContext(allow_unregistered=True)


def parse_input(parser_input: str) -> None:
    """Parse a string."""
    parser = Parser(CTX, parser_input)
    parser.parse_op()


def parse_file(mlir_file: Path) -> None:
    """Parse a MLIR file."""
    contents = mlir_file.read_text()
    parse_input(contents)


def time_parser__apply_pdl_extra_file() -> None:
    """Time parsing the `apply_pdl_extra_file.mlir` file."""
    parse_file(MLIR_FILES["apply_pdl_extra_file"])


def time_parser__add() -> None:
    """Time parsing the `add.mlir` file."""
    parse_file(MLIR_FILES["add"])


def time_parser__all() -> None:
    """Time parsing all `.mlir` files in xDSL's `tests/` directory ."""
    mlir_files = GENERIC_TEST_MLIR_DIR.iterdir()
    for mlir_file in mlir_files:
        parse_file(Path(mlir_file))


if __name__ == "__main__":
    import cProfile
    import timeit

    from viztracer import VizTracer

    TEST_NAME = Path(__file__).stem
    MLIR_NAME = "apply_pdl_extra_file"
    MLIR_FILE = MLIR_FILES[MLIR_NAME]

    # Time parsing .mlir files for a single number on performance.
    print(
        "File 'apply_pdl_extra_file.mlir' parsed in "
        f"{timeit.timeit(time_parser__apply_pdl_extra_file, number=1)}s"
    )
    print(f"All test .mlir files lexed in {timeit.timeit(time_parser__all, number=1)}s")

    # # Profile end-to-end lexing specific .mlir files with cProfile.
    # output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}.prof"
    # cProfile.run(f"time_lexer__{MLIR_NAME}()", output_prof)
    # print(f"cProfile written to '{output_prof}'!")

    # # Profile lexing only for specific .mlir files with cProfile.
    # lexer_input = Input(MLIR_FILE.read_text(), str(MLIR_FILE))
    # output_prof = (
    #     f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}__lex_only.prof"
    # )
    # cProfile.run("lex_input(lexer_input)", output_prof)
    # print(f"cProfile lex only profile written to '{output_prof}'!")

    # # Profile lexing only for specific .mlir files with viztracer.
    # lexer_input = Input(MLIR_FILE.read_text(), str(MLIR_FILE))
    # output_prof = (
    #     f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}__lex_only.json"
    # )
    # with VizTracer(output_file=output_prof):
    #     lex_input(lexer_input)
    # print(f"VizTracer lex only profile written to '{output_prof}'!")
