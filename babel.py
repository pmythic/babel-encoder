#pyright: basic
import argparse
import random
import string
import sys

# --- Algorithm -----------------------------------------------------------
#
# Printable ASCII runs from chr(32) [space] to chr(126) [~], giving 95
# characters total.
#
# Encoding projects an arbitrarily large integer into the printable ASCII
# range using modulo arithmetic.
#
#   encode(n) = chr((n % 95) + 32)
#
# Decoding cannot uniquely recover n, because modulo discards information.
# Instead, decode represents the entire equivalence class:
#
#   decode(c) = (ord(c) - 32) + 95k
#
# where k is any nonnegative integer.
#
# These are inexact inverses:
#
#   encode(decode(c)) == c
#
# but generally:
#
#   decode(encode(n)) != n
#
# because many distinct integers map to the same encoded character.
# ------------------------------------------------------------------------

PRINTABLE_LO = 32
PRINTABLE_HI = 126

def babel_encode(t):
    concat = ''.join([str(ord(c)) for c in t]) # 3 characters concatenated, turned to a string. 
    t = int(concat) 
    t = (t % 95)
    t = t + PRINTABLE_LO
    return chr(t)

def babel_decode(t):
    target = ord(t) - PRINTABLE_LO
    concat = ''
    for a in range(PRINTABLE_LO, PRINTABLE_HI+1):
        for b in range(PRINTABLE_LO, PRINTABLE_HI+1):
            for c in range(PRINTABLE_LO, PRINTABLE_HI+1):
                concat = ''.join([str(a), str(b), str(c)])
                if int(concat) % 95 == target:
                    return chr(a)+chr(b)+chr(c)
    return concat

def babel(s, decoding=False, offset=0):
    res = ''
    if decoding:
        if offset:
            res += gen_offset(offset)
        for c in s:
            triple = babel_decode(c)
            res = res + triple

    else:
        res = ""
        for i in range(0, len(s), 3):
            res += babel_encode(s[i:i+3])

    return res

def gen_offset(n):
    """generate randomised offset string of length n"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', '--file', '--filename',
        action="store_true",
        dest='file_provided',
        help='Treat input as filename'
    )

    parser.add_argument(
        'input',
        nargs='+',
        help='File name (read in bytes), or input (depending on if -f flag set)'
    )

    decode_group = parser.add_argument_group('decoding')

    decode_group.add_argument(
        '-d', '--decode',
        action='store_true',
        help='Decode instead of encode'
    )

    decode_group.add_argument(
        '--offset',
        type=int,
        default=0,
        required=False,
        help='Reveal-offset when decoding'
    )

    args = parser.parse_args()

    if args.offset and not args.decode:
        parser.error("--offset requires --decode. Use it to 'reveal' a string after <offset> characters.")

    if args.file_provided:
        if not args.input:
            parser.error('-f requires a filename')
        with open(args.input[0], "rb") as f:
            text = f.read()
    elif args.input:
        text = " ".join(args.input)
    else:
        text = sys.stdin.read()

    out = babel(text, decoding=args.decode, offset=args.offset)
    print(out)
