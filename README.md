# hashicorp
Working with harhicorp vault

## installation steps for macOS:

`brew tap hashicorp/tap`

`brew install hashicorp/tap/vault`

## installation for linux/ubuntu

`wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg`

`echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

`sudo apt update && sudo apt install vault`

## packages used:

* hvac : `pip install hvac`
* python-dotenv : `pip3 install python-dotenv`

## commands to verify:

### vault deployment:

`vault -version`

### to check available package and its version:

`pip3 freeze`


## notes on hashicorp:

there are two type of mode:
* dev mode [only for development, can't be used for production] => will be using this
* server mode [only for production]

command to run vault dev mode : `vault server -dev`

whenever we run our local vault, four things we need to make note:
* port
* storage
* Unseal Key
* Root Token
all this will be visible when we start our vault.
the unseat key will be used as vault_addr and root token as vault_token in our code.

run the following commands to set the VAULT_ADDR and VAULT_TOKEN:

`export VAULT_ADDR='<port address>'`

`export VAULT_TOKEN='<root token>'`

to check the status of the value: `vault status`

vault cli read/write/delete commands:
* `vault kv put <path> key_1=value_1`
* `vault kv get <path>`
* `vault kv delete <path>`

here;
* vault -> standard syntax
* kv -> type of secret stored: key/value
* put/get/delete -> methods
* path -> path to store ur secret inside the vault like: my/path

whenever the path is defined , we have to enable it inside the vault (enable secret engine). For that the following commands is executed:

`vault secrets enable -path=<path> kv`

![alt text](<Screenshot 2025-07-27 at 1.10.29 PM.png>)
![alt text](<Screenshot 2025-07-27 at 1.24.52 PM.png>)

to disable the vault path : `vault secrets disable <path>`

![alt text](<Screenshot 2025-07-27 at 2.30.27 PM.png>)
![alt text](<Screenshot 2025-07-27 at 2.40.27 PM.png>)

read/write/delete cli operation:

![alt text](<Screenshot 2025-07-27 at 1.15.48 PM.png>)

to get the store secrets in json format : `vault kv get -format-json <path>`

![alt text](<Screenshot 2025-07-27 at 1.17.39 PM.png>)

to check all the secret path present in your vault: `vault secrets list`

![alt text](<Screenshot 2025-07-27 at 1.25.35 PM.png>)

here:
'my/' is a custom path while others are default path of the vault.


## reference links:
* https://hub.docker.com/r/hashicorp/vault
* https://developer.hashicorp.com/vault/install
* restAPI from CLI: https://developer.hashicorp.com/vault/api-docs




## hashicorp in prod mode
* unset token : `unset VAULT_TOKEN`
* set up hashicorp config.hcp file:
```
storage "raft" {
  path    = "./vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
ui = true
```



* Create "RAFT" storage backend directory : `mkdir -p ./vault/data`

* Starting vault server using config.hcl : `vault server -config=config.hcl`

* Export VAULT_ADDR : `export VAULT_ADDR='http://127.0.0.1:8200'`

* Initialize vault : `vault operator init`

* Unseal vault : `vault operator unseal`


#### UI link will look like this : `http://localhost:8200/ui/vault/dashboard`


## roles and policies in hashicorp vault:
* https://developer.hashicorp.com/vault/tutorials/get-started/introduction-roles
* https://developer.hashicorp.com/vault/docs/concepts/policies


## defining roles in hashicorp:
example of a aws path with type as aws

* Enable the secret engine path for AWS : `vault secrets enable -path=aws aws`

* View the secret list: `vault secrets list`

* Write AWS root config inside your hashicorp vault

```
vault write aws/config/root \
access_key=YOUR_ACCESS_KEY \
secret_key=YOUR_SECRET_KEY \
region=eu-north-1
```

* Setup role 

```
vault write aws/roles/my-ec2-role \
        credential_type=iam_user \
        policy_document=-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1426528957000",
      "Effect": "Allow",
      "Action": [
        "ec2:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
```

* Generate access key and secret key for that role: `vault read aws/creds/my-ec2-role`

*  Revoke the secrets if you do not want it any longer: `vault lease revoke <lease_id>`

## policy in hashicory:

* List vault policies : `vault policy list`

* Write your custom policy : `vault policy write my-policy -  EOF`

```
# Dev servers have version 2 of KV secrets engine mounted by default, so will
# need these paths to grant permissions:
path "secret/data/*" {
  capabilities = ["create", "update"]
}

path "secret/data/foo" {
  capabilities = ["read"]
}
EOF
```

* Read Vault policy details : `vault policy read my-policy`

* Delete Vault policy by policy name : `vault policy delete my-policy`

* Attach token to policy : `export VAULT_TOKEN="$(vault token create -field token -policy=my-policy)"`

* Associate auth method with policy 

```
vault write auth/approle/role/my-role \
    secret_id_ttl=10m \
    token_num_uses=10 \
    token_ttl=20m \
    token_max_ttl=30m \
    secret_id_num_uses=40 \
    token_policies=my-policy
```

* Generate and Export Role ID: `export ROLE_ID="$(vault read -field=role_id auth/approle/role/my-role/role-id)"`

* Generate and Export Secret ID: `export SECRET_ID="$(vault write -f -field=secret_id auth/approle/role/my-role/secret-id)"`