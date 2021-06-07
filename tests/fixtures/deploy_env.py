import pytest


@pytest.fixture(scope="module")
def projecttoken(accounts, TokenMock):
    token = accounts[0].deploy(TokenMock, "Dummy Token", "DMT")
    yield token


@pytest.fixture(scope="module")
def nulltoken(accounts, TokenMock):
    token = accounts[0].deploy(TokenMock, "Some Token", "STK")
    yield token

@pytest.fixture(scope="module")
def locker(accounts, Locker):
    locker = accounts[0].deploy(Locker)
    yield locker


@pytest.fixture(scope="module")
def erc1155(accounts, Futures1155):
    e = accounts[0].deploy(Futures1155, "https://nft.iber.group/degenfarm/V1/locks")
    yield e

@pytest.fixture(scope="module")
def lockfutures(accounts, LockerFutures, erc1155):
    lockfutures = accounts[0].deploy(LockerFutures)
    lockfutures.setFuturesERC1155(erc1155.address)
    yield lockfutures
