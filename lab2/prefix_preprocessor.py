"""Peter Rasmussen, Lab 2, prefix_preprocessor.py

This module provides the PrefixPreProcessor class, which reads a file of prefix statements character
by character and checks each prefix statement for errors. PrefixPreProcessor returns a list of
dictionaries. Each dictionary corresponds to one line in the input file and contains prefix
statements, errors (if any), and complexity metrics.

"""

# standard library imports
from pathlib import Path
from time import time_ns
from typing import Union

# local imports
from lab2.prefix_syntax_checker import PrefixSyntaxChecker


class PrefixPreProcessor:
    """
    This class converts prefix expressions into postfix equivalents.
    Methods are organized top-down: highest-level methods come first, static methods come last.
    """

    def __init__(
            self,
            input_file: Union[str, Path],
            operands: str,
            operators: str,
            other_symbols: str,
            accepted_symbols: str
    ) -> None:
        """
        Initialize IO attributes and output file header and define symbol set
        :param input_file: Input file to read
        :param use_numerals: True to include numerals among accepted_symbols
        :param additional_operators: True to include additional operators
        """
        self.input_file = Path(input_file)
        self.operands = operands
        self.operators = operators
        self.other_symbols = other_symbols
        self.accepted_symbols = accepted_symbols
        self.file_di = {'start': time_ns(), 'stop': None, 'symbols': 0, 'lines': 0,
                        'prefix_data': []}

    def preprocess_prefix_input(self) -> dict:
        """
        Convert prefix input from file, echoing inputs and postfix conversions to output file.
        This method runs prior to
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
                    if prefix_syntax_checker.no_prior_error() and not line_di['is_empty']:
                        line_di['valid_prefix'] = True
                    else:
                        line_di['valid_prefix'] = False
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
