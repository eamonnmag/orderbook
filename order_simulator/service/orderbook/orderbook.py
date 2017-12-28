from heapq import heappush, heappop
from order_simulator.service.orderbook import AbstractOrderBook


class OrderBook(AbstractOrderBook):
    def __init__(self):
        self.orderMapPrice = {}
        self.orderMapId = {}

    def clear(self):
        self.orderMapPrice = {}
        self.orderMapId = {}

    def add(self, orderid, timestamp, price, quantity):

        order = {
            'id': orderid,
            'timestamp': timestamp,
            'price': price,
            'quantity': quantity
        }

        if orderid in self.orderMapId:
            return False

        self.orderMapId[orderid] = order

        if price not in self.orderMapPrice:
            self.orderMapPrice[price] = {}

        self.orderMapPrice[price][orderid] = order

        return True

    def update(self, orderid, timestamp, price, quantity):
        if orderid not in self.orderMapId:
            return False

        order = {
            'id': orderid,
            'timestamp': timestamp,
            'price': price,
            'quantity': quantity
        }

        self.delete(orderid)
        self.add(orderid, timestamp, price, quantity)

        # old_price = self.orderMapId[orderid]['price']
        #
        # if price != old_price:
        #     self.orderMapPrice[old_price].pop(orderid, None)
        #
        # self.orderMapPrice[price][orderid] = order
        # self.orderMapId[orderid] = order

        return True

    def delete(self, orderid):
        if orderid not in self.orderMapId:
            return False

        order = self.orderMapId[orderid]
        self.orderMapId.pop(orderid, None)
        self.orderMapPrice[order['price']].pop(orderid, None)
        if not self.orderMapPrice[order['price']]:
            self.orderMapPrice.pop(order['price'], None)

        return True

    def getMinPrice(self):
        if self.orderMapPrice:
            return min(self.getOrderbookByPrice())

        return 0

    def getMaxPrice(self):
        if self.orderMapPrice:
            return max(self.getOrderbookByPrice())

        return 0

    def getOrderbookByPrice(self):
        return self.orderMapPrice

    def getOrderbookById(self):
        return self.orderMapId

# cumulative quantity per price, number of order per price
