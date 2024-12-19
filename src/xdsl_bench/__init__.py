#!/usr/bin/env python3
"""A meta-repo for benchmarking xDSL.

This file exists to indicate to the `setup_tools` build
system that other directories such as `profile/` are not the
build targets.
"""

print(
    "This repository contains infrastructure for building benchmarks, "
    "but no packages in itself."
)
