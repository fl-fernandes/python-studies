import unittest
from findmidnode import LinkedList

class TestFindMidNode(unittest.TestCase):
  def initialize_list(self, size) -> LinkedList:
    l = LinkedList()
    for i in range (0, size):
      l.push(i)
    return l
  
  def test_10_sized_list(self):
    l = self.initialize_list(10)
    
    self.assertEqual(5, l.get_middle().data)

  def test_13_sized_list(self):
    l = self.initialize_list(13)

    self.assertEqual(7, l.get_middle().data)  