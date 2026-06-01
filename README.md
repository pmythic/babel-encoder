# Babel

A deterministic encoder inspired by Borges, normal numbers, and the possibility that every text already exists somewhere.

---

## Overview

Babel is a command-line encoding tool that transforms arbitrary data into streams of printable ASCII characters using a deterministic, sort-of-reversible mapping.

The central idea is simple:

- Infinite sequences can contain arbitrary information.
- A deterministic encoding can map raw data into apparently-random symbolic streams.
- Somewhere within sufficiently large structures, every possible finite text may already exist.

Babel explores this idea using:
- printable ASCII transformations,
- deterministic stream mappings,
- offset-based decoding,
- and infinite numeric sequences such as π.

---

## Features

- Deterministic reversible encoding
- Printable ASCII-only output
- File or text input
- Offset-based decoding/reveals
- Stream-based transformation model
- Designed for experimentation and philosophical exploration

---

## Installation

Clone the repository:

```bash
git clone https://github.com/pmythic/babel-encoder.git
cd babel-encoder
```

No external dependencies are currently required.

---

## Usage

### Encode text

```bash
python3 babel.py "hello world"
```

### Encode a file

```bash
python3 babel.py -f document.txt
```

### Decode data

```bash
python3 babel.py --decode "X!a92m..."
```

### Decode with an offset

```bash
python3 babel.py --decode --offset 50000 "X!a92m..."
```

### Encode pi to n digits

```bash
python3 babel.py --pi 1000
```

---

## Command-Line Options

| Option | Description |
|---|---|
| `-f`, `--filename` | Interpret input as a file path |
| `--decode` | Decode instead of encode |
| `--offset N` | Apply deterministic stream offset |
| `-h`, `--help` | Show help message |
| `-pi`, `--pi` | Use pi to a specified number of digits|

---

## Philosophy

Babel is inspired by:

- Jorge Luis Borges’ *The Library of Babel*, 1941.
- deterministic chaos
- emergence and computability

An encoded stream may appear meaningless, while still deterministically containing recoverable structure.

---

## Important Note

Babel is **NOT intended to be cryptographically secure**.

Although the output may resemble ciphertext, the project is designed for:
- artistic experimentation,
- encoding theory demonstrations,
- deterministic symbolic mapping,
- and educational/philosophical purposes.

Do not use it to protect sensitive information.

---

## License

MIT License
