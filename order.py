from log import Logger
import settings
from typing import Type
from mysql_database import SqlOrders
from messenger import SmsSender, EmailSender
from gui import LaundryGui


class Order:
    def __init__(self, email_client: str, phone_client: str, contact_method: str, items: dict, order_notes: str = 'NULL') -> None:
        self._sql_orders_connector = SqlOrders()
        self._email_client = email_client
        self._phone_client = phone_client
        self._items: dict = {}
        self._amount_items = 0
        self._ID = self._sql_orders_connector.new_order_id()
        self._cost = self.calculate_cost()
        self._notes = order_notes
        self._weight = 0
        self._sender = EmailSender(self._email_client) if contact_method == "email" else SmsSender(self._phone_client)
        if items:
            self._add_items(items)

    def get_weight(self) -> int:
        return self._weight    

    def calculate_cost(self) -> int:
        sum_order: int = sum((settings.PRISE_LIST[item] * self._items[item]) for item in self._items)
        return (max(settings.MIN_ORDER, sum_order))
    
    def calculate_time(self) -> float:
        return sum(settings.GARMENT_WEIGHT[item] * self._items[item] * settings.KILOGRAM_PER_HOUR for item in self._items.keys())
    
    @Logger.log_record
    def _add_items(self, items:dict) -> None:
        for item in items:
            item_cut = str(item).replace("-", "")
            if item_cut in settings.PRISE_LIST.keys():
                self._items[item_cut] = items[item]
                self._amount_items += items[item]
                self._weight += settings.GARMENT_WEIGHT[item_cut] * items[item]

            
    @Logger.log_record
    def _insert_to_sql(self) -> None:
        self._sql_orders_connector.add((self._ID, self._email_client, self._phone_client, self._cost, self._amount_items, self._notes, False))
    
    def order_summary(self) -> None:
        self._sender.order_summary(self._ID, self._items, int(self.calculate_cost()), int(self.calculate_time()))
        self._insert_to_sql()
        LaundryGui.popup_window(f"Your order has been successfully received!\nThe washing will be finished in {round(self.calculate_time(), 2)} hours.\nWe will notify you when your order is ready")

    def order_ready(self):
        self._sender.Your_order_is_ready(self._ID)


