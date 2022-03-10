from random import random
import pytest, time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from brownie import accounts, network
from scripts.advanced.deploy_create import deploy_create


def test_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    advanced_collectible, creation_tx = deploy_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter == 1
