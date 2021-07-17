import logging
import math
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 180e18

#a lot of accounts in _beneficiaries
def test_lock_token_fail(accounts, projecttoken, blocklocker):
	current_block = chain.height
	beneficiaries = []
	beneficiariesShares = []
	percents = 0
	x = blocklocker.MAX_BENEFICIARIES_PER_LOCK() + 1
	for i in range(x):
		accounts.add()
		beneficiaries.append(accounts[i+1].address)
		if i != x-1:
			beneficiariesShares.append(math.floor(blocklocker.TOTAL_IN_PERCENT() / x))
			percents += math.floor(blocklocker.TOTAL_IN_PERCENT() / x)
		else:
			beneficiariesShares.append(blocklocker.TOTAL_IN_PERCENT() - percents)
	
	y = blocklocker.MAX_VESTING_RECORDS_PER_LOCK() + 1

	_unlockedFrom =  [range(y).index(j) + current_block for j in range(y)]
	_unlockAmount = _unlockedFrom
	_lockingAmount = sum(_unlockedFrom)
	logging.info('beneficiaries len= {}'.format(len(beneficiaries) - 1))
	logging.info('VestingRecord len= {}'.format(len(_unlockAmount) - 1))
	projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})

	#with reverts("MAX_BENEFICIARIES_PER_LOCK LIMIT"):
	with reverts("MAX_BENEFICIARIES_PER_LOCK LIMIT"):
		blocklocker.lockTokens(
			projecttoken.address,
			_lockingAmount,
			_unlockedFrom,
			_unlockAmount,
			beneficiaries,
			beneficiariesShares,
			{'from': accounts[0]}
		)