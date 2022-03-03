from brownie import accounts, config, network


def get_account():
    if network.show_active == "development":
        return accounts[0]
    else:
        # account = accounts.load("test-acc")  # for encryption method
        return accounts.add(
            config["wallets"]["from_key"]
        )  # for environment variable setup
