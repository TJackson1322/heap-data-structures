"""Compare median sorting times across input orders."""

import random
from statistics import median
from time import perf_counter

from heapsort import heapsort


def randomized_quicksort(values, rng):
    if len(values) <= 1:
        return values
    pivot = rng.choice(values)
    smaller = [value for value in values if value < pivot]
    equal = [value for value in values if value == pivot]
    larger = [value for value in values if value > pivot]
    return randomized_quicksort(smaller, rng) + equal + randomized_quicksort(larger, rng)


def merge_sort(values):
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def sort_with_heap(values):
    heapsort(values)
    return values


def run_benchmarks():
    data_rng = random.Random(42)
    pivot_rng = random.Random(43)
    algorithms = {
        "Heapsort": sort_with_heap,
        "Quicksort": lambda values: randomized_quicksort(values, pivot_rng),
        "Merge Sort": merge_sort,
    }
    print("Median time in milliseconds (10 trials per case)")
    print(f"{'Size':>6} {'Input':<16} {'Heapsort':>12} {'Quicksort':>12} {'Merge Sort':>12}")
    for size in (100, 1000, 5000):
        random_values = data_rng.sample(range(size * 10), size)
        ascending = sorted(random_values)
        cases = {"Random": random_values, "Sorted": ascending, "Reverse-sorted": ascending[::-1]}
        for label, values in cases.items():
            expected = sorted(values)
            timings = {name: [] for name in algorithms}
            names = list(algorithms)
            for trial in range(10):
                offset = trial % len(names)
                for name in names[offset:] + names[:offset]:
                    sample = values.copy()
                    start = perf_counter()
                    result = algorithms[name](sample)
                    elapsed_ms = (perf_counter() - start) * 1000
                    assert result == expected, f"{name} failed on {label}"
                    timings[name].append(elapsed_ms)
            row = " ".join(f"{median(times):12.3f}" for times in timings.values())
            print(f"{size:6} {label:<16} {row}")


if __name__ == "__main__":
    run_benchmarks()
