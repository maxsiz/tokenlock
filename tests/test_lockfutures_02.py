import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_lock_tokens(accounts, projecttoken, nulltoken, lockfutures):
    projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0], {'from': accounts[0]}))
    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 90000, chain.time() + 5000000, chain.time() + 32000000, chain.time() + 42000000,
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



def test_lockfutures_emit(accounts, projecttoken, nulltoken, lockfutures,erc1155):


    # with reverts("Claiming NFT insufficient for now"):
    #     lockfutures.claimWithNFT(0)

        logging.info(lockfutures.getLockCount())

        lockfutures.emitFutures(0,0, {'from': accounts[3]})

        with reverts("This futures already issued"):
            lockfutures.emitFutures(0, 0, {'from': accounts[1]})

        logging.info(erc1155.balanceOf(accounts[1], 0))

        logging.info(lockfutures.getLockRecordByIndex(0))
        lockfutures.emitFutures(0, 1, {'from': accounts[2]})


        logging.info(lockfutures.getLockRecordByIndex(0))

        lockfutures.emitFutures(0, 2, {'from': accounts[3]})
        logging.info(erc1155.balanceOf(accounts[1], 2))



        ## claim
        with reverts("Claiming NFT insufficient for now"):
            lockfutures.claimWithNFT(0, {'from': accounts[4]})

        chain.mine(200)


        chain.sleep(90000)


        chain.mine(200)
        nft_before_amount = erc1155.balanceOf(accounts[4], 0)
        lockfutures.claimWithNFT(0, {'from': accounts[4]})



        assert projecttoken.balanceOf(accounts[4]) == nft_before_amount
