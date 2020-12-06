###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################


import copy

class Queue:
    def __init__(self):
        self.q = []
    
    def enqueue(self, states, front = False):
        if type(states) == list:
            if front:
                states.reverse()
            
            for state in states:
                if not front:
                    self.q.append(state)
                else:
                    self.q.insert(0, state)
        else:
            if not front:
                self.q.append(states)
            else:
                self.q.insert(0, states)
            
    
    def dequeue(self, back = False):
        if not back:
            return self.q.pop(0)
        else:
            return self.q.pop(-1)
        
    def len(self):
        return len(self.q)
    
    def flush(self):
        self.q = []
        
    def peek(self, ndx = None):
        if ndx is None:
            return copy.deepcopy(self.q)
        else:
            return self.q[ndx]

if __name__ == "__main__":
    q = Queue()
    q.enqueue("state1")
    print(q.dequeue())
    q.enqueue(["state2","state3"])
    print(q.peek())
    q.enqueue("state4", front=True)
    q.enqueue("state5")
    print(q.peek())
    print(q.dequeue())
    print(q.peek())
    print(q.dequeue(back=True))
    print(q.peek())
    q.flush()
    print(q.peek())
    