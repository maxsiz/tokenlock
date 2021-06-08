import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_claim_token(accounts, locker, projecttoken):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() - 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6], accounts[1]],
        [1250, 1250, 7414, 86],
        {'from': accounts[0]}
    )

    with reverts("Insufficient for now"):
        locker.claimTokens(0, 10e18, {'from': accounts[1]})

    with reverts("Cant claim zero"):
        locker.claimTokens(0, 0, {'from': accounts[1]})

    locker.claimTokens(0, 100, {'from': accounts[1]})

    locker.claimTokens(0, 200, {'from': accounts[1]})

    assert projecttoken.balanceOf(accounts[1]) == 300


