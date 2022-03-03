from brownie import MockV3Aggregator, FundMe, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the pricefeed address to fund me contract (aggregator contract address on kovan)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pricefeed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        pricefeed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        pricefeed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
