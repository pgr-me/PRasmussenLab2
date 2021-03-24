"""Peter Rasmussen, Lab 2, prefix_syntax_checker.py

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


class PrefixSyntaxError(Exception):
    """Exception to capture prefix syntax errors."""

    pass


class PrefixSyntaxChecker:
    """
    This class checks prefix syntax.
    Methods are organized in a top-down fashion: highest-level methods come first, static methods
    come last.
    For readability, we only capture the first error in a prefix term.
    """

    def __init__(self, operand_symbols, operator_symbols):
        self.operand_symbols = operand_symbols
        self.operator_symbols = operator_symbols
        self.other_symbols = '\n \t'
        self.accepted_symbols = (
            self.operand_symbols + self.operator_symbols + self.other_symbols
        )
        self.error = ""

    def check_syntax(self, character: str, column: int):
        """Check for leading operand, if symbol is legal, and operand & operator counts.
        :param character: Symbol to check.
        :param column: Line column number.
        """
        self.check_leading_operand(character, column)
        self.check_if_legal_symbol(character, column)
        self.check_if_legal_symbol(character, column)

    def check_leading_operand(self, character: str, column: int):
        """
        Check for leading operand in prefix input.
        :param character: Symbol to check.
        :param column: Line column number.
        """
        try:
            if self.no_prior_error() and self.is_operand(character) and (column == 1):
                error_message = (
                    "Prefix statement cannot begin with an operand character"
                )
                raise PrefixSyntaxError(error_message)
        except PrefixSyntaxError as e:
            self.error = e.__repr__()

    def check_if_legal_symbol(self, character: str, column: int):
        """
        Check if symbol is legal (i.e., among accepted symbols).
        :param character: Symbol to check.
        :param column: Line column number.
        """
        try:
            if self.no_prior_error() and not self.is_accepted_symbol(character):
                error_message = (
                    f"Illegal character `{character}` found in column {column}"
                )
                raise PrefixSyntaxError(error_message)
        except PrefixSyntaxError as e:
            self.error = e.__repr__()

    def check_op_counts(self, operands: int, operators: int, column: int, final=False):
        """
        Check operand and operator counts.
        Only checks if there is no prior errors encountered.
        :param operands: Number of operands at specified column number
        :param operators: Number of operators at specified column number
        :param column: Current column number of line
        :param final: True if final check for correct operator and operand counts
        """

        if not self.no_prior_error():
            return

        # Return if there are no operators or operands
        if (operands == 0) & (operators == 0):
            return

        # Condition to check operator and operand counts depends on if the char is final one in line
        if final:
            condition = operands - 1 == operators
        else:
            condition = operators >= operands - 1

        try:
            if not condition:
                few_many = "many"
                if (final and operators < operands - 1) or (
                    not final and operators < operands
                ):
                    few_many = "few"
                error_message = f"Column {column}: Too {few_many} operators, {operators}, for operand characters, {operands}."
                raise PrefixSyntaxError(error_message)
        except PrefixSyntaxError as e:
            self.error = e.__repr__()

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
        return symbol in self.operand_symbols

    def is_operator(self, symbol: str) -> bool:
        """
        Determine if symbol is an accepted operator.
        :param symbol: Symbol to evaluate
        :return: True if symbol is an accepted operator
        """
        return symbol in self.operator_symbols

    def is_other(self, symbol: str) -> bool:
        """
        Determine if symbol is another accepted - yet non-operator, non-operand - symbol.
        :param symbol: Symbol to evaluate
        :return: True if accepted other symbol
        """
        return symbol in self.other_symbols

    def no_prior_error(self) -> bool:
        """Check if there has been no error.
        :param: None
        :return: True if no previous error encountered.
        """
        return self.error == ""

    @staticmethod
    def is_empty(operands: int, operators: int) -> bool:
        """
        Determine whether string contains any operands or operators.
        The string is "empty" if it only contains spaces and tabs.
        :param operands: Number of operands in the string
        :param operators: Number of operators in the string
        :return: True if string contains zero operands and operators
        """
        return operands + operators == 0
