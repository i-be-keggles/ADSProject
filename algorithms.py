def quicksort(times):
    if len(times) <= 1:
        return times
    pivot = times[len(times) // 2]
    left = [x for x in times if x < pivot]
    middle = [x for x in times if x == pivot]
    right = [x for x in times if x > pivot]
    return quicksort(left) + middle + quicksort(right)