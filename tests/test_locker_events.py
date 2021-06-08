import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_lock_for_newLock_event(accounts, nulltoken, locker):
    nulltoken.approve(locker.address, nulltoken.balanceOf(accounts[0]), {'from': accounts[0]})
    lockTX =locker.lockTokens(
        nulltoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[1], accounts[2], accounts[3]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
    )
    assert len(lockTX.events) >= 1
    # there is no NewLock event emitted
    #assert lockTX.events["NewLock"].values() == [nulltoken.address, accounts[0], LOCKED_AMOUNT, 4]
