#!/bin/bash

# === Retrieve IMDSv2 Token ===
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" 2>/dev/null || \
  wget -q -O - --method PUT "http://169.254.169.254/latest/api/token" \
  --header "X-aws-ec2-metadata-token-ttl-seconds: 21600" 2>/dev/null)

HEADER="X-aws-ec2-metadata-token: $TOKEN"
BASE_URL="http://169.254.169.254/latest"

# === Fetch Function (curl or wget) ===
if command -v curl &>/dev/null; then
    fetch() {
        local path="$1"
        local tmpfile=$(mktemp)
        local status=$(curl -s -w "%{http_code}" -H "$HEADER" "$BASE_URL/$path" -o "$tmpfile")
        if [[ "$status" == "404" || "$status" == "403" ]]; then
            echo "No Results"
        else
            cat "$tmpfile"
        fi
        rm -f "$tmpfile"
    }
elif command -v wget &>/dev/null; then
    fetch() {
        local path="$1"
        local tmpfile=$(mktemp)
        local status=$(wget -q --server-response --header "$HEADER" "$BASE_URL/$path" -O "$tmpfile" 2>&1 | awk '/^  HTTP/{print $2}' | tail -1)
        if [[ "$status" == "404" || "$status" == "403" ]]; then
            echo "No Results"
        else
            cat "$tmpfile"
        fi
        rm -f "$tmpfile"
    }
else
    echo "Neither curl nor wget found. Cannot enumerate metadata."
    exit 1
fi

echo -e "\n===== EC2 Metadata Summary ====="
for key in ami-id instance-id instance-type instance-life-cycle instance-action; do
    val=$(fetch "meta-data/$key")
    echo "$key: $val"
done

region=$(fetch "meta-data/placement/region")
echo "region: $region"

echo -e "\n===== Hostnames ====="
echo "hostname: $(fetch meta-data/hostname)"
echo "local-hostname: $(fetch meta-data/local-hostname)"

echo -e "\n===== Account & Instance Identity ====="
doc=$(fetch "dynamic/instance-identity/document")
echo -e "--- dynamic/instance-identity/document ---\n$doc"

info=$(fetch "meta-data/identity-credentials/ec2/info")
echo -e "\n--- identity-credentials/ec2/info ---\n$info"

echo -e "\n===== Network Interfaces ====="
for mac in $(fetch "meta-data/network/interfaces/macs/" | grep -v "No Results"); do
  echo "Interface: $mac"
  for attr in owner-id public-hostname security-groups ipv4-associations/ ipv6s \
              subnet-ipv4-cidr-block subnet-ipv6-cidr-blocks public-ipv4s \
              vpc-id vpc-ipv4-cidr-block vpc-ipv6-cidr-blocks vpc-ephemeral-ip-associations \
              interface-id device-number vpc-endpoint-ids; do
    val=$(fetch "meta-data/network/interfaces/macs/${mac}${attr}")
    echo "$attr: $val"
  done
  echo ""
done

echo -e "\n===== Top-Level Security Groups ====="
echo "$(fetch meta-data/security-groups)"

echo -e "\n===== IAM Role Credentials (if available) ====="
if [[ "$(fetch 'meta-data/iam/')" != "No Results" ]]; then
  iam_info=$(fetch "meta-data/iam/info")
  echo -e "iam/info:\n$iam_info\n"
  for role in $(fetch "meta-data/iam/security-credentials/" | grep -v "No Results"); do
    echo "IAM Role: $role"
    fetch "meta-data/iam/security-credentials/$role"
    echo ""
  done
else
  echo "IAM role info not available."
fi

echo -e "\n===== Identity-Credentials (if available) ====="
IC_BASE="meta-data/identity-credentials/"
if [[ "$(fetch "$IC_BASE")" != "No Results" ]]; then
  for path in $(fetch "$IC_BASE"); do
    echo "Identity path: $path"
    for role in $(fetch "$IC_BASE$path/security-credentials/" | grep -v "No Results"); do
      echo "Identity Role: $role"
      fetch "$IC_BASE$path/security-credentials/$role"
      echo ""
    done
  done
else
  echo "No identity-credentials directory."
fi

echo -e "\n===== Block Device Mapping ====="
devices=$(fetch "meta-data/block-device-mapping/")
for d in $devices; do
  echo "$d: $(fetch "meta-data/block-device-mapping/$d")"
done

echo -e "\n===== Scheduled Maintenance Events ====="
events=$(fetch "meta-data/events/maintenance/scheduled")
echo "Scheduled Events: $events"

echo -e "\n===== SSH Public Keys ====="
keys=$(fetch "meta-data/public-keys/")
if [[ "$keys" != "No Results" ]]; then
  for idx in $(echo "$keys" | cut -d= -f1); do
    key_val=$(fetch "meta-data/public-keys/$idx/openssh-key")
    echo "Key $idx: $key_val"
  done
else
  echo "No public keys"
fi

echo -e "\n===== EC2 Tags (if exposed) ====="
tag_keys=$(fetch "meta-data/tags/instance")
if [[ "$tag_keys" != "No Results" ]]; then
  for tag in $tag_keys; do
    val=$(fetch "meta-data/tags/instance/$tag")
    echo "$tag: $val"
  done
else
  echo "No instance tags or tag access disabled."
fi

echo -e "\n===== User Data ====="
udata=$(fetch "user-data")
echo "user-data: $udata"
