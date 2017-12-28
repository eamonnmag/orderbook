from datetime import datetime

class OrderItem(object):
    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.get('order_id')
        self.client_id = kwargs.get('client_id')
        self.quantity = int(kwargs.get('quantity'))
        self.side = kwargs.get('side')
        self.price = float(kwargs.get('price'))
        self.timestamp = kwargs.get('timestamp', datetime.now())
        self.security = kwargs.get('security')


class TransactionItem(object):
    def __init__(self, *args, **kwargs):
        self.seller_order_id = kwargs.get('seller_order_id')
        self.buyer_order_id = kwargs.get('buyer_order_id')
        self.quantity = int(kwargs.get('quantity'))
        self.side = kwargs.get('side')
        self.price = float(kwargs.get('price'))
        self.timestamp = kwargs.get('timestamp', datetime.now())
        self.security = kwargs.get('security')

    @staticmethod
    def create_transaction_from_order(order_item):
        return TransactionItem(order_id=order_item.order_id,
                               client_id=order_item.client_id,
                               quantity=order_item.quantity,
                               side=order_item.side,
                               price=order_item.price,
                               timestamp=order_item.timestamp,
                               security=order_item.security)
