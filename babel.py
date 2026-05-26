#pyright: basic
import argparse
import random
import string
import sys

# --- Algorithm -----------------------------------------------------------
#
# Printable ASCII runs from chr(32) [space] to chr(126) [~], giving 95
# characters. We treat these as a ring and shift every character by SHIFT
# positions using modular arithmetic.
#
#   encode(c) = chr( ((ord(c) - 32 + SHIFT) % 95) + 32 )
#   decode(c) = chr( ((ord(c) - 32 - SHIFT) % 95) + 32 )
#
# These are exact inverses: decode(encode(c)) == c for all printable ASCII.
# Non-printable characters are passed through unchanged.
#
# The shift is 47, roughly half of 95m so the mapping has no obvious
# fixed points and looks nicely scrambled.

SHIFT = 47
PRINTABLE_LO = 32
PRINTABLE_HI = 126

def babel_encode(t):
    t = int(''.join([str(ord(c)) for c in t])) # 3 characters concatenated, turned to a string. 
    t = (t % 95)
    t = t + 32
    return chr(t)

def babel_decode_as_triple(t):
    """ hacky workaround, not perfectly reversible, but creates a valid preimage """
    target = ord(t) - 32

    for a in range(32, 127):
        for b in range(32, 127):

            prefix = str(a) + str(b)

            for c in range(32, 127):
                n = int(prefix + str(c))

                if n % 95 == target:
                    return chr(a) + chr(b) + chr(c)

def babel(s, decoding=False, offset=0):
    res = ''
    if decoding:
        if offset:
            res += gen_offset(offset)
        for i, c in enumerate(s):
            pass
    else:
        for i, c in enumerate(s):
            pass

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
