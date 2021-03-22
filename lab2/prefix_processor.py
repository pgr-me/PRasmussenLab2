"""Peter Rasmussen, Lab 2, prefix_processor.py

This module provides the PrefixConverter and PrefixSyntaxError classes. The PrefixConverter class
converts a file of newline-delimited prefix expressions, when possible, into their postfix
equivalents.

Example output file:
    # Peter Rasmussen, Lab 2
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
from pathlib import Path
from time import time_ns
from typing import Union

# local imports
from lab2.prefix_syntax_checker import PrefixSyntaxChecker


class PrefixProcessor:
    """
    This class converts prefix expressions into postfix equivalents.
    Methods are organized top-down: highest-level methods come first, static methods come last.
    """

    def __init__(
            self,
            input_file: Union[str, Path],
            use_numerals: bool = False,
            additional_operators: Union[None, str] = None,
            output_file_header="Peter Rasmussen, Lab 2",
    ) -> None:
        """
        Initialize IO attributes and output file header and define symbol set
        :param input_file: Input file to read
        :param output_file: Output file to write
        :param use_numerals: True to include numerals among accepted_symbols
        :param output_file_header: Preface output with file header
        """
        self.input_file = Path(input_file)
        self.numerals = "0123456789"
        self.alphabet_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.operands = self.alphabet_symbols
        if use_numerals:
            self.operands += self.numerals
            self.output_file_header += (
                "# Numerals included: Please note numerals are only valid "
                "for single digit integers (0 to 9)\n"
            )
        self.other_symbols = "\n \t"
        if additional_operators is not None:
            for char in additional_operators:
                if char in self.operands:
                    raise KeyError(f'Additional operator {char} cannot be an operand.')
                if char in self.other_symbols:
                    raise ValueError(
                        f'Additional operator {char} cannot be newline, space, or tab.')
            self.operators = "+-*/$" + additional_operators
        self.accepted_symbols = self.operators + self.operands + self.other_symbols

        self.file_di = {'start': time_ns(), 'stop': None, 'symbols': 0, 'lines': 0,
                          'prefix_data': []}

    def convert_prefix_input(self) -> dict:
        """
        Convert prefix input from file, echoing inputs and postfix conversions to output file.
        :return: Echoed prefix with corresponding postfix equivalents; summary stats at file bottom
        """

        line = 0
        with open(self.input_file, "r") as f:

            # While loop adapted from https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
            # Specifically, lines 119 through 122
            # The while loop iterates at the character level
            echoed_prefix = ''
            # Initialize symbol and line dict
            line_di = {'start': time_ns(), 'stop': None, 'elapsed': None, 'echoed_prefix': '',
                         'operands': 0, 'operators': 0, 'line': line, 'column': 0, 'is_empty': None,
                         'error': ''}
            symbol = ''  # Dummy symbol to let us initialize while loop
            while symbol:
                # Read each character and push to prefix stack
                symbol = f.read(1)

                # If we reach the end of the line, populate file_di and re-initialize line_di
                if symbol == "\n":
                    line_di['is_empty'] = prefix_syntax_checker.is_empty(line_di['operands'],
                                                                           line_di['operators'])
                    line_di['error'] = prefix_syntax_checker.error
                    line_di['stop'] = time_ns()
                    line_di['elapsed'] = line_di['stop'] - line_di['start']
                    self.file_di['prefix_data'].append(line_di)

                    # Re-initialize symbol and line dict
                    line_di = {'start': time_ns(), 'stop': None, 'echoed_prefix': '',
                                 'operands': 0, 'operators': 0, 'line': line, 'column': 0,
                                 'error': ''}

                else:
                    line_di['column'] += 1  # Increment column count
                    line_di['echoed_prefix'] += symbol  # Add character to echoed prefix string
                    line_di['operands'] += prefix_syntax_checker.is_operand(symbol)
                    line_di['operators'] += prefix_syntax_checker.is_operator(symbol)

                    # Check prefix syntax for errors
                    prefix_syntax_checker = PrefixSyntaxChecker(self.operands,
                                                                self.operators,
                                                                self.other_symbols)
                    prefix_syntax_checker.check_leading_operand(symbol, line_di['column'])
                    prefix_syntax_checker.check_if_legal_symbol(symbol, line_di['column'])
                    prefix_syntax_checker.check_op_counts(line_di['operands'],
                                                          line_di['operators'], line_di['column'])

            # After reaching end of file, compute total time complexity and return the file_di
            self.file_di['stop'] = time_ns()
            self.file_di['elapsed'] = self.file_di['stop'] - self.file_di['start']
            return self.file_di
