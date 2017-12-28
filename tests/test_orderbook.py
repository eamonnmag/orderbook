import pytest

from order_simulator.service.orderbook.orderbook import OrderBook
import datetime


@pytest.fixture(scope='module')
def ob():
    return OrderBook()


def test_empty(ob):
    assert ob.getMinPrice() == 0
    assert ob.getMaxPrice() == 0
    assert ob.getOrderbookByPrice() == {}
    assert ob.getOrderbookById() == {}


def test_add(ob):
    ob.add(1, datetime.datetime.now(), 18, 10)
    assert ob.getMinPrice() == 18
    assert ob.getMaxPrice() == 18
    print(ob.getOrderbookByPrice())

def test_update(ob):
    print(ob.getOrderbookByPrice())
    ob.update(1, datetime.datetime.now(), 25, 100)
    print(ob.getOrderbookByPrice())
    assert ob.getMinPrice() == 25
    assert ob.getMaxPrice() == 25
    print(ob.getOrderbookByPrice())

def test_delete(ob):
    print(ob.getOrderbookByPrice())
    ob.delete(1)
    print(ob.getOrderbookByPrice())
    assert ob.getMinPrice() == 0
    assert ob.getMaxPrice() == 0


def test_quantity(ob):
    ob.add(1, datetime.datetime.now(), 18, 10)
    ob.add(2, datetime.datetime.now(), 18, 10)
    ob.add(3, datetime.datetime.now(), 18, 10)
    ob.add(4, datetime.datetime.now(), 18, 10)
    ob.add(5, datetime.datetime.now(), 18, 10)
    assert ob.getQuantity(18) == 50


def test_nborders(ob):
    assert ob.getNbOrders(18) == 5
