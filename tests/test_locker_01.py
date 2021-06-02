import pytest
import logging
from brownie import Wei, reverts, chain
LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_lock(accounts, projecttoken, locker):
    projecttoken.approve(locker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    locker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 100 , chain.time() + 200, chain.time() + 300 ],
        [10e18,20e18,70e18],
        [accounts[1],accounts[2],accounts[3]],
        [10,20,30],
        {'from':accounts[0]}
    )

    logging.info('registry for account[1]={}'.format(locker.registry(accounts[1], 0)))

    # with reverts("MinterRole: caller does not have the Minter role"):
    #     bettoken.burn(accounts[0], 1, {"from":accounts[1]})
    # assert bettoken.balanceOf(accounts[0]) == 0
