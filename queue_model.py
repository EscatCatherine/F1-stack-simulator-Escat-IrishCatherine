"""Queue Object (FIFO)"""
class Queue:
    def __init__(self, items=None):
        self.items = list(items or [])  # index 0 = FRONT, last index = REAR

    def enqueue(self, value):
        self.items.append(value)  # add to the REAR

    def dequeue(self):
        return self.items.pop(0) if self.items else None  # remove from the FRONT

    def peek(self):
        return self.items[0] if self.items else None  # look at the FRONT

    def is_empty(self):
        return not self.items

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()
