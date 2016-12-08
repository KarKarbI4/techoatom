def my_qsort(arr):
    _my_qsort(arr, 0, len(arr))

def _my_qsort (array, start, end):
    if end - start <= 1:
        return 0
    pivot_indx = start
    pivot = array[start]
    i = start + 1
    for j in range(start + 1, end):
        if array[j] < pivot:
            array[j], array[i] = array[i], array[j]
            i += 1
    array[start], array[i - 1] = array[i - 1], array[start]
    pivot_indx = i - 1

    _my_qsort(array, start, pivot_indx)
    _my_qsort(array, pivot_indx + 1, end)

if __name__ == "__main__":
    arr = [4, 43, 2, 3, 7, 5, 10, 3]
    my_qsort(arr)
    print(arr)
