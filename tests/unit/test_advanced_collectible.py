from brownie import network, AdvancedCollectible
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # arrange/act
    advanced_collectible, created_tx = deploy_and_create()
    # Don't have the vrfcoordinator,
    # we need to get requestId to call back the Randomness function to get random number
    requestId = created_tx.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # assert
    # There should be a counter for the first one
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
