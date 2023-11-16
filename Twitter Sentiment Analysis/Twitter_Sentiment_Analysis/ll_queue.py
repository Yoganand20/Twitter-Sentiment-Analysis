class Node:
    def __init__(self, data):
       self.data = data
       self.next = None
 
class Queue:
    def __init__(self):
        self.head = None
        self.last = None
        self.size=0
 
    def enqueue(self, data):
        if self.last is None:
            self.head = Node(data)
            self.last = self.head
        else:
            self.last.next = Node(data)
            self.last = self.last.next
        self.size=self.size+1;
 
    def dequeue(self):
        if self.head is None:
            self.size=0;
            return None
        else:
            to_return = self.head.data
            self.head = self.head.next
            self.size=self.size-1;
            return to_return
        
    def to_dict(self):
        # Convert the queue to a list
        queue_list = []
        current = self.head
        while current:
            queue_list.append(current.data)
            current = current.next
        return {'queue': queue_list}
 