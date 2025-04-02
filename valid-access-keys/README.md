# Access Keys Validator
A Bash script that helps identify which AWS IAM user an unknown **secret access key** belongs to. This tool is useful during AWS penetration tests, CTFs, or internal audits where an access key must be matched to a user account without using hardcoded profiles or affecting existing credential configurations.

## Features
- Enumerates all IAM users and their associated access keys
- Attempts to match the provided secret access key with every listed access key
- Provides detailed status for each match attempt

## Usage

```bash
chmod +x access-keys-validator.sh
./access-keys-validator.sh
```
## Prerequisites
Make sure you have assumed a role or configured a profile with sufficient permissions to:
    List IAM users (iam:ListUsers)
    List access keys (iam:ListAccessKeys)

**Note**: The script uses inline credentials for testing. It will not overwrite your configured AWS profiles.

## How It Works
- Prompts the user to enter a secret access key
- Lists all IAM users in the current AWS account
- For each user, lists their access key IDs
- Attempts to call `sts get-caller-identity` using each access key and the provided secret
- If a match is successful, it prints the corresponding username and access key ID
- Terminates when a valid match is found

## Output Example
```
# Enter the AWS Secret Access Key: 
# [*] Starting search for matching access key...
# [*] Checking user: admin
# [*] Checking user: alex
# [*] Checking user: ansible
# [*] Checking user: ashish
# [*] Checking user: automation
#     [-] Trying Access Key ID: XXXXXXXXXXXXXXXXXXXX for user: automation
#     [x] Signature does not match for key: XXXXXXXXXXXXXXXXXXXX
# [*] Checking user: support
#     [-] Trying Access Key ID: ZZZZZZZZZZZZZZZZZZZZ for user: support
# [+] Match found!
#     The secret access key belongs to user: support with Access Key ID: ZZZZZZZZZZZZZZZZZZZZ
```

## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.