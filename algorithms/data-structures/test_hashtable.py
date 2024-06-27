import unittest
from hashtable import HashTable, DataNotFound

class HashTableTest(unittest.TestCase):
  def test_hash_function(self):
    table = HashTable(5)
    
    self.assertEqual(1, table._hash(1))
    self.assertEqual(0, table._hash(-10))
    self.assertEqual(2, table._hash(2))
    self.assertEqual(2, table._hash(7))
    self.assertEqual(4, table._hash(29))

  def test_add_get(self):
    table = HashTable(2)

    table.add(0, 'a str')
    table.add(1, 12)
    table.add(-44, 13.3)
    table.add(13, {'a': 'dict'})

    self.assertEqual('a str', table.get(0))
    self.assertEqual(12, table.get(1))
    self.assertEqual(13.3, table.get(-44))
    self.assertEqual({'a': 'dict'}, table.get(13))
    self.assertRaises(DataNotFound, lambda: table.get(-1))
    self.assertEqual(4, table.size)

  def test_delete(self):
    table = HashTable(10)

    table.add(0, 'a str')
    table.add(1, 12)
    table.remove(1)

    self.assertEqual('a str', table.get(0))
    self.assertRaises(DataNotFound, lambda: table.get(1))
    self.assertEqual(1, table.size)

  def test_delete_all_occurrences(self):
    table = HashTable(10)

    table.add(0, 'a str')
    table.add(1, 12)
    table.add(0, 8)
    table.add(0, .9)

    # all_occurrences = False

    table.remove(0)
    self.assertEqual(8, table.get(0))
    self.assertEqual(3, table.size)

    # all_occurrences = True

    table.remove(0, True)
    self.assertRaises(DataNotFound, lambda: table.get(0))
    self.assertEqual(1, table.size)
    