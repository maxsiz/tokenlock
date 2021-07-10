import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18
zero_address_ = '0x0000000000000000000000000000000000000000'

 
def test_claimToken(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    '''logging.info('unlockedFrom = {}'.format(unlockedFrom))
    logging.info('unlockAmount = {}'.format(unlockAmount))
    logging.info('beneficiaries = {}'.format(beneficiaries))
    logging.info('beneficiariesShares = {}'.format(beneficiariesShares))'''

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
    
    '''logging.info('blocklocker.registry(accounts[3], lockIndex) = {}'.format(blocklocker.registry(accounts[3], lockIndex)))'''

    assert projecttoken.balanceOf(blocklocker.address) == LOCKED_AMOUNT

    ################################################revert cases####################################
    #nonexist lockIndex
    with reverts("Lock record not saved yet"):
        blocklocker.claimTokens(100, 1, {"from": accounts[1]})

    #zero amount
    with reverts("Cant claim zero"):
        blocklocker.claimTokens(0, 0, {"from": accounts[1]})

    #account is not in list of beneficiaries
    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, 1, {"from": accounts[7]})

    #block for claiming  has not come
    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, 1, {"from": accounts[1]})

    ############################################claiming cases####################################
    #mine blocks
    chain.mine(102)
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[1].address)
    logging.info('blocklocker.registry(accounts[1], lockIndex) = {}'.format(blocklocker.registry(accounts[1], lockIndex)))
    #account1  claims
    blocklocker.claimTokens(0, 1, {"from": accounts[1]})
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - 1
    assert projecttoken.balanceOf(accounts[1].address) == balance_account + 1
    assert blocklocker.registry(accounts[1], lockIndex)[2] == 1 #check claimedAmount
    logging.info('blocklocker.registry(accounts[1], lockIndex) = {}'.format(blocklocker.registry(accounts[1], lockIndex)))

    #account1 claims again in first round
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[1].address)
    claimedAmount = blocklocker.registry(accounts[1], lockIndex)[2]
    blocklocker.claimTokens(0, 1, {"from": accounts[1]})
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - 1
    assert projecttoken.balanceOf(accounts[1].address) == balance_account + 1
    assert blocklocker.registry(accounts[1], lockIndex)[2] == claimedAmount + 1 #check claimedAmount
    logging.info('blocklocker.registry(accounts[1], lockIndex) = {}'.format(blocklocker.registry(accounts[1], lockIndex)))

    #account 1 tries to claim tokens more than account can get
    amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[1], lockIndex)[1]/10000
    logging.info('amount = {}'.format(amount))
    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, amount, {"from": accounts[1]})

    # logging.info('chain.height = {}'.format(chain.height))
    # account2 claims tokens in current round
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[2].address)
    claimedAmount = blocklocker.registry(accounts[2], lockIndex)[2]
    amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[2], lockIndex)[1]/10000
    blocklocker.claimTokens(0, amount, {"from": accounts[2]})
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - amount
    assert projecttoken.balanceOf(accounts[2].address) == balance_account + amount
    assert blocklocker.registry(accounts[2], lockIndex)[2] == claimedAmount + amount #check claimedAmount
    logging.info('blocklocker.registry(accounts[2], lockIndex) = {}'.format(blocklocker.registry(accounts[2], lockIndex)))

    # second account claims tokens in current round again - there is no tokens for claiming of account2
    amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[2], lockIndex)[1]/10000
    with reverts("Insufficient for now"):
        blocklocker.claimTokens(0, amount, {"from": accounts[2]})
    
    logging.info('blocklocker.registry(accounts[2], lockIndex) = {}'.format(blocklocker.registry(accounts[2], lockIndex)))

    #account 3 ignored possibility to claiming in first round. Account 3 tries to get all tokens in second round
    #mine blocks
    chain.mine(102)
    amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[3], lockIndex)[1]/10000
    amount = amount + blocklocker.getLockRecordByIndex(lockIndex)[3][1][1] * blocklocker.registry(accounts[3], lockIndex)[1]/10000
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[3].address)
    claimedAmount = blocklocker.registry(accounts[3], lockIndex)[2]
    blocklocker.claimTokens(0, amount, {"from": accounts[3]})
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - amount
    assert projecttoken.balanceOf(accounts[3].address) == balance_account + amount
    assert blocklocker.registry(accounts[3], lockIndex)[2] == claimedAmount + amount #check claimedAmount
    logging.info('blocklocker.registry(accounts[3], lockIndex) = {}'.format(blocklocker.registry(accounts[3], lockIndex)))

############################################account was added in beneficiary list several time
def test_claimToken_1(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    #blocking
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [current_block + 100, current_block + 200],
        [40e18 ,60e18],
        [accounts[7] ,accounts[7]],
        [4000, 6000],
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1
    logging.info('blocklocker.getLockRecordByIndex(lockIndex) = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)))

    #mine blocks
    chain.mine(105)
    logging.info('blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)[3][0][1]))

    #amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] #there are two beneficiaries. Both equals account7
    #amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] # * blocklocker.registry(accounts[3], lockIndex)[1]/10000
    amount =  1
    logging.info('amount = {}'.format(amount))
    balance_contract = projecttoken.balanceOf(blocklocker.address)
    balance_account = projecttoken.balanceOf(accounts[7].address)
    claimedAmount = blocklocker.registry(accounts[7], lockIndex)[2]

    logging.info('blocklocker.registry(accounts[7], lockIndex) = {}'.format(blocklocker.registry(accounts[7], lockIndex)))
    logging.info('blocklocker.getUserBalances(accounts[7], lockIndex) = {}'.format(blocklocker.getUserBalances(accounts[7], lockIndex)))

    blocklocker.claimTokens(lockIndex, amount, {"from": accounts[7]})
    
    assert projecttoken.balanceOf(blocklocker.address) == balance_contract - amount
    assert projecttoken.balanceOf(accounts[7].address) == balance_account + amount
    assert blocklocker.registry(accounts[7], lockIndex)[2] == claimedAmount + amount #check claimedAmount
    
    
    # несколько раз один и тот же счет добавлен в блокировку - потом по нему изъятие  - задача 1
    # попытка - добавить зеро адрес в бенефициары
    # попытка - добавить адрес контракта в бенефициары




