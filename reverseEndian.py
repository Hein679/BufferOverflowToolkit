#!/usr/bin/python
import re
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='''Reverse Endianness for a string of bytes.

EXAMPLES:
    reverseEndian.py \"625011AF\"
    reverseEndian.py \"62 50 11 AF\"
    reverseEndian.py \"\\x62\\x50\\x11\\xAF"
    reverseEndian.py "\\x62 \\x50 \\x11 \\xAF"''', formatter_class=RawTextHelpFormatter)
parser.add_argument('input', metavar="[input]", type=str, help='Bytes to reverse endianess')
args = parser.parse_args()

input = args.input
input = re.findall(r'[0-9a-fA-F]{2}', input)
input.reverse()
input = '\\x'.join(input)
input = "\\x" + input 

print(input)