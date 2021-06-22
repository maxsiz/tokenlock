import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_lock_tokens(accounts, projecttoken, locker):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 1000, chain.time() + 2000, chain.time() + 3000, chain.time() + 4000, chain.time() + 5000],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )

    logging.info(locker.getUserBalances(accounts[1], 0))
    logging.info(locker.getUserBalances(accounts[2], 0))
    logging.info((locker.getUserBalances(accounts[3], 0)[0]))
    logging.info(locker.getUserBalances(accounts[4], 0))
    logging.info(locker.getUserBalances(accounts[5], 0))
    logging.info(locker.getUserBalances(accounts[6], 0))

    assert (locker.getUserBalances(accounts[1], 0))[0] == 100e18 * 1500 / 10000
    assert (locker.getUserBalances(accounts[2], 0))[0] == 100e18 * 1500 / 10000
    assert (locker.getUserBalances(accounts[3], 0))[0] == 100e18 * 700 / 10000
    assert (locker.getUserBalances(accounts[4], 0))[0] == 100e18 * 100 / 10000
    assert (locker.getUserBalances(accounts[5], 0))[0] == 100e18 * 2200 / 10000
    assert (locker.getUserBalances(accounts[6], 0))[0] == 100e18 * 4000 / 10000

    assert projecttoken.balanceOf(locker.address) == LOCKED_AMOUNT


def test_claim_tokens_first(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0,100, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)

    locker.claimTokens(0, locker.getUserBalances(accounts[1], 0)[1], {'from' : accounts[1]})
    locker.claimTokens(0, locker.getUserBalances(accounts[2], 0)[1], {'from' : accounts[2]})
    locker.claimTokens(0, locker.getUserBalances(accounts[3], 0)[1], {'from' : accounts[3]})
    locker.claimTokens(0, locker.getUserBalances(accounts[4], 0)[1], {'from' : accounts[4]})
    locker.claimTokens(0, locker.getUserBalances(accounts[5], 0)[1], {'from' : accounts[5]})
    locker.claimTokens(0, locker.getUserBalances(accounts[6], 0)[1], {'from' : accounts[6]})



    assert projecttoken.balanceOf(accounts[1]) == 10e18 * 1500 / 10000
    assert projecttoken.balanceOf(accounts[2]) == 10e18 * 1500 / 10000
    assert projecttoken.balanceOf(accounts[3]) == 10e18 * 700 / 10000
    assert projecttoken.balanceOf(accounts[4]) == 10e18 * 100 / 10000
    assert projecttoken.balanceOf(accounts[5]) == 10e18 * 2200 / 10000
    assert projecttoken.balanceOf(accounts[6]) == 10e18 * 4000 / 10000

    assert projecttoken.balanceOf(locker.address) == 100e18 - 10e18


def test_claim_tokens_second(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0, 100, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)
    firstUser = locker.getUserBalances(accounts[1], 0)[1]
    secondUser = locker.getUserBalances(accounts[2], 0)[1]
    thirdUser = locker.getUserBalances(accounts[3], 0)[1]

    locker.claimTokens(0, locker.getUserBalances(accounts[1], 0)[1], {'from': accounts[1]})
    locker.claimTokens(0, locker.getUserBalances(accounts[2], 0)[1], {'from': accounts[2]})
    locker.claimTokens(0, locker.getUserBalances(accounts[3], 0)[1], {'from': accounts[3]})
    # locker.claimTokens(0, locker.getUserBalances(accounts[4], 0)[1], {'from': accounts[4]})
    # locker.claimTokens(0, locker.getUserBalances(accounts[5], 0)[1], {'from': accounts[5]})
    # locker.claimTokens(0, locker.getUserBalances(accounts[6], 0)[1], {'from': accounts[6]})
    #
    assert projecttoken.balanceOf(accounts[1]) == (30e18 * 1500 / 10000) + (10e18 * 1500 / 10000)
    assert projecttoken.balanceOf(accounts[2]) == (30e18 * 1500 / 10000) + (10e18 * 1500 / 10000)
    assert projecttoken.balanceOf(accounts[3]) == (30e18 * 700 / 10000) + (10e18 * 700 / 10000)

    assert (locker.getUserBalances(accounts[4], 0))[1] == 30e18 * 100 / 10000
    assert (locker.getUserBalances(accounts[5], 0))[1] == 30e18 * 2200 / 10000
    assert (locker.getUserBalances(accounts[6], 0))[1] == 30e18 * 4000 / 10000

    #
    assert projecttoken.balanceOf(locker.address) == 100e18 - 10e18 - firstUser - secondUser - thirdUser


def test_claim_tokens_third(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0, 100, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)

    firstUser = locker.getUserBalances(accounts[1], 0)[1]
    userBalance = projecttoken.balanceOf(accounts[1])
    lockerBalance = projecttoken.balanceOf(locker.address)

    locker.claimTokens(0, firstUser, {'from': accounts[1]})


    assert projecttoken.balanceOf(accounts[1]) == firstUser + userBalance
    assert projecttoken.balanceOf(locker.address) == lockerBalance - firstUser


def test_claim_tokens_fourth(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0, 100, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)

    firstUser = locker.getUserBalances(accounts[1], 0)[1]
    userBalance = projecttoken.balanceOf(accounts[1])
    lockerBalance = projecttoken.balanceOf(locker.address)


    locker.claimTokens(0, firstUser, {'from': accounts[1]})

    assert projecttoken.balanceOf(accounts[1]) == firstUser + userBalance
    assert projecttoken.balanceOf(locker.address) == lockerBalance - firstUser


def test_claim_tokens_fifth(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0, 100, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)

    locker.claimTokens(0, locker.getUserBalances(accounts[1], 0)[1], {'from': accounts[1]})
    locker.claimTokens(0, locker.getUserBalances(accounts[2], 0)[1], {'from': accounts[2]})
    locker.claimTokens(0, locker.getUserBalances(accounts[3], 0)[1], {'from': accounts[3]})
    locker.claimTokens(0, locker.getUserBalances(accounts[4], 0)[1], {'from': accounts[4]})
    locker.claimTokens(0, locker.getUserBalances(accounts[5], 0)[1], {'from': accounts[5]})
    locker.claimTokens(0, locker.getUserBalances(accounts[6], 0)[1], {'from': accounts[6]})

    assert projecttoken.balanceOf(accounts[1]) == 100e18 * 1500 / 10000
    assert projecttoken.balanceOf(accounts[2]) == 100e18 * 1500 / 10000
    assert projecttoken.balanceOf(accounts[3]) == 100e18 * 700 / 10000
    assert projecttoken.balanceOf(accounts[4]) == 100e18 * 100 / 10000
    assert projecttoken.balanceOf(accounts[5]) == 100e18 * 2200 / 10000
    assert projecttoken.balanceOf(accounts[6]) == 100e18 * 4000 / 10000

    assert projecttoken.balanceOf(locker.address) == 0