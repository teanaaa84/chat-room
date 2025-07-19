class Stack_node:#کتاب
    def __init__(self, value):
        self.value = value#اسمش
        self.next = None   #کتاب زیریش


class Stack:#میز
    def __init__(self, top=None):
        self.top = top#بالاترین کتاب

    def push(self, value):
        new_node = Stack_node(value) #کتاب جدید 
        new_node.next = self.top #این کتاب حدید کتاب قبلیش تاپ استکمونه 
        self.top = new_node #مقدار جدید تاپ استکو بزار این کتاب جدیده ک وارد شده
        return self.top

    def pop(self):
        if self.is_empty():
            return None
        value=self.top.value
        self.top=self.top.next

        return value

    def is_empty(self):
        if self.top==None:
            return True
        else:
            return False
        

    def peek(self):
        if self.is_empty():
            return None
        return self.top.value

# Usage
stack = Stack()
stack.push(1)
stack.push(2)
print (stack.peek())
print(stack.is_empty())
print(stack.pop())