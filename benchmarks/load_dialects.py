#!/usr/bin/env python3
"""Benchmark loading dialects in xDSL."""

# TODO: Define the benchmarks

if __name__ == "__main__":
    from collections.abc import Callable

    from xdsl_bench.utils import profile

    BENCHMARKS: dict[str, Callable[[], None]] = {}
    profile(BENCHMARKS)
