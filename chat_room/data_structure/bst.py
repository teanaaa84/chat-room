from models.message import Message


class bst_node:
    def __init__(self, message):
        self.message = message
        self.left = None
        self.right = None


class bst_search:
    def __init__(self):
        self.p = None

    def insert(self, message):
        if self.p is None:
            self.p = bst_node(message)
            return
        current = self.p
        while True:
            if message.id < current.message.id:
                if current.left is None:
                    current.left = bst_node(message)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = bst_node(message)
                    return
                current = current.right

    def search(self, message_id):
        current = self.p
        while current is not None:
            if message_id == current.message.id:
                return current
            elif message_id < current.message.id:
                current = current.left
            else:
                current = current.right
        return None

    def min_bst(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, node, message_id):
        if node is None:
            return node
        if message_id < node.message.id:
            node.left = self.delete(node.left, message_id)
        elif message_id > node.message.id:
            node.right = self.delete(node.right, message_id)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self.min_bst(node.right)
            node.message = temp.message
            node.right = self.delete(node.right, temp.message.id)
        return node

    def traverse(self, node):
        if node:
            self.traverse(node.left)
            print(node.message.content)
            self.traverse(node.right)

# ------------------------test------------------------

# import unittest, random, datetime

# class TestBst(unittest.TestCase):
#     def test_insert_and_search(self):
#         bst = bst_search()

#         msg1 = Message(
#             random.randint(1, 10000), "ali_yasini", datetime.datetime.now(), "hello"
#         )
#         msg2 = Message(
#             random.randint(1, 10000), "masoud", datetime.datetime.now(), "salam"
#         )
#         msg3 = Message(
#             random.randint(1, 10000), "tiniii", datetime.datetime.now(), "hi"
#         )

#         # Insert messages
#         bst.insert(msg1)
#         bst.insert(msg2)
#         bst.insert(msg3)

#         # Search each message by ID
#         self.assertEqual(bst.search(msg1.id).message.content, msg1.content)
#         self.assertEqual(bst.search(msg2.id).message.content, msg2.content)
#         self.assertEqual(bst.search(msg3.id).message.content, msg3.content)

#     def test_min(self):
#         bst = bst_search()
#         msgs = [
#             Message(10, "user1", datetime.datetime.now(), "msg1"),
#             Message(5, "user2", datetime.datetime.now(), "msg2"),
#             Message(15, "user3", datetime.datetime.now(), "msg3"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)
#         min_node = bst.min_bst(bst.p)
#         self.assertEqual(min_node.message.id, 5)

#     def test_delete(self):
#         bst = bst_search()
#         msgs = [
#             Message(10, "user1", datetime.datetime.now(), "msg1"),
#             Message(5, "user2", datetime.datetime.now(), "msg2"),
#             Message(15, "user3", datetime.datetime.now(), "msg3"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)

#         bst.p = bst.delete(bst.p, 10)  # حذف ریشه
#         self.assertIsNone(bst.search(10))
#         self.assertIsNotNone(bst.search(5))
#         self.assertIsNotNone(bst.search(15))

#     def test_traverse(self):
#         bst = bst_search()
#         msgs = [
#             Message(10, "user1", datetime.datetime.now(), "msg1"),
#             Message(5, "user2", datetime.datetime.now(), "msg2"),
#             Message(15, "user3", datetime.datetime.now(), "msg3"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)
#         # برای تست traverse می‌توانیم خروجی را به لیست جمع کنیم:
#         result = []

#         def collect(node):
#             if node:
#                 collect(node.left)
#                 result.append(node.message.content)
#                 collect(node.right)

#         collect(bst.p)
#         self.assertEqual(result, ["msg2", "msg1", "msg3"])

#     def test_insert_duplicate_id(self):
#         bst = bst_search()
#         now = datetime.datetime.now()
#         msg1 = Message(50, "a", now, "hello")
#         msg2 = Message(50, "b", now, "again")  # same id as msg1

#         bst.insert(msg1)
#         bst.insert(msg2)

#         result = bst.search(50)
#         self.assertEqual(result.message.content, "hello")  # یا maybe "again"!

#     def test_delete_nonexistent_id(self):
#         bst = bst_search()
#         msg = Message(10, "user", datetime.datetime.now(), "hi")
#         bst.insert(msg)

#         before = bst.search(10)
#         bst.p = bst.delete(bst.p, 999)  # id وجود نداره
#         after = bst.search(10)

#         self.assertEqual(before.message.content, after.message.content)

#     def test_delete_node_with_two_children(self):
#         bst = bst_search()
#         msgs = [
#             Message(50, "root", datetime.datetime.now(), "middle"),
#             Message(30, "left", datetime.datetime.now(), "left"),
#             Message(70, "right", datetime.datetime.now(), "right"),
#             Message(60, "r-left", datetime.datetime.now(), "r-left"),
#             Message(80, "r-right", datetime.datetime.now(), "r-right"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)

#         # حذف گره 70 که دو فرزند دارد
#         bst.p = bst.delete(bst.p, 70)

#         self.assertIsNone(bst.search(70))  # مطمئن شو حذف شده
#         self.assertIsNotNone(bst.search(60))  # فرزند چپش هنوز هست
#         self.assertIsNotNone(bst.search(80))  # فرزند راستش هم هست

#     def test_traverse_inorder_sorted_output(self):
#         bst = bst_search()
#         msgs = [
#             Message(30, "user", datetime.datetime.now(), "msg30"),
#             Message(10, "user", datetime.datetime.now(), "msg10"),
#             Message(40, "user", datetime.datetime.now(), "msg40"),
#             Message(20, "user", datetime.datetime.now(), "msg20"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)

#         result = []

#         def collect(node):
#             if node:
#                 collect(node.left)
#                 result.append(node.message.id)
#                 collect(node.right)

#         collect(bst.p)

#         self.assertEqual(result, sorted(result))

#     def test_search_existing_and_missing_messages(self):
#         bst = bst_search()
#         msg1 = Message(1, "a", datetime.datetime.now(), "hi")
#         bst.insert(msg1)

#         self.assertIsNotNone(bst.search(1))  # موجود
#         self.assertIsNone(bst.search(9999))  # ناموجود

#     def test_empty_tree(self):
#         bst = bst_search()
#         self.assertIsNone(bst.search(1))
#         self.assertIsNone(bst.p)
#         bst.p = bst.delete(bst.p, 1)
#         self.assertIsNone(bst.p)

#     def test_delete_all_nodes(self):
#         bst = bst_search()
#         msgs = [
#             Message(10, "u", datetime.datetime.now(), "1"),
#             Message(5, "u", datetime.datetime.now(), "2"),
#             Message(15, "u", datetime.datetime.now(), "3"),
#         ]
#         for msg in msgs:
#             bst.insert(msg)

#         for msg in msgs:
#             bst.p = bst.delete(bst.p, msg.id)

#         for msg in msgs:
#             self.assertIsNone(bst.search(msg.id))

#         self.assertIsNone(bst.p)  # ریشه هم باید None شده باشه


# if __name__ == "__main__":
#     unittest.main()
