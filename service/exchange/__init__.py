from service.orderbook import AbstractOrderBook


class ExchangeService(object):
    """
    Models a loose exchange composed of Agents and a data structure
    """

    def __init__(self):
        self.observers = []
        self.ledger = {}
        self.order_book = AbstractOrderBook()

    def register(self, agent):
        """

        :param agent:
        :return:
        """
        if not (agent in self.observers):
            self.observers.append(agent)
            return True

        return False

    def notify_observers(self, event):
        """
        :return:
        """

        for observer in self.observers:
            observer.notify(event)

        return True

    def update_ledger(self, item):
        """

        :param item: LedgerItem
        :return:
        """

        if item:
            if item.item_type not in self.ledger:
                self.ledger[item.item_type] = []

            self.ledger[item.item_type].append(item)
            return True

        return False
