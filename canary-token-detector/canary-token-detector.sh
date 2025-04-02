#!/bin/bash

# Prompt for AWS credentials and region
read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -s -p "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo ""
read -p "Enter AWS Region (e.g. us-east-1): " AWS_REGION

# Export creds for use only in this session
export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION

echo "[*] Sending test SNS message to trigger identity resolution..."

# Use an intentionally invalid phone number to trigger a permission error
RESPONSE=$(aws sns publish --message "whoami" --phone-number "1234567890" --region "$AWS_REGION" 2>&1)

# Analyze output
if echo "$RESPONSE" | grep -q "AuthorizationError"; then
    USER_ARN=$(echo "$RESPONSE" | grep -oP 'User: \K[^ ]+')
    echo "[+] Match found (canary token detected): $USER_ARN"
    echo ""
    echo "[*] Raw error output: $RESPONSE"
elif echo "$RESPONSE" | grep -q "SignatureDoesNotMatch"; then
    echo "[-] Invalid credentials: Signature does not match"
elif echo "$RESPONSE" | grep -q "AccessDenied"; then
    echo "[-] Valid key, but access denied"
else
    echo "[-] Unexpected response:"
    echo "$RESPONSE"
fi

# Cleanup credentials
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION