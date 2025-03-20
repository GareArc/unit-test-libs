def quick_sort(arr: list[int]) -> list[int]:
    """
    Sorts the list using the quick sort algorithm (Lomuto partition scheme).
    Returns a new sorted list.
    """
    return _quick_sort_recursive(arr, 0, len(arr) - 1)


def _quick_sort_recursive(arr: list[int], low: int, high: int) -> list[int]:
    if low < high:
        pivot_index = _partition(arr, low, high)
        _quick_sort_recursive(arr, low, pivot_index - 1)
        _quick_sort_recursive(arr, pivot_index + 1, high)
    return arr


def _partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
