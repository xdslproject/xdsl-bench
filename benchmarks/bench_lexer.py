#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script benchmarks the xDSL lexer on MLIR files.

Two strategies are used:
 - Recording the average time taken for many repititions of individual MLIR files
 - Recording the average time taken across a wide set of MLIR files
"""

from pathlib import Path
import timeit
import glob

from xdsl.utils.lexer import Input
from xdsl.utils.mlir_lexer import MLIRLexer, MLIRTokenKind


NUM_REPITITIONS = 1000
BENCHMARKS_DIR = Path(__file__).parent


def lex_input(lexer_input: Input) -> None:
    """Lex an input."""
    lexer = MLIRLexer(lexer_input)
    while lexer.lex().kind is not MLIRTokenKind.EOF:
        pass

def lex_file(mlir_file: Path) -> None:
    """Time lexing a mlir file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, mlir_file)
    lex_input(lexer_input)


def lex_file_timeit(mlir_file: Path, num_repititions: int = 1) -> float:
    """Time lexing a mlir file."""
    contents = mlir_file.read_text()
    lexer_input = Input(contents, mlir_file)
    return timeit.timeit(
        lambda: lex_input(lexer_input), number=num_repititions
    ) / num_repititions


def time_lexer__apply_pdl_extra_file() -> float:
    """."""
    mlir_file = BENCHMARKS_DIR / "../xdsl/tests/filecheck/transforms/apply-pdl/apply_pdl_extra_file.mlir"
    return lex_file_timeit(
        mlir_file,
        num_repititions=NUM_REPITITIONS
    )


def time_lexer__rvscf_lowering_emu() -> float:
    """."""
    mlir_file = BENCHMARKS_DIR / "../xdsl/tests/filecheck/with-riscemu/rvscf_lowering_emu.mlir"
    return lex_file_timeit(
        mlir_file,
        num_repititions=NUM_REPITITIONS
    )


def time_lexer_all() -> None:
    """."""
    mlir_files = glob.iglob(
         str(BENCHMARKS_DIR.parent) + "/xdsl/tests/**/*.mlir",
         recursive=True
    )
    for mlir_file in mlir_files:
        lex_file(Path(mlir_file))


if __name__ == "__main__":
    print(f"apply_pdl_extra_file.mlir: {time_lexer__apply_pdl_extra_file()}s")
    print(f"rvscf_lowering_emu.mlir: {time_lexer__rvscf_lowering_emu()}s")
    print(f"tests/**/*.mlir: {time_lexer_all()}s")
