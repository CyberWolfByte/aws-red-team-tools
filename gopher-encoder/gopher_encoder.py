#!/usr/bin/env python3

import argparse
import urllib.parse
import sys


def custom_url_encode(raw_gopher: str) -> str:
    raw_gopher = raw_gopher.strip()

    if not raw_gopher.startswith("gopher://"):
        raise ValueError("Input must start with 'gopher://'")

    # Split into lines
    lines = raw_gopher.splitlines()
    request_line = lines[0]
    headers = lines[1:]

    # Parse scheme + initial payload separator
    scheme_end = request_line.find('/_')
    if scheme_end == -1:
        raise ValueError("Invalid Gopher request: missing '/_'")

    scheme_part = request_line[:scheme_end + 2]  # gopher://.../_
    data_part = request_line[scheme_end + 2:]    # Everything after '/_'

    encoded_scheme = urllib.parse.quote(scheme_part, safe='')

    # Double-encode the payload
    encoded_data = urllib.parse.quote(data_part, safe='')
    encoded_data = urllib.parse.quote(encoded_data, safe='')

    # Append CRLF after request line
    encoded_data += "%250D%250A"

    # Process headers
    encoded_headers = ""
    for header in headers:
        if ':' in header:
            key, value = header.split(':', 1)
            key_enc = urllib.parse.quote(key.strip(), safe='')

            # Preserve space after colon DO NOT strip() the value
            value_preserved = value if value.startswith(
                ' ') else ' ' + value  # ensure space
            value_enc = urllib.parse.quote(value_preserved, safe='')
            # double encode space and text
            value_enc = urllib.parse.quote(value_enc, safe='')

            encoded_headers += f"{key_enc}%3A{value_enc}%250D%250A"
        else:
            line_enc = urllib.parse.quote(header.strip(), safe='')
            encoded_headers += f"{line_enc}%250D%250A"

    return encoded_scheme + encoded_data + encoded_headers


def read_input(args) -> str:
    if args.file:
        with open(args.file, 'r') as f:
            return f.read()
    elif args.stdin:
        print("Paste the raw Gopher request (end with Ctrl+D):")
        input_data = sys.stdin.read()
        if not input_data.endswith('\n'):
            print()
        return input_data
    elif args.raw:
        return args.raw
    else:
        raise ValueError("No valid input source provided.")


def main():
    parser = argparse.ArgumentParser(
        description="Encode raw Gopher request to AWS IMDSv2-safe URL format.")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-f', '--file', help='Path to file containing raw Gopher request')
    group.add_argument('-s', '--stdin', action='store_true',
                       help='Read raw Gopher request from terminal')

    parser.add_argument(
        'raw', nargs='?', help='Raw Gopher request as a single argument string')
    parser.add_argument(
        '-o', '--output', help='Write encoded output to file instead of stdout')
    args = parser.parse_args()

    if not args.file and not args.stdin and not args.raw:
        parser.error(
            "You must provide a raw Gopher request via argument, --file, or --stdin")

    try:
        raw_input = read_input(args)
        encoded = custom_url_encode(raw_input)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(encoded)
            print(f"[+] Encoded Gopher request written to: {args.output}")
        else:
            print(encoded)

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
