class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_front(self, data):
        
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_end(self, data):
       
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete_front(self):
      
        if self.head:
            self.head = self.head.next

    def delete_end(self):
       
        if self.head:
            if not self.head.next:
                self.head = None
                return
            second_last = self.head
            while second_last.next and second_last.next.next:
                second_last = second_last.next
            second_last.next = None

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    def delete(self, data):
        if self.is_empty():
            return None
        
        if self.head.data == data:
            removed_data = self.head.data
            self.head = self.head.next
            if self.head is None:  
                self.tail = None
            
            return removed_data
        
      
        current = self.head
        while current.next:
            if current.next.data == data:
                removed_data = current.next.data
                current.next = current.next.next
                if current.next is None: 
                    self.tail = current
                
                return removed_data
            current = current.next
        
      
        return None
        
    def is_empty(self):
        """Check if the list is empty."""
        return self.head is None

    def search(self, value):
        """Search for a value in the linked list and return its position (1-based index)."""
        current = self.head
        position = 1
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1  

    def reverse(self):
        """Reverse the linked list."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
  