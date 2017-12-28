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
            self.orderMapPrice[price] = []

        self.orderMapPrice[price].append(orderid)


        return True


    def updateQuantity(self, orderid, quantity):
        if orderid not in self.orderMapId:
            return False

        self.orderMapId[orderid]['quantity'] = quantity

        return True


    def update(self, orderid, timestamp, price, quantity):
        if orderid not in self.orderMapId:
            return False

        self.delete(orderid)
        self.add(orderid, timestamp, price, quantity)


        return True


    def delete(self, orderid):
        if orderid not in self.orderMapId:
            return False

        order = self.orderMapId[orderid]
        self.orderMapId.pop(orderid, None)
        self.orderMapPrice[order['price']].remove(orderid)
        if not self.orderMapPrice[order['price']]:
            self.orderMapPrice.pop(order['price'], None)

        return True


    def getMinPrice(self):
        if self.orderMapPrice:
            return min(self.orderMapPrice)

        return 0

    def getMaxPrice(self):
        if self.orderMapPrice:
            return max(self.orderMapPrice)

        return 0

    def pop_from_max(self):
        max = self.getMaxPrice()
        if max == 0:
            return None

        orderid = self.orderMapPrice[max].pop(1)
        return self.orderMapId.pop(orderid, None)


    def peek_from_max(self):
        max = self.getMaxPrice()
        if max == 0:
            return None

        orderid = self.orderMapPrice[max][0]
        return self.orderMapId[orderid]


    def pop_from_min(self):
        min = self.getMinPrice()
        if min == 0:
            return None

        orderid = self.orderMapPrice[min].pop(1)
        return self.orderMapId.pop(orderid, None)


    def peek_from_min(self):
        min = self.getMinPrice()
        if min == 0:
            return None

        orderid = self.orderMapPrice[min][0]
        return self.orderMapId[orderid]


    def getOrdersByPrice(self):
        return self.orderMapPrice

    def getOrdersById(self):
        return self.orderMapId


    def getQuantity(self, price):
        if price not in self.orderMapPrice:
            return 0

        quantity = 0
        for order in self.orderMapPrice[price]:
            quantity += self.orderMapId[order]['quantity']

        return quantity


    def getNbOrders(self, price):
        if price not in self.orderMapPrice:
            return 0

        return len(self.orderMapPrice[price])
