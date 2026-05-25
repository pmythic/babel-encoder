#pyright: basic
import argparse

def babel_encode(t):
    concatenated = int("".join([str(ord(c)) for c in t]))
    reduced = concatenated % 95
    result = reduced + 32 
    return chr(result)

def babel(s):
    encoded = ""
    for i in range(0, len(s), 3):
        encoded = encoded + str(babel_encode(s[i:i+3]))

    return "".join(encoded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "input",
            help="text input or filename"
    )

    parser.add_argument(
            "-f",
            "--file",
            action="store_true",
            help="Treat input as a filename"
    )

    args = parser.parse_args()

    if args.file:
        with open(args.input, "r") as f:
            text = f.read()
            out = babel(text)
    else:
        out = babel(args.input)

    print(out)
