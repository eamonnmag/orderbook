import abc


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
