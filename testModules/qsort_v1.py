def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i  # bug


def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)


def qSort(li):
    n = len(li)
    quickSort(li, 0, n-1)
    return li


# arr = [7, 2, 3, 4, 5, 6]
# n = len(arr)
# quickSort(arr, 0, n-1)
# print("Sorted array is:\n{}".format(arr))
