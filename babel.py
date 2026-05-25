import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', '--file', '--filename',
        dest='filename',
        help='File to encode/decode'
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Input string if no file is supplied'
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
        help='Reveal offset when decoding'
    )

    args = parser.parse_args()

    print(args)
