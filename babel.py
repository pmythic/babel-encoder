import argparse
import random
import string
import sys
import subprocess
import os
from pathlib import Path
from chudnovsky import pi_chudnovsky

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

def babel_encode(t: str) -> str:
    concat = ''.join([str(ord(c)) for c in t]) # 3 characters concatenated, turned to a string. 
    ic = int(concat) 
    ic = (ic % 95)
    ic = ic + PRINTABLE_LO
    return chr(ic)


def babel_decode(t: str, num_candidates: int = 5) -> str:
    target = ord(t) - PRINTABLE_LO
    candidates: list[str] = []
    seen: set[tuple[int, int]] = set()
 
    # Randomly sample (a, b) pairs and find a valid c for each.
    # ~70-90% of random pairs have a valid c, so this converges quickly.
    for _ in range(num_candidates * 20):
        if len(candidates) >= num_candidates:
            break
        a = random.randint(PRINTABLE_LO, PRINTABLE_HI)
        b = random.randint(PRINTABLE_LO, PRINTABLE_HI)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        for c in range(PRINTABLE_LO, PRINTABLE_HI + 1):
            if int(str(a) + str(b) + str(c)) % 95 == target:
                candidates.append(chr(a) + chr(b) + chr(c))
                break
 
    if candidates:
        return random.choice(candidates)
 
    # Fallback: deterministic search (always finds a result)
    for a in range(PRINTABLE_LO, PRINTABLE_HI + 1):
        for b in range(PRINTABLE_LO, PRINTABLE_HI + 1):
            for c in range(PRINTABLE_LO, PRINTABLE_HI + 1):
                if int(str(a) + str(b) + str(c)) % 95 == target:
                    return chr(a) + chr(b) + chr(c)
    return ''




def babel(s: str, decoding: bool = False, offset: int = 0) -> str:
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

def gen_offset(n: int) -> str:
    """generate randomised offset string of length n"""
    alphabet: str = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=n))

def gen_pi_py(n: int) -> str:
    """generate n digits of pi. Use Chudnovsky's formula via a simple python implementation"""
    return pi_chudnovsky(n)


def gen_pi_c(n: int) -> str:
    """generate n digits of pi. Use Chudnovsky's formula via a C program"""
    root = Path(__file__).parent

    src_path = root / 'chudnovsky.c'
    bin_path = root / 'chudnovsky'

    if (not bin_path.exists()) or src_path.stat().st_mtime > bin_path.stat().st_mtime:
        _ = subprocess.run(['make', 'clean'], check=True)
        _ = subprocess.run(['make'], check=True)
    digits = subprocess.run(['make', 'run', f'N={str(n)}'], capture_output=True, text=True, check=True)
    return digits.stdout.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    exclusive_group = parser.add_mutually_exclusive_group()
    _ = exclusive_group.add_argument(
        '-p', '-pi', '--pi',
        type=int,
        dest='pi',
        help='Use <input> digits of pi for encoding'
    )

    _ = exclusive_group.add_argument(
        '-f', '--file', '--filename',
        action="store_true",
        dest='file_provided',
        help='Treat input as filename'
    )

    _ = parser.add_argument(
        'input',
        nargs='*', 
        help='File name (read in bytes), or input (depending on if -f flag set)'
    )

    decode_group = parser.add_argument_group('decoding')

    _ = decode_group.add_argument(
        '-d', '--decode',
        action='store_true',
        help='Decode instead of encode'
    )

    _ = decode_group.add_argument(
        '--offset',
        type=int,
        default=0,
        required=False,
        help='Prepend N random chars to decoded output for a reveal effect. Must be a multiple of 3 (auto-rounded down if not).'
    )

    args = parser.parse_args()
    text = ''

    if args.offset and not args.decode:
        parser.error("--offset requires --decode. Use it to 'reveal' a string after <offset> characters.")

    if args.pi is not None:
        # pi is intended to be mutually exclusive with everything else
        if args.file_provided or args.decode or args.input:
            parser.error("--pi is mutually exclusive with file input, decoding, offset, and normal input")
        try:
            if args.pi < 3:
                parser.error("pi must have >3 digits")
            text = "".join(gen_pi_py(args.pi))
        except Exception as e:
            parser.error(f"pi encoding failed: {e}")
    else:
        if args.file_provided:
            if not args.input:
                parser.error('-f requires a filename')
            with open(args.input[0], "rb") as f:
                text = f.read().decode("utf-8", errors="replace").removesuffix('\n')
        elif args.input:
            text = " ".join(args.input)
            if len(text) < 3:
                parser.error('input must at least 3 characters')
        else:
            if not os.isatty(0):
                text = sys.stdin.read().removesuffix('\n')
            else:
                if not args.input:
                    parser.error("input not provided")

    if args.offset % 3 != 0:
        adjusted = (args.offset // 3) * 3
        print(f"\nWarning: offset {args.offset} is not a multiple of 3 — rounding down to {adjusted}.\n", file=sys.stderr)
        args.offset = adjusted

    out = babel(text, decoding=args.decode, offset=args.offset)
    print(out)
