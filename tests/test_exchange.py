from order_simulator.agents import Event
from order_simulator.agents.basic_agent import BasicAgent
from order_simulator.service.exchange import Side


def test_register_agent(exchange_service):
    """
    :return:
    """

    agent_1 = BasicAgent(client_id='basic_agent_1')
    agent_2 = BasicAgent(client_id='basic_agent_2')

    agent_1.exchange = exchange_service.register_agent('AAPL', agent_1)
    agent_2.exchange = exchange_service.register_agent('AAPL', agent_2)

    assert (len(exchange_service.get_exchange('AAPL').agents) == 2)


def test_notify(exchange_service):
    """

    :return:
    """
    event = Event(event_type='buy', payload={'price': 10, 'volume': 5, 'security': 'AAPL'})
    exchange_service.notify_agents('AAPL', event)


def test_place_order(exchange_service):
    """

    :return:
    """

    exchange_service.place_order(client_id='basic_agent',
                                 exchange_name="AAPL",
                                 side=Side.SELL,
                                 quantity=25,
                                 price=10.2)

    exchange_service.place_order(client_id='basic_agent',
                                 exchange_name="AAPL",
                                 side=Side.SELL,
                                 quantity=25,
                                 price=10.5)

    assert (len(exchange_service.get_orders('AAPL')) == 2)

    exchange_service.place_order(client_id='basic_agent',
                                 exchange_name="AAPL",
                                 side=Side.BUY,
                                 quantity=15,
                                 price=10.2)

    assert (len(exchange_service.get_orders('AAPL')) == 3)


