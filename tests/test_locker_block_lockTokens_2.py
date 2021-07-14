import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100
zero_address_ = '0x0000000000000000000000000000000000000000'


#simple blocking   
def test_lock_token(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    unlockedFrom = []
    unlockAmount = []
    beneficiaries = []
    beneficiariesShares = []
    amount = 0
    amount1 = 0
    for i in [2, 3, 4, 5, 6]:
        unlockedFrom.append(current_block + i*100)
        if i != 6:
            unlockAmount.append(10)
            beneficiariesShares.append(1000)
            amount += 10
            amount1 += 1000
        else:
            unlockAmount.append(LOCKED_AMOUNT - amount)
            beneficiariesShares.append(10000 - amount1)
        beneficiaries.append(accounts[i])

    balance_before = projecttoken.balanceOf(blocklocker.address)
    #blocking
    projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        unlockedFrom,
        unlockAmount,
        beneficiaries,
        beneficiariesShares,
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1

    assert projecttoken.balanceOf(blocklocker.address) == balance_before + LOCKED_AMOUNT

    for i in [2, 3, 4, 5, 6]:
        logging.info('i check= {}'.format(i))

        assert blocklocker.registry(accounts[i], lockIndex)[1] == beneficiariesShares[i-2]
        assert blocklocker.registry(accounts[i], lockIndex)[2] == 0
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i-2][0] == unlockedFrom[i-2]
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i-2][1] == unlockAmount[i-2]