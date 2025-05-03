# EC2 IMDS Enumerator
A comprehensive metadata enumeration tool for compromised AWS EC2 instances. This script leverages IMDSv2 to quickly retrieve critical instance, network, identity, and credential information directly from the instance metadata service.

## Features
- Automatically fetches and uses IMDSv2 token for secure metadata queries
- Falls back to `wget` if `curl` is unavailable
- Enumerates key metadata including instance ID, region, network interfaces, IAM roles, identity credentials, and scheduled events
- Extracts user data, SSH keys, and EC2 tags if exposed
- Displays output in a structured and readable format

## Prerequisites
- Script must be run on an EC2 instance
- Bash environment with either `curl` or `wget`

## Usage
```bash
chmod +x ec2-imds-enumerator.sh
./ec2-imds-enumerator.sh
```
## How It Works
- Retrieves an IMDSv2 session token via HTTP PUT
- Uses the token to access the metadata API at http://169.254.169.254/latest/
- Calls metadata endpoints to extract:
	- Instance metadata (ID, type, lifecycle, region)
	- Hostnames and network interfaces
	- IAM and identity credentials
	- SSH public keys and EC2 instance tags
	- User data and block device mappings
- Organizes and prints the metadata to terminal for analysis

## Output Example
===== EC2 Metadata Summary =====
ami-id: ami-0f123abcde4567890
instance-id: i-0a12b3456cdef7890
instance-type: t3.medium
instance-life-cycle: on-demand
instance-action: none
region: us-west-2

===== Hostnames =====
hostname: ip-10-0-0-5.ec2.internal
local-hostname: ip-10-0-0-5.ec2.internal

===== Account & Instance Identity =====
--- dynamic/instance-identity/document ---
{
  "accountId" : "123456789012",
  "architecture" : "x86_64",
  "availabilityZone" : "us-west-2a",
  "imageId" : "ami-0f123abcde4567890",
  "instanceId" : "i-0a12b3456cdef7890",
  ...
}

===== Identity-Credentials (if available) =====
Identity path: ec2/
Identity Role: ec2-instance
{
  "AccessKeyId" : "ASIAEXAMPLEKEYID1234",
  "SecretAccessKey" : "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "Token" : "FwoGZXIvYXdzEHYaDABEXAMPLESESSIONTOKEN",
  "Expiration" : "2025-05-04T18:07:46Z"
}

===== User Data =====
user-data: #!/bin/bash
echo "A script with sensitive data"
...

## Contributing
If you have an idea for improvement or wish to collaborate, feel free to contribute.

## Disclaimer
Use responsibly. This tool is intended for red teamers, security auditors, and penetration testers with proper authorization.