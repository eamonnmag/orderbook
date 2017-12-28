from order_simulator.agents import AbstractAgent


class BasicAgent(AbstractAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def place_order(self):
        super().place_order()

    def notify(self, event):
        super().notify(event)

        print('notified...')
