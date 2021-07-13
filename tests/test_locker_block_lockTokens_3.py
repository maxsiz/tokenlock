import logging
from brownie import Wei, reverts, chain
import web3

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18
zero_address_ = '0x0000000000000000000000000000000000000000'

#a lot of accounts in _beneficiaries
def test_lock_token_fail(accounts, projecttoken, blocklocker):
	current_block = chain.height
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

	projecttoken.approve(blocklocker.address, projecttoken.balanceOf(accounts[0]), {'from':accounts[0]})

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