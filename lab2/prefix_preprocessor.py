"""Peter Rasmussen, Lab 2, prefix_preprocessor.py

This module provides the PrefixPreProcessor class, which reads a file of prefix statements character
by character and checks each prefix statement for errors. PrefixPreProcessor.preprocess_prefix_input
returns a list of dictionaries. Each dictionary corresponds to one line in the input file and
contains prefix statements, errors (if any), and complexity metrics. This module uses the
prefix_syntax_checker module to catch prefix syntax errors.

"""

# standard library imports
from pathlib import Path
from time import time_ns
from typing import Union

# local imports
from lab2.prefix_syntax_checker import PrefixSyntaxChecker


class PrefixPreprocessor:
    """
    This class converts prefix expressions into postfix equivalents.
    Methods are organized top-down: highest-level methods come first, static methods come last.
    """

    def __init__(self, input_file: Union[str, Path], operands: str, operators: str):
        """
        Initialize input file, operands, and operators.
        :param input_file: Input file to read
        :param operands: Set of prefix operand symbols
        :param operators: Set of prefix operator symbols
        """
        self.input_file = Path(input_file)
        self.operands = operands
        self.operators = operators
        self.other_symbols = "\n \t"
        self.accepted_symbols = self.operands + self.operators + self.other_symbols
        self.file_di = {
            "start": time_ns(),
            "stop": None,
            "symbols": 0,
            "lines": 0,
            "prefix_data": [],
        }

    def preprocess_prefix_input(self) -> dict:
        """
        Convert prefix input from file, echoing inputs and postfix conversions to output file.
        :return: Echoed prefix with corresponding postfix equivalents; summary stats at file bottom
        """

        line = 1
        with open(self.input_file, "r") as f:

            # While loop adapted from https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
            # Specifically, lines 61 through 63
            # The while loop iterates at the character level
            # Initialize symbol and line dict
            line_di = self.make_line_di(line)
            prefix_syntax_checker = PrefixSyntaxChecker(self.operands, self.operators)
            while True:
                # Read and preprocess each character
                symbol = f.read(1)

                # If we reach the end of the line, populate file_di and re-initialize line_di
                if (symbol == "\n") or (not symbol):
                    line_di["line"] = line
                    line_di["is_empty"] = prefix_syntax_checker.is_empty(
                        line_di["n_operands"], line_di["n_operators"]
                    )

                    # Do one final check of op counts
                    prefix_syntax_checker.check_op_counts(
                        line_di["n_operands"],
                        line_di["n_operators"],
                        line_di["column"],
                        final=True,
                    )
                    line_di["error"] = prefix_syntax_checker.error
                    if (
                        prefix_syntax_checker.no_prior_error()
                        and not line_di["is_empty"]
                    ):
                        line_di["valid_prefix"] = True
                    else:
                        line_di["valid_prefix"] = False
                    line_di["stop"] = time_ns()
                    line_di["elapsed"] = line_di["stop"] - line_di["start"]

                    self.file_di["prefix_data"].append(line_di)

                    # Increment line number, re-initialize line dict, and reset error
                    line += 1
                    line_di = self.make_line_di(line)
                    prefix_syntax_checker.error = ""

                else:
                    line_di["column"] += 1  # Increment column count
                    line_di["prefix"].append(
                        symbol
                    )  # Add character to echoed prefix string
                    line_di["n_operands"] += prefix_syntax_checker.is_operand(symbol)
                    line_di["n_operators"] += prefix_syntax_checker.is_operator(symbol)

                    # Check prefix syntax for errors
                    prefix_syntax_checker.check_leading_operand(
                        symbol, line_di["column"]
                    )
                    prefix_syntax_checker.check_if_legal_symbol(
                        symbol, line_di["column"]
                    )
                    prefix_syntax_checker.check_op_counts(
                        line_di["n_operands"], line_di["n_operators"], line_di["column"]
                    )

                # Terminate while loop at end of file
                if not symbol:
                    break
            # After reaching end of file, compute total time complexity and return the file_di
            self.file_di["stop"] = time_ns()
            self.file_di["elapsed"] = self.file_di["stop"] - self.file_di["start"]
            self.file_di["lines"] = line
            return self.file_di

    @staticmethod
    def make_line_di(line) -> dict:
        """
        Make a dictionary that line that contains complexity metrics, line number, prefix, and, if
        applicable, and error encountered during syntax checking.
        :return: Line-level dictionary of preprocessed prefix outputs
        """
        return {
            "start": time_ns(),
            "stop": None,
            "elapsed": None,
            "prefix": [],
            "n_operands": 0,
            "n_operators": 0,
            "line": line,
            "column": 0,
            "is_empty": None,
            "error": "",
        }
