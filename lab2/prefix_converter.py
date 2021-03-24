"""Peter Rasmussen, Lab 2, prefix_converter.py

This module provides the PrefixConverter and PrefixSyntaxError classes. The PrefixConverter class
converts a file of newline-delimited prefix expressions, when possible, into their postfix
equivalents.

Example output file:
    # Peter Rasmussen, Lab 1
    # Input file: /path/to/required_input.txt
    # Output file: /path/required_output.txt

    Line 1: Prefix: -+ABC, Postfix: AB+C-
    Line 2: Prefix: -A+BC, Postfix: ABC+-
    Line 3: Prefix: /A+BC +C*BA  , Postfix: PrefixSyntaxError('Column 11: Too few operators, ...

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    Complexity outputs
    Function: convert_prefix_input	Time (ns): 10375000	Loops: 3
    Function: convert_prefix_stack	Time (ns): 7775000	Loops: 9
    Function: _convert_prefix_stack	Time (ns): 7190000	Loops: 8

Header statements make up the first four lines of the output file. Prefix processing outputs are
listed line by line thereafter. Each line of prefix output begins with the line number of the
corresponding prefix expression. Then, the original prefix statement is echoed. Finally, the postfix
expression is written. Below the conversion outputs are complexity outputs: time and number of
loops, a crude proxy for space complexity.

Prefix statements with syntax errors are not converted into postfix. Instead, an error
message encapsulated in PrefixSyntaxError object is written to in lieu of a postfix expression.

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
        self.other_symbols = '\n \t'
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
