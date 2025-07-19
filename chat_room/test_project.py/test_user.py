import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.user import User
from data_structure.stack import Stack
from data_structure.bst import bst_search

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(user_id=1, username="tina", password="1234")

    def test_user_creation(self):
        self.assertEqual(self.user.user_id, 1)
        self.assertEqual(self.user.username, "tina")
        self.assertEqual(self.user.password, "1234")

    def test_user_has_bst_and_stack(self):
        self.assertIsInstance(self.user.messages_bst, bst_search)
        self.assertIsInstance(self.user.unread_stack, Stack)

    def test_initial_unread_stack_is_empty(self):
        self.assertTrue(self.user.unread_stack.is_empty())

if __name__ == "__main__":
    unittest.main()
