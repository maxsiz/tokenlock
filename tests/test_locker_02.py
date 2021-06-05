import pytest
import logging
from brownie.test import given, strategy
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


# test for reverts
def test_locks(accounts, projecttoken, locker):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from': accounts[0]})
    with reverts("Sum vesting records must be equal lock amount"):
        locker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time()+100, chain.time()+200, chain.time()+300],
            [0, 0, 0],
            [accounts[4], accounts[5], accounts[6]],
            [10, 20, 30],
            {'from': accounts[0]}
        )
    with reverts("Length of periods and amounts arrays must be equal"):
        locker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time() + 300],
            [10e18, 20e18, 70e18],
            [accounts[4], accounts[5], accounts[6]],
            [10, 20, 30],
            {'from': accounts[0]}
        )

    with reverts("Length of beneficiaries and shares arrays must be equal"):
        locker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time()+100, chain.time()+200, chain.time()+300],
            [10e18, 20e18, 70e18],
            [accounts[4], accounts[5], accounts[6]],
            [10, 20],
            {'from': accounts[0]}
        )
# testing lock function for calling lock function two times with same values
def test_locks_double_lock(accounts, projecttoken, locker):
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6]],
        [100, 100, 100],
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
def generate_random_amounts(maxAmount):
    amounts = []
    if maxAmount == 0:
        return  amounts.append(0)
    for i in range(maxAmount):
        amounts.append(1)

    return  amounts
# generate accounts based on sum beneficiaries
def generate_random_accounts(amount, accounts):
    userAr = []
    if amount == 0:
        return userAr.append(accounts[0])
    for i in range(amount):
        userAr.append(accounts[i])

    return userAr


# test for random amount and random beneficiaries
@given(amount=strategy('uint256', max_value=10, exclude=0))
def test_locks_adjust_amounts(accounts, nulltoken, locker, amount):
    users = generate_random_accounts(amount, accounts)
    amountsAr = generate_random_amounts(amount)
    locks_balance = nulltoken.balanceOf(locker.address)
    locker.lockTokens(
        nulltoken.address,
        amount,
        amountsAr,
        amountsAr,
        users,
        amountsAr,
        {'from': accounts[0]}
    )
    # logging.info('registry for account[0]={}'.format(locker.registry(accounts[0], 0)))
    assert nulltoken.balanceOf(locker.address) == locks_balance + amount

def test_lock_properties(accounts, locker):
    logging.info(locker.getMyShares({'from': accounts[1]}))
    logging.info(locker.getLockRecordByIndex(2))
    assert locker.getLockCount() > 0
    logging.info(locker.getArraySum([10e18, 20e18, 70e18]))





