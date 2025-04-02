import boto3
from botocore.exceptions import ClientError
import getpass
import os

def prompt_credentials():
    # Load from env if set, else prompt
    access_key = os.getenv("AWS_ACCESS_KEY_ID") or input("Enter AWS Access Key ID: ").strip()
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY") or getpass.getpass("Enter AWS Secret Access Key: ").strip()
    region = os.getenv("AWS_REGION") or input("Enter AWS Region (e.g. us-west-2): ").strip()
    return access_key, secret_key, region

def verify_principal(access_key, secret_key, region):
    try:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        sns_client = session.client("sns")
        sns_client.publish(Message="test", PhoneNumber="invalid-number")
    except ClientError as e:
        msg = str(e)
        if "not authorized to perform" in msg:
            return True, msg.split("User: ")[1].split(" is not authorized")[0]
        if "does not match the signature" in msg:
            return False, "Invalid credentials"
        if "status code: 403" in msg:
            return False, "Access denied"
        return False, f"Error: {msg}"
    return False, "Verification failed"

if __name__ == "__main__":
    access_key, secret_key, region = prompt_credentials()
    success, result = verify_principal(access_key, secret_key, region)
    print(f"{'[+] Match:' if success else '[-]'} {result}")