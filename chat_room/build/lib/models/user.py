from models.message import Message

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id        # شناسه یکتا برای هش‌تیبل
        self.username = username      # نام نمایشی
        self.messages = []            # پیام‌هایی که این کاربر فرستاده

    def send_message(self, content, time):
        msg_id = len(self.messages) + 1
        msg = Message(msg_id, self.username, time, content)
        self.messages.append(msg)
        return msg

    def get_all_messages(self):
        return self.messages
