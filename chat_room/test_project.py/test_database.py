import unittest
import os
from database_manager import DatabaseManager
from models.user import User

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.test_db_file = "test_database.json"
        self.db_manager = DatabaseManager(db_file=self.test_db_file)

        self.sample_user = User(
            user_id=1,
            username="testuser",
            password="testpass"
        )

    def tearDown(self):
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_add_and_get_user(self):
        self.db_manager.add_user(self.sample_user)
        user = self.db_manager.get_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "testpass")

    def test_save_and_load(self):
        self.db_manager.add_user(self.sample_user)
        self.db_manager.save_data()

        # ساخت نمونه جدید برای بارگذاری مجدد
        new_db_manager = DatabaseManager(db_file=self.test_db_file)
        user = new_db_manager.get_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "testpass")

if __name__ == "__main__":
    unittest.main()
