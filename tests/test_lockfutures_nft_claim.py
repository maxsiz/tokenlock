import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_lock_tokens(accounts, projecttoken, nulltoken, lockfutures):
    projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0], {'from': accounts[0]}))
    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000,
         chain.time() + 500000000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )


    nulltoken.approve(lockfutures.address, nulltoken.balanceOf(accounts[0], {'from': accounts[0]}))
    lockfutures.lockTokens(
        nulltoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000,
         chain.time() + 500000000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )

    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000,
         chain.time() + 500000000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )


    lockfutures.lockTokens(
        nulltoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000,
         chain.time() + 500000000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )

    assert nulltoken.balanceOf(lockfutures.address) == LOCKED_AMOUNT + LOCKED_AMOUNT
    assert projecttoken.balanceOf(lockfutures.address) == LOCKED_AMOUNT + LOCKED_AMOUNT


def test_emitfutures(accounts, lockfutures, erc1155):
    for j in range(4):
        for i in range(5):
            lockfutures.emitFutures(j, i, {'from': accounts[i + 1]})

    for j in range(4):
        for i in range(5):
            assert lockfutures.getNFTIdByLockVestingIndexes(j, i) == j * 1000000000000000000 + i


def test_claim_futures_1(accounts, lockfutures, erc1155, projecttoken, nulltoken):

    chain.sleep(2000000)
    chain.mine(5)

    lockfutures.claimWithNFT(0, {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(1, 0), {'from': accounts[1]})


    with reverts("Claiming NFT insufficient for now"):
        lockfutures.claimWithNFT(1, {'from': accounts[1]})

    chain.sleep(3000000)
    chain.mine(5)

    lockfutures.claimWithNFT(1, {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(1, 1), {'from': accounts[1]})

    chain.sleep(500000000)
    chain.mine(5)

    lockfutures.claimWithNFT(2, {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(1, 2), {'from': accounts[1]})

    chain.sleep(600000000)
    chain.mine(5)

    lockfutures.claimWithNFT(3, {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(1, 3), {'from': accounts[1]})


    chain.sleep(700000000)
    chain.mine(5)

    lockfutures.claimWithNFT(4, {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(1, 4), {'from': accounts[1]})


    assert projecttoken.balanceOf(accounts[1]) == 100e18 * 1500 / 10000

    assert nulltoken.balanceOf(accounts[1]) == 100e18 * 1500 / 10000


def test_claim_futures_2(accounts, lockfutures, erc1155, projecttoken, nulltoken):

    chain.sleep(2000000)
    chain.mine(5)

    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(2, 0), {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(3, 0), {'from': accounts[1]})

    chain.sleep(3000000)
    chain.mine(5)

    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(2, 1), {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(3, 1), {'from': accounts[1]})

    chain.sleep(500000000)
    chain.mine(5)

    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(2, 2), {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(3, 2), {'from': accounts[1]})

    chain.sleep(600000000)
    chain.mine(5)

    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(2, 3), {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(3, 3), {'from': accounts[1]})


    chain.sleep(700000000)
    chain.mine(5)

    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(2, 4), {'from': accounts[1]})
    lockfutures.claimWithNFT(lockfutures.getNFTIdByLockVestingIndexes(3, 4), {'from': accounts[1]})


    assert projecttoken.balanceOf(accounts[1]) == (LOCKED_AMOUNT * 1500 / 10000) * 2
    assert nulltoken.balanceOf(accounts[1]) == (LOCKED_AMOUNT * 1500 / 10000) * 2

    assert  projecttoken.balanceOf(lockfutures.address) ==(LOCKED_AMOUNT + LOCKED_AMOUNT) -  ((LOCKED_AMOUNT * 1500 / 10000) * 2)
    assert  nulltoken.balanceOf(lockfutures.address) ==(LOCKED_AMOUNT + LOCKED_AMOUNT) -  ((LOCKED_AMOUNT * 1500 / 10000) * 2)
