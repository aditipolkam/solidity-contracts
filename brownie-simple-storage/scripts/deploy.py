from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    # account = accounts.load("test-acc") #for encryption method
    # account = accounts.add(config["wallets"]["from_key"])  # for environment variable setup
    account = accounts[0]  # default account
    simple_storage = SimpleStorage.deploy({"from": account})

    # using the simple storage functions
    stored_value = simple_storage.retrieve()
    print("Stored value:", stored_value)
    transaction = simple_storage.store(42, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print("Updated stored value:", updated_stored_value)


def main():
    deploy_simple_storage()
