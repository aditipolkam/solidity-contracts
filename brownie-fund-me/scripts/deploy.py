from brownie import MockV3Aggregator, FundMe, network, config
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    # print(account)
    # pass the pricefeed address to fund me contract (aggregator contract address on kovan)
    if network.show_active() != "development":
        pricefeed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"Active network is {network.show_active()}")
        print("Deploying mocks...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, 20000000000000000000000, {"from": account}
        )
        pricefeed_address = mock_aggregator.address
        print("Mocks deployed")

    fund_me = FundMe.deploy(
        pricefeed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
