"""Peter Rasmussen, Lab 2, __main__.py

This program recursively converts a file of newline-delimited prefix expressions into an output of
postfix expressions. Each line of the output begins with the line number of the prefix expression
from the input file, followed by the echoed prefix expression and its postfix equivalent. Postfix
expressions are not rendered for invalid prefix expressions (i.e., those that have syntax errors).
In these cases, the prefix syntax error is written instead of a postfix expression. Below the
prefix-postfix outputs is a brief complexity summary, which lists the cumulative runtime and number
of loops for the three key functions used in this program. More details on these functions,
including their definition, are provided in the prefix_converter.py module.

Upon execution, the user must provide the input file path (in_file) and output file path (out_file).
Optionally, the user may specify whether to include numerals as acceptable operand symbols and
whether to include additional operators. Please note that only single-digit numerals (0-9) are
supported in this implementation. Additionally, the user may specify a file header that is
prepended to the outputs. Please refer to the arg_parser statements for more information on these
optional arguments.

Example execution:
    python -m path/to/lab2 -i path/to/input_file.txt -o path/to/output_file.txt

The structure of this package is based on the Python lab0 package that Scott Almes developed for
this course. Per Scott Almes, this module "is the entry point into this program when the module is
executed as a standalone program. IE 'python -m lab2'."

"""

# standard library imports
import argparse
import os
from pathlib import Path
from typing import Union

# local imports
from lab2.symbols import Symbols
from lab2.prefix_preprocessor import PrefixPreProcessor
from lab2.prefix_converter import PrefixConverter

# Parse arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--in_file", "-i", type=Path, help="Input File Pathname")
arg_parser.add_argument("--out_file", "-o", type=Path, help="Output File Pathname")
arg_parser.add_argument(
    "--file_header", "-f", default="Peter Rasmussen, Lab 2", type=str,
    help="Include numerals as operands",
)
arg_parser.add_argument(
    "--use_numerals", "-n", default=False, type=bool, help="Include numerals operands"
)
arg_parser.add_argument(
    "--additional_operators", "-a", default=None, type=Union[None, str],
    help="Use additional operators",
)
args = arg_parser.parse_args()

# Declare in_path, out_path, use_numerals, and file_header variables
in_path = Path(args.in_file)
out_path = Path(args.out_file)
use_numerals = args.use_numerals
additional_operators = args.additional_operators
file_header = (
    f"# {98 * '@'}\n"
    f"# {args.file_header}\n"
    f"# Input file: {in_path.absolute()}\n"
    f"# Output file: {out_path.absolute()}\n"
    "\n"
)

# Instantiate symbols object, which contains operands, operators, and other accepted characters
symbols = Symbols(use_numerals=use_numerals, additional_operators=additional_operators)
# Preprocess prefix file, checking for errors and recording complexity metrics
prefix_preprocessor = PrefixPreProcessor(in_path, symbols.operands, symbols.operators)
file_di: dict = prefix_preprocessor.preprocess_prefix_input()
with open(str(out_path), 'w') as f:
    f.write(file_header)
    f.write(f"# {98 * '@'}\n")
    f.write("# Prefix-postfix conversion\n")
    for line_di in file_di["prefix_data"]:
        prefix = line_di["prefix"]
        line = line_di["line"]
        if line_di["valid_prefix"]:
            prefix_converter = PrefixConverter(prefix, symbols.operands, symbols.operators)
            postfix = prefix_converter.convert_prefix()
        elif line_di["error"] != "":
            postfix = line_di["error"]
        else:
            postfix = "Nothing to process"
        output = f"Line: {line}: Prefix {prefix}, Postfix: {postfix}"
        f.write(output + os.linesep)
    f.write(f"\n# {98 * '@'}\n")
    f.write("Complexity outputs\n")
    f.write("Stuff")
