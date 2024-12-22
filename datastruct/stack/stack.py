class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        """Returns the number of elements in the stack"""
        return len(self.items)

    # Optionally, if you prefer using len() directly, you can implement __len__()
    def __len__(self):
        return len(self.items)
