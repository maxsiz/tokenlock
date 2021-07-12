import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18
zero_address_ = '0x0000000000000000000000000000000000000000'

def test_lock_token_fail(accounts, projecttoken, blocklocker):
    current_block = chain.height
    
    #zero address
    with reverts(""):
        blocklocker.lockTokens(
            zero_address_,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18, 30e18, 30e18, 15e18, 15e18],
            [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # amount = 0
    with reverts("Cant lock 0 amount"):
        blocklocker.lockTokens(
            projecttoken.address,
            0,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18, 30e18, 30e18, 15e18, 15e18],
            [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # without allowance
    with reverts("Please approve first"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18, 30e18, 30e18, 15e18, 15e18],
            [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )
    projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})
    
    # _unlockAmount is incorrect
    with reverts("Sum vesting records must be equal lock amount"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [11e18, 30e18, 30e18, 15e18, 15e18],
            [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # lengths of _unlockedFrom and _unlockAmount do not equal
    with reverts("Length of periods and amounts arrays must be equal"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [40e18, 30e18, 15e18, 15e18],
            [accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # lengths of _beneficiaries and _beneficiariesShares do not equal
    with reverts("Length of beneficiaries and shares arrays must be equal"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            [accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # sum of shares is incorrect
    with reverts("Sum of shares array must be equal to 100%"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            [accounts[1] ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1600, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )
    # add zero address to beneficiary list
    with reverts("Cant add zero address"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            [zero_address_ ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    # add contract address to beneficiary list
    with reverts("Bad idea"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            [blocklocker.address ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    #a lot of accounts in _beneficiaries
    beneficiaries = []
    beneficiariesShares = []
    x = blocklocker.MAX_VESTING_RECORDS_PER_LOCK() + 1
    for i in range(x):
        accounts.add()
        beneficiaries.append(accounts[i+1])
        if i != blocklocker.MAX_VESTING_RECORDS_PER_LOCK():
            beneficiariesShares.append(blocklocker.TOTAL_IN_PERCENT()/blocklocker.MAX_VESTING_RECORDS_PER_LOCK())
        else:
            beneficiariesShares.append(0)
        logging.info('i = {}'.format(i))
    with reverts("MAX_VESTING_RECORDS_PER_LOCK LIMIT"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            beneficiaries,
            beneficiariesShares,
            {'from': accounts[0]}
        )

    #MAX_LOCkS_PER_BENEFICIARY LIMIT

    '''with reverts("MAX_LOCkS_PER_BENEFICIARY LIMIT"):
        blocklocker.lockTokens(
            projecttoken.address,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10e18 ,30e18, 30e18, 15e18, 15e18],
            [accounts[1] ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )'''


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
    for i in range(6):
        unlockedFrom.append(current_block + (i+1)*100)
        if i != 5:
            unlockAmount.append(10e18)
            beneficiariesShares.append(1000)
            amount += 10e18
            amount1 += 1000
        else:
            unlockAmount.append(LOCKED_AMOUNT - amount)
            beneficiariesShares.append(10000 - amount1)
        beneficiaries.append(accounts[i+1])
    '''logging.info('unlockedFrom = {}'.format(unlockedFrom))
    logging.info('unlockAmount = {}'.format(unlockAmount))
    logging.info('beneficiaries = {}'.format(beneficiaries))
    logging.info('beneficiariesShares = {}'.format(beneficiariesShares))'''

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
    '''logging.info('blocklocker.getLockRecordByIndex(lockIndex) = {}'.format(blocklocker.getLockRecordByIndex(lockIndex)))
    logging.info('blocklocker.registry(accounts[1], lockIndex) = {}'.format(blocklocker.registry(accounts[1], lockIndex)))
    logging.info('blocklocker.registry(accounts[3], lockIndex) = {}'.format(blocklocker.registry(accounts[3], lockIndex)))'''

    assert projecttoken.balanceOf(blocklocker.address) == LOCKED_AMOUNT
    for i in range(6):
        assert blocklocker.registry(accounts[i + 1], lockIndex)[1] == beneficiariesShares[i]
        assert blocklocker.registry(accounts[i + 1], lockIndex)[2] == 0
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i][0] == unlockedFrom[i]
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i][1] == unlockAmount[i]


#a lot of rounds
'''def test_lock_token_too_many_rounds(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    unlockedFrom = []
    unlockAmount = []
    beneficiaries = []
    beneficiariesShares = []
    amount = 0
    amount1 = 0
    for i in range(1000):
        unlockedFrom.append(current_block + (i+1)*100)
        unlockAmount.append(LOCKED_AMOUNT/1000)

    #blocking
    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        unlockedFrom,
        unlockAmount,
        [accounts[1] ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
        [1600, 1500, 700, 100, 2200, 4000],
        {'from': accounts[0]}
    )
    lockIndex = blocklocker.getLockCount() - 1

    assert projecttoken.balanceOf(blocklocker.address) == LOCKED_AMOUNT
    for i in range(1000):
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i][0] == unlockedFrom[i]
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i][1] == unlockAmount[i]'''

#a lot of accounts in _beneficiaries
'''def test_lock_token_too_many_accounts(accounts, projecttoken, blocklocker):
    #prepare data
    current_block = chain.height
    unlockedFrom = []
    unlockAmount = []
    beneficiaries = []
    beneficiariesShares = []
    amount = 0
    amount1 = 0
    for i in range(5):
        unlockedFrom.append(current_block + (i+1)*100)
        unlockAmount.append(LOCKED_AMOUNT/5)
    for i in range(1000):
        accounts.add()
        beneficiaries.append(accounts[i+1])
        beneficiariesShares.append(10)

    blocklocker.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        unlockedFrom,
        unlockAmount,
        beneficiaries,
        beneficiariesShares,
        {'from': accounts[0]}
    )'''


    # несколько раз сделать изъятие токенов по одному счету за раунд
    # по нескольким счетам сделать изъятие за раунд
    # попытка изъять, когда все уже выбрано счетом за раунд
    # несколько раз один и тот же счет добавлен в блокировку - потом по нему изъятие
    # пропустил раунд и не забирал монеты, потом во втором раунде за один раз за два раунда пытается забрать
    # попытка - добавить зеро адрес в бенефициары
    # попытка - добавить адрес контракта в бенефициары




