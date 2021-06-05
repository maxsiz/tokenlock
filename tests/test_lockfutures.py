import logging
from brownie import Wei, reverts, chain


LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_mint_futures_nft(accounts, lockfutures, projecttoken):
        projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0], {'from': accounts[0]}))
        lockfutures.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time() + 2000000, chain.time() + 200, chain.time() + 2000000],
            [10e18, 20e18, 70e18],
            [accounts[1], accounts[2], accounts[3]],
            [10, 20, 30],
            {'from': accounts[0]}
        )
        logging.info(lockfutures.getLockRecordByIndex(0))
        with reverts("To late for this vesting"):
            lockfutures.emitFutures(0, 1)

        lockfutures.emitFutures(0, 2)

        with reverts("This futures already issued"):
            lockfutures.emitFutures(0, 2)

        lockfutures.emitFutures(0, 0)
        # ideally it should fail
        lockfutures.emitFutures(0, 0)

        logging.info(lockfutures.getLockRecordByIndex(0))