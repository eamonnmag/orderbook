from order_simulator.agents import Event, EventType
from order_simulator.service.exchange.ledger_item import TransactionItem, OrderItem
from order_simulator.service.orderbook import AbstractOrderBook
from datetime import datetime
from enum import Enum

class Side(Enum):
    BUY = 1
    SELL = 2

class ExchangeService(object):
    """
    Models a loose exchange composed of Agents and a data structure
    """

    def __init__(self):
        self.exchanges = {}

    def register_exchange(self, exchange):
        """

        :param agent:
        :return:
        """
        if exchange.name not in self.exchanges:
            self.exchanges[exchange.name] = exchange
            return True

        return False

    def register_agent(self, exchange_name, agent):
        """

        :param agent:
        :return:
        """
        if exchange_name in self.exchanges:
            self.exchanges[exchange_name].register_agent(agent)
            return True

        return False

    def place_order(self, client_id, exchange_name, side, volume, price):
        """
        :param exchange_name:
        :param side:
        :param volume:
        :param price:
        :return:
        """
        return self.exchanges[exchange_name].place_order(client_id, volume, price, side)

    def get_orders(self, exchange_name):
        """

        :param exchange_name:
        :return:
        """
        return self.exchanges[exchange_name].orders

    def get_transactions(self, exchange_name):
        """

        :param exchange_name:
        :return:
        """
        return self.exchanges[exchange_name].transactions

    def notify_agents(self, exchange_name, event):
        """
        :return:
        """

        for agent in self.exchanges[exchange_name].agents:
            agent.notify(event)

        return True

    def list_exchanges(self):
        return list(self.exchanges.keys())

    def get_exchange(self, exchange_name):
        return self.exchanges[exchange_name]


class Exchange(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')

        self.agents = []

        self.orders = []
        self.transactions = []

        self.order_book = AbstractOrderBook()

    def register_agent(self, agent):
        """

        :param agent:
        :return:
        """
        if agent not in self.agents:
            self.agents.append(agent)
            return True

        return False

    def add_order(self, order):
        """

        :param item: OrderItem
        :return:
        """

        if order:
            if order not in self.orders:
                self.orders.append(order)
                return True

        return False

    def add_transaction(self, transaction):
        """

        :param item: TransactionItem
        :return:
        """

        if transaction:
            if transaction not in self.transactions:
                self.transactions.append(transaction)
                return True

        return False

    def get_orders(self):
        return self.orders

    def get_transactions(self):
        return self.transactions

    def place_order(self, client_id, volume, price, side):
        """

        :param volume: quantity
        :param price
        :param side
        :return:
        """

        order_item = OrderItem(
            order_id=len(self.orders), # TODO
            client_id=client_id, # TODO
            volume=volume,
            side=side,
            price=price,
            timestamp=datetime.now(),
            security=self.name
        )

        self.add_order(order_item)
        self.execute_order(order_item)

        return order_item

    def execute_order(self, order_item):
        """

        :return:
        """

        # either place on the order book if

        self.add_transaction(TransactionItem.create_transaction_from_order(order_item))

        event = Event(event_type=EventType.NEW_BID_STATE_FOR_ONE_PRICE,
                      payload={'price': order_item.price, 'side': order_item.side, 'volume': order_item.volume})
        self.notify_agents(event)

    def notify_agents(self, event):
        """
        :return:
        """

        for agent in self.agents:
            agent.notify(event)

        return True
