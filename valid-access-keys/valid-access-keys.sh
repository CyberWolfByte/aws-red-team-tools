#!/bin/bash

# Load or prompt for secret access key
if [[ -z "$SECRET_ACCESS_KEY" ]]; then
    read -s -p "Enter the AWS Secret Access Key: " SECRET_ACCESS_KEY
    echo ""
fi

MATCH_FOUND=0
echo "[*] Starting search for matching access key..."

# List all users
USER_LIST=$(aws iam list-users --query 'Users[*].UserName' --output text)

# Loop through each IAM user
for user in $USER_LIST; do
    [[ "$user" =~ ^[a-zA-Z0-9+,.@_-]+$ ]] || continue
    echo "[*] Checking user: $user"

    # List access keys
    ACCESS_KEYS=$(aws iam list-access-keys --user-name "$user" --query 'AccessKeyMetadata[*].AccessKeyId' --output text)

    for key_id in $ACCESS_KEYS; do
        echo "    [-] Trying Access Key ID: $key_id for user: $user"

        # Use temporary credentials inline
        RESPONSE=$(AWS_ACCESS_KEY_ID="$key_id" AWS_SECRET_ACCESS_KEY="$SECRET_ACCESS_KEY" aws sts get-caller-identity 2>&1)

        if [[ "$RESPONSE" == *"SignatureDoesNotMatch"* ]]; then
            echo "    [x] Signature does not match for key: $key_id"
        elif [[ "$RESPONSE" == *"AccessDenied"* ]]; then
            echo "    [x] Access denied — valid key but insufficient permissions"
        elif [[ "$RESPONSE" == *"error"* || "$RESPONSE" == *"Exception"* ]]; then
            echo "    [x] Unexpected error occurred for key: $key_id"
        else
            echo "[+] Match found!"
            echo "    The secret access key belongs to user: $user with Access Key ID: $key_id"
            MATCH_FOUND=1
            break 2
        fi
    done
done

# Final message
if [[ "$MATCH_FOUND" -eq 0 ]]; then
    echo "[!] No match found for the provided secret access key."
fi

# Always clean up secret from memory
unset SECRET_ACCESS_KEY