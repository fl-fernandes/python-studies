import unittest
from linkedlist import List

class LinkedListTests(unittest.TestCase):
  def test_append(self):
    list = List()
    list.append(0)
    list.append(5.5)
    list.append('a string')

    self.assertEqual(0, list.at(0))
    self.assertEqual(5.5, list.at(1))
    self.assertEqual('a string', list.at(2))
    self.assertEqual(3, list.size)

  def test_at(self):
    list = List()
    list.append(1)
    list.append(2)
    list.append(3)

    self.assertEqual(1, list.at(0))
    self.assertEqual(1, list.at(-3))
    self.assertEqual(2, list.at(1))
    self.assertEqual(2, list.at(-2))
    self.assertEqual(3, list.at(2))
    self.assertEqual(3, list.at(-1))

  def test_at_invalid_index(self):
    list = List()
    list.append(1)

    self.assertRaises(IndexError, lambda: list.at(1))
    self.assertRaises(IndexError, lambda: list.at(-2))

  def test_pop(self):
    list = List()
    list.append(1)
    list.append(2)
    list.append(3)
    list.append(4)

    list.pop()
    self.assertEqual(3, list.size)
    self.assertEqual(list.at(0), 1)
    self.assertEqual(list.at(1), 2)
    self.assertEqual(list.at(2), 3)

    list.pop(2)
    self.assertEqual(2, list.size)
    self.assertEqual(list.at(0), 1)
    self.assertEqual(list.at(1), 2)

    list.pop(-2)
    self.assertEqual(1, list.size)
    self.assertEqual(list.at(0), 2)

  def test_pop_invalid_index(self):
    list = List()
    list.append(1)

    self.assertRaises(IndexError, lambda: list.pop(1))
    self.assertRaises(IndexError, lambda: list.pop(-2))
  
  def test_for_each(self):
    list = List()
    list.append(1)
    list.append(2)
    list.append(3)
    global callback_invocations
    global current_index
    callback_invocations = 0
    current_index = 0

    def assert_callback_value(val_index: int, val):
      global callback_invocations
      global current_index
      self.assertEqual(list.at(val_index), val)
      callback_invocations+=1
      current_index+=1

    list.for_each(lambda val, index : assert_callback_value(current_index, val))
    self.assertEqual(list.size, callback_invocations)

  def test_iterator(self):
    list = List()
    list.append(1)
    list.append(2)
    list.append(3)

    index = 0
    for val in list:
      self.assertEqual(list.at(index), val)
      index += 1

if __name__ == '__main__':
  unittest.main()