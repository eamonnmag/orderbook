import abc


class AbstractOrderBook(object):
    """
    AbstractOrderBook
    """

    @abc.abstractmethod
    def clear(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def add(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def updateQuantity(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def getOrdersByPrice(self):
        """

        :return:
        """

    @abc.abstractmethod
    def getOrdersById(self):
        """

        :return:
        """

    @abc.abstractmethod
    def getMinPrice(self):
        """

        :return:
        """

    @abc.abstractmethod
    def getMaxPrice(self):
        """

        :return:
        """

    @abc.abstractmethod
    def pop_from_max(self):
        """

        :return:
        """

    @abc.abstractmethod
    def peek_from_max(self):
        """

        :return:
        """

    @abc.abstractmethod
    def pop_from_min(self):
        """

        :return:
        """

    @abc.abstractmethod
    def peek_from_min(self):
        """

        :return:
        """

    @abc.abstractmethod
    def getQuantity(self, price):
        """

        :param price:
        :return:
        """

    @abc.abstractmethod
    def getNbOrders(self, price):
        """

        :param price:
        :return:
        """
