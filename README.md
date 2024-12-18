#  Benchmarks for xDSL

This repository contains infrastructure for the benchmarking and performance
profiling of the xDSL compiler framework.

## Benchmark design goals

## Automated ASV regression benchmarking

> airspeed velocity (asv) is a tool for benchmarking Python packages over their
> lifetime. Runtime, memory consumption and even custom-computed values may be
> tracked. The results are displayed in an interactive web frontend that
> requires only a basic static webserver to host.
>
> -- [ASV documentation](https://asv.readthedocs.io/en/stable/index.html)

We use it in CI to benchmark commits made to the main branch of the xDSL
repository.

Every day by the cron schedule `0 4 * * *`, a GitHub actions workflow is run
using ASV to benchmark the 15 most recent commits to the xDSL repository, and
commit the results to the `.asv/results/github-action` directory of this
repository. Then, the interactive web frontend is built from these results and
all previously committed results from previous workflow runs, then finally
deployed to GitHub pages [^1] [^2] [^3] [^4] [^5] [^6].

This web frontend can be found at <https://edmundgoodman.co.uk/xdsl-bench/>.

## Profiling

Running profiling benchmarks locally rather than via ASV requires also
installing `xdsl` to the virtual environment. This can be done with
`uv sync --group xdsl`, which points to the submodule directory.

The general approach is using the same benchmarks defined for ASV to avoid
duplication, but setting up `cProfile` tracing in the
`if __name__ == "__main__":` construct. As such, ASV can run the benchmarks as
usual, but directly running the files with Python can be used to perform custom
profiling.

## References

[^1]: <https://speakerdeck.com/anissa111/benchmarking-your-scientific-python-packages-using-asv-and-github-actions>
[^2]: <https://github.com/airspeed-velocity/asv_samples/blob/main/.github/workflows/build_test.yml>
[^3]: <https://labs.quansight.org/blog/2021/10/re-engineering-cicd-pipelines-for-scipy>
[^4]: <https://labs.quansight.org/blog/2021/08/github-actions-benchmarks>
[^5]: <https://github.com/man-group/ArcticDB/wiki/Running-ASV-Benchmarks>
[^6]: <https://github.com/man-group/ArcticDB/blob/master/.github/workflows/benchmark_commits.yml>
