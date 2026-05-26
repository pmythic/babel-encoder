#pyright: basic
import argparse
import random
import string
import sys

# algorithm needs to be
# deterministic, reversible, simple enough to explain quickly
# algorithm does not need to be
# cryptographically secure

# ignore the offset - that's just used for 'big reveals'

"""
algorithm needs to take units of the input, string or not, perform something
to the units, then return
"""

def babel_encode(t):
    pass

def babel_decode(t):
    pass

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
