import abc
from enum import Enum

class AbstractAgent(object):

    def __init__(self, *args, **kwargs):
        self.client_id = kwargs.get('client_id')

    @abc.abstractmethod
    def place_order(self):
        """
        :return: will place an order on the system
        """
        pass

    @abc.abstractmethod
    def notify(self, event):
        """
        Called to inform the agent of a change
        @param: event - Event object containing information about what is happening on the exchange
        :return:
        """


class EventType(Enum):
    # TransactionDone(timestamp, transaction_id, price, quantity)
    TRANSACTION_DONE = 1
    # Closing
    CLOSING = 2
    # NewAskStateForOnePrice(timestamp, price, count, sum)
    NEW_ASK_STATE_FOR_ONE_PRICE = 3
    # NewBidStateForOnePrice(timestamp, price, count, sum)
    NEW_BIN_STATE_FOR_ONE_PRICE = 4
    # Opening
    OPENING = 4


class Event(object):
    """
    Event object wrapper
    """

    def __init__(self, *args, **kwargs):
        self.event_type = kwargs.get('event_type')
        self.payload = kwargs.get('payload')

    def get_payload(self):
        return self.payload

    def get_event_type(self):
        return self.event_type
