# import hvac

# client = hvac.Client(url='http://127.0.0.1:8200',token="hvs.N8FWxa08WjuGXHmGspkW9Dt0")
# print(client.is_authenticated())
# read_response = client.secrets.kv.read_secret_version(path='path',mount_point='my')

# print(read_response)


import hvac

client = hvac.Client(
    url='http://127.0.0.1:8200',
    token="hvs.N8FWxa08WjuGXHmGspkW9Dt0"
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
