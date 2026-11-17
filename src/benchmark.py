"""Benchmark every sorting algorithm on every input type and size.

Measures, per run:
  - Time:        wall-clock ns (perf_counter_ns), CPU ns (process_time_ns),
                 and estimated CPU cycles = CPU seconds * --cpu-ghz * 1e9
  - Operations:  comparisons and swaps, as counted by each algorithm
                 (mergesort's "swaps" are array writes; see algorithms.py)
  - Correctness: output is a sorted permutation of the input, same length

Usage:
    python src/benchmark.py --cpu-ghz 3.2
    python src/benchmark.py --cpu-ghz 3.2 --sizes 1000,5000 --repeats 2
"""

import argparse
import csv
import math
import random
import statistics
import sys
import threading
import time

from algorithms import INPUTS, SORTERS, is_correctly_sorted

CSV_FIELDS = ["algorithm", "input", "size", "repeat", "wall_ns", "cpu_ns",
              "est_cycles", "comparisons", "swaps", "correct", "status"]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cpu-ghz", type=float, required=True,
                   help="CPU clock frequency in GHz, used to estimate cycles from CPU time")
    p.add_argument("--sizes", default="1000,5000,10000,50000,100000",
                   help="comma-separated input sizes (default: %(default)s)")
    p.add_argument("--repeats", type=int, default=3,
                   help="runs per (algorithm, input, size) (default: %(default)s)")
    p.add_argument("--time-budget", type=float, default=30.0,
                   help="seconds; a pair predicted to exceed this at the next size "
                        "is skipped from then on (default: %(default)s)")
    p.add_argument("--seed", type=int, default=0, help="RNG seed (default: %(default)s)")
    p.add_argument("--algorithms", default=",".join(SORTERS),
                   help="comma-separated subset of: " + ", ".join(SORTERS))
    p.add_argument("--inputs", default=",".join(INPUTS),
                   help="comma-separated subset of: " + ", ".join(INPUTS))
    p.add_argument("--out", default="results.csv", help="CSV path (default: %(default)s)")
    return p.parse_args()


def run_once(sort_fn, original, cpu_ghz):
    """Sort a fresh copy of `original` and return the measurement dict."""
    arr = list(original)
    cpu0, wall0 = time.process_time_ns(), time.perf_counter_ns()
    comparisons, swaps = sort_fn(arr)
    wall1, cpu1 = time.perf_counter_ns(), time.process_time_ns()
    cpu_ns = cpu1 - cpu0

    return {
        "wall_ns": wall1 - wall0,
        "cpu_ns": cpu_ns,
        "est_cycles": round(cpu_ns * cpu_ghz),  # ns * (cycles per ns)
        "comparisons": comparisons,
        "swaps": swaps,
        "correct": is_correctly_sorted(original, arr),
        "status": "ok",
    }


def benchmark(args):
    sizes = sorted(int(s) for s in args.sizes.split(","))
    algorithms = args.algorithms.split(",")
    input_names = args.inputs.split(",")
    random.seed(args.seed)

    # Generate each input once per size so every algorithm sorts identical data.
    inputs = {}
    for name in input_names:
        for n in sizes:
            data = INPUTS[name](n)
            if data is None:
                print(f"[skip] input '{name}' is not implemented yet")
                break
            inputs[(name, n)] = data

    rows = []
    for alg in algorithms:
        for name in input_names:
            last_n, last_secs, over_budget = None, None, False
            for n in sizes:
                if (name, n) not in inputs:
                    break
                base = {"algorithm": alg, "input": name, "size": n}

                # Predict this size from the last one assuming worst-case O(n^2);
                # quadratic blow-ups get skipped instead of running for hours.
                if not over_budget and last_secs is not None:
                    over_budget = last_secs * (n / last_n) ** 2 > args.time_budget
                if over_budget:
                    rows.append({**base, "repeat": 0, "status": "skipped"})
                    print(f"{alg:20} {name:11} n={n:<7} skipped (over time budget)")
                    continue

                walls, runs = [], []
                for r in range(args.repeats):
                    random.seed(args.seed + r)  # reproducible randomPivot
                    try:
                        res = run_once(SORTERS[alg], inputs[(name, n)], args.cpu_ghz)
                    except Exception as e:
                        res = {"correct": False, "status": f"error:{type(e).__name__}"}
                    runs.append({**base, "repeat": r, **res})
                    if res["status"] != "ok":
                        break
                    walls.append(res["wall_ns"])
                    if res["wall_ns"] / 1e9 > args.time_budget:
                        break

                rows.extend(runs)
                print_summary_line(alg, name, n, runs)
                if walls:
                    last_n, last_secs = n, statistics.median(walls) / 1e9
    return rows


def print_summary_line(alg, name, n, runs):
    good = [r for r in runs if r["status"] == "ok"]
    if not good:
        print(f"{alg:20} {name:11} n={n:<7} {runs[-1]['status']}")
        return
    med = lambda k: statistics.median(r[k] for r in good)
    nlogn = n * math.log2(n) if n > 1 else 0
    correct = all(r["correct"] for r in runs)
    print(f"{alg:20} {name:11} n={n:<7} wall={med('wall_ns') / 1e6:10.2f}ms "
          f"cpu={med('cpu_ns') / 1e6:10.2f}ms cycles~{med('est_cycles'):.3e} "
          f"cmp={med('comparisons'):>13,.0f} (n log n={nlogn:>12,.0f}) "
          f"swaps={med('swaps'):>13,.0f} correct={correct}")


def main():
    args = parse_args()
    rows = benchmark(args)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, restval="")
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    # Deep recursion (quicksort on adversarial input) needs a higher recursion
    # limit, and a bigger thread stack so the interpreter doesn't segfault.
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024) #512mb
    t = threading.Thread(target=main)
    t.start()
    t.join()
