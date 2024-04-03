#!/usr/bin/python
import re
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='''Parse msfvenom generated shellcode into a single line. 
                                 
EXAMPLES:
    ParseShellcode.py reverse_shell.txt
''', formatter_class=RawTextHelpFormatter)
parser.add_argument('input_file', metavar="[input_file.txt]", type=str, help='Shellcode.txt to transform')
args = parser.parse_args()

input = ""
with open(args.input_file, "r") as file:
    input = file.read()

input = re.findall(r'\\x[0-9a-fA-F]{2}', input)
input = ''.join(input)
print(input)