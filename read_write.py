from dotenv import load_dotenv
import os
import hvac

# Vault connection details
VAULT_ADDR = os.getenv("VAULT_ADDR") # Replace with your Vault container's address
VAULT_TOKEN = os.getenv("VAULT_TOKEN") # Replace with your Vault token (e.g., root token or an authenticated token)

# Initialize the Vault client
client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

# Verify authentication
if client.is_authenticated():
    print("Successfully authenticated to Vault.")
else:
    print("Authentication failed. Check VAULT_ADDR and VAULT_TOKEN.")
    exit()

# Define the path and data for the secret
secret_path = 'secret/my-app/database'  # Example path
secret_data = {'username': 'myuser', 'password': 'mysecurepassword'}

# Write the secret
try:
    client.secrets.kv.v2.create_or_update_secret(
        mount_point='secret',  # Assuming 'secret' is your KV v2 secrets engine mount point
        path=secret_path,
        secret=secret_data,
    )
    print(f"Secret written successfully to: {secret_path}")
except hvac.exceptions.VaultError as e:
    print(f"Error writing secret: {e}")

# Read the secret
try:
    read_response = client.secrets.kv.v2.read_secret_version(
        mount_point='secret',
        path=secret_path,
    )
    retrieved_data = read_response['data']['data']
    print(f"Secret retrieved from {secret_path}:")
    print(f"  Username: {retrieved_data['username']}")
    print(f"  Password: {retrieved_data['password']}") # Be cautious when printing sensitive data
except hvac.exceptions.VaultError as e:
    print(f"Error reading secret: {e}")