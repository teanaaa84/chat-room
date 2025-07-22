import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from data_structure.hash import HashTable, HashTableNode

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable(size=10)

    def test_hash_function(self):
        """Test hash function returns valid indices"""
        indices = set()
        for i in range(100):
            index = self.hash_table.hash_function(f"key{i}")
            self.assertGreaterEqual(index, 0)
            self.assertLess(index, self.hash_table.size)
            indices.add(index)
        
        # Test that hash function distributes keys across the table
        self.assertGreater(len(indices), 1)

    def test_insert_and_get(self):
        """Test basic insert and get operations"""
        # Test single insertion
        self.hash_table.insert("user1", "value1")
        result = self.hash_table.get("user1")
        self.assertEqual(result, "value1")

        # Test multiple insertions
        self.hash_table.insert("user2", "value2")
        self.hash_table.insert("user3", "value3")
        
        self.assertEqual(self.hash_table.get("user2"), "value2")
        self.assertEqual(self.hash_table.get("user3"), "value3")

    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist"""
        result = self.hash_table.get("nonexistent")
        self.assertIsNone(result)

    def test_collision_handling(self):
        """Test that collisions are handled correctly using chaining"""
        # Create a small table to force collisions
        small_table = HashTable(size=1)
        
        small_table.insert("key1", "value1")
        small_table.insert("key2", "value2")
        small_table.insert("key3", "value3")
        
        # All should be retrievable despite collisions
        self.assertEqual(small_table.get("key1"), "value1")
        self.assertEqual(small_table.get("key2"), "value2")
        self.assertEqual(small_table.get("key3"), "value3")

    def test_update_existing_key(self):
        """Test updating an existing key"""
        self.hash_table.insert("user1", "old_value")
        self.hash_table.insert("user1", "new_value")
        
        result = self.hash_table.get("user1")
        self.assertEqual(result, "new_value")

    def test_delete_existing_key(self):
        """Test deleting an existing key"""
        self.hash_table.insert("user1", "value1")
        self.hash_table.insert("user2", "value2")
        
        # Delete user1
        result = self.hash_table.delete("user1")
        self.assertTrue(result)
        
        # Verify user1 is gone but user2 remains
        self.assertIsNone(self.hash_table.get("user1"))
        self.assertEqual(self.hash_table.get("user2"), "value2")

    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist"""
        result = self.hash_table.delete("nonexistent")
        self.assertFalse(result)

    def test_delete_with_collisions(self):
        """Test deleting keys when there are collisions"""
        small_table = HashTable(size=1)
        
        small_table.insert("key1", "value1")
        small_table.insert("key2", "value2")
        small_table.insert("key3", "value3")
        
        # Delete middle key in chain
        result = small_table.delete("key2")
        self.assertTrue(result)
        
        # Verify key2 is gone but others remain
        self.assertIsNone(small_table.get("key2"))
        self.assertEqual(small_table.get("key1"), "value1")
        self.assertEqual(small_table.get("key3"), "value3")

    def test_delete_first_in_chain(self):
        """Test deleting the first key in a collision chain"""
        small_table = HashTable(size=1)
        
        small_table.insert("key1", "value1")
        small_table.insert("key2", "value2")
        
        # Delete first key
        result = small_table.delete("key1")
        self.assertTrue(result)
        
        # Verify key1 is gone but key2 remains
        self.assertIsNone(small_table.get("key1"))
        self.assertEqual(small_table.get("key2"), "value2")

    def test_delete_last_in_chain(self):
        """Test deleting the last key in a collision chain"""
        small_table = HashTable(size=1)
        
        small_table.insert("key1", "value1")
        small_table.insert("key2", "value2")
        
        # Delete last key
        result = small_table.delete("key2")
        self.assertTrue(result)
        
        # Verify key2 is gone but key1 remains
        self.assertIsNone(small_table.get("key2"))
        self.assertEqual(small_table.get("key1"), "value1")

    def test_large_number_of_insertions(self):
        """Test handling a large number of insertions"""
        for i in range(100):
            self.hash_table.insert(f"user{i}", f"value{i}")
        
        # Verify all can be retrieved
        for i in range(100):
            result = self.hash_table.get(f"user{i}")
            self.assertEqual(result, f"value{i}")

    def test_hash_table_node_creation(self):
        """Test HashTableNode creation"""
        node = HashTableNode("key", "value")
        self.assertEqual(node.key, "key")
        self.assertEqual(node.user, "value")
        self.assertIsNone(node.next)

if __name__ == "__main__":
    unittest.main()

