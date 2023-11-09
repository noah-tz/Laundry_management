from log import Logger
import settings
from typing import Type
from mysql_database import MysqlDatabase
from messenger import Messenger
from gui import LaundryGui


class Order:
    start_ID = MysqlDatabase.check_start_ID_orders()
    def __init__(self, email_client: str, items: dict, order_notes: str = None) -> None:
        self.email_client = email_client
        self.phone_client = MysqlDatabase.get_value_from_table("clients", "phone_client", "email_client", self.email_client)
        self.items: dict = {}
        self.amount_items = 0
        self.ID = Order.start_ID
        Order.start_ID += 1
        self.cost = self.calculate_cost()
        self.notes = order_notes
        if items:
            self.add_items(items)

    def calculate_cost(self) -> int:
        sum_order: int = sum((settings.PRISE_LIST[item] * self.items[item]) for item in self.items)
        return (max(settings.MIN_ORDER, sum_order))
    
    def calculate_time(self) -> float:
        return sum(settings.GARMENT_WEIGHT[item] * self.items[item] * settings.KILOGRAM_PER_HOUR for item in self.items.keys())
    
    @Logger.log_record
    def add_items(self, items:dict):
        for item in items:
            item_cut = str(item).replace("-", "")
            if item_cut in settings.PRISE_LIST.keys():
                self.items[item_cut] = items[item]
                self.amount_items += items[item]

            
    @Logger.log_record
    def __insert_to_sql(self):
        MysqlDatabase.add_order(self.ID, self.email_client, self.phone_client, self.cost, self.amount_items, self.notes)


    
    def order_summary(self):
        Messenger.order_summary(self.email_client, self.ID, self.items, int(self.calculate_cost()), int(self.calculate_time()))
        self.__insert_to_sql()
        LaundryGui.popup_window(f"Your order has been successfully received!\nThe washing will be finished in {round(self.calculate_time(), 2)} hours.\nWe will notify you when your order is ready")


    @Logger.log_record
    @staticmethod
    def order_pickup(order_ID: int, email_client):
        if not MysqlDatabase.get_value_from_table('orders', 'order_collected', 'order_id', order_ID):
            MysqlDatabase.update("orders", "order_collected", True, "order_id", order_ID)
            order_cost = MysqlDatabase.get_value_from_table('orders', 'order_cost', 'order_id',order_ID)
            LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
            LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
            Messenger.thank_you(email_client)
        else:
            LaundryGui.popup_window('Your order has already been collected')
