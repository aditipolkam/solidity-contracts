from webbrowser import get
from brownie import (
    Contract,
    accounts,
    config,
    network,
    MockV3Aggregator,
    VRFCoordinatorMock,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        accounts.load(id)

    if (
        network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # account = accounts.load("test-acc")  # for encryption method
    return accounts.add(config["wallets"]["from_key"])  # for environment variable setup


contract_to_mock = {
    "eth_usd_pricee_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
}


def get_contract(contract_name):
    """this function will grab the contract addresses from the brownie config file if defined, otherwise,
    it will deploy a mock version of that contract and return than mock contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )


DECIMALS = 8
STARTING_PRICE = 200000000000


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    """this function will deploy a mock version of the contracts and save them to the brownie config file"""
    account = get_account()
    MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    print("Deployed.")
