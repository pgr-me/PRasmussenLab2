"""Peter Rasmussen, Lab 2, symbols.py

This module provides the Symbols class, which bundles operands, operators, and other accepted
symbols into itself.

"""

# standard library imports
from typing import Union


class Symbols:
    """
    This class bundles symbols used for error checking and prefix-to-postfix conversion into itself.
    """

    def __init__(
        self, use_numerals: bool = False, additional_operators: Union[None, str] = None
    ):
        self.numerals = "0123456789"
        self.alphabet_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.operands = self.alphabet_symbols
        if use_numerals:
            self.operands += self.numerals
        self.other_symbols = "\n \t"
        self.operators = "+-*/$"
        if additional_operators is not None:
            for char in additional_operators:
                if char in self.operands:
                    raise KeyError(f"Additional operator {char} cannot be an operand.")
                if char in self.other_symbols:
                    raise ValueError(
                        f"Additional operator {char} cannot be newline, space, or tab."
                    )
            self.operators += additional_operators
        self.accepted_symbols = self.operators + self.operands + self.other_symbols
