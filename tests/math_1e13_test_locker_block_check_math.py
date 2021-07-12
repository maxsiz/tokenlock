import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 130_679_234e18

##########################################################################
##########################################################################
#### For use this test must set TOTAL_IN_PERCENT = 1e13 in LockerContract
##########################################################################

_beneficiariesShares = [3453010598455,850258350917,350731547753,712091410025,956540654348,
    1594234474928,318846910290,807745398936,956540654348,
]

START_BLOCK=10
DELTA = 100
_unlockedFrom = [
    START_BLOCK+DELTA,
    START_BLOCK+DELTA*2,
    START_BLOCK+DELTA*3,
    START_BLOCK+DELTA*4,
    START_BLOCK+DELTA*5,
    START_BLOCK+DELTA*6,
    START_BLOCK+DELTA*7,
]
_unlockedAmount = [
    1306792340e16,
    1306792340e16,
    1306792340e16,
    1960188510e16,
    1960188510e16,
    2613584680e16,
    2613584680e16
]
#Sum=10000000000000

SAFT_PER_INVESTOR = [
    45123678e18,
    11111111e18,
     4583333e18,
     9305556e18,
    12500000e18,
    20833334e18,
     4166667e18,
    10555555e18,
    12500000e18
]
#10000000000000
zero_address_ = '0x0000000000000000000000000000000000000000'

 
def test_lockToken_1(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    projecttoken.approve(blocklocker.address, LOCKED_AMOUNT, {'from':accounts[0]})
    _beneficiaries = [accounts[1],accounts[2],accounts[3],accounts[4],accounts[5],accounts[6],
    accounts[7],accounts[8],accounts[9]]

    logging.info('Shares Sum={}, TOTAL_IN_PERCENT={}, diff={}'.format(
        blocklocker.getArraySum(_beneficiariesShares),
        blocklocker.TOTAL_IN_PERCENT(),
        blocklocker.getArraySum(_beneficiariesShares)-
        blocklocker.TOTAL_IN_PERCENT()
    ))
    logging.info('Allowance={}'.format(projecttoken.allowance(accounts[0], blocklocker.address)))
    #blocking
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        _unlockedFrom,
        _unlockedAmount,
        _beneficiaries,
        _beneficiariesShares,
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1
    logging.info('blocklocker.getLockRecordByIndex(lockIndex) = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)))
    #amount = blocklocker.getLockRecordByIndex(lockIndex)[3][0][1] * blocklocker.registry(accounts[1], lockIndex)[1]/10000

    assert projecttoken.balanceOf(blocklocker.address) == LOCKED_AMOUNT

def test_claimToken_1(accounts, projecttoken, blocklocker):
    balances_after = {}
    _beneficiaries = [accounts[1],accounts[2],accounts[3],accounts[4],accounts[5],accounts[6],
    accounts[7],accounts[8],accounts[9]]
    #claim
    #mine blocks
    chain.mine(START_BLOCK)
    claimed_total = 0
    lockIndex  = blocklocker.getLockCount() - 1
    for lock in _unlockedAmount:
        chain.mine(DELTA)
        unlocked_in_vesting = 0
        for acc in _beneficiaries:
            (totalBalance,for_unlock_now) = blocklocker.getUserBalances(acc, lockIndex)
            #logging.info('acc={}, %={}'.format(acc, for_unlock_now/LOCKED_AMOUNT*100))   
            tx = blocklocker.claimTokens(lockIndex, for_unlock_now, {"from": acc})
            logging.info('Acc {} has get {}'.format(
                acc.address,
                Wei(tx.events['Transfer']['value']).to('ether')
            ))
            balances_after[acc.address] = balances_after.get(acc.address,0) + tx.events['Transfer']['value']
            unlocked_in_vesting += tx.events['Transfer']['value']
        logging.info('unlockedAmount     = {}'.format(
            Wei(lock).to('ether')
        ))
        logging.info('claimed in Vesting = {}'.format(
            Wei(unlocked_in_vesting).to('ether')
        ))
        assert Wei(lock) == Wei(unlocked_in_vesting) 
        claimed_total += unlocked_in_vesting;   
        #logging.info(balances_after)

    logging.info('************Vesting totals****************************')
    logging.info('LOCKED_AMOUNT         = {}'.format(Wei(LOCKED_AMOUNT).to('ether')))
    logging.info('Sum Vestings          = {}'.format(Wei(sum(_unlockedAmount)).to('ether')))
    logging.info('Sum SAFT_PER_INVESTOR = {}'.format(Wei(sum(SAFT_PER_INVESTOR)).to('ether')))         
    logging.info('Claimed Total         = {}'.format(Wei(claimed_total).to('ether')))
    logging.info('Balance of Locker     = {}'.format(
            Wei(projecttoken.balanceOf(blocklocker.address)).to('ether')
    ))
    for b in _beneficiaries:
        logging.info('{}:{}'.format(
            b.address,
            Wei(projecttoken.balanceOf(b.address)).to('ether')
        ))
    assert Wei(LOCKED_AMOUNT) == Wei(sum(SAFT_PER_INVESTOR))
    assert Wei(sum(SAFT_PER_INVESTOR)) == Wei(claimed_total)        
    #assert projecttoken.balanceOf(blocklocker.address) == balance_contract - amount
    #assert projecttoken.balanceOf(accounts[1].address) == balance_account + amount
    #assert blocklocker.getUserShares(accounts[1])[0][2] == amount #check claimedAmount





