import logging
from brownie import Wei, reverts, chain


LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_mint_futures(accounts, lockfutures, projecttoken, erc1155):
        projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0], {'from': accounts[0]}))
        lockfutures.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time() + 2000000, chain.time() + 200, chain.time() + 1655818774],
            [10e18, 20e18, 70e18],
            [accounts[1], accounts[2], accounts[3]],
            [1000, 2000, 7000],
            {'from': accounts[0]}
        )
        logging.info(lockfutures.getLockRecordByIndex(0))

        lockfutures.emitFutures(0, 2, True, {'from': accounts[3]})
        logging.info(erc1155.balanceOf(accounts[1],2))




def test_claim_futures_vesting(accounts, lockfutures, projecttoken, erc1155):

    with reverts("Claiming NFT insufficient for now"):
        lockfutures.claimWithNFT(2, {'from': accounts[1]})

    chain.sleep(2000)
    chain.mine(2)
    with reverts("Claiming NFT insufficient for now"):
        lockfutures.claimWithNFT(2, {'from': accounts[1]})


    chain.sleep(1655091000)
    chain.mine(2)
    with reverts("Claiming NFT insufficient for now"):
        lockfutures.claimWithNFT(2, {'from': accounts[1]})

    chain.sleep(5091000)
    chain.mine(2)
    lockfutures.claimWithNFT(2, {'from': accounts[1]})

    logging.info(projecttoken.balanceOf(accounts[1], {'from': accounts[1]}))

    assert erc1155.balanceOf(accounts[1],2) == 0


