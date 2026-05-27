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
    t = int(''.join([str(ord(c)) for c in t])) # 3 characters concatenated, turned to a string. 
    t = (t % 95)
    t = t + PRINTABLE_LO
    return chr(t)

def babel_decode_as_triple(t) -> str:
    """ hacky workaround, not perfectly reversible, but creates a valid preimage """
    target = ord(t) - PRINTABLE_LO

    for a in range(PRINTABLE_LO, PRINTABLE_HI+1):
        for b in range(PRINTABLE_LO, PRINTABLE_HI+1):

            prefix = str(a) + str(b)

            for c in range(PRINTABLE_LO, PRINTABLE_HI+1):
                n = int(prefix + str(c))

                if n % 95 == target:
                    return ''.join([chr(a), chr(b), chr(c)])

    return ''

def babel(s, decoding=False, offset=0):
    res = ''
    if decoding:
        pad_len = ord(s[0]) - 32
        s = s[1:]

        if offset:
            res += gen_offset(offset)
        for c in s:
            res += babel_decode_as_triple(c)
        if pad_len:
            res = res[:-pad_len]

    else:
        pad_len = (3 - (len(s) % 3)) % 3
        s_padded = s + (" " * pad_len)

        res = ""
        for i in range(0, len(s_padded), 3):
            res += babel_encode(s_padded[i:i+3])

        # prepend padding metadata as a single character
        res = chr(pad_len + 32) + res
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
