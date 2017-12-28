from order_simulator.agents import Event
from order_simulator.agents.basic_agent import BasicAgent

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
