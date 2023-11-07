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
        self.phone_client = MysqlDatabase.get_value_from_table("clients", "phone_client", self.email_client, "email_client")
        self.items: dict = {}
        self.amount_items = 0
        self.ID = Order.start_ID
        Order.start_ID += 1
        self.amount = self.calculate_amount()
        self.notes = order_notes
        self.add_items(items)

    def calculate_amount(self) -> int:
        sum_order: int = sum((settings.GARMENT_WEIGHT[item] * self.items[item]) / 4000 for item in self.items)
        return (max(settings.MIN_ORDER, sum_order))
    
    def calculate_time(self) -> float:
        return sum(settings.GARMENT_WEIGHT[item] * self.items[item] / settings.WEIGHT_PER_HOUR for item in self.items.keys())
    
    @Logger.log_record
    def add_items(self, items:dict):
        for item in items:
            item_cut = str(item).replace("-", "")
            if item_cut in settings.PRISE_LIST.keys():
                self.items[item_cut] = items[item]
                self.amount_items += items[item]

            
    @Logger.log_record
    def __insert_to_sql(self):
        MysqlDatabase.add_order(self.ID, self.email_client, self.phone_client, self.amount, self.amount_items, self.notes)


    
    def order_summary(self):
        Messenger.order_summary(self.email_client, self.ID, self.items, int(self.calculate_amount()), int(self.calculate_time()))
        self.__insert_to_sql()
        LaundryGui.popup_window(f"Your order has been successfully received!\nEstimated completion time is {int(self.calculate_time())}")
