
class Node:
  def __init__(self, data) -> None:
    self.data = data
    self.next = None

class LinkedList:
  def __init__(self) -> None:
    self.head: Node = None

  def push(self, data) -> None:
    '''
      Time Complexity
        best case (list is empty) -> O(1)
        worst case -> O(N), where N is the number of nodes in the linked list
    '''
    if self.head is None:
      self.head = Node(data)
    else:
      node = self.head
      while node.next is not None:
        node = node.next
      node.next = Node(data)

  def get_middle(self) -> Node:
    '''
      Time Complexity: O(N), where N is the number of nodes in the linked list
      Auxiliary Space: O(1)
    '''
    slow_pointer = self.head
    fast_pointer = self.head
    while fast_pointer is not None:
      fast_pointer = fast_pointer.next
      if fast_pointer is not None:
        fast_pointer = fast_pointer.next
      slow_pointer = slow_pointer.next
    return slow_pointer

