class LedgerItem(object):
    ORDER = 'order'
    TRANSACTION = 'transaction'

    def __init__(self, *args, **kwargs):

        self.order_id = kwargs.get('order_id')
        self.item_type = kwargs.get('item_type')
        self.client_id = int(kwargs.get('client_id'))
        self.volume = int(kwargs.get('volume'))
        self.side = kwargs.get('side')
        self.price = float(kwargs.get('price'))
        self.timestamp = kwargs.get('timestamp')
        self.security = kwargs.get('security')

