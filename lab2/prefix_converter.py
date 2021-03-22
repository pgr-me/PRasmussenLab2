"""Peter Rasmussen, Lab 1, prefix_converter.py

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
from pathlib import Path
from time import time_ns
from typing import Union

# local imports
from lab1.stack import Stack


class PrefixSyntaxError(Exception):
    """Exception to capture prefix syntax errors."""

    pass


class PrefixConverter:
    """
    This class converts prefix expressions into postfix equivalents.
    Methods are organized in a top-down fashion: highest-level methods come first,
    static methods come last.
    """

    def __init__(
        self,
        input_file: Union[str, Path],
        output_file: Union[str, Path],
        use_numerals: bool = False,
        output_file_header="Peter Rasmussen, Lab 1",
    ) -> None:
        """
        Initialize IO attributes and output file header and define symbol set
        :param input_file: Input file to read
        :param output_file: Output file to write
        :param use_numerals: True to include numerals among accepted_symbols
        :param output_file_header: Preface output with file header
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.operator_symbols = "+-*/$"
        self.numerals = "0123456789"
        self.alphabet_symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.operand_symbols = self.alphabet_symbols
        self.output_file_header = (
            f"# {output_file_header}\n"
            f"# Input file: {self.input_file.absolute()}\n"
            f"# Output file: {self.output_file.absolute()}\n"
        )
        if use_numerals:
            self.operand_symbols += self.numerals
            self.output_file_header += (
                "# Numerals included: Please note numerals are only valid "
                "for single digit integers (0 to 9)\n"
            )
        self.output_file_header += "\n"
        self.output_string = self.output_file_header
        self.other_symbols = "\n \t"
        self.accepted_symbols = (
            self.operator_symbols + self.operand_symbols + self.other_symbols
        )
        # This dictionary is NOT used for any of the conversion operations
        # It is only used to measure time complexity
        self.complexity_dict = {"convert_prefix_input": {"loops": 0, "time": 0},
                                "convert_prefix_stack": {"loops": 0, "time": 0},
                                "_convert_prefix_stack": {"loops": 0, "time": 0}}

    def convert_prefix_input(self) -> str:
        """
        Convert prefix input from file, echoing inputs and postfix conversions to output file.
        :return: Echoed prefix with corresponding postfix equivalents; summary stats at file bottom
        """
        start = time_ns()
        prefix_stack = Stack()
        operand_count = 0
        operator_count = 0
        line = 1
        column = 0
        error = ""
        postfix_conversion = ""
        prefix_expression = ""

        with open(self.input_file, "r") as f:

            # While loop adapted from https://www.geeksforgeeks.org/python-program-to-read-character-by-character-from-a-file/
            # Specifically, lines 119 through 122
            # The while loop iterates at the character level
            symbol_count = 0
            while 1:

                # Read each character and push to prefix stack
                symbol = f.read(1)
                prefix_stack.push(symbol)

                # Increment column after we finish processing the current symbol
                column += 1

                # Increment symbol count
                symbol_count += 1

                # Check if symbol is legal
                error = self.check_if_legal_character(symbol, column, error=error)

                # At EOL, process prefix_stack reinitialize prefix stack, op counts, column, & error
                if (symbol == "\n") | (not symbol):

                    # Pop newline of prefix stack because we don't want it in our prefix_expression
                    prefix_stack.pop()
                    prefix_expression = prefix_stack.to_string(top_down=False)

                    # Do final check to see if op counts align
                    error = PrefixConverter.check_op_counts(
                        operand_count, operator_count, column, error, final=True
                    )

                    # If error has been encountered, let error be the output
                    if error != "":
                        postfix_conversion = error

                    # Else if the line was blank or only had some mix of \t and spaces indicate so
                    elif (operand_count == 0) and (operator_count == 0):
                        postfix_conversion = "Nothing to process"

                    # Otherwise, convert the correct prefix into postfix
                    else:
                        postfix_stack = self.convert_prefix_stack(
                            PrefixConverter.reverse_stack(prefix_stack)
                        )
                        postfix_conversion = postfix_stack.pop()

                    self.output_string += (
                        f"Line {line}: Prefix: {prefix_expression}, "
                        f"Postfix: {postfix_conversion}\n"
                    )

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
                    error = PrefixConverter.check_op_counts(
                        operand_count, operator_count, column, error
                    )

                # Terminate while loop if we reach end of file
                if symbol == "":
                    break
        elapsed = time_ns() - start
        self.complexity_dict['convert_prefix_input'] = {"time": elapsed, "loops": line}
        return self.output_string

    def convert_prefix_stack(self, stack: Stack) -> Stack:
        """
        Transform prefix stack into single-item postfix stack.
        This method is a wrapper for _convert_prefix_stack.
        :param stack: Prefix stack to convert
        :return: Single-item postfix stack
        """
        # Initialize time and loop metrics
        start = time_ns()
        loops = 0
        while stack.size > 1:
            stack = self._convert_prefix_stack(stack)
            loops += 1

        # Recover elapsed time and number of loops
        elapsed = time_ns() - start
        heretofore_elapsed = self.complexity_dict['convert_prefix_stack']['time']
        heretofore_loops = self.complexity_dict['convert_prefix_stack']['loops']
        elapsed += heretofore_elapsed
        loops += heretofore_loops
        self.complexity_dict['convert_prefix_stack'] = {"time": elapsed, "loops": loops}
        return stack

    def _convert_prefix_stack(self, pre_stack: Stack) -> Stack:
        """
        Convert subset of prefix terms into postfix equivalents.
        This method is used by convert_prefix_stack.
        :param pre_stack: Prefix stack to convert
        :return: Partially or wholly converted prefix stack
        """
        # Initialize time and loop metrics
        start = time_ns()
        loops = 0

        stack = Stack(
            datatype=pre_stack.datatype, preallocation=pre_stack.preallocation
        )
        pre_substring = ""
        while pre_stack.size > 0:

            value = pre_stack.pop()

            # If statement immediately below guards against inclusion of unwanted symbols
            if self.is_operator(value[0]) | self.is_operand(value[0]):
                stack.push(value)
                pre_substring = PrefixConverter.make_prefix_substring(
                    pre_substring, value[0]
                )
                if self.is_prefix_term(pre_substring):
                    # Code from lines 247 to 251 informed by https://www.geeksforgeeks.org/prefix-postfix-conversion/
                    operand_2 = stack.pop()
                    operand_1 = stack.pop()
                    operator = stack.pop()
                    post_substring = operand_1 + operand_2 + operator
                    stack.push(post_substring)
        stack = PrefixConverter.reverse_stack(stack)
        # Recover elapsed time and number of loops
        elapsed = time_ns() - start
        heretofore_elapsed = self.complexity_dict['convert_prefix_stack']['time']
        heretofore_loops = self.complexity_dict['convert_prefix_stack']['loops']
        elapsed += heretofore_elapsed
        loops += heretofore_loops
        self.complexity_dict['_convert_prefix_stack'] = {"time": elapsed, "loops": loops}
        return stack

    def check_for_leading_operand(
        self, character: str, column_number: int, error: str
    ) -> str:
        """
        Check for leading operand in prefix input.
        Only checks if no prior error encountered for current prefix statement.
        :param character: Symbol to check
        :param column_number: Column number of current line
        :param error: Inherited error string; method only runs if no prior error found for line
        :return: Error string; string equal to '' if errors found and no prior errors
        """
        # For readability, we only catch the first error of a prefix input
        if error == "":
            try:
                if column_number == 1 and self.is_operand(character):
                    error_message = (
                        f"Prefix statement cannot begin with an operand character"
                    )
                    raise PrefixSyntaxError(error_message)
            except PrefixSyntaxError as e:
                error = e.__repr__()
        # If an error has already been caught, we simply return that error
        return error

    def check_if_legal_character(
        self, character: str, column_number: int, error: str
    ) -> str:
        """
        Check if character is legal.
        Only performs check if no prior error encountered for current prefix statement.
        :param character:
        :param column_number:
        :param error: Inherited error string; method only runs if no prior error found for line
        :return: Error string; string equal to '' if errors found and no prior errors
        """
        # For readability, we only catch the first error of a prefix input
        if error == "":
            try:
                if character not in self.accepted_symbols:
                    error_message = f"Illegal character `{character}` encountered in column {column_number}"
                    raise PrefixSyntaxError(error_message)
            except PrefixSyntaxError as e:
                error = e.__repr__()
        # If an error has already been caught, we simply return that error
        return error

    def is_accepted_symbol(self, symbol: str) -> bool:
        """
        Determine if symbol is an accepted operand, operator, or other accepted symbol.
        :param symbol: Symbol to evaluate
        :return: True if symbol is accepted
        """
        return (
            self.is_operand(symbol) | self.is_operator(symbol) | self.is_other(symbol)
        )

    def is_operand(self, symbol: str) -> bool:
        """
        Determine if symbol is an accepted operand.
        :param symbol: Symbol to evaluate
        :return: True if symbol is an accepted operand
        """
        if type(symbol) != str:
            raise TypeError(f"Symbol {symbol} must be a string but is a {type(symbol)}")
        if symbol == "":
            return False
        return symbol in self.operand_symbols

    def is_operator(self, symbol: str) -> bool:
        """
        Determine if symbol is an accepted operator.
        :param symbol: Symbol to evaluate
        :return: True if symbol is an accepted operator
        """

        if type(symbol) != str:
            raise TypeError(f"Symbol {symbol} must be a string but is a {type(symbol)}")
        if symbol == "":
            return False
        return symbol in self.operator_symbols

    def is_other(self, symbol: str) -> bool:
        """
        Determine if symbol is another accepted - yet non-operator, non-operand - symbol.
        :param symbol: Symbol to evaluate
        :return: True if accepted other symbol
        """
        if type(symbol) != str:
            raise TypeError(f"Symbol {symbol} must be a string but is a {type(symbol)}")
        if symbol == "":
            return False
        return symbol in self.other_symbols

    def is_prefix_term(self, s: str) -> bool:
        """
        Determine if three-character string is a prefix term.
        :param s: String to evaluate
        :return: True if string is a valid prefix term
        """
        try:
            return (
                self.is_operator(s[0])
                and self.is_operand(s[1])
                and self.is_operand(s[2])
            )
        except IndexError:
            return False

    def write_output(self) -> None:
        """
        Write outputs to file.
        :return:
        """
        with open(self.output_file, "w") as f:
            # Write prefix-to-postfix conversion outputs
            f.write(self.output_string)
            # Write complexity stats
            f.write('\n')
            f.write(80 * '@')
            f.write('\nComplexity outputs')
            for function, di in self.complexity_dict.items():
                loops = di["loops"]
                time = di["time"]
                f.write(f"\nFunction: {function}\tTime (ns): {time}\tLoops: {loops}")

    @staticmethod
    def check_op_counts(
        operands: int, operators: int, column_number: int, error: str, final=False
    ) -> str:
        """
        Check operand and operator counts.
        Only checks if there is no prior errors encountered.
        :param operands: Number of operands at specified column number
        :param operators: Number of operators at specified column number
        :param column_number: Current column number of line
        :param error: Inherited error string; method only runs if no prior error found for line
        :param final: True if final check for correct operator and operand counts
        :return: Error string; string equal to '' if errors found and no prior errors
        """
        # For readability, we only catch the first error of a prefix input

        # Return if there are no operators or operands
        if (operands == 0) & (operators == 0):
            return error

        # Condition to check operator and operand counts depends on if the char is final one in line
        if final:
            condition = operands - 1 == operators
        else:
            condition = operators >= operands - 1

        # Only try if no error has been previously detected
        # This way we don't overwhelm the user with multiple error messages in the output
        if error == "":
            try:
                if not condition:
                    if final:
                        if operators < operands - 1:
                            error_message = f"Column {column_number}: Too few operators, {operators}, for operand characters, {operands}."
                        else:
                            error_message = f"Column {column_number}: Too many operators, {operators}, for operand characters, {operands}."
                    else:
                        if operators < operands:
                            error_message = f"Column {column_number}: Too few operators, {operators}, for operand characters, {operands}."
                        else:
                            error_message = f"Column {column_number}: Too many operators, {operators}, for operand characters, {operands}."
                    raise PrefixSyntaxError(error_message)
            except PrefixSyntaxError as e:
                error = e.__repr__()
        return error

    @staticmethod
    def make_prefix_substring(string: str, char: str) -> str:
        """
        Dynamically build a prefix string from existing prefix string and input char.
        :param string: Existing prefix string
        :param char: Replacement character
        :return: Update prefix substring
        """
        if len(string) > 3:
            raise IndexError("Input string cannot be of length greater than 3")
        if len(string) == 3:
            return string[1] + string[2] + char
        else:
            return string + char

    @staticmethod
    def reverse_stack(stack: Stack) -> Stack:
        """
        Reverse the contents of a stack.
        :param stack: Input stack to reverse
        :return: Reversed output stack
        """
        auxiliary_stack = Stack(
            datatype=stack.datatype, preallocation=stack.preallocation
        )
        while stack.size > 0:
            auxiliary_stack.push(stack.pop())
        return auxiliary_stack
