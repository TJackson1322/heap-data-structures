"""In-place ascending Heapsort."""

def sift_down(values, root, size):
    while 2 * root + 1 < size:
        child = 2 * root + 1
        if child + 1 < size and values[child + 1] > values[child]:
            child += 1
        if values[root] >= values[child]:
            return
        values[root], values[child] = values[child], values[root]
        root = child


def heapsort(values):
    for root in range(len(values) // 2 - 1, -1, -1):
        sift_down(values, root, len(values))
    for end in range(len(values) - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        sift_down(values, 0, end)


if __name__ == "__main__":
    for values in ([], [5], [1, 2, 3], [3, 2, 1], [7, 2, 9, 2, 5], [3, 3, 3]):
        expected = sorted(values)
        heapsort(values)
        assert values == expected
    print("All Heapsort checks passed.")
