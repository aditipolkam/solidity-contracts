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
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
myaddress = "0xF591cCB0edA6AC9F51407204750Bb72fC72Ac90A"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# build transaction
nonce = w3.eth.getTransactionCount(myaddress)  # get latest transaction
