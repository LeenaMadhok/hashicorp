from dotenv import load_dotenv
import os
import hvac

# Vault connection details
VAULT_ADDR = os.getenv("VAULT_ADDR") # Replace with your Vault container's address
VAULT_TOKEN = os.getenv("VAULT_TOKEN") # Replace with your Vault token (e.g., root token or an authenticated token)

client = hvac.Client(
    url=VAULT_ADDR,
    token=VAULT_TOKEN
)

if client.is_authenticated():
    print("Vault auth successful")

    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path='path',          # just the secret path below 'my/'
            mount_point='my',     # your KV v2 mount point
            raise_on_deleted_version=True       # explicitly set to avoid warning
        )
        print("Secret data:", read_response['data']['data'])

    except hvac.exceptions.InvalidPath:
        print("Secret not found at 'my/path'. Please create it first!")

else:
    print("Vault auth failed")
