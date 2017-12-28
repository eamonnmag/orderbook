from datetime import datetime

from order_simulator.agents import Event
from order_simulator.agents.basic_agent import BasicAgent
from order_simulator.service.exchange.ledger_item import LedgerItem


def test_register(exchange_service):
    """
    :return:
    """

    agent = BasicAgent(client_id=['basic_agent'])
    exchange_service.register(agent)

    assert (len(exchange_service.observers) == 1)


def test_notify(exchange_service):
    """

    :return:
    """
    event = Event(event_type='buy', payload={'price': 10, 'volume': 5, 'security': 'AAPL'})
    exchange_service.notify_observers(event)


def test_add_to_ledger(exchange_service):
    """

    :return:
    """
    item = LedgerItem(order_id=1, item_type=LedgerItem.ORDER, client_id=1, volume=25, side='sell', price=10.2,
                      timestamp=datetime.now(), security='AAPL')

    exchange_service.update_ledger(item)

    assert (len(exchange_service.get_ledger()) == 1)
    assert (exchange_service.get_ledger()[LedgerItem.ORDER][0].order_id == 1)
    assert (exchange_service.get_ledger()[LedgerItem.ORDER][0].security == 'AAPL')

