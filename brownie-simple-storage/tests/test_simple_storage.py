from brownie import SimpleStorage, accounts


def test_deploy():
    # arranging
    account = accounts[0]

    # acting
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # asserting
    assert starting_value == expected
