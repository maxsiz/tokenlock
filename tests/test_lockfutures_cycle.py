import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_lock_token_to_locker(accounts, lockfutures, projecttoken, erc1155):

    projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0], {'from': accounts[0]}))
    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000, chain.time() + 500000000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )

    logging.info(lockfutures.getUserBalances(accounts[1], 0))

    assert (lockfutures.getUserBalances(accounts[1], 0))[0] == 100e18 * 1500 / 10000


def test_mint_futures_from_futures(accounts, lockfutures, erc1155):

    lockfutures.emitFutures(0, 0, {'from' : accounts[2]})

    logging.info(erc1155.balanceOf(accounts[1],1))
    logging.info(erc1155.balanceOf(accounts[2],1))


def test_locker_claim_tokens_check(accounts, lockfutures, erc1155, projecttoken):

    chain.sleep(2000000)

    with reverts("Insufficient for now"):
            lockfutures.claimTokens(0, 10e18*1500/10000 + 30e18*1500/10000, {'from': accounts[1]})

    # lets try  claim nft minted token. ==> here is bug. ideally it should fail because we minted 0 tokenID already.
    lockfutures.claimTokens(0, 10e18 * 1500 / 10000, {'from': accounts[1]})
    balance = projecttoken.balanceOf(accounts[1])

    logging.info(erc1155.balanceOf(accounts[1],0))

    chain.sleep(10000000000000)
    chain.mine(2)

    lockfutures.claimWithNFT(0, {'from': accounts[1]})
    logging.info(balance)
    logging.info(projecttoken.balanceOf(accounts[1]))

    lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[1], 0)[1], {'from': accounts[1]})
    lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[2], 0)[1], {'from': accounts[2]})
    lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[3], 0)[1], {'from': accounts[3]})
    lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[4], 0)[1], {'from': accounts[4]})
    lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[5], 0)[1], {'from': accounts[5]})
    # lockfutures.claimTokens(0, lockfutures.getUserBalances(accounts[6], 0)[1], {'from': accounts[6]})

    logging.info(projecttoken.balanceOf(lockfutures.address))
    logging.info(lockfutures.getUserBalances(accounts[6], 0))


    assert projecttoken.balanceOf(lockfutures.address) == 40000000000000000000 - 1500000000000000000
