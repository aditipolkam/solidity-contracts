from random import random
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from brownie import accounts, network
from scripts.advanced.deploy_create import deploy_create


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_create()
    requestId = creation_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    assert advanced_collectible.tokenCounter() >= 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
