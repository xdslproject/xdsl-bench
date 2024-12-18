#  Benchmarks for xDSL

This repository contains infrastructure for the benchmarking and performance
profiling of the xDSL compiler framework.

## Benchmark design goals

## Automated ASV regression benchmarking

> airspeed velocity (asv) is a tool for benchmarking Python packages over their
> lifetime. Runtime, memory consumption and even custom-computed values may be
> tracked. The results are displayed in an interactive web frontend that requires
> only a basic static webserver to host.
>
> -- [ASV documentation](https://asv.readthedocs.io/en/stable/index.html)

We use it in CI to benchmark commits made to the main branch of the xDSL
repository.

Every day by the cron schedule `0 4 * * *`, a GitHub actions
workflow is run to use ASV to benchmark the 15 most recent commits to the
xDSL repository, and commit the results to the `.asv/results/github-action`
directory of this repository. Then, the interactive web frontend is built from
these results and all previously committed results from previous workflow runs,
then finally deployed to GitHub pages.

## Profiling
