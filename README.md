# COMP_7010_Research_Project
Exploring the real-time performance of O(nlog(n)) sorting algorithms when faced with various adversarial inputs.

## To run the code:
1. Create and activate a python virtual environment in the project root directory with the following
    1. `python -m venv venv`
    2. `source venv/bin/activate`
2. run `pip install -r requirements.txt`
3. run `pytest src/algorithms.py` to check correctness, or `pytest -s src/algorithms.py` to also print the comparison/swap counts for each case
    - Cases that fail because of known quicksort bugs are marked `xfail` (see the `# BUG:` comments in `src/algorithms.py`); inputs whose generators are still stubs are skipped.

## To run the benchmark:
`python src/benchmark.py --cpu-ghz <your CPU clock in GHz>`

Runs every algorithm on every input type and size, prints a median summary and writes `results.csv` (one row per run). Useful options: `--sizes 1000,5000`, `--repeats 3`, `--algorithms mergesort,heapsort`, `--inputs sorted,equal`, `--time-budget 30`, `--seed 0`, `--out results.csv`. Run with `--help` for everything.

| Column | Meaning |
|---|---|
| `algorithm`, `input`, `size`, `repeat` | what was run |
| `wall_ns` | wall-clock time (`time.perf_counter_ns`) |
| `cpu_ns` | process CPU time (`time.process_time_ns`) |
| `est_cycles` | estimated CPU cycles = `cpu_ns * --cpu-ghz` |
| `comparisons`, `swaps` | operation counts reported by the algorithm (mergesort's swaps are array writes) |
| `correct` | output is sorted, same length, and same contents as the input |
| `status` | `ok`, `error:<Exception>`, or `skipped` (predicted to exceed `--time-budget` assuming O(n^2) growth) |

Timing includes the overhead of the operation counters. It's the same for every algorithm, so comparisons between them are fair.
