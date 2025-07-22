import sys
import os
import tempfile
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime
from storage.database_manager import DatabaseManager
from models.user import User
from models.message import Message

class TestStorage(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.db_manager = DatabaseManager(db_file=self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_initialize_empty_database(self):
        """Test creating a new empty database"""
        # Create a new database manager with non-existent file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        os.unlink(temp_file.name)  # Delete the file
        
        db = DatabaseManager(db_file=temp_file.name)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(temp_file.name))
        
        # Check that it contains empty users dict
        with open(temp_file.name, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, {"users": {}})
        
        # Clean up
        os.unlink(temp_file.name)

    def test_add_and_retrieve_user(self):
        """Test adding a user and retrieving it"""
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        retrieved_user = self.db_manager.get_user("testuser")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.password, "testpass")
        self.assertEqual(retrieved_user.user_id, 1)

    def test_save_and_load_data(self):
        """Test that data persists after saving and reloading"""
        # Add a user
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        # Save data
        self.db_manager.save_data()
        
        # Create new database manager instance
        new_db_manager = DatabaseManager(db_file=self.temp_file.name)
        
        # Retrieve user
        retrieved_user = new_db_manager.get_user("testuser")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.password, "testpass")

    def test_send_message(self):
        """Test sending a message between users"""
        # Create users
        sender = User(user_id=1, username="sender", password="pass1")
        receiver = User(user_id=2, username="receiver", password="pass2")
        
        self.db_manager.add_user(sender)
        self.db_manager.add_user(receiver)
        
        # Send message
        result = self.db_manager.send_message(sender, "receiver", "Hello!")
        self.assertTrue(result)
        
        # Check that message was added to receiver's BST
        receiver_user = self.db_manager.get_user("receiver")
        self.assertIsNotNone(receiver_user)
        
        # Check that message was added to unread stack
        unread_messages = self.db_manager.get_unread_messages("receiver")
        self.assertEqual(len(unread_messages), 1)
        self.assertEqual(unread_messages[0].content, "Hello!")
        self.assertEqual(unread_messages[0].sender, "sender")

    def test_send_message_to_nonexistent_user(self):
        """Test sending message to user that doesn't exist"""
        sender = User(user_id=1, username="sender", password="pass1")
        self.db_manager.add_user(sender)
        
        result = self.db_manager.send_message(sender, "nonexistent", "Hello!")
        self.assertFalse(result)

    def test_add_reply_to_message(self):
        """Test adding a reply to an existing message"""
        # Create user and add a message
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        # Send a message first
        self.db_manager.send_message(user, "testuser", "Original message")
        
        # Get the message ID (assuming it's 1 for first message)
        message_id = 1
        
        # Add reply
        result = self.db_manager.add_reply(message_id, "testuser", "This is a reply")
        self.assertTrue(result)
        
        # Verify reply was added
        user_obj = self.db_manager.get_user("testuser")
        message_node = user_obj.messages_bst.search(message_id)
        self.assertIsNotNone(message_node)
        
        replies = message_node.message.replies.get_all_replies()
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0]["content"], "This is a reply")
        self.assertEqual(replies[0]["from"], "testuser")

    def test_add_reply_to_nonexistent_message(self):
        """Test adding reply to message that doesn't exist"""
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        result = self.db_manager.add_reply(999, "testuser", "Reply")
        self.assertFalse(result)

    def test_get_unread_messages(self):
        """Test retrieving unread messages"""
        # Create user and send messages
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        # Send multiple messages
        self.db_manager.send_message(user, "testuser", "Message 1")
        self.db_manager.send_message(user, "testuser", "Message 2")
        self.db_manager.send_message(user, "testuser", "Message 3")
        
        # Get unread messages
        unread = self.db_manager.get_unread_messages("testuser")
        self.assertEqual(len(unread), 3)
        
        # Verify messages are in correct order (stack is LIFO)
        self.assertEqual(unread[0].content, "Message 3")
        self.assertEqual(unread[1].content, "Message 2")
        self.assertEqual(unread[2].content, "Message 1")
        
        # Verify stack is cleared after reading
        unread_again = self.db_manager.get_unread_messages("testuser")
        self.assertEqual(len(unread_again), 0)

    def test_get_unread_messages_for_nonexistent_user(self):
        """Test getting unread messages for user that doesn't exist"""
        unread = self.db_manager.get_unread_messages("nonexistent")
        self.assertEqual(unread, [])

    def test_bst_to_list_conversion(self):
        """Test converting BST to list for storage"""
        # Create a user with messages
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        # Send messages
        self.db_manager.send_message(user, "testuser", "Message 1")
        self.db_manager.send_message(user, "testuser", "Message 2")
        
        # Convert BST to list
        messages_list = []
        self.db_manager._bst_to_list(user.messages_bst.p, messages_list)
        
        # Verify conversion
        self.assertEqual(len(messages_list), 2)
        self.assertIsInstance(messages_list[0], Message)
        self.assertIsInstance(messages_list[1], Message)

    def test_is_in_stack_check(self):
        """Test checking if message exists in stack"""
        # Create a stack with a message
        from data_structure.stack import Stack
        stack = Stack()
        
        message = Message(message_id=1, sender="test", time="2023-01-01", content="test")
        stack.push(message)
        
        # Test message in stack
        result = self.db_manager._is_in_stack(stack, message)
        self.assertTrue(result)
        
        # Test message not in stack
        other_message = Message(message_id=2, sender="test", time="2023-01-01", content="other")
        result = self.db_manager._is_in_stack(stack, other_message)
        self.assertFalse(result)

    def test_generate_message_id(self):
        """Test generating unique message IDs"""
        user = User(user_id=1, username="testuser", password="testpass")
        self.db_manager.add_user(user)
        
        # First message should have ID 1
        id1 = self.db_manager._generate_message_id(user)
        self.assertEqual(id1, 1)
        
        # Send a message
        self.db_manager.send_message(user, "testuser", "Message")
        
        # Next message should have ID 2
        id2 = self.db_manager._generate_message_id(user)
        self.assertEqual(id2, 2)

    def test_multiple_users_and_messages(self):
        """Test complex scenario with multiple users and messages"""
        # Create multiple users
        user1 = User(user_id=1, username="user1", password="pass1")
        user2 = User(user_id=2, username="user2", password="pass2")
        user3 = User(user_id=3, username="user3", password="pass3")
        
        self.db_manager.add_user(user1)
        self.db_manager.add_user(user2)
        self.db_manager.add_user(user3)
        
        # Send messages between users
        self.db_manager.send_message(user1, "user2", "Hello from user1")
        self.db_manager.send_message(user2, "user1", "Hello from user2")
        self.db_manager.send_message(user1, "user3", "Hello from user1 to user3")
        
        # Save and reload
        self.db_manager.save_data()
        new_db_manager = DatabaseManager(db_file=self.temp_file.name)
        
        # Verify all users exist
        self.assertIsNotNone(new_db_manager.get_user("user1"))
        self.assertIsNotNone(new_db_manager.get_user("user2"))
        self.assertIsNotNone(new_db_manager.get_user("user3"))
        
        # Verify messages
        unread_user2 = new_db_manager.get_unread_messages("user2")
        unread_user1 = new_db_manager.get_unread_messages("user1")
        unread_user3 = new_db_manager.get_unread_messages("user3")
        
        self.assertEqual(len(unread_user2), 1)
        self.assertEqual(len(unread_user1), 1)
        self.assertEqual(len(unread_user3), 1)

if __name__ == "__main__":
    unittest.main()

