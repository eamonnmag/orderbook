import pytest

from order_simulator.service.exchange import ExchangeService, Exchange


@pytest.fixture(scope='function')
def exchange_service():
    '''Returns an empty Exchange'''

    exchange_service = ExchangeService()

    exchange_service.register_exchange(Exchange(name='AAPL'))
    exchange_service.register_exchange(Exchange(name='MSFT'))

    return exchange_service
