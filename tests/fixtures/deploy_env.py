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
def lockfutures(accounts, LockerFutures):
    lockfutures = accounts[0].deploy(LockerFutures, '0xFbD588c72B438faD4Cf7cD879c8F730Faa213Da0')
    yield lockfutures
