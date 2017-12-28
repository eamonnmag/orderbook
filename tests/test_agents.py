import pytest

from order_simulator.agents.buy_and_sell_one_value_less_than_last_execution import \
    BuyAndSellOneValueLessThanLastExecution
from order_simulator.service.exchange import Side


def test_buy_and_sell_one_value_less_than_last_execution(exchange_service):
    agent = BuyAndSellOneValueLessThanLastExecution(client_id="banana")

    exchange_service.register_agent('AAPL', agent)

    exchange_service.place_order(client_id='basic_agent',
                                 exchange_name="AAPL",
                                 side=Side.SELL,
                                 quantity=25,
                                 price=10.2)

    exchange_service.place_order(client_id='basic_agent',
                                 exchange_name="AAPL",
                                 side=Side.BUY,
                                 quantity=25,
                                 price=10.5)





