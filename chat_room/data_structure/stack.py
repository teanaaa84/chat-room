from typing import Optional

class Stack_node:  # کتاب
    def __init__(self, value):
        self.value = value  # اسمش
        self.next: Optional['Stack_node'] = None  # کتاب زیریش


class Stack:  # میز
    def __init__(self, top: Optional[Stack_node] = None):
        self.top = top  # بالاترین کتاب

    def push(self, value):
        new_node = Stack_node(value)  # کتاب جدید
        new_node.next = self.top  # این کتاب حدید کتاب قبلیش تاپ استکمونه
        self.top = new_node  # مقدار جدید تاپ استکو بزار این کتاب جدیده ک وارد شده
        return self.top.value

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty!")
        else:
            if self.top is None:
                raise IndexError("stack is empty!")
            value = self.top.value
            self.top = self.top.next
            return value

    def is_empty(self):
        return self.top is None

    def peek(self):
        if self.is_empty():
            return None
        if self.top is None:
            return None
        return self.top.value


# ------------------------test------------------------

# import unittest


# class TestStack(unittest.TestCase):
#     def test_push(self):
#         s = Stack()
#         s.push("hello")
#         s.push("goodbye")
#         self.assertEqual(s.pop(), "goodbye")

#     def test_empty(self):
#         s = Stack()
#         self.assertTrue(s.is_empty())

#     def test_pop_empty(self):
#         s = Stack()
#         with self.assertRaises(IndexError):
#             s.pop()


# if __name__ == "__main__":

#     unittest.main()
