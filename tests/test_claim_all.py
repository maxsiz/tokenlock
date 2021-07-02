import pytest
import logging
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18

def test_lock_tokens(accounts, lockfutures, projecttoken, erc1155):
    projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 1000, chain.time() + 200000, chain.time() + 300000],
        [10e18, 20e18, 70e18],
        [accounts[4], accounts[5], accounts[6], accounts[1]],
        [1250, 1250, 7414, 86],
        {'from': accounts[0]}
    )
    logging.info(projecttoken.balanceOf(lockfutures.address))
    logging.info(lockfutures.getUserBalances(accounts[4], 0))

def test_claim_tokens(accounts, lockfutures, projecttoken):
     with reverts("Insufficient for now"):
        lockfutures.claimTokens(0, 100000, {'from': accounts[4]})


     chain.sleep(10000)
     chain.mine(3)
     logging.info(lockfutures.getUserBalances(accounts[4], 0))
     lockfutures.claimTokens(0,1000000, {'from': accounts[4]})


def test_mint_tokens(accounts, lockfutures, erc1155):
    with reverts('To late for this vesting'):
        lockfutures.emitFutures(0,0 ,{'from': accounts[4]})

    lockfutures.emitFutures(0,1, {'from':accounts[5]})

    chain.sleep(10000)
    chain.mine(6)

    lockfutures.emitFutures(0,2, {'from':accounts[6]})

    assert erc1155.balanceOf(accounts[4],1) == (20e18 * 1250) / 10000
    assert erc1155.balanceOf(accounts[4],2) == 8.75e18


def test_claim_nft_tokens(accounts, lockfutures, erc1155, projecttoken):
    with reverts('Claiming NFT insufficient for now'):
        lockfutures.claimWithNFT(1, {'from': accounts[4]})


    chain.sleep(200000)
    chain.mine(6)

    lockfutures.claimWithNFT(1, {'from': accounts[4]})

    lockfutures.claimWithNFT(1, {'from': accounts[5]})

    assert erc1155.balanceOf(accounts[4],1) == 0
    assert erc1155.balanceOf(accounts[5],1) == 0




def test_claim_all_tokens(accounts, lockfutures, erc1155, projecttoken):
    chain.sleep(300000)
    chain.mine(6)
    lockfutures.claimTokens(0, (lockfutures.getUserBalances(accounts[4], 0))[1], {'from' :accounts[4]})
    lockfutures.claimTokens(0, (lockfutures.getUserBalances(accounts[5], 0))[1], {'from' :accounts[5]})
    lockfutures.claimWithNFT(2, {'from': accounts[6]})
    lockfutures.claimWithNFT(2, {'from': accounts[1]})




    lockfutures.claimWithNFT(2, {'from': accounts[4]})
    lockfutures.claimWithNFT(2, {'from': accounts[5]})
    lockfutures.claimTokens(0, (lockfutures.getUserBalances(accounts[6], 0))[1], {'from': accounts[6]})
    lockfutures.claimTokens(0, (lockfutures.getUserBalances(accounts[1], 0))[1], {'from': accounts[1]})


    logging.info(projecttoken.balanceOf(lockfutures.address))
    assert projecttoken.balanceOf(accounts[5]) == (LOCKED_AMOUNT * 1250) / 10000
    assert projecttoken.balanceOf(accounts[4]) == (LOCKED_AMOUNT * 1250) / 10000



def test_claim_tokens(accounts, lockfutures, erc1155, projecttoken):

    lockfutures.claimWithNFT(1, {'from': accounts[6]})
    lockfutures.claimWithNFT(1, {'from': accounts[1]})


    assert projecttoken.balanceOf(accounts[1]) == (LOCKED_AMOUNT * 86) / 10000
    assert projecttoken.balanceOf(accounts[6]) == (LOCKED_AMOUNT * 7414) / 10000
    assert projecttoken.balanceOf(lockfutures.address) == 0



