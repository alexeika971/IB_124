import sys
import os
# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from file_io import read_file, write_file
from modes.ecb import encrypt_ecb, decrypt_ecb

def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="AES-128 ECB Encryption/Decryption Tool")

    parser.add_argument('-algorithm', required=True, choices=['aes'], help='Cipher algorithm (only "aes" is supported)')
    parser.add_argument('-mode', required=True, choices=['ecb'], help='Mode of operation (only "ecb" is supported)')
    parser.add_argument('-key', required=True, help='Hexadecimal key (32 hex characters for AES-128)')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-encrypt', action='store_true', help='Perform encryption')
    group.add_argument('-decrypt', action='store_true', help='Perform decryption')

    parser.add_argument('-input', required=True, help='Path to the input file')
    parser.add_argument('-output', help='Path to the output file (optional)')

    args = parser.parse_args()

    if len(args.key) != 32:
        print("Error: Key must be exactly 32 hexadecimal characters (16 bytes).", file=sys.stderr)
        sys.exit(1)
    try:
        key_bytes = bytes.fromhex(args.key)
    except ValueError:
        print("Error: Key must be a valid hexadecimal string.", file=sys.stderr)
        sys.exit(1)

    if not args.output:
        if args.encrypt:
            args.output = args.input + '.enc'
        else:
            args.output = args.input + '.dec'

    if os.path.isdir(args.output):
        print(f"Error: Output path '{args.output}' is a directory.", file=sys.stderr)
        sys.exit(1)

    return args, key_bytes

def main():
    """Main entry point for the CLI."""
    try:
        args, key_bytes = parse_arguments()

        try:
            data = read_file(args.input)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            if args.encrypt:
                result = encrypt_ecb(data, key_bytes)
            else:
                result = decrypt_ecb(data, key_bytes)
        except ValueError as e:
            print(f"Cryptographic error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error during processing: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            write_file(args.output, result)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"Operation completed successfully. Output written to: {args.output}")

    except KeyboardInterrupt:
        print("Operation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()