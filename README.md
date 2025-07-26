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

`export VAULT_ADDR='<port address>`

`export VAULT_TOKEN='<root token>`

to check the status of the value: `vault status`

