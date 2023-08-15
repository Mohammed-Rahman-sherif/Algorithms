def binary_search(arr, target):
    left = 0
    right = len(arr) -1
    
    while left <= right:
        middle = (left + right) // 2
        if arr[middle] == target:
            return middle
        
        elif arr[middle] < target:
            left = middle + 1

        else:
            right = middle -1

    return -1



def binary_search_recursive(arr, target, left, right):
    if left <= right:
        middle = (left + right) // 2

        if arr[middle] == target:
            return middle
        
        elif arr[middle] < target:
            return binary_search_recursive(arr, target, middle + 1, right)

        else:
            return binary_search_recursive(arr, target, left, middle - 1)
    
    else: return -1


arr = [10, 20, 30, 40, 50, 60]
target = 21

result = (binary_search_recursive(arr, target, 0, len(arr)-1))

if result != -1:
    print(f"Target {target} found at index {result}")
else:
    print("Target not found in the list")