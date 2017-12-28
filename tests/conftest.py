import pytest

from order_simulator.service.exchange import ExchangeService


@pytest.fixture(scope='function')
def exchange_service():
    '''Returns an empty Exchange'''

    return ExchangeService()
