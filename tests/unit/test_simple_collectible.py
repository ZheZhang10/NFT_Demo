
from brownie import network
from scripts.simple_collectible.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # arrange/act
    simple_collectible = deploy_and_create()
    # assert
    assert simple_collectible.ownerOf(0) == get_account()
