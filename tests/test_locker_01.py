import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_lock(accounts, projecttoken, locker):
    with reverts("Please approve first"):
        locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100 , chain.time() + 200, chain.time() + 300 ],
        [10e18,20e18,70e18],
        [accounts[1],accounts[2],accounts[3]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
        )

    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100, chain.time() + 200, chain.time() + 300],
        [10e18, 20e18, 70e18],
        [accounts[1], accounts[1], accounts[1]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
    )

    logging.info('registry for account[3]={}'.format(locker.registry(accounts[1], 0)))

    # with reverts("Please approve first"):
    #     bettoken.burn(accounts[0], 1, {"from":accounts[1]})
    assert projecttoken.balanceOf(locker.address) == LOCKED_AMOUNT



def test_lock_properties(accounts, locker, projecttoken):
    logging.info(locker.getUserShares(accounts[1].address))
    chain.sleep(600)
    chain.mine(2)
    logging.info((locker.getUserBalances(accounts[1], 0)))
    locker.claimTokens(0, 100e18, {'from': accounts[1]})


    logging.info(locker.getLockRecordByIndex(0))
    projecttoken.balanceOf(accounts[1])
    logging.info(projecttoken.balanceOf(accounts[1]))
    logging.info(projecttoken.balanceOf(locker.address))

    assert locker.getLockCount() > 0
    assert projecttoken.balanceOf(accounts[1]) == 100e18

