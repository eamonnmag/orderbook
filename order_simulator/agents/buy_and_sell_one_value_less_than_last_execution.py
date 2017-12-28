from order_simulator.agents import AbstractAgent, EventType
from order_simulator.service.exchange import Side


class BuyAndSellOneValueLessThanLastExecution(AbstractAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exchange = None
        self.order_ids_sent = set()

    def place_order(self, exchange, side, volume, price):
        return self.exchange.place_order(
            client_id=self.client_id,
            exchange_name=exchange,
            quantity=volume,
            price=price,
            side=side
        )

    def notify(self, event):
        """
        :param event: Event
        :return:
        """

        data = event.get_payload()
        event_type = event.get_event_type()

        if event_type == EventType.SUCCESSFUL_REGISTRATION:
            self.exchange = data["stock_reference"]
        if event_type == EventType.TRANSACTION_DONE:
            if data["buyer_order_id"] in self.order_ids_sent:
                return
            if data["seller_order_id"] in self.order_ids_sent:
                return

            print("Transaction done")
            price = data["price"]
            quantity = data["quantity"]

            order_item = self.place_order(
                exchange="AAPL",
                side=Side.BUY,
                volume=100,
                price=price - 1
            )
            self.order_ids_sent.add(order_item.order_id)

            order_item = self.place_order(
                exchange="AAPL",
                side=Side.SELL,
                volume=100,
                price=price + 1
            )
            self.order_ids_sent.add(order_item.order_id)
