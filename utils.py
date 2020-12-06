###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################


import copy

class Queue:
    """Queue structure (FIFO)"""
    def __init__(self):
        """Queue initialization"""
        self.q = []
    
    def enqueue(self, states, front = False):
        """Enqueue single state or list of states to front or to the back

        Args:
            states (list or single): States to be added to Queue
            front (bool, optional): Option to add state to opposite end. Defaults to False.
        """
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
        """Dequeue single state from front or at the back

        Args:
            back (bool, optional): Option to get state from opposite end. Defaults to False.

        Returns:
            single state
        """
        if not back:
            return self.q.pop(0)
        else:
            return self.q.pop(-1)
        
    def len(self):
        """Get length of queue"""
        return len(self.q)
    
    def flush(self):
        """Remove all states in the queue"""
        self.q = []
        
    def peek(self, ndx = None):
        """Get state information form the queue without removing from the queue

        Args:
            ndx (int, optional): If given, returns the state at the index. Else it returns the next state. Defaults to None.

        Returns:
            state
        """
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
    