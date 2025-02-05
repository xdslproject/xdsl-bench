#  Benchmarks for xDSL

This repository contains infrastructure for the benchmarking and performance
profiling of the xDSL compiler framework.

***This repository is currently under development, so is not stable. Benchmarking infrastructure may fail and not immediately be fixed.***

## Automated regression benchmarking with ASV

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

This web frontend can be found at <https://xdsl.dev/xdsl-bench/>.

## Profiling

Running profiling benchmarks locally rather than via ASV requires also
installing `xdsl` to the virtual environment. This should be done by default
when syncing without extra flags, but can also be done with
`uv sync --group profile`, which points to the submodule directory.

### `cProfile` + `snakeviz`

The general approach is using the same benchmarks defined for ASV to avoid
duplication, but setting up `cProfile` tracing in the
`if __name__ == "__main__":` construct. As such, ASV can run the benchmarks as
usual, but directly running the files with Python can be used to perform custom
profiling.

The generated profiles files can then be viewed using
[`snakeviz`](https://jiffyclub.github.io/snakeviz/), drawing an interactive
call graph of the execution.

For example, the commands to profile lexing the `apply_pdl_extra_file.mlir`
file using the lexer benchmark.

```bash
uv run python benchmarks/lexer.py
uv run snakeviz profiles/lexer__apply_pdl_extra_file.prof
```

You can also use [`flameprof`](https://github.com/baverman/flameprof/) to
visualise the profile data as follows, but the generated SVG files are not
interactive and less readable:

```bash
uv run python benchmarks/lexer.py
uv run flameprof profiles/lexer__apply_pdl_extra_file__lex_only.prof \
    > profiles/lexer__apply_pdl_extra_file__lex_only.svg
```

### `viztracer`

An alternative to profiling with `cProfile` and visualising with `snakeviz`
is the end-to-end profiler [`viztracer`](https://github.com/gaogaotiantian/viztracer).

For example, the commands to profile an end-to-end test of running xDSL-opt on
an empty MLIR program with `viztracer` are shown below:

```bash
uv run viztracer \
    -o profiles/empty_program.json \
    xdsl/xdsl/tools/xdsl_opt.py \
    xdsl/tests/xdsl_opt/empty_program.mlir
    --output-file profiles/empty_program.json
uv run vizviewer profiles/empty_program.json
```

## Roadmap

### ASV flow

- [x] Fix ASV virtual environment issues due to versioneer with submodules
- [x] Get ASV running locally
- [x] Get ASV running on GitHub actions 
- [x] Add ASV machine description
- [x] Deploy ASV website to GitHub pages
- [x] Fix committing results so graph can have multiple points
- [x] Identify why submodule checkout fails to any commits other than head
- [x] Move repo to xDSL organisation
- [x] Support multiple python versions
- [ ] ? Consider moving committed ASV runs to their own branch so they don't
    interfere with other things
- [ ] ? Consider inverting submodules to move benchmarks back into main repo and
      instead keep artifacts in submodule

### Benchmarks

- [x] Importing `xDSLOptMain`
- [x] Lexing
- [x] End-to-end optimisation 
- [x] Parsing
- [ ] Printing
- [ ] Loading dialects
  - [ ] `builtin.py`
  - [ ] `arith.py`
- [ ] Re-writing optimisations
  - [ ] `Builder`
  - [ ] `Rewriter`
  - [ ] `PatternRewriter`
- [ ] Package installation time

### Profiling

- [x] `cProfile` + `snakeviz`
- [x] `viztracer`
- [ ] `scalene`
- [ ] Memory profilers 

## Additional resources

- <https://cerfacs.fr/coop/python-profiling>
- <https://www.petermcconnell.com/posts/perf_eng_with_py12/>
- <https://danmackinlay.name/notebook/python_debug>
- <https://www.brendangregg.com/blog/index.html>
- <https://superfastpython.com/benchmark-python-function/>
- <https://github-pages.arc.ucl.ac.uk/python-tooling/pages/benchmarking-profiling.html>
- <https://discuss.python.org/t/python-benchmarking-in-unstable-environments/22334>
- <https://switowski.com/blog/how-to-benchmark-python-code/>


## References

[^1]: <https://speakerdeck.com/anissa111/benchmarking-your-scientific-python-packages-using-asv-and-github-actions>
[^2]: <https://github.com/airspeed-velocity/asv_samples/blob/main/.github/workflows/build_test.yml>
[^3]: <https://labs.quansight.org/blog/2021/10/re-engineering-cicd-pipelines-for-scipy>
[^4]: <https://labs.quansight.org/blog/2021/08/github-actions-benchmarks>
[^5]: <https://github.com/man-group/ArcticDB/wiki/Running-ASV-Benchmarks>
[^6]: <https://github.com/man-group/ArcticDB/blob/master/.github/workflows/benchmark_commits.yml>
