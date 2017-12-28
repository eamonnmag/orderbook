from order_simulator.agents import Event, EventType
from order_simulator.service.exchange.ledger_item import TransactionItem
from order_simulator.service.exchange.ledger_item import TransactionItem, OrderItem
from datetime import datetime
from enum import Enum

from order_simulator.service.orderbook.orderbook import OrderBook


class Side(Enum):
    BUY = 'buy'
    SELL = 'sell'


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

    def place_order(self, client_id, exchange_name, side, quantity, price):
        """
        :param exchange_name:
        :param side:
        :param volume:
        :param price:
        :return:
        """
        return self.exchanges[exchange_name].place_order(client_id, quantity, price, side)

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

        self.books = {Side.BUY: OrderBook(), Side.SELL: OrderBook()}

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

    def place_order(self, client_id, quantity, price, side):
        """

        :param volume: quantity
        :param price
        :param side
        :return:
        """

        order_item = OrderItem(
            order_id=len(self.orders),  # TODO
            client_id=client_id,  # TODO
            quantity=quantity,
            side=side,
            price=price,
            timestamp=datetime.now(),
            security=self.name
        )

        self.add_order(order_item)

        self.books[side].add(order_item.order_id, order_item.timestamp, order_item.price, order_item.quantity)

        self.execute_order()

        return order_item

    def execute_order(self):
        """

        :return:
        """

        while True:
            seller = self.books[Side.SELL].peek_from_max()
            buyer = self.books[Side.BUY].peek_from_min()

            # First we check if there is a match
            # This happens when we the extremes of our triangles touch.
            # So we have a low ask and a high bid.

            if seller and buyer:

                sale_quantity = buyer.get('quantity')
                if seller.get('quantity') < buyer.get('quantity'):
                    sale_quantity = seller.get('quantity')

                # Update Seller Quantity
                self.books[Side.SELL].updateQuantity(seller.get('id'), seller.get('quantity') - sale_quantity)

                # Update Buyer Quantity
                self.add_transaction(
                    TransactionItem(order_id=buyer.get('id'), side=Side.BUY, quantity=sale_quantity,
                                    price=buyer.get('price')))

                event = Event(event_type=EventType.NEW_BUY_STATE_FOR_ONE_PRICE,
                              payload={'price': buyer.get('price'), 'side': 'buy',
                                       'quantity': sale_quantity})
                self.notify_agents(event)

                left_to_buy = max(buyer.get('quantity') - sale_quantity, 0)

                self.books[Side.BUY].updateQuantity(buyer.get('id'), left_to_buy)
            else:
                break

    def notify_agents(self, event):
        """
        :return:
        """

        for agent in self.agents:
            agent.notify(event)

        return True
