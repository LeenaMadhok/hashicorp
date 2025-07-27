import hvac

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token="hvs.N8FWxa08WjuGXHmGspkW9Dt0"
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
