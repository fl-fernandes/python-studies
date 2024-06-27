import numpy as np
from linkedlist import List
import typing
from dataclasses import dataclass

type KeyType = float

@dataclass
class Pair:
  key: KeyType
  value: typing.Any

class DataNotFound(Exception):
  def __init__(self, key: typing.Any):
    super().__init__(f'No data with key [{key}] has been found.')

class HashTable:
  """
    A HashMap data structure.

    The numpy library is a dependency for this class because-
    an numpy array is used in order to have a real array for the table.

    To resolve collisions, this implementation uses the List defined at _linkedlist.py_.
    which is a circular linked list.

    All time complexities will be represented in two separated categories,-
    one that considers only the hash table implementation itself, and another one-
    that also considers the list implementation behind.
    The representation will follow the pattern-
    "[time complexity: {table complexity}/{list complexity}/{final complexity}]".

    Args:
      capacity:
        The table capacity - the internal array size 
  """
  def __init__(self, capacity: int):
    self._table = np.empty(capacity, List) # initialize an empty numpy array of N size
    self._capacity = capacity
    self._size = 0

  def _hash(self, key: KeyType) -> int:
    return key % self._capacity
  
  @property
  def size(self) -> int:
    """
    The size of the hash table/the number of values in it.
    [time complexity: O(1)]
    """
    return self._size
  
  @property
  def capacity(self) -> int:
    """
    The capacity of the hash_table/the size of the internal array.
    [time complexity: O(1)]
    """
    return self._capacity

  def add(self, key: KeyType, value: typing.Any):
    """
    Adds a value to the hash table.
    [time complexity: O(1)/O(n)/O(n)]

    Args:
      key:
        The key of the value to be added
      value:
        The value to be added
    """
    position = self._hash(key)
    if self._table[position] == None:
      self._table[position] = List()
    self._table[position].append(Pair(key, value))
    self._size += 1

  def get(self, key: KeyType) -> typing.Any:
    """
    Retrieves the value of the first occurrence of a given key.
    [time complexity: O(n)]
    
    Args:
      key:
        The key of the value to be retrieved
    """
    position = self._hash(key)
    table_slot = self._table[position]
    for pair in table_slot:
      if pair.key == key:
        return pair.value
    raise DataNotFound(key)

  def remove(self, key: KeyType, all_occurrences = False):
    """
    Removes a value from the list based on its key.
    [time complexity: O(n)/O(n)/O(n2)]

    Args:
      key:
        The key of the value to be removed
      all_occurrences:
        If true, removes all occurrences of a given key, else, removes the first one 
    """
    position = self._hash(key)
    if self._table[position] is not None:
      index = 0
      while True:
        try:
          pair = self._table[position].at(index)
          if pair.key == key:
            self._table[position].pop(index)
            self._size -= 1
            if not all_occurrences:
              return
            index = 0
          else:
            index += 1
        except IndexError:
          return

