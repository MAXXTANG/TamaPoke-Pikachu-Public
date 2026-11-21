#!/usr/bin/env python3
"""Decrypt the owner's AES-256-GCM device/archive backup without extracting it."""

import argparse
import base64
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


MAGIC = b"TAMAPOKE-AES256GCM-v1\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key-file", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; choose a new output path")
    key_data = json.loads(args.key_file.read_text())
    key = base64.b64decode(key_data["key_base64"], validate=True)
    data = args.input.read_bytes()
    if len(key) != 32 or not data.startswith(MAGIC) or len(data) < len(MAGIC) + 28:
        parser.error("invalid key or archive format")
    nonce_start = len(MAGIC)
    plaintext = AESGCM(key).decrypt(
        data[nonce_start : nonce_start + 12], data[nonce_start + 12 :], MAGIC
    )
    descriptor = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as output:
        output.write(plaintext)
    print(f"Decrypted and authenticated: {args.output}")


if __name__ == "__main__":
    main()
