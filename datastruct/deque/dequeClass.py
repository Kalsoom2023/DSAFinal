class DequeClass:
    def __init__(self):
        self.items = []

    def enqueue_front(self, item):
        self.items.insert(0, item)

    def enqueue_rear(self, item):
        self.items.append(item)

    def dequeue_front(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def dequeue_rear(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def rear(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0
