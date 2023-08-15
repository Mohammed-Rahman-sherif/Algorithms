class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def create_linked_list(values):
    if not values:
        return None

    head = Node(values[0])
    current = head
    for value in values[1:]:
        current.next = Node(value)
        current = current.next

    return head

def binary_search(head, target):
    current = head
    while current is not None:
        if current.data == target:
            return True
        elif current.data < target:
            current = current.next
        else:
            return False

    return False

# Create a linked list with the provided values
values = [5, 6, 7, 8, 9, 10, 11]
head = create_linked_list(values)

target = 6

result = binary_search(head, target)

if result:
    print("Value found")
else:
    print("Value not found")
