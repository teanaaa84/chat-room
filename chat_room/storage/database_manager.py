import json
import os
from datetime import datetime
from models.user import User
from models.message import Message
from data_structure.hash import HashTable
from data_structure.stack import Stack
import uuid


class DatabaseManager:
    def __init__(self, db_file="messenger_db.json"):
        print("DatabaseManager: Starting initialization...")
        self.db_file = db_file
        self.user_table = HashTable(size=100)  # هش تیبل برای کاربران
        print("DatabaseManager: Loading data...")
        self.load_data()
        print("DatabaseManager: Initialization complete")

    def load_data(self):
        print("DatabaseManager: Checking if database file exists...")
        if not os.path.exists(self.db_file):
            print("DatabaseManager: Database file not found, creating empty database...")
            self._initialize_empty_db()
        
        # Load users from users.json if it exists
        users_file = "users.json"
        if os.path.exists(users_file):
            print("DatabaseManager: Loading users from users.json...")
            try:
                with open(users_file, "r", encoding="utf-8") as f:
                    users_data = json.load(f)
                    for username, user_info in users_data.items():
                        existing_user = self.user_table.get(username)
                        if not existing_user:
                            user = User(
                                user_id=user_info.get("id", str(uuid.uuid4())[:8].upper()),
                                username=username,
                                password="123456"
                            )
                            self.user_table.insert(username, user)
                            print(f"DatabaseManager: Loaded user '{username}' from users.json")
            except Exception as e:
                print(f"DatabaseManager: Error loading users.json: {e}")

        # Check if messenger_db.json is empty
        if os.path.exists(self.db_file):
            print("DatabaseManager: Checking if database file is empty...")
            if os.path.getsize(self.db_file) == 0:
                print("DatabaseManager: Database file is empty, initializing...")
                self._initialize_empty_db()
            else:
                print("DatabaseManager: Loading data from existing database...")
                try:
                    with open(self.db_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for username, user_data in data.get("users", {}).items():
                            user = User(
                                user_id=user_data["user_id"],
                                username=username,
                                password=user_data["password"],
                            )
                            for msg_data in user_data.get("messages", []):
                                message = Message(
                                    message_id=msg_data["id"],
                                    sender=msg_data["from"],
                                    time=msg_data["timestamp"],
                                    content=msg_data["text"],
                                    to=msg_data.get("to")
                                )
                                for reply in msg_data.get("replies") or []:
                                    message.replies.add_reply(reply)
                                # اضافه کردن پیام به BST گیرنده
                                user.messages_bst.insert(message)
                                # اضافه کردن پیام به BST فرستنده (اگر کاربر فرستنده وجود دارد)
                                if message.sender != username:
                                    sender_user = self.user_table.get(message.sender)
                                    if sender_user:
                                        sender_user.messages_bst.insert(message)
                                if msg_data.get("unread", False):
                                    user.unread_stack.push(message)
                            existing_user = self.user_table.get(username)
                            if existing_user:
                                existing_user.messages_bst = user.messages_bst
                                existing_user.unread_stack = user.unread_stack
                            else:
                                self.user_table.insert(username, user)
                except Exception as e:
                    print(f"DatabaseManager: Error loading messenger_db.json: {e}")

    def save_data(self):
        data = {"users": {}}

        # ذخیره کاربران
        for i in range(self.user_table.size):
            node = self.user_table.table[i]
            while node:
                user = node.user
                user_data = {
                    "user_id": user.user_id,
                    "password": user.password,
                    "messages": [],
                }

                # تبدیل BST به لیست برای ذخیره سازی
                messages_list = []
                self._bst_to_list(user.messages_bst.p, messages_list)

                for msg in messages_list:
                    msg_data = {
                        "id": msg.id,
                        "from": msg.sender,
                        "to": user.username,  # نیاز به اصلاح در ساختار Message دارید
                        "text": msg.content,
                        "timestamp": msg.time,
                        "replies": msg.replies.get_all_replies(),
                        "unread": self._is_in_stack(user.unread_stack, msg),
                    }
                    user_data["messages"].append(msg_data)

                data["users"][user.username] = user_data
                node = node.next

        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _initialize_empty_db(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f)

    def _bst_to_list(self, node, result):
        """تبدیل BST به لیست مرتب شده بر اساس زمان"""
        if node:
            self._bst_to_list(node.left, result)
            result.append(node.message)
            self._bst_to_list(node.right, result)

    def _is_in_stack(self, stack, message):
        """بررسی وجود پیام در استک خوانده نشده‌ها"""
        temp = stack.top
        while temp:
            if temp.value.id == message.id:
                return True
            temp = temp.next
        return False

    def load_users_from_json(self, json_file_path):
        """Load users from a specific JSON file"""
        if not os.path.exists(json_file_path):
            print(f"load_users_from_json: File {json_file_path} not found")
            return
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                users_data = json.load(f)
                for username, user_info in users_data.items():
                    # Create user with default password if not exists
                    existing_user = self.user_table.get(username)
                    if not existing_user:
                        user = User(
                            user_id=user_info.get("id", str(uuid.uuid4())[:8].upper()),
                            username=username,
                            password="123456"  # Default password
                        )
                        self.user_table.insert(username, user)
                        print(f"load_users_from_json: Loaded user '{username}' from {json_file_path}")
        except Exception as e:
            print(f"load_users_from_json: Error loading {json_file_path}: {e}")

    def add_user(self, user):
        """اضافه کردن کاربر جدید به سیستم"""
        print(f"add_user: Adding user '{user.username}' to system")
        self.user_table.insert(user.username, user)
        print(f"add_user: User '{user.username}' added to hash table")
        self.save_data()
        print(f"add_user: Data saved to file")

    def get_user(self, username):
        """دریافت کاربر بر اساس نام کاربری"""
        return self.user_table.get(username)

    def send_message(self, sender, receiver_username, content, parent_id=None):
        """ارسال پیام جدید"""
        receiver = self.get_user(receiver_username)
        if not receiver:
            return False

        new_msg = Message(
            message_id=self._generate_message_id(receiver),
            sender=sender.username,
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
            to=receiver_username,  # Store receiver
            parent_id=parent_id
        )

        # اضافه به BST گیرنده
        receiver.messages_bst.insert(new_msg)

        # اضافه به استک خوانده نشده‌های گیرنده
        receiver.unread_stack.push(new_msg)

        # اضافه به BST فرستنده هم (برای نمایش در چت)
        sender.messages_bst.insert(new_msg)

        self.save_data()
        return True

    def _generate_message_id(self, user):
        """تولید شناسه منحصربفرد برای پیام"""
        max_id = 0
        # نیاز به پیاده‌سازی تابع برای پیدا کردن ماکزیمم ID در BST
        # این یک پیاده‌سازی ساده است
        messages = []
        self._bst_to_list(user.messages_bst.p, messages)
        for msg in messages:
            if msg.id > max_id:
                max_id = msg.id
        return max_id + 1

    def add_reply(self, message_id, username, reply_content):
        """اضافه کردن پاسخ به یک پیام"""
        user = self.get_user(username)
        if not user:
            return False

        # جستجوی پیام در BST
        message_node = user.messages_bst.search(message_id)
        if not message_node:
            return False

        # اضافه کردن پاسخ
        message_node.message.replies.add_reply(
            {
                "from": username,
                "content": reply_content,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        self.save_data()
        return True

    def get_unread_messages(self, username):
        """دریافت پیام‌های خوانده نشده"""
        user = self.get_user(username)
        if not user:
            return []

        unread = []
        temp = user.unread_stack.top
        while temp:
            unread.append(temp.value)
            temp = temp.next

        # پاک کردن استک پس از خوانده شدن
        user.unread_stack = Stack()
        self.save_data()

        return unread
