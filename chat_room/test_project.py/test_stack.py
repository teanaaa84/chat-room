import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structure.stack import Stack, Stack_node

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_empty_stack(self):
        """Test empty stack operations"""
        self.assertTrue(self.stack.is_empty())
        self.assertIsNone(self.stack.peek())
        
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_push_single_element(self):
        """Test pushing a single element"""
        self.stack.push("test")
        
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.peek(), "test")

    def test_push_multiple_elements(self):
        """Test pushing multiple elements"""
        elements = ["first", "second", "third", "fourth"]
        
        for element in elements:
            self.stack.push(element)
        
        # Stack should have all elements
        self.assertFalse(self.stack.is_empty())
        
        # Peek should return the last pushed element
        self.assertEqual(self.stack.peek(), "fourth")

    def test_pop_single_element(self):
        """Test popping a single element"""
        self.stack.push("test")
        result = self.stack.pop()
        
        self.assertEqual(result, "test")
        self.assertTrue(self.stack.is_empty())

    def test_pop_multiple_elements(self):
        """Test popping multiple elements (LIFO order)"""
        elements = ["first", "second", "third"]
        
        for element in elements:
            self.stack.push(element)
        
        # Pop in reverse order (LIFO)
        for element in reversed(elements):
            result = self.stack.pop()
            self.assertEqual(result, element)
        
        # Stack should be empty
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_stack(self):
        """Test popping from empty stack raises exception"""
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_does_not_remove(self):
        """Test that peek doesn't remove elements"""
        self.stack.push("test")
        
        # Peek multiple times
        self.assertEqual(self.stack.peek(), "test")
        self.assertEqual(self.stack.peek(), "test")
        self.assertEqual(self.stack.peek(), "test")
        
        # Element should still be there
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.pop(), "test")

    def test_push_pop_sequence(self):
        """Test alternating push and pop operations"""
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(self.stack.pop(), "b")
        self.stack.push("c")
        self.assertEqual(self.stack.pop(), "c")
        self.assertEqual(self.stack.pop(), "a")
        self.assertTrue(self.stack.is_empty())

    def test_stack_with_different_data_types(self):
        """Test stack with different data types"""
        # Test with integers
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        
        # Test with lists
        self.stack.push([1, 2, 3])
        self.stack.push([4, 5, 6])
        self.assertEqual(self.stack.pop(), [4, 5, 6])
        self.assertEqual(self.stack.pop(), [1, 2, 3])
        
        # Test with None
        self.stack.push(None)
        self.assertIsNone(self.stack.pop())

    def test_stack_node_creation(self):
        """Test Stack_node creation"""
        node = Stack_node("test_value")
        
        self.assertEqual(node.value, "test_value")
        self.assertIsNone(node.next)

    def test_stack_with_custom_objects(self):
        """Test stack with custom objects"""
        class TestObject:
            def __init__(self, name, value):
                self.name = name
                self.value = value
            
            def __eq__(self, other):
                return self.name == other.name and self.value == other.value
        
        obj1 = TestObject("obj1", 1)
        obj2 = TestObject("obj2", 2)
        
        self.stack.push(obj1)
        self.stack.push(obj2)
        
        self.assertEqual(self.stack.pop(), obj2)
        self.assertEqual(self.stack.pop(), obj1)

    def test_large_number_of_elements(self):
        """Test stack with a large number of elements"""
        num_elements = 1000
        
        # Push many elements
        for i in range(num_elements):
            self.stack.push(f"element_{i}")
        
        # Verify all can be popped
        for i in range(num_elements - 1, -1, -1):
            result = self.stack.pop()
            self.assertEqual(result, f"element_{i}")
        
        self.assertTrue(self.stack.is_empty())

    def test_stack_initialization_with_top(self):
        """Test stack initialization with existing top node"""
        # Create a node
        node = Stack_node("initial")
        
        # Create stack with this node as top
        stack_with_top = Stack(top=node)
        
        self.assertFalse(stack_with_top.is_empty())
        self.assertEqual(stack_with_top.peek(), "initial")
        self.assertEqual(stack_with_top.pop(), "initial")
        self.assertTrue(stack_with_top.is_empty())

    def test_return_value_of_push(self):
        """Test that push returns the pushed value"""
        result = self.stack.push("test_value")
        self.assertEqual(result, "test_value")

    def test_stack_after_clear_operations(self):
        """Test stack behavior after clearing all elements"""
        # Add elements
        self.stack.push("a")
        self.stack.push("b")
        self.stack.push("c")
        
        # Clear by popping all
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        
        # Stack should be empty
        self.assertTrue(self.stack.is_empty())
        self.assertIsNone(self.stack.peek())
        
        # Should be able to add new elements
        self.stack.push("new")
        self.assertEqual(self.stack.peek(), "new")

if __name__ == "__main__":
    unittest.main() 