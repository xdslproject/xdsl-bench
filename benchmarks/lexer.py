#!/usr/bin/env python3
"""Benchmark the xDSL lexer on MLIR files."""

from pathlib import Path

from xdsl.utils.lexer import Input
from xdsl.utils.mlir_lexer import MLIRLexer, MLIRTokenKind

BENCHMARKS_DIR = Path(__file__).parent
RAW_TEST_MLIR_DIR = BENCHMARKS_DIR / "resources" / "raw_test_mlir"
MLIR_FILES: dict[str, Path] = {
    "apply_pdl_extra_file": RAW_TEST_MLIR_DIR / "filecheck__transforms__apply-pdl__apply_pdl_extra_file.mlir",
    "rvscf_lowering_emu": RAW_TEST_MLIR_DIR / "filecheck__with-riscemu__rvscf_lowering_emu.mlir"
}


def lex_input(lexer_input: Input) -> None:
    """Lex an xDSL input."""
    lexer = MLIRLexer(lexer_input)
    while lexer.lex().kind is not MLIRTokenKind.EOF:
        pass


def lex_file(mlir_file: Path) -> None:
    """Lex a mlir file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, str(mlir_file))
    lex_input(lexer_input)


def time_lexer__apply_pdl_extra_file() -> None:
    """Time lexing the `apply_pdl_extra_file.mlir` file."""
    lex_file(MLIR_FILES["apply_pdl_extra_file"])


def time_lexer__rvscf_lowering_emu() -> None:
    """Time lexing the `rvscf_lowering_emu.mlir` file."""
    lex_file(MLIR_FILES["rvscf_lowering_emu"])


def time_lexer__all() -> None:
    """Time lexing all `.mlir` files in xDSL's `tests/` directory ."""
    mlir_files = RAW_TEST_MLIR_DIR.iterdir()
    for mlir_file in mlir_files:
        lex_file(Path(mlir_file))


if __name__ == "__main__":
    import cProfile
    import timeit

    from viztracer import VizTracer

    TEST_NAME = Path(__file__).stem
    MLIR_NAME = "apply_pdl_extra_file"
    MLIR_FILE = MLIR_FILES[MLIR_NAME]

    # Time lexing .mlir files for a single number on performance.
    print(
        "File 'apply_pdl_extra_file.mlir' lexed in "
        f"{timeit.timeit(time_lexer__apply_pdl_extra_file, number=1)}s"
    )
    print(f"All test .mlir files lexed in {timeit.timeit(time_lexer__all, number=1)}s")

    # Profile end-to-end lexing specific .mlir files with cProfile.
    output_prof = f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}.prof"
    cProfile.run(f"time_lexer__{MLIR_NAME}()", output_prof)
    print(f"cProfile written to '{output_prof}'!")

    # Profile lexing only for specific .mlir files with cProfile.
    lexer_input = Input(MLIR_FILE.read_text(), str(MLIR_FILE))
    output_prof = (
        f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}__lex_only.prof"
    )
    cProfile.run("lex_input(lexer_input)", output_prof)
    print(f"cProfile lex only profile written to '{output_prof}'!")

    # Profile lexing only for specific .mlir files with viztracer.
    lexer_input = Input(MLIR_FILE.read_text(), str(MLIR_FILE))
    output_prof = (
        f"{BENCHMARKS_DIR.parent}/profiles/{TEST_NAME}__{MLIR_NAME}__lex_only.json"
    )
    with VizTracer(output_file=output_prof):
        lex_input(lexer_input)
    print(f"VizTracer lex only profile written to '{output_prof}'!")
