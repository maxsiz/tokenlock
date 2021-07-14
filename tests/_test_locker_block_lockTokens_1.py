import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100
zero_address_ = '0x0000000000000000000000000000000000000000'

def test_lock_token_fail(accounts, projecttoken, blocklocker):
    current_block = chain.height
    
    #zero address
    with reverts(""):
        blocklocker.lockTokens(
            zero_address_,
            LOCKED_AMOUNT,
            [current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
            [10, 30, 30, 15, 15],
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
            [10, 30, 30, 15, 15],
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
            [10, 30, 30, 15, 15],
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
            [11, 30, 30, 15, 15],
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
            [40, 30, 15, 15],
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
            [10 ,30, 30, 15, 15],
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
            [10 ,30, 30, 15, 15],
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
            [10 ,30, 30, 15, 15],
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
            [10 ,30, 30, 15, 15],
            [blocklocker.address ,accounts[2], accounts[3], accounts[4], accounts[5], accounts[6]],
            [1500, 1500, 700, 100, 2200, 4000],
            {'from': accounts[0]}
        )

    #MAX_LOCkS_PER_BENEFICIARY LIMIT
    with reverts("MAX_LOCkS_PER_BENEFICIARY LIMIT"):
        for i in range(blocklocker.MAX_LOCkS_PER_BENEFICIARY()+2):
            blocklocker.lockTokens(
                projecttoken.address,
                LOCKED_AMOUNT,
                [current_block + 100],
                [LOCKED_AMOUNT],
                [accounts[1]],
                [blocklocker.TOTAL_IN_PERCENT()],
                {'from': accounts[0]}
            )
    #try to claim after 1000 blocking
    assert projecttoken.balanceOf(accounts[1]) == 0
    blocklocker.claimTokens(0, 1, {"from": accounts[1]})
    assert projecttoken.balanceOf(accounts[1]) == 1

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
        assert blocklocker.getUserShares(accounts[i])[0][1] == beneficiariesShares[i-2]
        assert blocklocker.getUserShares(accounts[i])[0][2] == 0
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i-2][0] == unlockedFrom[i-2]
        assert blocklocker.getLockRecordByIndex(lockIndex)[3][i-2][1] == unlockAmount[i-2]




