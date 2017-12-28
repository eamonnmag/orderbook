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
    def delete(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

    @abc.abstractmethod
    def getOrderbookByPrice(self):
        """

        :return:
        """

    @abc.abstractmethod
    def getOrderbookById(self):
        """

        :return:
        """

    def getMinPrice(self):
        """

        :return:
        """

    def getMaxPrice(self):
        """

        :return:
        """
