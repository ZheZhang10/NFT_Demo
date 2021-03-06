from brownie import AdvancedCollectible
from brownie.network.web3 import Web3
from scripts.helpful_scripts import fund_with_link, get_account

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(contract_address= advanced_collectible.address, amount= Web3.toWei(0.1, "ether"))
    creat_transaction = advanced_collectible.createCollectible({"from": account})
    creat_transaction.wait(1)
    print("Collectible Created!!!")


