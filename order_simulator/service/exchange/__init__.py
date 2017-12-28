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

        minSellPrice = self.books[Side.SELL].getMinPrice()
        maxBuyPrice = self.books[Side.BUY].getMinPrice()

        # First we check if there is a match
        # This happens when we the extremes of our triangles touch.
        # So we have a low ask and a high bid.

        if len(self.books[Side.BUY].orderMapPrice) > 0 and len(self.books[Side.SELL].orderMapPrice) > 0:
            available_buyers = self.books[Side.BUY].getOrdersByPrice()[maxBuyPrice]
            available_sellers = self.books[Side.SELL].getOrdersByPrice()[minSellPrice]

            print(available_sellers)
            print(available_buyers)
            for buy_order_id in available_buyers:
                print(buy_order_id)
                buyer_obj = available_buyers[buy_order_id]

                for sell_order_id in available_sellers:
                    seller_obj = available_sellers[sell_order_id]

                    sale_quantity = buyer_obj.get('quantity')
                    if seller_obj.get('quantity') < buyer_obj.get('quantity'):
                        sale_quantity = seller_obj.get('quantity')

                    # Update Seller Quantity
                    self.books[Side.SELL].update(sell_order_id, seller_obj.get('timestamp'), seller_obj.get('price'),
                                                 seller_obj.get('quantity') - sale_quantity)

                    # Update Buyer Quantity
                    self.add_transaction(
                        TransactionItem(order_id=buy_order_id, side=Side.BUY, quantity=sale_quantity,
                                        price=seller_obj.get('price')))

                    event = Event(event_type=EventType.NEW_BID_STATE_FOR_ONE_PRICE,
                                  payload={'price': buyer_obj.get('price'), 'side': 'buy',
                                           'quantity': sale_quantity})

                    self.notify_agents(event)
                    left_to_buy = max(buyer_obj.get('quantity') - sale_quantity, 0)

                    self.books[Side.BUY].update(buy_order_id, buyer_obj.get('timestamp'), buyer_obj.get('price'),
                                                left_to_buy)

                    print('Buy Order Book')
                    print(self.books[Side.BUY])

                    print('Sell Order Book')
                    print(self.books[Side.SELL])

            # For each executed transaction, we will create a transaction in the ledger, and
            # tell our agents about the event that has just happened...

            # self.add_transaction(TransactionItem.create_transaction_from_order(order_item))

    def notify_agents(self, event):
        """
        :return:
        """

        for agent in self.agents:
            agent.notify(event)

        return True
