from brownie import accounts, network, config, Contract, VRFCoordinatorMock, LinkToken
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "mainnet-fork"]
# {contract} / {tokenID}
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    # if in local deploy mocks, else return contract
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        # address
        contract_address = config["networks"][network.show_active()][contract_name]
        # abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Linktoken...")
    link_token = LinkToken.deploy({"from": account})
    print("Deployed Linktoken!")
    print("Deploying VRFCoordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deplyed All Mocks!")


def fund_with_link(contract_address, account = None, link_token = None, amount = Web3.toWei(1, "ether")):
    print("Funding link token...")
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded link token!!!")
    return tx

BreedMapping = {0:"PUG", 1:"SHIBA_INU", 2:"ST_BERNARD"}
# mapping different state number to different breed
def get_breed(breed_number):
    return BreedMapping[breed_number]




