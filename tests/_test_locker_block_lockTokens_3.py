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
	x = blocklocker.MAX_VESTING_RECORDS_PER_LOCK() + 1
	for i in range(x):
		accounts.add()
		beneficiaries.append(accounts[i+1].address)
		if i != x-1:
			beneficiariesShares.append(math.floor(blocklocker.TOTAL_IN_PERCENT() / x))
			percents += math.floor(blocklocker.TOTAL_IN_PERCENT() / x)
		else:
			beneficiariesShares.append(blocklocker.TOTAL_IN_PERCENT() - percents)
	logging.info('beneficiaries = {}'.format(beneficiaries))
	projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})

	#with reverts("MAX_VESTING_RECORDS_PER_LOCK LIMIT"):
	with reverts("MAX_VESTING_RECORDS_PER_LOCK LIMIT"):
		blocklocker.lockTokens(
			projecttoken.address,
			LOCKED_AMOUNT,
			[current_block + 100, current_block + 200, current_block + 300, current_block + 400, current_block + 500],
			[36e18 ,36e18, 36e18, 36e18, 36e18],
			beneficiaries,
			beneficiariesShares,
			{'from': accounts[0]}
		)