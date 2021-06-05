import pytest


@pytest.fixture(scope="module")
def projecttoken(accounts, TokenMock):
    token = accounts[0].deploy(TokenMock,"Dummy Token", "DMT")
    yield token

@pytest.fixture(scope="module")
def nulltoken(accounts, TokenMock):
    token = accounts[0].deploy(TokenMock, "Some Token", "STK")
    yield token

@pytest.fixture(scope="module")
def locker(accounts, Locker):
    locker = accounts[0].deploy(Locker)
    yield locker