# Canary Token Detector
Canary Token Detector is a lightweight security tool for identifying AWS IAM credentials that may be monitored or booby-trapped via **canary tokens**. These canaries, when triggered, alert defenders about unauthorized credential usage often leaking the IAM identity in error messages.

This tool tests AWS Access Key and Secret Access Key combinations against AWS SNS to trigger authorization failures that may reveal the principal identity.

Supports both **Python** and **Bash** implementations:
- `canary-token-detector.py`
- `canary-token-detector.sh`

## Features
- Avoids saving credentials to disk or history
- Triggers `sns:Publish` with an invalid number to produce identity-leaking error messages
- Detects canary-style `AuthorizationError` responses
- Extracts and displays the IAM principal (User or Role) when exposed

## Usage
```bash
# Python 
python3 canary-token-detector.py

# Bash
chmod +x canary-token-detector.sh
./canary-token-detector.sh
```

## How It Works
- Prompts user for AWS credentials and region
- Attempts to publish a dummy SNS message to an invalid phone number
- If a canary token or trap credential is used, AWS may return an AuthorizationError containing the calling identity
- The script extracts and reports this identity as a potential match
- Credentials are kept in memory only and cleared after use

## Output Examples
```
# Python
[+] Match: arn:aws:iam::121110987654:user/canarytokens.com@@0a1bcd1efg2hij3lmnopkwzxy

# Bash
[*] Sending test SNS message to trigger identity resolution...
[+] Match found (canary token detected): arn:aws:iam::121110987654:user/canarytokens.com@@0a1bcd1efg2hij3lmnopkwzxy

[*] Raw error output:
An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:iam::121110987654:user/canarytokens.com@@0a1bcd1efg2hij3lmnopkwzxy is not authorized to perform: SNS:Publish on resource: 1234567890 because no identity-based policy allows the SNS:Publish action
```

## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.

## Disclaimer Use responsibly. This tool is intended for red teamers, security auditors, and penetration testers with proper authorization.