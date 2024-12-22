class QuadraticHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def hash_function(self, key):
        return key % self.size

    def resize(self):
        old_table = self.table.copy()
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0

       
        for item in old_table:
            if item is not None:
                self.insert(item)

    def insert(self, key):
     
        if self.count / self.size > 0.7:
            self.resize()

    
        index = self.hash_function(key)
        original_index = index
        step_count = 0

      
        step = 1
        while self.table[index] is not None:
            index = (original_index + step ** 2) % self.size
            step_count += 1
            step += 1

        self.table[index] = key
        self.count += 1
        return original_index, index, step_count


