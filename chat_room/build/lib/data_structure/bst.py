import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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


#test
# مرحله 1: ساخت درخت و وارد کردن پیام‌ها
tree = bst_search()
tree.insert(Message(10, "Ali", "hello", 1))
tree.insert(Message(5, "Sara", "how are you", 2))
tree.insert(Message(15, "Reza", "what", 3))
tree.insert(Message(3, "Mina", "fuck", 4))
tree.insert(Message(7, "Nima", "you", 5))

# مرحله 2: جستجوی پیام با ID = 5
result = tree.search(5)
print("🔍 find ID=5:")
if result:
    print(f"founded: {result.message.content}")
else:
    print("not founded")

# مرحله 3: حذف پیام با ID = 5
tree.p = tree.delete(tree.p, 5)

# مرحله 4: پیمایش inorder درخت
print("\n🌲(in-order traversal):")
tree.traverse(tree.p)