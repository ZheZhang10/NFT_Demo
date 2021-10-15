from os import times
import pytest
from brownie import network, AdvancedCollectible
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)

# test on rinkeby testnet
def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # arrange/act
    advanced_collectible, created_tx = deploy_and_create()
    time.sleep(60)
    # assert
    # There should be a counter for the first one
    assert advanced_collectible.tokenCounter() == 1
