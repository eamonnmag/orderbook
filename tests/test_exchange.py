from datetime import datetime

from order_simulator.agents import Event
from order_simulator.agents.basic_agent import BasicAgent
from order_simulator.service.exchange.ledger_item import LedgerItem, OrderItem


def test_register_agent(exchange_service):
    """
    :return:
    """

    agent = BasicAgent(client_id='basic_agent')

    exchange_service.register_agent('AAPL', agent)

    assert (len(exchange_service.get_exchange('AAPL').agents) == 1)


def test_notify(exchange_service):
    """

    :return:
    """
    event = Event(event_type='buy', payload={'price': 10, 'volume': 5, 'security': 'AAPL'})
    exchange_service.notify_agents('AAPL', event)


def test_add_to_ledger(exchange_service):
    """

    :return:
    """
    item = OrderItem(order_id=1, client_id=1, volume=25, side='sell', price=10.2,
                     timestamp=datetime.now(), security='AAPL')

    exchange_service.place_order('AAPL', item)

    assert (len(exchange_service.get_orders('AAPL')) == 1)


def test_buy(exchange_service):
    """

    :param exchange_service:
    :return:
    """
