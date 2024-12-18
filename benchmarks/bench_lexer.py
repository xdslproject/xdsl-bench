#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script benchmarks the xDSL lexer on MLIR files.

Two strategies are used:
 - Recording the average time taken for many repititions of individual MLIR files
 - Recording the average time taken across a wide set of MLIR files
"""

import timeit
from pathlib import Path

from xdsl.utils.lexer import Input
from xdsl.utils.mlir_lexer import MLIRLexer, MLIRTokenKind

NUM_REPITITIONS = 1000
BENCHMARKS_DIR = Path(__file__).parent


def lex_input(lexer_input: Input) -> None:
    """Lex an xDSL input."""
    lexer = MLIRLexer(lexer_input)
    while lexer.lex().kind is not MLIRTokenKind.EOF:
        pass


def lex_file(mlir_file: Path) -> None:
    """Lex a mlir file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, mlir_file)
    lex_input(lexer_input)


def lex_file_timeit(mlir_file: Path, num_repititions: int = 1) -> float:
    """Time lexing a mlir file, excluding time taken reading the file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, mlir_file)
    return (
        timeit.timeit(lambda: lex_input(lexer_input), number=num_repititions)
        / num_repititions
    )


def time_lexer__apply_pdl_extra_file() -> None:
    """Time lexing the `apply_pdl_extra_file.mlir` file."""
    return lex_file(
        BENCHMARKS_DIR
        / "../xdsl/tests/filecheck/transforms/apply-pdl/apply_pdl_extra_file.mlir"
    )


def time_lexer__rvscf_lowering_emu() -> None:
    """Time lexing the `rvscf_lowering_emu.mlir` file."""
    return lex_file(
        BENCHMARKS_DIR / "../xdsl/tests/filecheck/with-riscemu/rvscf_lowering_emu.mlir"
    )


def time_lexer_all() -> None:
    """Time lexing all `.mlir` files in xDSL's `tests/` directory ."""
    mlir_files = (BENCHMARKS_DIR.parent / "xdsl/tests").rglob("*.mlir")
    for mlir_file in mlir_files:
        lex_file(Path(mlir_file))


if __name__ == "__main__":
    print(f"All test .mlir files lexed in {timeit.timeit(time_lexer_all, number=1)}s")
