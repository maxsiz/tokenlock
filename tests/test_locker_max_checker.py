import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_deposit_token1(accounts, locker, projecttoken):
    userlist = []
    shares = []
    for i in range(100):
        userlist.append(accounts[1])
        shares.append(100)
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        100e18,
        [chain.time() + 1000],
        [100e18],
        userlist,
        shares,
        {'from': accounts[0]}
    )
    logging.info(projecttoken.balanceOf(locker.address))

    chain.sleep(3000)
    chain.mine(5)

    logging.info(projecttoken.balanceOf(locker.address))

### This  tests  need for livenet

# def test_deposit_max1(accounts, locker, projecttoken):
#     userlist = []
#     shares = []
#     for i in range(200):
#         userlist.append(accounts[1])
#         shares.append(50)
#     projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
#     locker.lockTokens(
#         projecttoken.address,
#         100e18,
#         [chain.time() + 1000],
#         [100e18],
#         userlist,
#         shares,
#         {'from': accounts[0]}
#     )
#     logging.info(projecttoken.balanceOf(locker.address))


# def test_deposit_max2(accounts, locker, projecttoken):
#     userlist = []
#     shares = []
#     for i in range(200):
#         userlist.append(accounts[1])
#         shares.append(20)
#     for j in range(30):
#         userlist.append(accounts[1])
#         shares.append(100)
#     for k in range(8):
#         userlist.append(accounts[1])
#         shares.append(375)

#     projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
#     locker.lockTokens(
#         projecttoken.address,
#         100e18,
#         [chain.time() + 1000],
#         [100e18],
#         userlist,
#         shares,
#         {'from': accounts[0]}
#     )
#     logging.info(projecttoken.balanceOf(locker.address))

def test_vestings_checker(accounts, projecttoken, locker):
    _unlockedFrom = []
    _unlockAmount = []
    for i in range(100):
        _unlockedFrom.append(chain.time() + i)
        _unlockAmount.append(1e18)
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        100e18,
        _unlockedFrom,
        _unlockAmount,
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )
    logging.info(projecttoken.balanceOf(locker.address))



### Vestings needs to be tested on livenet also.

# def test_vestings_checker(accounts, projecttoken, locker):
#     _unlockedFrom = []
#     _unlockAmount = []
#     for i in range(200):
#         _unlockedFrom.append(chain.time() + i)
#         _unlockAmount.append(5e17)
#     projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
#     locker.lockTokens(
#         projecttoken.address,
#         100e18,
#         _unlockedFrom,
#         _unlockAmount,
#         [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
#         [1500, 1500, 700, 100, 2200, 4000],
#         {'from': accounts[0]}
#     )
#     logging.info(projecttoken.balanceOf(locker.address))



# def test_vestings_checker(accounts, projecttoken, locker):
#     _unlockedFrom = []
#     _unlockAmount = []
#     for i in range(300):
#         _unlockedFrom.append(chain.time() + i)
#         _unlockAmount.append(1e18)
#     projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
#     locker.lockTokens(
#         projecttoken.address,
#         300e18,
#         _unlockedFrom,
#         _unlockAmount,
#         [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
#         [1500, 1500, 700, 100, 2200, 4000],
#         {'from': accounts[0]}
#     )
#     logging.info(projecttoken.balanceOf(locker.address))
