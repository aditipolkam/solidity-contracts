import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
from scripts.deploy_create import deploy_create


def can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_create()
    assert simple_collectible.ownerOf(0) == get_account()
