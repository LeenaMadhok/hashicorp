import hvac
from dotenv import load_dotenv
import os

# Mount point is 'my' — KV v1
# Vault connection details
VAULT_ADDR = os.getenv("VAULT_ADDR") # Replace with your Vault container's address
VAULT_TOKEN = os.getenv("VAULT_TOKEN") # Replace with your Vault token (e.g., root token or an authenticated token)
MOUNT_POINT = 'my_v1'
SECRET_PATH = 'path'  # Adjust if you want a subpath, e.g., 'app/config'

# Initialize the Vault client
client = hvac.Client(
    url=VAULT_ADDR,
    token=VAULT_TOKEN
)

def create_secret():
    """
    Create or update a secret at 'my_v1/path'
    """
    secret_data = {
        'username': 'admin',
        'password': 'supersecret123'
    }

    client.secrets.kv.v1.create_or_update_secret(
        path=SECRET_PATH,
        secret=secret_data,
        mount_point=MOUNT_POINT
    )

    print(f"Secret written to {MOUNT_POINT}/{SECRET_PATH}")

def read_secret():
    """
    Read and return the secret from 'my/path'
    """
    read_response = client.secrets.kv.v1.read_secret(
        path=SECRET_PATH,
        mount_point=MOUNT_POINT
    )

    secret_data = read_response['data']
    print(f"Secret read from {MOUNT_POINT}/{SECRET_PATH}: {secret_data}")
    return secret_data

# --- Main Execution ---
if client.is_authenticated():
    print("Vault auth successful\n")

    create_secret()
    read_secret()
else:
    print("Vault auth failed")
