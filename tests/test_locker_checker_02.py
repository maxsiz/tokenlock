import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_lock_token(accounts, projecttoken, locker):
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

    assert projecttoken.balanceOf(locker.address) == LOCKED_AMOUNT



def test_lock_claim_by_little(accounts, projecttoken, locker):
    with reverts("Insufficient for now"):
        locker.claimTokens(0, 2**256-1, {'from': accounts[1]})

    chain.sleep(1000)
    chain.mine(2)

    availableTo = (locker.getUserBalances(accounts[1], 0))[1]
    locker.claimTokens(0, 999999, {'from': accounts[1]})

    locker.claimTokens(0, 2441241, {'from' : accounts[1]})

    locker.claimTokens(0, 52363262, {'from' : accounts[1]})

    locker.claimTokens(0, 100000000, {'from': accounts[1]})

    locker.claimTokens(0, 20000000, {'from' : accounts[1]})

    locker.claimTokens(0, 7600000, {'from': accounts[1]})

    locker.claimTokens(0, 9000000000, {'from' : accounts[1]})

    with reverts("Insufficient for now"):
        locker.claimTokens(0, (locker.getUserBalances(accounts[2], 0))[1], {'from': accounts[1]})

    locker.claimTokens(0, (locker.getUserBalances(accounts[1], 0))[1], {'from': accounts[1]})

    logging.info(projecttoken.balanceOf(accounts[1]))

    assert projecttoken.balanceOf(accounts[1]) == availableTo

