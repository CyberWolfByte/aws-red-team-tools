#!/usr/bin/env python3

import argparse
import urllib.parse
import json
import sys
from urllib.parse import urlencode

# Function to single encode a given URL
def url_encode(url: str) -> str:
    return urllib.parse.quote(url, safe='')

# Constructs the proxy URL with optional method and headers
def construct_proxy_url(proxy: str, target: str, method: str = None, headers: str = None) -> str:
    # Normalize the proxy input to avoid trailing '&' or '?'
    proxy = proxy.rstrip("?&")

    # Single encode the target URL once before embedding
    encoded_target = url_encode(target)

    # Detect existing query parameters (e.g., ?url= or ?target=)
    has_param_key = "=" in proxy and proxy.endswith("=")

    # Construct the base query parameter
    query_params = [] if has_param_key else [encoded_target]

    # Append method if provided
    if method and method.strip():
        query_params.append(method.strip())

    # Append headers if provided
    if headers and headers.strip():
        query_params.append(headers.strip())

    # Construct the query string
    query_string = "&".join(query_params)

    # Determine the correct separator ('?' or '&')
    separator = "&" if "?" in proxy else "?"

    # Construct the final proxy URL
    if has_param_key:
        # Embed the encoded target directly in the provided param key
        proxy_url = proxy + encoded_target + (f"&{query_string}" if query_string else "")
    else:
        # Construct the proxy URL normally
        proxy_url = f"{proxy}{separator}{query_string}"

    # Single encode the entire proxy URL to achieve the intended double encoding
    final_payload = url_encode(proxy_url)

    return final_payload

# Encodes the target URL within the proxy structure
def encode_ssrf_chain(target: str, proxy: str = None, method: str = None, headers: str = None) -> str:
    # Single encode the target URL
    single_encoded_target = url_encode(target)

    # Construct the proxy URL using the single encoded target
    if proxy:
        # Pass the original target (not single encoded) to avoid over-encoding
        final_payload = construct_proxy_url(proxy, target, method, headers)
    else:
        # Default to single encoded target if no proxy is provided
        final_payload = single_encoded_target

    return final_payload

# Recursively decodes a deeply encoded URL until fully resolved
def recursive_decode(encoded_url: str) -> str:
    previous = ""
    current = urllib.parse.unquote(encoded_url)

    # Continue decoding until the URL no longer changes
    while current != previous:
        previous = current
        current = urllib.parse.unquote(current)

    return current

# Main function to handle argument parsing and execution
def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="SSRF Encoder/Decoder for URL-encoded payloads."
    )

    # Mutually exclusive group to prevent --single and --decode from being used simultaneously
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--single", action='store_true', help="Single encode the target URL only")
    group.add_argument("--decode", action='store_true', help="Recursively decode the target URL")

    # Main arguments
    parser.add_argument("--target", help="Target URL to encode or decode (required)", required=True)
    parser.add_argument("--proxy", help="Proxy endpoint including parameter key, e.g., '?url=' or '?target='")
    parser.add_argument("--method", help="Optional method parameter as key=value, e.g., 'method=GET' or 'method=PUT'")
    parser.add_argument("--headers", help="Optional headers parameter as key=value, e.g., 'headers=X-aws-ec2-metadata-token-ttl-seconds=21600'")
    parser.add_argument("--output", help="Output file to save the encoded or decoded payload")
    parser.add_argument("--verbose", action='store_true', help="Verbose mode with step-by-step output")

    args = parser.parse_args()

    try:
        # Decode Mode
        if args.decode:
            # Perform recursive decoding
            decoded_output = recursive_decode(args.target)

            # Output to file or console
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(decoded_output)
                print(f"[+] Decoded output saved to: {args.output}")
            else:
                print(decoded_output)
            return

        # Single Encode Mode
        if args.single:
            # Perform single encoding
            encoded_output = url_encode(args.target)
        else:
            # Perform encoding with SSRF chain
            encoded_output = encode_ssrf_chain(
                target=args.target,
                proxy=args.proxy,
                method=args.method,
                headers=args.headers
            )

        # Output handling for encoded payload
        if args.output:
            with open(args.output, 'w') as f:
                f.write(encoded_output)
            print(f"[+] Payload saved to: {args.output}")
        else:
            print(encoded_output)

        # Verbose mode output for debugging and transparency
        if args.verbose:
            print("[INFO] Target URL encoded once:", url_encode(args.target))
            if args.proxy:
                # Display constructed proxy URL with single encoding applied
                print("[INFO] Proxy URL constructed:", construct_proxy_url(args.proxy, args.target, args.method, args.headers))
                print("[INFO] Final single encoded payload:", encoded_output)

    except Exception as e:
        # Error handling and output to stderr
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)

# Entry point for script execution
if __name__ == "__main__":
    main()
