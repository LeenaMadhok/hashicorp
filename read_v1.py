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

    # Use kv.v1 for reading from KV v1 engine
    read_response = client.secrets.kv.v1.read_secret(
        path='path',         # <- 'my/path' means 'path' under 'my/' mount
        mount_point='my_v1'
    )

    print("Secret data:", read_response['data'])

else:
    print("Vault auth failed")
