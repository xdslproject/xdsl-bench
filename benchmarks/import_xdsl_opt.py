#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ImportXdslOpt:
    """A benchmark that measures the time to import xdsl_opt_main.

    This is most of the constant cost of running xdsl-opt.
    """

    def setup(self):
        """Set up the benchmarks."""
        pass

    def time_import_inspect(self):
        """Import benchmark using the default asv mechanism."""
        from xdsl.xdsl_opt_main import xDSLOptMain

    def timeraw_import_inspect(self):
        """Import benchmark using the `raw` asv mechanism."""
        return """
        from xdsl.xdsl_opt_main import xDSLOptMain
        """
