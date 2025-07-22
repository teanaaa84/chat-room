import sys
import os
import unittest
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structure.bst import bst_search, bst_node
from models.message import Message

class TestBST(unittest.TestCase):
    def setUp(self):
        self.bst = bst_search()
        self.now = datetime.now()

    def test_empty_bst(self):
        """Test empty BST operations"""
        self.assertIsNone(self.bst.p)
        self.assertIsNone(self.bst.search(1))
        self.assertIsNone(self.bst.min_bst(None))

    def test_insert_single_node(self):
        """Test inserting a single node"""
        message = Message(1, "user1", self.now, "Hello")
        self.bst.insert(message)
        
        self.assertIsNotNone(self.bst.p)
        self.assertEqual(self.bst.p.message.id, 1)
        self.assertEqual(self.bst.p.message.content, "Hello")

    def test_insert_multiple_nodes(self):
        """Test inserting multiple nodes"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
            Message(3, "user4", self.now, "Message 3"),
            Message(7, "user5", self.now, "Message 7"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Verify all messages can be found
        for msg in messages:
            found = self.bst.search(msg.id)
            self.assertIsNotNone(found)
            self.assertEqual(found.message.content, msg.content)

    def test_search_existing_node(self):
        """Test searching for existing nodes"""
        message = Message(5, "user1", self.now, "Test message")
        self.bst.insert(message)
        
        found = self.bst.search(5)
        self.assertIsNotNone(found)
        self.assertEqual(found.message.content, "Test message")

    def test_search_nonexistent_node(self):
        """Test searching for non-existent nodes"""
        message = Message(5, "user1", self.now, "Test message")
        self.bst.insert(message)
        
        found = self.bst.search(10)
        self.assertIsNone(found)

    def test_min_bst(self):
        """Test finding minimum value in BST"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
            Message(3, "user4", self.now, "Message 3"),
            Message(7, "user5", self.now, "Message 7"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        min_node = self.bst.min_bst(self.bst.p)
        self.assertEqual(min_node.message.id, 3)

    def test_min_bst_empty(self):
        """Test min_bst with empty tree"""
        min_node = self.bst.min_bst(None)
        self.assertIsNone(min_node)

    def test_delete_leaf_node(self):
        """Test deleting a leaf node"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Delete leaf node (5)
        self.bst.p = self.bst.delete(self.bst.p, 5)
        
        # Verify deletion
        self.assertIsNone(self.bst.search(5))
        self.assertIsNotNone(self.bst.search(10))
        self.assertIsNotNone(self.bst.search(15))

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Delete node with one child (10)
        self.bst.p = self.bst.delete(self.bst.p, 10)
        
        # Verify deletion
        self.assertIsNone(self.bst.search(10))
        self.assertIsNotNone(self.bst.search(5))

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
            Message(12, "user4", self.now, "Message 12"),
            Message(18, "user5", self.now, "Message 18"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Delete root node (10)
        self.bst.p = self.bst.delete(self.bst.p, 10)
        
        # Verify deletion
        self.assertIsNone(self.bst.search(10))
        # Verify other nodes still exist
        for msg in [5, 15, 12, 18]:
            self.assertIsNotNone(self.bst.search(msg))

    def test_delete_nonexistent_node(self):
        """Test deleting a non-existent node"""
        message = Message(5, "user1", self.now, "Test message")
        self.bst.insert(message)
        
        # Try to delete non-existent node
        original_root = self.bst.p
        self.bst.p = self.bst.delete(self.bst.p, 10)
        
        # Tree should remain unchanged
        self.assertEqual(self.bst.p, original_root)

    def test_delete_all_nodes(self):
        """Test deleting all nodes from the tree"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Delete all nodes
        for msg in messages:
            self.bst.p = self.bst.delete(self.bst.p, msg.id)
        
        # Tree should be empty
        self.assertIsNone(self.bst.p)

    def test_traverse_inorder(self):
        """Test inorder traversal"""
        messages = [
            Message(10, "user1", self.now, "Message 10"),
            Message(5, "user2", self.now, "Message 5"),
            Message(15, "user3", self.now, "Message 15"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Collect traversal results
        result = []
        def collect_content(node):
            if node:
                collect_content(node.left)
                result.append(node.message.content)
                collect_content(node.right)
        
        collect_content(self.bst.p)
        
        # Should be in sorted order
        expected = ["Message 5", "Message 10", "Message 15"]
        self.assertEqual(result, expected)

    def test_insert_duplicate_ids(self):
        """Test inserting messages with duplicate IDs"""
        message1 = Message(5, "user1", self.now, "First message")
        message2 = Message(5, "user2", self.now, "Second message")
        
        self.bst.insert(message1)
        self.bst.insert(message2)
        
        # Should find the first message inserted
        found = self.bst.search(5)
        self.assertEqual(found.message.content, "First message")

    def test_bst_structure_after_insertions(self):
        """Test that BST maintains proper structure after insertions"""
        messages = [
            Message(8, "user1", self.now, "Root"),
            Message(4, "user2", self.now, "Left"),
            Message(12, "user3", self.now, "Right"),
            Message(2, "user4", self.now, "Left-Left"),
            Message(6, "user5", self.now, "Left-Right"),
            Message(10, "user6", self.now, "Right-Left"),
            Message(14, "user7", self.now, "Right-Right"),
        ]
        
        for msg in messages:
            self.bst.insert(msg)
        
        # Verify root
        self.assertEqual(self.bst.p.message.id, 8)
        
        # Verify left subtree
        self.assertEqual(self.bst.p.left.message.id, 4)
        self.assertEqual(self.bst.p.left.left.message.id, 2)
        self.assertEqual(self.bst.p.left.right.message.id, 6)
        
        # Verify right subtree
        self.assertEqual(self.bst.p.right.message.id, 12)
        self.assertEqual(self.bst.p.right.left.message.id, 10)
        self.assertEqual(self.bst.p.right.right.message.id, 14)

    def test_bst_node_creation(self):
        """Test BST node creation"""
        message = Message(1, "user1", self.now, "Test")
        node = bst_node(message)
        
        self.assertEqual(node.message, message)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

if __name__ == "__main__":
    unittest.main() 