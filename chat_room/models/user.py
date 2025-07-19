from data_structure.bst import bst_search
from data_structure.stack import  Stack

class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.messages_bst = bst_search()  # برای جستجوی سریع پیام‌ها
        self.unread_stack = Stack()  # پیام‌های خوانده نشده

    def send_message(self, content, time):
        msg_id = len(self.messages) + 1
        msg = Message(msg_id, self.username, time, content)
        self.messages.append(msg)
        return msg

    def get_all_messages(self):
        return self.messages
