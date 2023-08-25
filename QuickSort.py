from timeit import timeit

def quickSort(arr):
    if len(arr) <= 1:
        return arr
    
    right = []
    left = []
    pivot = arr[-1]

    for element in arr[:-1]:
        if element <= pivot:
            left.append(element)

        else:
            right.append(element)

    return quickSort(left) + [pivot] + quickSort(right)


if __name__ == "__main__":
    test_cases = [[10, 40, 20, 70, 30, 25, 60, 90, 85, 5],
                  [20, 40, 10],
                  [40, 20, 10],
                  [10, 20, 40],
                  [10, 40, 20],
                  [1],
                  [],
                  [0, 10, 0]]
    
    for case in test_cases:
        sorted_array = quickSort(case)
        time_taken = timeit(lambda: quickSort(case), number=1)
        print(f"Sorted array: {sorted_array} Time consumed: {time_taken:.2f} seconds")
