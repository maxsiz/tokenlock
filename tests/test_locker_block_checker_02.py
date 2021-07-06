import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_lock_token(accounts, projecttoken, blocklocker):
    current_block = chain.height
    projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
        [10e18, 30e18, 30e18, 15e18, 15e18],
        [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )

    logging.info(blocklocker.getUserBalances(accounts[1], 0))

    assert projecttoken.balanceOf(blocklocker.address) == LOCKED_AMOUNT



def test_lock_claim_by_little(accounts, projecttoken, blocklocker):
    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, 2**256-1, {'from': accounts[1]})

    #chain.sleep(1000)
    chain.mine(102)

    availableTo = (blocklocker.getUserBalances(accounts[1], 0))[1]
    blocklocker.claimTokens(0, 999999, {'from': accounts[1]})

    blocklocker.claimTokens(0, 2441241, {'from' : accounts[1]})

    blocklocker.claimTokens(0, 52363262, {'from' : accounts[1]})

    blocklocker.claimTokens(0, 100000000, {'from': accounts[1]})

    blocklocker.claimTokens(0, 20000000, {'from' : accounts[1]})

    blocklocker.claimTokens(0, 7600000, {'from': accounts[1]})

    blocklocker.claimTokens(0, 9000000000, {'from' : accounts[1]})

    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, (blocklocker.getUserBalances(accounts[2], 0))[1], {'from': accounts[1]})

    blocklocker.claimTokens(0, (blocklocker.getUserBalances(accounts[1], 0))[1], {'from': accounts[1]})

    logging.info(projecttoken.balanceOf(accounts[1]))

    assert projecttoken.balanceOf(accounts[1]) == availableTo


