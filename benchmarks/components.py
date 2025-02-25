#!/usr/bin/env python3
"""Benchmarks for the pipeline stages of the xDSL implementation."""

from io import StringIO
from pathlib import Path

from xdsl.context import Context
from xdsl.dialects.arith import Arith
from xdsl.dialects.builtin import Builtin, ModuleOp
from xdsl.ir import Operation
from xdsl.parser import Parser as XdslParser
from xdsl.printer import Printer
from xdsl.transforms.canonicalize import CanonicalizePass
from xdsl.transforms.constant_fold_interp import ConstantFoldInterpPass
from xdsl.utils.lexer import Input
from xdsl.utils.mlir_lexer import MLIRLexer, MLIRTokenKind

CTX = Context(allow_unregistered=True)
CTX.load_dialect(Arith)
CTX.load_dialect(Builtin)
MODULE_PRINTER = Printer(stream=StringIO())

BENCHMARKS_DIR = Path(__file__).parent
EXTRA_MLIR_DIR = BENCHMARKS_DIR / "resources" / "extra_mlir"


class Component:
    """Parent class containing workload paths."""

    WORKLOAD_EMPTY = EXTRA_MLIR_DIR / "xdsl_opt__empty_program.mlir"
    WORKLOAD_CONSTANT_100 = EXTRA_MLIR_DIR / "constant_folding_100.mlir"
    WORKLOAD_CONSTANT_1000 = EXTRA_MLIR_DIR / "constant_folding_1000.mlir"
    WORKLOAD_LARGE_DENSE_ATTR = EXTRA_MLIR_DIR / "large_dense_attr.mlir"
    WORKLOAD_LARGE_DENSE_ATTR_HEX = EXTRA_MLIR_DIR / "large_dense_attr_hex.mlir"

    @classmethod
    def lex_file(cls, mlir_file: Path) -> None:
        """Lex a mlir file."""
        contents = mlir_file.read_text()
        lexer_input = Input(contents, str(mlir_file))
        lexer = MLIRLexer(lexer_input)
        while lexer.lex().kind is not MLIRTokenKind.EOF:
            pass

    @classmethod
    def parse_operation(cls, mlir_file: Path) -> Operation:
        """Parse a MLIR file as an operation."""
        contents = mlir_file.read_text()
        parser = XdslParser(CTX, contents)
        return parser.parse_op()

    @classmethod
    def parse_module(cls, mlir_file: Path) -> ModuleOp:
        """Parse a MLIR file as a module."""
        contents = mlir_file.read_text()
        parser = XdslParser(CTX, contents)
        return parser.parse_module()

    @classmethod
    def constant_fold_module(cls, module: ModuleOp) -> ModuleOp:
        """Apply the constant folding pattern rewriter to a module."""
        ConstantFoldInterpPass().apply(CTX, module)
        return module

    @classmethod
    def canonicalize_module(cls, module: ModuleOp) -> ModuleOp:
        """Apply the canonicalization pattern rewriter to a module."""
        CanonicalizePass().apply(CTX, module)
        return module

    @classmethod
    def verify_module(cls, module: ModuleOp) -> None:
        """Verify a module."""
        module.verify()

    @classmethod
    def print_module(cls, module: ModuleOp) -> None:
        """Print a module."""
        MODULE_PRINTER.print_op(module)


class LexPhase(Component):
    """Benchmark the xDSL lexer on MLIR files."""

    def time_empty_program(self) -> None:
        """Time lexing an empty program."""
        Component.lex_file(Component.WORKLOAD_EMPTY)

    def time_constant_100(self) -> None:
        """Time lexing constant folding for 100 items."""
        Component.lex_file(Component.WORKLOAD_CONSTANT_100)

    def time_constant_1000(self) -> None:
        """Time lexing constant folding for 1000 items."""
        Component.lex_file(Component.WORKLOAD_CONSTANT_1000)

    def ignore_time_dense_attr(self) -> None:
        """Time lexing a 1024x1024xi8 dense attribute."""
        Component.lex_file(Component.WORKLOAD_LARGE_DENSE_ATTR)

    def time_dense_attr_hex(self) -> None:
        """Time lexing a 1024x1024xi8 dense attribute given as a hex string."""
        Component.lex_file(Component.WORKLOAD_LARGE_DENSE_ATTR_HEX)


class ParsePhase(Component):
    """Benchmark the xDSL parser on MLIR files."""

    def time_constant_100(self) -> None:
        """Time parsing constant folding for 100 items."""
        Component.parse_operation(Component.WORKLOAD_CONSTANT_100)

    def time_constant_1000(self) -> None:
        """Time parsing constant folding for 100 items."""
        Component.parse_operation(Component.WORKLOAD_CONSTANT_1000)

    def ignore_time_dense_attr(self) -> None:
        """Time parsing a 1024x1024xi8 dense attribute."""
        Component.parse_operation(Component.WORKLOAD_LARGE_DENSE_ATTR)

    def time_dense_attr_hex(self) -> None:
        """Time parsing a 1024x1024xi8 dense attribute given as a hex string."""
        Component.parse_operation(Component.WORKLOAD_LARGE_DENSE_ATTR_HEX)


class PatternRewritePhase(Component):
    """Benchmark rewriting in xDSL."""

    PARSED_CONSTANT_100 = Component.parse_module(Component.WORKLOAD_CONSTANT_100)
    PARSED_CONSTANT_1000 = Component.parse_module(Component.WORKLOAD_CONSTANT_1000)
    PARSED_LARGE_DENSE_ATTR_HEX = Component.parse_module(
        Component.WORKLOAD_LARGE_DENSE_ATTR_HEX
    )

    def time_constant_100(self) -> None:
        """Time canonicalising constant folding for 100 items."""
        Component.canonicalize_module(PatternRewritePhase.PARSED_CONSTANT_100)

    def time_constant_1000(self) -> None:
        """Time canonicalising constant folding for 1000 items."""
        Component.canonicalize_module(PatternRewritePhase.PARSED_CONSTANT_1000)

    def time_constant_interp_100(self) -> None:
        """Time pattern rewriting 100 items with the constant folding pass."""
        Component.constant_fold_module(PatternRewritePhase.PARSED_CONSTANT_100)

    def time_constant_interp_1000(self) -> None:
        """Time pattern rewriting 1000 items with the constant folding pass."""
        Component.constant_fold_module(PatternRewritePhase.PARSED_CONSTANT_1000)

    def time_dense_attr_hex(self) -> None:
        """Time canonicalising a 1024x1024xi8 dense attribute given as a hex string."""
        Component.canonicalize_module(PatternRewritePhase.PARSED_LARGE_DENSE_ATTR_HEX)


class VerifyPhase:
    """Benchmark verifying in xDSL.

    For a single rewriting pass, we verify with the input before the pass and
    the output after the pass.

    Note that this is run on the parsed input, rather than the output of the
    re-writing pass. This is because constant folding and dead-code elimination
    reduce the rewritten results to negligibly small sizes, so only the first
    verification pass contributes to the overall performance.
    """

    PARSED_CONSTANT_100 = Component.parse_module(Component.WORKLOAD_CONSTANT_100)
    PARSED_CONSTANT_1000 = Component.parse_module(Component.WORKLOAD_CONSTANT_1000)
    PARSED_LARGE_DENSE_ATTR_HEX = Component.parse_module(
        Component.WORKLOAD_LARGE_DENSE_ATTR_HEX
    )

    def time_constant_100(self) -> None:
        """Time verifying constant folding for 100 items."""
        Component.verify_module(VerifyPhase.PARSED_CONSTANT_100)

    def time_constant_1000(self) -> None:
        """Time verifying constant folding for 1000 items."""
        Component.verify_module(VerifyPhase.PARSED_CONSTANT_1000)

    def time_dense_attr_hex(self) -> None:
        """Time verifying a 1024x1024xi8 dense attribute given as a hex string."""
        Component.verify_module(VerifyPhase.PARSED_LARGE_DENSE_ATTR_HEX)


class PrintPhase:
    """Benchmark printing in xDSL.

    Note that this is run on the parsed input, rather than the output of the
    re-writing pass. This is because constant folding and dead-code elimination
    reduce the rewritten results to negligibly small sizes, for which printing
    is very quick.
    """

    PARSED_CONSTANT_100 = Component.parse_module(Component.WORKLOAD_CONSTANT_100)
    PARSED_CONSTANT_1000 = Component.parse_module(Component.WORKLOAD_CONSTANT_1000)
    PARSED_LARGE_DENSE_ATTR_HEX = Component.parse_module(
        Component.WORKLOAD_LARGE_DENSE_ATTR_HEX
    )

    def time_constant_100_input(self) -> None:
        """Time printing the input to the constant folding for 100 items."""
        Component.print_module(PrintPhase.PARSED_CONSTANT_100)

    def time_constant_1000_input(self) -> None:
        """Time printing the input to the constant folding for 1000 items."""
        Component.print_module(PrintPhase.PARSED_CONSTANT_1000)

    def time_dense_attr_hex_input(self) -> None:
        """Time printing the input to the a 1024x1024xi8 dense attribute given as a hex string."""
        Component.print_module(PrintPhase.PARSED_LARGE_DENSE_ATTR_HEX)


def draw_comparison_chart() -> None:
    """Compare the pipeline phase times for a workload."""
    draw_plots = True
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        draw_plots = False

    import time

    from bench_utils import warmed_timeit

    if draw_plots:
        plt.style.use("default")
        plt.rcParams.update(
            {
                "grid.alpha": 0.7,
                "grid.linestyle": "--",
                "figure.dpi": 100,
                "font.family": "Menlo",
            }
        )
        plt.title("Pipeline phase times for constant folding 100 items")

    phase_functions = {
        "Lexing": LEXER.time_constant_100,
        "Lexing + Parsing": PARSER.time_constant_100,
        "Rewriting": PATTERN_REWRITER.time_constant_100,
        "Verifying": VERIFIER.time_constant_100,
        "Printing": PRINTER.time_constant_100_input,
    }

    raw_phase_times = {
        name: warmed_timeit(func) for name, func in phase_functions.items()
    }
    print(raw_phase_times)
    phase_means = {
        "Lexing": raw_phase_times["Lexing"][0],
        "Parsing": raw_phase_times["Lexing + Parsing"][0]
        - raw_phase_times["Lexing"][0],
        "Rewriting": raw_phase_times["Rewriting"][0],
        "Verifying": raw_phase_times["Verifying"][0],
        "Printing": raw_phase_times["Printing"][0],
    }
    phase_medians = {
        "Lexing": raw_phase_times["Lexing"][1],
        "Parsing": raw_phase_times["Lexing + Parsing"][1]
        - raw_phase_times["Lexing"][1],
        "Rewriting": raw_phase_times["Rewriting"][1],
        "Verifying": raw_phase_times["Verifying"][1],
        "Printing": raw_phase_times["Printing"][1],
    }
    phase_errors = {
        "Lexing": raw_phase_times["Lexing"][2],
        "Parsing": raw_phase_times["Lexing + Parsing"][2]
        + raw_phase_times["Lexing"][2],
        "Rewriting": raw_phase_times["Rewriting"][2],
        "Verifying": raw_phase_times["Verifying"][2],
        "Printing": raw_phase_times["Printing"][2],
    }

    for name in phase_means:
        if name in phase_errors:
            print(
                f"{name}: {phase_means[name]:.3g} ± {phase_errors[name]:.3g}s (median {phase_medians[name]:.3g})"
            )
    print(f"Total: {sum(phase_means.values()):.3g} ± {sum(phase_errors.values()):.3g}s")

    if draw_plots:
        plt.bar(
            phase_means.keys(),
            phase_means.values(),
            yerr=[phase_errors[name] for name in phase_means],
            error_kw={"capsize": 5},
            label="mean",
        )
        plt.scatter(
            phase_medians.keys(),
            phase_medians.values(),
            label="median",
        )
        plt.xlabel("Pipeline phase", fontweight="bold")
        plt.ylabel("Time [s]", fontweight="bold")
        plt.grid(axis="y")
        plt.legend()
        plt.savefig(
            f"/Users/edjg/Desktop/ubenchmarks/out{int(time.time())}.pdf", dpi=300
        )
        plt.show()


if __name__ == "__main__":
    from collections.abc import Callable

    from bench_utils import profile

    LEXER = LexPhase()
    PARSER = ParsePhase()
    PATTERN_REWRITER = PatternRewritePhase()
    VERIFIER = VerifyPhase()
    PRINTER = PrintPhase()

    BENCHMARKS: dict[str, Callable[[], None]] = {
        "Lexer.empty_program": LEXER.time_empty_program,
        "Lexer.constant_100": LEXER.time_constant_100,
        "Lexer.constant_1000": LEXER.time_constant_1000,
        # "Lexer.dense_attr": LEXER.ignore_time_dense_attr,
        "Lexer.dense_attr_hex": LEXER.time_dense_attr_hex,
        "Parser.constant_100": PARSER.time_constant_100,
        "Parser.constant_1000": PARSER.time_constant_1000,
        # "Parser.dense_attr": PARSER.ignore_time_dense_attr,
        "Parser.dense_attr_hex": PARSER.time_dense_attr_hex,
        "PatternRewriter.constant_100": PATTERN_REWRITER.time_constant_100,
        "PatternRewriter.constant_interp_100": PATTERN_REWRITER.time_constant_interp_100,
        "PatternRewriter.constant_1000": PATTERN_REWRITER.time_constant_1000,
        "PatternRewriter.constant_interp_1000": PATTERN_REWRITER.time_constant_interp_1000,
        "PatternRewriter.dense_attr_hex": PATTERN_REWRITER.time_dense_attr_hex,
        "Verifier.constant_100": VERIFIER.time_constant_100,
        "Verifier.constant_1000": VERIFIER.time_constant_1000,
        "Verifier.dense_attr_hex": VERIFIER.time_dense_attr_hex,
        "Printer.constant_100_input": PRINTER.time_constant_100_input,
        "Printer.constant_1000_input": PRINTER.time_constant_1000_input,
        "Printer.dense_attr_hex_input": PRINTER.time_dense_attr_hex_input,
    }
    profile(BENCHMARKS)
