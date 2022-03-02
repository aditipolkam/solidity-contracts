from brownie import accounts, config, SimpleStorage, network
import os


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    # using the simple storage functions
    stored_value = simple_storage.retrieve()
    print("Stored value:", stored_value)
    transaction = simple_storage.store(42, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print("Updated stored value:", updated_stored_value)


def get_account():
    if network.show_active == "development":
        return accounts[0]
    else:
        # account = accounts.load("test-acc")  # for encryption method
        return accounts.add(
            config["wallets"]["from_key"]
        )  # for environment variable setup


def main():
    deploy_simple_storage()
