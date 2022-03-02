from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    # account = accounts.load("test-acc") #for encryption method
    # account = accounts.add(config["wallets"]["from_key"])  # for environment variable setup
    account = accounts[0]  # default account
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)


def main():
    deploy_simple_storage()
