from dataclasses import dataclass
import typing

@dataclass
class Node:
  value: typing.Any
  previous_node = None
  next_node = None
  
class Iterator:
  def __init__(self, head_node: Node, list_size: int):
    self.node = head_node
    self.list_size = list_size
    self.current_index = 0

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.list_size == self.current_index:
      raise StopIteration
    value = self.node.value
    self.node = self.node.next_node
    self.current_index += 1
    return value
 
class List:
  """A circular linked list"""

  def __init__(self):
    self._head: Node = None
    self._tail: Node = None
    self._size: int = 0

  def __str__(self) -> str:
    return self.__repr__()

  def __repr__(self) -> str:
    str_repr = '['
    node = self._head
    while True:
      str_repr += str(node.value)
      node = node.next_node
      if node == self._head:
        break
      else:
        str_repr += ', '
    str_repr += ']'
    return str_repr
  
  def __iter__(self) -> Node:
    return Iterator(self._head, self.size)

  @property
  def size(self) -> int:
    """The size of the list"""
    return self._size

  def append(self, value: typing.Any) -> None:
    """
    Appends/adds an element to the end of the list
    [time complexity: O(1)]

    Args:
      value:
        The value to be appended
    """
    new_node = Node(value)
    if self._head is None: # when the list is empty
      self._head = new_node
      self._tail = self._head
      self._head.next_node = self._tail
      self._tail.previous_node = self._head
    else: # when the list is not empty
      new_node.previous_node = self._tail
      self._tail.next_node = new_node
      self._tail = new_node

    # this is a circular list, so head's previous node will
    # always be the tail, and tail's next node will always be the head
    self._head.previous_node = self._tail
    self._tail.next_node = self._head
    self._size+=1

  def _convert_nagative_index_into_positive(self, negative_index: int) -> int:
    return self.size - abs(negative_index)
  
  def _is_index_closest_to_the_head(self, index: int) -> bool:
    mid_index = ((self.size - 1) // 2)
    return index <= mid_index if mid_index // 2 == 0 else index <= mid_index + 1
  
  def _get_node_at(self, index: int) -> Node:
    converted_index = index
    if index < 0:
      converted_index = self._convert_nagative_index_into_positive(index)
    
    if converted_index > self.size - 1 or converted_index < 0:
      raise IndexError(f'Index [{index}] is out of range')
    
    if self._is_index_closest_to_the_head(converted_index): # closest to the head
      node = self._head
      for i in range(0, converted_index):
        node = node.next_node
    else: # closest to the tail
      node = self._tail
      for i in range(self.size-1, converted_index, -1):
        node = self._tail.previous_node
    
    return node

  def pop(self, index: int = -1) -> None:
    """
    Removes a value from a given index of the list.
    [time complexity: O(n)]

    Args:
      index:
        The index of the value to be removed. Defaults to -1.
        Negative numbers represents the inverse order of the list.
        -1 represents the last index, -2 represents the index before the last one.
    
    Raises:
      IndexError: The given index is out of range
    """
    node = self._get_node_at(index)

    if node == self._head and node == self._tail: # list has only one node
      self._head = None
      self._tail = None
    elif node == self._head: # given node is the head
      self._head = node.next_node
    elif node == self._tail: # given node is the tail
      self._tail = node.previous_node

    node.previous_node.next_node = node.next_node
    node.next_node.previous_node = node.previous_node
    self._size-=1

  def at(self, index: int) -> typing.Any:
    """
    Returns the value at a given index
    [time complexity: O(n)]

    Args:
      index:
        The index of the given value.
        Negative numbers represents the inverse order of the list.
        -1 represents the last index, -2 represents the index before the last one.

    Returns:
      The value at the given index

    Raises:
      IndexError: The given index is out of range
    """
    return self._get_node_at(index).value
  
  def for_each(self, callback) -> None:
    """
    Returns each value of the list to the callback function
    [time complexity: O(n)]
    
    Args:
      callback: 
        The callback function. The callback function returns the value and its index
        Usage example for a given list of [0, 1, 2]:
          list.for_each(lambda val, index : print(f'v: {val}, i: {index}'))
    """
    node = self._head
    current_index = 0
    while True:
      callback(node.value, current_index)
      node = node.next_node
      current_index+=1
      if node == self._head: # because the list is circular, the tail points to the head
        break


list = List()
list.append(1)
list.append(2)
list.append(3)

print(list)