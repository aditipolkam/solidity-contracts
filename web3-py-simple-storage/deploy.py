from dotenv import load_dotenv
import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3

load_dotenv()

with open("../SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# w3 connect to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
myaddress = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# build transaction
nonce = w3.eth.getTransactionCount(myaddress)  # get latest transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": myaddress,
        "nonce": nonce,
    }
)
print("Deploying contract...")
# sign transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

# send transaction
txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployed!")

# working with contracts
# 1.contract address
# 2.contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# initial value of favnum
print("Initial value of favNum: ", simple_storage.functions.retrieve().call())

print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": myaddress,
        "nonce": nonce + 1,
    }
)
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

txn_hash = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Updated!")
print("Updated value of favNum: ", simple_storage.functions.retrieve().call())
