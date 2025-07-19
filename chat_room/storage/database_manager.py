import json
import os
from datetime import datetime
from models.user import User
from models.message import Message
from data_structure.hash import HashTable


class DatabaseManager:
    def __init__(self, db_file="messenger_db.json"):
        self.db_file = db_file
        self.user_table = HashTable(size=100)  # هش تیبل برای کاربران
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.db_file):
            self._initialize_empty_db()
            return

        with open(self.db_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            # بارگیری کاربران
            for username, user_data in data.get("users", {}).items():
                user = User(
                    user_id=user_data["user_id"],
                    username=username,
                    password=user_data["password"],
                )

                # بارگیری پیام‌های کاربر
                for msg_data in user_data.get("messages", []):
                    message = Message(
                        message_id=msg_data["id"],
                        sender=msg_data["from"],
                        time=msg_data["timestamp"],
                        content=msg_data["text"],
                    )

                    # بارگیری پاسخ‌ها
                    for reply in msg_data.get("replies", []):
                        message.replies.add_reply(reply)

                    # اضافه کردن پیام به BST کاربر
                    user.messages_bst.insert(message)

                    # اضافه کردن به استک پیام‌های خوانده نشده اگر لازم باشد
                    if msg_data.get("unread", False):
                        user.unread_stack.push(message)

                self.user_table.insert(username, user)

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

    def add_user(self, user):
        """اضافه کردن کاربر جدید به سیستم"""
        self.user_table.insert(user.username, user)
        self.save_data()

    def get_user(self, username):
        """دریافت کاربر بر اساس نام کاربری"""
        return self.user_table.get(username)

    def send_message(self, sender, receiver_username, content):
        """ارسال پیام جدید"""
        receiver = self.get_user(receiver_username)
        if not receiver:
            return False

        new_msg = Message(
            message_id=self._generate_message_id(receiver),
            sender=sender.username,
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
        )

        # اضافه به BST گیرنده
        receiver.messages_bst.insert(new_msg)

        # اضافه به استک خوانده نشده‌های گیرنده
        receiver.unread_stack.push(new_msg)

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
