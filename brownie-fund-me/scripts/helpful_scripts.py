from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if network.show_active not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        # account = accounts.load("test-acc")  # for encryption method
        return accounts.add(
            config["wallets"]["from_key"]
        )  # for environment variable setup


def deploy_mocks():
    print(f"Active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks deployed")
