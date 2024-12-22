class QueueClass:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
       
        self.items.append(item)

    def dequeue(self):
        
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None  

    def front(self):
        
        if not self.is_empty():
            return self.items[0]
        else:
            return None 

    def size(self):
        return len(self.items)
    def rear(self):
         if not self.is_empty():
            return self.items[-1]
         else:
            return None  