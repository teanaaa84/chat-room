import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structure.link_list import link_list, link_list_node

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.linked_list = link_list()

    def test_empty_linked_list(self):
        """Test empty linked list operations"""
        self.assertIsNone(self.linked_list.head)
        replies = self.linked_list.get_all_replies()
        self.assertIsNone(replies)

    def test_add_single_reply(self):
        """Test adding a single reply"""
        reply = {"from": "user1", "content": "Hello", "time": "2023-01-01"}
        self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0], reply)

    def test_add_multiple_replies(self):
        """Test adding multiple replies"""
        replies_data = [
            {"from": "user1", "content": "First reply", "time": "2023-01-01"},
            {"from": "user2", "content": "Second reply", "time": "2023-01-02"},
            {"from": "user3", "content": "Third reply", "time": "2023-01-03"},
        ]
        
        for reply in replies_data:
            self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), 3)
        
        # Verify all replies are in the list
        for i, reply in enumerate(replies_data):
            self.assertEqual(replies[i], reply)

    def test_linked_list_node_creation(self):
        """Test linked list node creation"""
        reply_data = {"from": "user1", "content": "test"}
        node = link_list_node(reply_data)
        
        self.assertEqual(node.reply, reply_data)
        self.assertIsNone(node.next)

    def test_add_reply_with_different_data_types(self):
        """Test adding replies with different data types"""
        # Test with string
        self.linked_list.add_reply("Simple string reply")
        
        # Test with dictionary
        self.linked_list.add_reply({"key": "value"})
        
        # Test with list
        self.linked_list.add_reply([1, 2, 3])
        
        # Test with None
        self.linked_list.add_reply(None)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), 4)
        self.assertEqual(replies[0], "Simple string reply")
        self.assertEqual(replies[1], {"key": "value"})
        self.assertEqual(replies[2], [1, 2, 3])
        self.assertIsNone(replies[3])

    def test_large_number_of_replies(self):
        """Test adding a large number of replies"""
        num_replies = 100
        
        for i in range(num_replies):
            reply = {"from": f"user{i}", "content": f"Reply {i}", "time": f"2023-01-{i+1:02d}"}
            self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), num_replies)
        
        # Verify all replies are correct
        for i in range(num_replies):
            expected = {"from": f"user{i}", "content": f"Reply {i}", "time": f"2023-01-{i+1:02d}"}
            self.assertEqual(replies[i], expected)

    def test_add_reply_after_getting_replies(self):
        """Test adding replies after getting all replies"""
        # Add initial replies
        self.linked_list.add_reply("First reply")
        self.linked_list.add_reply("Second reply")
        
        # Get replies
        replies1 = self.linked_list.get_all_replies()
        self.assertEqual(len(replies1), 2)
        
        # Add more replies
        self.linked_list.add_reply("Third reply")
        self.linked_list.add_reply("Fourth reply")
        
        # Get replies again
        replies2 = self.linked_list.get_all_replies()
        self.assertEqual(len(replies2), 4)
        self.assertEqual(replies2[0], "First reply")
        self.assertEqual(replies2[1], "Second reply")
        self.assertEqual(replies2[2], "Third reply")
        self.assertEqual(replies2[3], "Fourth reply")

    def test_add_reply_with_complex_objects(self):
        """Test adding replies with complex nested objects"""
        complex_reply = {
            "from": "user1",
            "content": "Complex reply",
            "metadata": {
                "timestamp": "2023-01-01T12:00:00",
                "attachments": ["file1.jpg", "file2.pdf"],
                "tags": ["important", "urgent"]
            },
            "reactions": {
                "like": 5,
                "love": 2,
                "laugh": 1
            }
        }
        
        self.linked_list.add_reply(complex_reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0], complex_reply)
        
        # Verify nested structure
        self.assertEqual(replies[0]["metadata"]["attachments"], ["file1.jpg", "file2.pdf"])
        self.assertEqual(replies[0]["reactions"]["like"], 5)

    def test_add_reply_with_empty_values(self):
        """Test adding replies with empty values"""
        empty_replies = [
            "",
            {},
            [],
            None,
            {"from": "", "content": "", "time": ""}
        ]
        
        for reply in empty_replies:
            self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), len(empty_replies))
        
        for i, reply in enumerate(empty_replies):
            self.assertEqual(replies[i], reply)

    def test_linked_list_structure(self):
        """Test the internal structure of the linked list"""
        # Add replies and verify the chain structure
        self.linked_list.add_reply("First")
        self.linked_list.add_reply("Second")
        self.linked_list.add_reply("Third")
        
        # Verify head exists
        self.assertIsNotNone(self.linked_list.head)
        self.assertEqual(self.linked_list.head.reply, "First")
        
        # Verify second node
        self.assertIsNotNone(self.linked_list.head.next)
        self.assertEqual(self.linked_list.head.next.reply, "Second")
        
        # Verify third node
        self.assertIsNotNone(self.linked_list.head.next.next)
        self.assertEqual(self.linked_list.head.next.next.reply, "Third")
        
        # Verify end of list
        self.assertIsNone(self.linked_list.head.next.next.next)

    def test_get_all_replies_preserves_order(self):
        """Test that get_all_replies preserves the order of addition"""
        replies_data = [
            "First reply",
            "Second reply", 
            "Third reply",
            "Fourth reply",
            "Fifth reply"
        ]
        
        for reply in replies_data:
            self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        
        # Verify order is preserved
        for i, expected_reply in enumerate(replies_data):
            self.assertEqual(replies[i], expected_reply)

    def test_add_reply_with_unicode_content(self):
        """Test adding replies with unicode content"""
        unicode_replies = [
            "Hello 世界",
            "مرحبا بالعالم",
            "Привет мир",
            "नमस्ते दुनिया",
            "こんにちは世界"
        ]
        
        for reply in unicode_replies:
            self.linked_list.add_reply(reply)
        
        replies = self.linked_list.get_all_replies()
        self.assertEqual(len(replies), len(unicode_replies))
        
        for i, reply in enumerate(unicode_replies):
            self.assertEqual(replies[i], reply)

if __name__ == "__main__":
    unittest.main() 