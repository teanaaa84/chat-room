import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models.user import User
from data_structure.hash import HashTable

class MockRegisterLogic:
    def __init__(self):
        self.user_table = HashTable()

    def signup(self, username, password, confirm):
        if password != confirm:
            return "Passwords do not match"
        if self.user_table.get(username) is not None:
            return "User already exists"
        user = User(user_id=1, username=username, password=password)
        self.user_table.insert(username, user)
        return "Success"

    def login(self, username, password):
        user = self.user_table.get(username)
        if user and user.password == password:
            return "Login success"
        return "Invalid username or password"

class TestRegisterLogic(unittest.TestCase):
    def setUp(self):
        self.logic = MockRegisterLogic()

    def test_signup_success(self):
        result = self.logic.signup("tina", "1234", "1234")
        self.assertEqual(result, "Success")

    def test_signup_password_mismatch(self):
        result = self.logic.signup("tina", "1234", "4321")
        self.assertEqual(result, "Passwords do not match")

    def test_signup_duplicate_username(self):
        self.logic.signup("tina", "1234", "1234")
        result = self.logic.signup("tina", "5678", "5678")
        self.assertEqual(result, "User already exists")

    def test_login_success(self):
        self.logic.signup("tina", "1234", "1234")
        result = self.logic.login("tina", "1234")
        self.assertEqual(result, "Login success")

    def test_login_fail_wrong_password(self):
        self.logic.signup("tina", "1234", "1234")
        result = self.logic.login("tina", "wrong")
        self.assertEqual(result, "Invalid username or password")

    def test_login_fail_user_not_found(self):
        result = self.logic.login("unknown", "1234")
        self.assertEqual(result, "Invalid username or password")

if __name__ == "__main__":
    unittest.main()
