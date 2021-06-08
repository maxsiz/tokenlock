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
            [1000, 2000, 7000],
            {'from': accounts[0]}
        )
    with reverts("Length of periods and amounts arrays must be equal"):
        locker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time() + 300],
            [10e18, 20e18, 70e18],
            [accounts[4], accounts[5], accounts[6]],
            [1000, 2000, 7000],
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
    with reverts("Cant lock 0 amount"):
        locker.lockTokens(
            projecttoken.address,
            0,
            [chain.time()+100, chain.time() + 200, chain.time() + 300],
            [0,0, 0],
            [accounts[1], accounts[2], accounts[3]],
            [1000, 2000, 7000],
            {'from': accounts[0]}
        )

    with reverts("Sum of shares array must be equal to 100%"):
        locker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [chain.time() + 100, chain.time() + 200, chain.time() + 300],
            [10e18, 20e18, 70e18],
            [accounts[1], accounts[2], accounts[3]],
            [100, 100, 100]
        )

# testing lock function for calling lock function two times with same values
def test_locks_double_lock(accounts, projecttoken, locker):
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
    )

    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
    )
    logging.info('registry for account[4]={}'.format(locker.registry(accounts[4], 0)))

    assert projecttoken.balanceOf(locker.address) == LOCKED_AMOUNT + LOCKED_AMOUNT

# testing lock function for zero amount
def test_locks_zero_amounts(accounts, nulltoken, locker):
    nulltoken.approve(locker.address, nulltoken.balanceOf(accounts[0]), {'from': accounts[0]})
    locker.lockTokens(
        nulltoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6], accounts[1]],
        [1250, 1250, 7414, 86],
        {'from': accounts[0]}
    )

    logging.info(locker.getMyShares({'from' : accounts[1]}))



# generate random amounts based on sum of beneficiaries
def generate_random_amounts(maxAmount):
    amounts = []
    for i in range(maxAmount):
        amounts.append(1)

    return  amounts

def generate_random_beneficiaries(maxAmount):
    shares = 10000 / maxAmount
    shareArray = []
    for i in range(maxAmount):
        shareArray.append(shares)
    return shareArray
# generate accounts based on sum beneficiaries
def generate_random_accounts(amount, accounts):
    userAr = []
    if amount == 0:
        return userAr.append(accounts[0])
    for i in range(amount):
        userAr.append(accounts[i])

    return userAr


# test for random amount and random beneficiaries
@given(amount=strategy('uint256', max_value=10, exclude=[0,1,3,6,7,8,9]))
def test_locks_adjust_amounts(accounts, nulltoken, locker, amount):
    users = generate_random_accounts(amount, accounts)
    amountsAr = generate_random_amounts(amount)
    shares = generate_random_beneficiaries(amount)
    logging.info(amount)
    logging.info(users)
    logging.info(shares)
    locks_balance = nulltoken.balanceOf(locker.address)
    locker.lockTokens(
        nulltoken.address,
        amount,
        amountsAr,
        amountsAr,
        users,
        shares,
        {'from': accounts[0]}
    )
    # logging.info('registry for account[0]={}'.format(locker.registry(accounts[0], 0)))
    assert nulltoken.balanceOf(locker.address) == locks_balance + amount

def test_lock_properties(accounts, locker):
    logging.info(locker.getMyShares({'from': accounts[1]}))
    logging.info(locker.getLockRecordByIndex(2))
    assert locker.getLockCount() > 0
    logging.info(locker.getArraySum([10e18, 20e18, 70e18]))





