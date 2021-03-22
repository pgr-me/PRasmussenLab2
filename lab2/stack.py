"""Peter Rasmussen, Lab 1, stack.py


This module provides Stack, StackUnderflowError, and StackOverflowError classes. The Stack class is
the fundamental data structure of this program, and includes all of the methods specified in that
data structure's ADT. The Stack class is implemented using an array of user-specified size
preallocation. The StackUnderflowError and StackOverflowError classes are custom classes that catch
instances when an empty stack is popped or a full stack is pushed, respectively.  PrefixConverter
class converts a file of newline-delimited prefix expressions, when possible, into their postfix
equivalents.

"""

from typing import Union


class StackUnderflowError(Exception):
    """Exception to capture stack underflow error."""

    pass


class StackOverflowError(Exception):
    """Exception to capture stack overflow error."""

    pass


class Stack:
    """
    This is a traditional stack that includes all required and nice-to-have
    methods from the data structure's ADT, implemented using an array, that has
    a homogenous datatype. The stack accepts strings, integers, floats, lists,
    and booleans, although in this package we only use strings. The class
    includes an additional 1) display method that shows the elements top to
    bottom and 2) to_string method that converts stacks to strings.
    """

    def __init__(self, datatype=str, preallocation=1000):
        """
        Set parameters and initialize stack attributes.
        :param datatype: Data type of each stack element; default is str.
        :param preallocation: Size of stack; default is 1000 elements.
        """
        self.datatype = datatype
        if self.datatype not in [str, int, float, bool, list]:
            raise TypeError("Stack only accepts str, int, float, or bool")
        self.preallocation = preallocation
        self.head: int = -1
        self.size: int = 0
        self.array: list = preallocation * [None]

    def display(self) -> None:
        """
        Print the contents of the stack, from top to bottom.
        :return: None
        """
        cursor = self.size - 1
        print("Top")
        while cursor >= 0:
            print(self.array[cursor])
            cursor -= 1
        print("Bottom")

    def is_empty(self) -> bool:
        """
        Check if stack is empty.
        :return: True if the stack is empty
        """
        return self.head == -1

    def pop(self) -> Union[str, int, float, bool, list]:
        """
        Pop the top element of the stack and return it.
        :return: Popped element
        """
        if self.head == -1:
            raise StackUnderflowError("Tried to pop from empty stack.")
        popped_value = self.array[self.head]
        self.head -= 1
        self.size -= 1
        return popped_value

    def push(self, item: Union[str, int, float, bool, list]) -> None:
        """
        Push an item to the top of the stack.
        :param item: Item to push to the stack
        :return: None
        """
        if type(item) != self.datatype:
            raise TypeError(
                f"Only elements of type {self.datatype} allowed in this stack."
            )
        if self.head == self.preallocation - 1:
            error_message = "Exceeded preallocation of {self.preallocation}"
            raise StackOverflowError(error_message)
        self.head += 1
        self.size += 1
        self.array[self.head] = item
        return None

    def peek(self) -> Union[str, int, float, bool, list]:
        """
        Peek at the top element of the stack.
        :return: Top element of the stack
        """
        if self.head == -1:
            return None
        value = self.pop()
        self.push(value)
        return value

    def to_string(self, top_down: bool = True) -> str:
        """
        Extract contents of stack into string but preserve stack.
        :param top_down: True to return elements top-down; false bottom-up
        :return: String concatenated from contents of stack
        """
        if self.datatype != str:
            raise TypeError("Implementation limited to stacks of strings")
        auxiliary_stack = Stack(datatype=self.datatype)
        string = ""
        while self.size > 0:
            value = self.pop()
            auxiliary_stack.push(value)
            if top_down:
                string += value
        while auxiliary_stack.size > 0:
            value = auxiliary_stack.pop()
            self.push(value)
            if not top_down:
                string += value
        return string
