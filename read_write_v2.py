import hvac

# Vault configuration
VAULT_ADDR = 'http://127.0.0.1:8200'
VAULT_TOKEN = 'hvs.N8FWxa08WjuGXHmGspkW9Dt0'  # replace with your token
MOUNT_POINT = 'my'  # KV v2 mount
SECRET_PATH = 'path'  # Relative path within the KV mount

# Initialize Vault client
client = hvac.Client(
    url=VAULT_ADDR,
    token=VAULT_TOKEN
)

def create_secret_v2():
    """
    Create or update a secret at the specified path using KV v2.
    """
    secret_data = {
        'key1': 'value1',
        'key2': 'value2'
    }

    client.secrets.kv.v2.create_or_update_secret(
        path=SECRET_PATH,
        secret=secret_data,
        mount_point=MOUNT_POINT
    )

    print(f"✅ Secret written to {MOUNT_POINT}/{SECRET_PATH}")


def read_secret_v2():
    """
    Read a secret from the specified path using KV v2.
    """
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path=SECRET_PATH,
            mount_point=MOUNT_POINT
        )

        secret_data = read_response['data']['data']
        print(f"✅ Secret read from {MOUNT_POINT}/{SECRET_PATH}: {secret_data}")
        return secret_data

    except hvac.exceptions.InvalidPath:
        print(f"❌ Secret not found at {MOUNT_POINT}/{SECRET_PATH}")
        return None


# --- Main execution ---
if __name__ == "__main__":
    if client.is_authenticated():
        print("🔐 Vault authentication successful.\n")

        create_secret_v2()
        read_secret_v2()

    else:
        print("❌ Vault authentication failed. Check your token and Vault status.")
