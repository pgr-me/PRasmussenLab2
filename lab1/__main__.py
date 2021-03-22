"""Peter Rasmussen, Lab 1, stack.py

This program converts a file of newline-delimited prefix expressions into an output of postfix
expressions. Each line of the output begins with the line number of the prefix expression from the
input file, followed by the echoed prefix expression and its postfix equivalent. Postfix expressions
are not rendered for invalid prefix expressions (i.e., those that have syntax errors). In these
cases, the prefix syntax error is written instead of a postfix expression. Below the prefix-postfix
outputs is a brief complexity summary, which lists the cumulative runtime and number of loops for
the three key functions used in this program. More details on these functions, including their
definition, are provided in the prefix_converter.py module.

Upon execution, the user must provide the input file path (in_file) and output file path (out_file).
Optionally, the user may specify whether to include numerals as acceptable operand symbols. Please
note that only single-digit numerals (0-9) are supported in this implementation. Additionally, the
user may specify a file header that is prepended to the outputs. Please refer to the arg_parser
statements for more information on these optional arguments.

Example execution:
    python -m path/to/lab1 -i path/to/input_file.txt -o path/to/output_file.txt

The structure of this package is based on the Python lab0 package that Scott Almes developed for
this course. Per Scott Almes, this module "is the entry point into this program when the module is
executed as a standalone program. IE 'python -m lab1'."

"""

# Generally used to process command line arguments and 'launch' the program
from pathlib import Path
import argparse

from lab1.prefix_converter import PrefixConverter

# Parse arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--in_file", "-i", type=Path, help="Input File Pathname")
arg_parser.add_argument("--out_file", "-o", type=Path, help="Output File Pathname")
arg_parser.add_argument(
    "--file_header",
    "-f",
    default="Peter Rasmussen, Lab 1",
    type=str,
    help="Include numerals as accepted operands",
)
arg_parser.add_argument(
    "--use_numerals",
    "-n",
    default=False,
    type=bool,
    help="Include numerals as accepted operands",
)
args = arg_parser.parse_args()

# Declare in_path, out_path, use_numerals, and file_header variables
in_path = Path(args.in_file)
out_path = Path(args.out_file)
use_numerals = args.use_numerals
file_header = args.file_header

# Instantiate prefix converter object and convert file of prefix strings to postfix equivalents
prefix_converter = PrefixConverter(in_path, out_path, use_numerals, file_header)
prefix_converter.convert_prefix_input()
prefix_converter.write_output()
