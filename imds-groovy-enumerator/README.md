# IMDSv2 Groovy Enumerator
IMDSv2 Groovy Enumerator is a script designed for use in Jenkins environments to extract metadata from AWS EC2 instances. It leverages the Instance Metadata Service v2 (IMDSv2) to enumerate IAM roles and temporary security credentials attached to the instance. Ideal for red teaming, cloud recon, or verifying instance roles in CI/CD pipelines.

## Features
- Retrieves a secure IMDSv2 session token for accessing instance metadata
- Dynamically detects and enumerates the attached IAM role
- Extracts temporary AWS credentials (AccessKeyId, SecretAccessKey, session Token)
- Captures and separates STDOUT and STDERR for debugging
- Modifiable for enumerating additional metadata paths (e.g., instance-id, ami-id)

## Prerequisites
- Jenkins 2.60+ (tested on 2.479.2)
- Jenkins node or master must be running inside an EC2 instance
- Script Console access or ability to run Groovy scripts with `cmd.execute()`

## Usage
- Paste the script into the **Jenkins Script Console** (`Manage Jenkins > Script Console`) and run it.

## How It Works
- Obtains a IMDSv2 token via a PUT request with a TTL of 6 hours.
- It queries the EC2 metadata service to retrieve the name of the attached IAM role.
- Fetches the full set of temporary credentials associated with that role.
- Logs both stdout and stderr for review or logging purposes in Jenkins.

## Output Example
```bash
STDOUT:
Token: AQAEEXAMPLEjht1cYOX7Q-zrwa1x2ZkPLQwn3zC9aQxuUow9Xu1o-sw==
Metadata (iam/security-credentials): Jenkins_Role
Full Response:
{
  "Code" : "Success",
  "LastUpdated" : "2025-04-04T12:54:17Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "ASIAEXAMPLE123456789",
  "SecretAccessKey" : "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "Token" : "FwoGZXIvYXdzEP///////////wEaDEexampletokenid5i/JqRz3NPhd0+...",
  "Expiration" : "2025-04-04T19:14:52Z"

STDERR:
```

## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.

## Disclaimer Use responsibly. This tool is intended for red teamers, security auditors, and penetration testers with proper authorization. Unauthorized use against AWS environments may violate terms of service or result in legal consequences.