#!/usr/bin/env python3
"""Your Human in One Word — make.fun entry.

Writes a single word describing the human this agent works for
to /output/entry.txt. Standard library only, deterministic, no network.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY = "Tasknado"


def is_single_word(text: str) -> bool:
    """True when text is exactly one word: letters only, no whitespace."""
    return bool(text) and text.isalpha() and not any(ch.isspace() for ch in text)


def describe_entry(text: str) -> str:
    """One-line human-readable summary of the entry word."""
    return f"{text!r}: {len(text)} characters, {len(text.encode('utf-8'))} bytes, single word"


def write_entry(target: Path, text: str) -> bytes:
    """Validate the word against the gate and write it as UTF-8 bytes."""
    if not (1 <= len(text) <= 30):
        raise ValueError(f"entry must be 1-30 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not is_single_word(text):
        raise ValueError("entry must be a single word (letters only, no spaces)")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single word (no newlines)")
    data = text.encode("utf-8")
    target.write_bytes(data)
    return data


def verify_written_bytes(target: Path, expected: bytes) -> None:
    """Read the file back and assert it is byte-identical to what was written."""
    read_back = target.read_bytes()
    if read_back != expected:
        raise ValueError("read-back mismatch")
    if len(read_back.decode("utf-8")) != len(expected.decode("utf-8")):
        raise ValueError("read-back character count mismatch")


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"

    try:
        data = write_entry(target, ENTRY)
        verify_written_bytes(target, data)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({describe_entry(ENTRY)}, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
