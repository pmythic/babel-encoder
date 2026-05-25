#pyright: basic
import argparse

def babel_encode(t):
    a = (t // 95)+32
    b = (t % 95)+32
    return ''.join([chr(a), chr(b)])

def babel_decode(t):
    a = ord(t[0]) - 32
    b = ord(t[1]) - 32

    return str(a * 95 + b).zfill(2)

def generate_offset_stream(l):
    return ("TEMP_STREAM" * l)

def babel(s, decoding=False, offset=0):
    res = ""
    if decoding:
        o_stream = generate_offset_stream(offset)
        for i in range(0, len(s), 2):
            res = res + str(babel_decode(s[i:i+2]))
    else:
        for i in range(0, len(s), 2):
            res = res + str(babel_encode(s[i:i+2]))

        return "".join(res)

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
        help='Decode flag instead of encode'
    )

    decode_group.add_argument(
        '--offset',
        type=int,
        default=0,
        required=False,
        help='Reveal offset when decoding'
    )

    args = parser.parse_args()

    if args.offset and not args.decode:
        parser.error("--offset requires --decode")

    if args.file_provided:
        with open(args.input[0], "rb") as f:
            text = f.read()
            out = babel(text, decoding=args.decode, offset=args.offset)
    else:
        text = " ".join(args.input)
        out = babel(text, decoding=args.decode, offset=args.offset)
