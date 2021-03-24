"""Peter Rasmussen, Lab 2, prefix_converter.py

This module recursively converts a prefix expression into its postfix equivalent. Since prefix
syntax errors are handled upstream in prefix_preprocessor.py, this script assumes inputs are error-
free.

"""

# standard library imports
from time import time_ns
from typing import Union


class PrefixConverter:
    """
    This class converts one prefix expression into its postfix equivalent.
    Methods are organized top-down: highest-level methods come first, static methods come last.
    """

    def __init__(
        self,
        operand_symbols: str,
        operator_symbols: str,
    ):
        """
        Initialize IO attributes and output file header and define symbol set
        :param operand_symbols: Operand symbols (e.g., a, b, C, D, etc.)
        :param operator_symbols: Operator symbols (e.g., +, -, *, /, $, etc.)
        """
        self.operand_symbols = operand_symbols
        self.operator_symbols = operator_symbols
        self.other_symbols = "\n \t"
        self.n_recursive_calls = 0
        self.start: Union[None, int] = None
        self.stop: Union[None, int] = None
        self.elapsed = 0

    def convert_prefix_to_postfix(self, prefix_str: list) -> list:
        """
        Wrapper function for __convert_prefix_to_postfix to enable complexity measurement.
        :param prefix_str: List of prefix symbols
        :return: List of postfix symbols
        """

        def __convert_prefix_to_postfix(prefix: list) -> list:
            """
            Convert an array of prefix characters to an array of postfix characters.
            :param prefix: List of prefix symbols
            :return: List of postfix symbols
            """
            postfix = []
            while len(prefix) > 0:
                if prefix[0] in self.operator_symbols and len(postfix) == 0:
                    postfix.append(prefix.pop(0))
                elif prefix[0] in self.operator_symbols:
                    self.n_recursive_calls += 1
                    postfix += self.convert_prefix_to_postfix(prefix)
                else:
                    postfix.append(prefix.pop(0))
            op_term = postfix[1] + postfix[2] + postfix[0]
            postfix = [op_term] + postfix[3:]
            return postfix

        self.start = time_ns()
        postfix_str = __convert_prefix_to_postfix(prefix_str)
        self.stop = time_ns()
        self.elapsed = self.stop - self.start
        return postfix_str
