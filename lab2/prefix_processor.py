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
    Methods are organized in a top-down fashion: highest-level methods come first,
    static methods come last.
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
        self.output_file_header = (
            f"# {output_file_header}\n"
            f"# Input file: {self.input_file.absolute()}\n"
            f"# Output file: {self.output_file.absolute()}\n"
        )
        if use_numerals:
            self.operands += self.numerals
            self.output_file_header += (
                "# Numerals included: Please note numerals are only valid "
                "for single digit integers (0 to 9)\n"
            )
        for char in additional_operators:
            if char in self.operands:
                raise KeyError(f'Additional operator symbol {char} cannot be an operand.')
        if additional_operators is not None:
            self.operators = "+-*/$" + additional_operators
        self.output_file_header += "\n"
        self.output_string = self.output_file_header
        self.other_symbols = "\n \t"
        self.accepted_symbols = (
            self.operators + self.operands + self.other_symbols
        )
        # This dictionary is NOT used for any of the conversion operations
        # It is only used to measure time complexity
        self.complexity_dict = {"convert_prefix_input": {"loops": 0, "time": 0},
                                "convert_prefix_stack": {"loops": 0, "time": 0},
                                "_convert_prefix_stack": {"loops": 0, "time": 0}}

    def convert_prefix_input(self) -> dict:
        """
        Convert prefix input from file, echoing inputs and postfix conversions to output file.
        :return: Echoed prefix with corresponding postfix equivalents; summary stats at file bottom
        """
        output = []


        with open(self.input_file, "r") as f:

            # While loop adapted from https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
            # Specifically, lines 119 through 122
            # The while loop iterates at the character level
            symbol_count = 0
            line = 0
            echoed_prefix = ''
            file_dict = {'start': time_ns(), 'stop': None, 'columns': 0, 'lines': 0,
                         'prefix_data': []}
            while 1:
                line_dict = {'start': time_ns(), 'stop': None, 'echoed_prefix': '',
                             'operand_count': 0, 'operator_count': 0, 'symbol_count': symbol_count,
                             'line': line, 'column': 0, 'error': ''}

                # Read each character and push to prefix stack
                symbol = f.read(1)
                column += 1  # Increment column count
                symbol_count += 1  # Increment symbol count
                echoed_prefix += symbol

                if not symbol:
                    return file_dict

                # Check prefix syntax for errors
                prefix_syntax_checker = PrefixSyntaxChecker(self.operands,
                                                            self.operators,
                                                            self.other_symbols)
                prefix_syntax_checker.check_leading_operand(symbol, column)
                prefix_syntax_checker.check_if_legal_symbol(symbol, column)
                prefix_syntax_checker.check_op_counts(n_operands, n_operators, column)
                prefix_stack.push(symbol)

                # At EOL, process prefix_stack reinitialize prefix stack, op counts, column, & error
                if (symbol == "\n") | (not symbol):

                    # Pop newline of prefix stack because we don't want it in our prefix_expression
                    prefix_stack.pop()
                    prefix_expression = prefix_stack.to_string(top_down=False)

                    # Do final check to see if op counts align
                    error = PrefixProcessor.check_op_counts(
                        operand_count, operator_count, column, error, final=True
                    )

                    # If error has been encountered, let error be the output
                    if error != "":
                        postfix_conversion = error

                    # Else if the line was blank or only had some mix of \t and spaces indicate so
                    elif (operand_count == 0) and (operator_count == 0):
                        postfix_conversion = "Nothing to process"



                    # Reset prefix_stack, op counts, line and column numbers, and error string
                    prefix_stack = Stack()
                    operator_count = 0
                    operand_count = 0
                    line += 1
                    column = 0
                    error = ""

                # Check for errors in the prefix syntax and push to line stack
                elif self.is_operand(symbol) | self.is_operator(symbol):
                    # Check for leading operand
                    error = self.check_for_leading_operand(symbol, column, error)

                    # Track operator and operand counts to check for syntax errors
                    if self.is_operator(symbol):
                        operator_count += 1
                    else:
                        operand_count += 1

                    # Check operand / operator count after reading each character
                    error = PrefixProcessor.check_op_counts(
                        operand_count, operator_count, column, error
                    )

                # Terminate while loop if we reach end of file
                if symbol == "":
                    break
        elapsed = time_ns() - start
        self.complexity_dict['convert_prefix_input'] = {"time": elapsed, "loops": line}
        return self.output_string

