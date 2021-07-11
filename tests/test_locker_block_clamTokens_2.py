import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18
zero_address_ = '0x0000000000000000000000000000000000000000'

 
def test_claimToken_2(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})

    #blocking
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
        [10e18 ,30e18, 30e18, 15e18, 15e18],
        [accounts[1] ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1500, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1
    logging.info('blocklocker.getLockRecordByIndex(lockIndex) = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)))
    amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[1], lockIndex)[1]/10000

    #blocking second time
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [current_block + 100, current_block + 200],
        [40e18 ,60e18],
        [accounts[1] ,accounts[7]],
        [4000, 6000],
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1
    logging.info('blocklocker.getLockRecordByIndex(lockIndex) = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)))

    assert projecttoken.balanceOf(blocklocker.address) == 2*LOCKED_AMOUNT

    #claim
    #mine blocks
    chain.mine(110)

    # account1 claims tokens in current round - there are several lockIndex which considers account1 in beneficiary list
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[1].address)
    claimedAmount = blocklocker.registry(accounts[1], lockIndex)[2]
   
    blocklocker.claimTokens(0, amount, {"from": accounts[1]})
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - amount
    assert projecttoken.balanceOf(accounts[1].address) == balance_account + amount
    assert blocklocker.getUserShares(accounts[1])[0][2] == amount #check claimedAmount
    logging.info('blocklocker.registry(accounts[1], lockIndex) = {}'.format(blocklocker.registry(accounts[1], lockIndex)))
    logging.info('blocklocker.getUserShares(accounts[1]) = {}'.format(blocklocker.getUserShares(accounts[1])))
    
    
    # несколько раз один и тот же счет добавлен в блокировку - потом по нему изъятие  - задача 1
    # попытка - добавить зеро адрес в бенефициары
    # попытка - добавить адрес контракта в бенефициары




