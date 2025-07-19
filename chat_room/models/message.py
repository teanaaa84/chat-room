from data_structure.link_list import link_list
from data_structure.stack import Stack


class Message:
    def __init__(self, message_id, sender, time, content):
        self.id = message_id
        self.sender = sender
        self.time = time
        self.content = content
        self.replies = link_list()  # برای پاسخ‌ها
        self.stack_node = None  # برای نمایش در استک
