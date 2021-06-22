import pytest
import logging
from brownie.test import given, strategy
from brownie import Wei, reverts, chain

LOGGER = logging.getLogger(__name__)

LOCKED_AMOUNT = 100e18


def test_futures_add(accounts, futuresmarket, projecttoken, lockfutures, erc1155):
    projecttoken.approve(lockfutures.address, projecttoken.balanceOf(accounts[0])-100000, {'from': accounts[0]})
    lockfutures.lockTokens(
        projecttoken.address,
        LOCKED_AMOUNT,
        [chain.time() + 2000000, chain.time() + 2000000, chain.time() + 2000000],
        [10e18, 20e18, 70e18],
        [accounts[1], accounts[2], accounts[3]],
        [1000, 2000, 7000],
        {'from': accounts[0]}
    )
    lockfutures.setFuturesERC1155(erc1155.address, {'from': accounts[0]})
    logging.info(lockfutures.getLockRecordByIndex(0))

    lockfutures.emitFutures(0, 2, {'from': accounts[3]})
    logging.info(erc1155.balanceOf(accounts[1], 2))

    lockfutures.emitFutures(0, 1, {'from': accounts[3]})


    asset = (erc1155.address, 2, 2)
    order_key = (accounts[0].address, 2, asset, ('0xc7ad46e0b8a400bb3c915120d284aafba8fc4735',0, 0))
    order = (order_key, 6)
    with reverts("order could be added by token owner only"):
        futuresmarket.addOrder(order, {'from': accounts[1]})


    with reverts("Your future balance is zero"):
        futuresmarket.addOrder(order, {"from": accounts[0]})

    asset = (erc1155.address, 2, 2)
    order_key = (accounts[1].address, 2, asset, (projecttoken.address,0, 1))
    order = (order_key, 6)

    with reverts("Please Approve First"):
        futuresmarket.addOrder(order, {'from': accounts[1]})

    erc1155.setApprovalForAll(futuresmarket.address, True, {'from': accounts[1]});
    futuresmarket.addOrder(order, {"from": accounts[1]})


    ## buy function
    projecttoken.approve(futuresmarket.address, 10000000000 , {'from': accounts[0]})
    futuresmarket.buyFutures(order, 6, {'from': accounts[0]})
    logging.info(erc1155.balanceOf(accounts[0], 2))

    asset = (erc1155.address, 1, 2)
    order_key = (accounts[3].address, 2, asset, (projecttoken.address, 0, 1))
    order = (order_key, 6)


    ## cancel function
    erc1155.setApprovalForAll(futuresmarket.address, True, {'from': accounts[3]});
    futuresmarket.addOrder(order, {"from": accounts[3]})
    with reverts("order could be canceled only by token owner"):
        futuresmarket.cancel(order, {'from': accounts[1]})

    cancelFut = futuresmarket.cancel(order, {'from': accounts[3]})


    assert cancelFut.events["Cancel"].values() == [accounts[3].address, 1]