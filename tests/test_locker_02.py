import pytest
import logging
from numpy.random import multinomial
from brownie import Wei, reverts, chain, given, strategy

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


# testing lock function for calling lock function two times with same values
def test_locks_double_lock(accounts, projecttoken, locker):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from': accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6]],
        [10, 20, 30],
        {'from': accounts[0]}
    )

    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6]],
        [10, 20, 30],
        {'from': accounts[0]}
    )
    logging.info('registry for account[4]={}'.format(locker.registry(accounts[4], 0)))

    assert projecttoken.balanceOf(locker.address) == LOCKED_AMOUNT + LOCKED_AMOUNT

# testing lock function for zero amount
def test_locks_zero_amounts(accounts, nulltoken, locker):
    nulltoken.approve(locker.address, nulltoken.balanceOf(accounts[0]), {'from': accounts[0]})
    locker.lockTokens(
        nulltoken.address,
        0,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [0, 0, 0],
        [accounts[1], accounts[2], accounts[3]],
        [0, 0, 0],
        {'from': accounts[0]}
    )

    assert nulltoken.balanceOf(locker.address) == 0

# generate random amounts based on sum of beneficiaries
def generate_random_amounts(amount, addresses):
    return multinomial(amount, [1/10000.] * addresses)

# generate accounts based on sum beneficiaries
def generate_random_accounts(beneficiaries, accounts):
    userAr = []
    for i in range(beneficiaries):
        userAr.append(accounts[i])

    return userAr


# test for random amount and random beneficiaries
@given(amount=strategy('uint256', max_value=1000e18))
@given(beneficiaries=strategy('uint256', max_value=10000))
def test_locks_adjust_amounts(accounts, nulltoken, locker, amount, beneficiaries):
    amountsAr = generate_random_amounts(amount, beneficiaries)
    users = generate_random_accounts(beneficiaries, accounts)
    locker.lockTokens(
        nulltoken.address,
        amount,
        amountsAr,
        amountsAr,
        users,
        amountsAr,
        {'from': accounts[0]}
    )
    logging.info('registry for account[0]={}'.format(locker.registry(accounts[0], 0)))
    assert nulltoken.balanceOf(locker.address) == amount


def test_lock_properties(accounts, locker):
    logging.info(locker.getMyShares({'from': accounts[1]}))
    logging.info(locker.getLockRecordByIndex(2))
    assert locker.getLockCount() > 0
    logging.info(locker.getArraySum([10e18, 20e18, 70e18]))





