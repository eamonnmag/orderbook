import abc


class AbstractOrderBook(object):
    """
    AbstractOrderBook
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
    def get_by_id(self, id):
        """

        :param id:
        :return:
        """
