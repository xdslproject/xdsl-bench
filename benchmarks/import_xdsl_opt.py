#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmarks that measure the time to import `xdsl_opt_main`."""


def time_import_inspect():
    """Import benchmark using the default asv mechanism."""
    from xdsl.xdsl_opt_main import xDSLOptMain


def timeraw_import_inspect():
    """Import benchmark using the `raw` asv mechanism."""
    return """
    from xdsl.xdsl_opt_main import xDSLOptMain
    """
