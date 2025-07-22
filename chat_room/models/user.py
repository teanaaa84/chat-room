from data_structure.bst import bst_search
from data_structure.stack import Stack
from models.message import Message

class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.messages_bst = bst_search()  # برای جستجوی سریع پیام‌ها
        self.unread_stack = Stack()  # پیام‌های خوانده نشده

    def send_message(self, content, time):
        msg_id = self._generate_message_id()
        msg = Message(msg_id, self.username, time, content)
        self.messages_bst.insert(msg)
        return msg

    def get_all_messages(self):
        messages = []
        self._bst_to_list(self.messages_bst.p, messages)
        return messages
    
    def _generate_message_id(self):
        """Generate unique message ID"""
        messages = []
        self._bst_to_list(self.messages_bst.p, messages)
        max_id = 0
        for msg in messages:
            if msg.id > max_id:
                max_id = msg.id
        return max_id + 1
    
    def _bst_to_list(self, node, result):
        """Convert BST to list for processing"""
        if node:
            self._bst_to_list(node.left, result)
            result.append(node.message)
            self._bst_to_list(node.right, result)
