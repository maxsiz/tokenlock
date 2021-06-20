import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_deposit_token(accounts, locker, projecttoken):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 1000, chain.time() + 2000, chain.time() - 3000],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6], accounts[1]],
        [1250, 1250, 7414, 86],
        {'from': accounts[0]}
    )
    logging.info(projecttoken.balanceOf(locker.address))
def test_claim_tokens(accounts, locker, projecttoken):
    with reverts("Index out of range"):
        locker.claimTokens(3, 10e18, {'from': accounts[1]})

    with reverts("Insufficient for now"):
        locker.claimTokens(0, 10e18, {'from': accounts[1]})

    with reverts("Cant claim zero"):
        locker.claimTokens(0, 0, {'from': accounts[1]})
    chain.sleep(1000)
    chain.mine(5)
    locker.claimTokens(0, 100, {'from': accounts[1]})

    locker.claimTokens(0, 200, {'from': accounts[1]})

    locker.claimTokens(0, 10e18, {'from': accounts[4]})
    logging.info(projecttoken.balanceOf(accounts[4]))
    logging.info(projecttoken.balanceOf(accounts[1]))

    assert projecttoken.balanceOf(accounts[4]) == 10e18
    assert projecttoken.balanceOf(accounts[1]) == 300
    assert projecttoken.balanceOf(locker.address) == (100000000000000000000 - 10000000000000000000 - 300)


def test_claim_all(accounts, locker, projecttoken):
    chain.sleep(400)
    chain.mine(1)
    locker.claimTokens(0, 8.75e18, {'from': accounts[5]})

    with reverts("Insufficient for now"):
        locker.claimTokens(0, 2.5e18, {'from': accounts[5]})

    chain.sleep(600)
    chain.mine(2)

    locker.claimTokens(0, 2.5e18, {'from': accounts[5]})
    logging.info(projecttoken.balanceOf(accounts[5]))

    chain.sleep(500)
    chain.mine(2)

    with reverts("Insufficient for now"):
        locker.claimTokens(0, 2.5e18, {'from': accounts[5]})

    chain.sleep(500)
    chain.mine(2)

    locker.claimTokens(0, 1.25e18, {'from': accounts[5]})
    logging.info(projecttoken.balanceOf(accounts[5]))


    assert projecttoken.balanceOf(accounts[5]) == (100e18 * 1250) / 10000


