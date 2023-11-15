from log import Logger
import settings
from client import Client
from typing import Type
from mysql_database import SqlOrders, SqlClients
from messenger import SmsSender, EmailSender
from gui import LaundryGui


class Order:
    def __init__(self, email_client: str, phone_client: str, contact_method: str, items: dict, order_notes: str = 'NULL') -> None:
        self.__sql_orders_connector = SqlOrders()
        self.__email_client = email_client
        self.__phone_client = phone_client
        self.__items: dict = {}
        self.__amount_items = 0
        self.__ID = self.__sql_orders_connector.new_order_id()
        self.__cost = self.calculate_cost()
        self.__notes = order_notes
        self.weight = 0
        self.__set_contact_method(contact_method)
        if items:
            self.add_items(items)
        self.__insert_to_sql()

    def __set_contact_method(self, contact_method: str) -> None:
        if contact_method == "email":
            self.__sender = EmailSender(self.__email_client)
        else:
            self.__sender = SmsSender(self.__phone_client)      

    def calculate_cost(self) -> int:
        sum_order: int = sum((settings.PRISE_LIST[item] * self.__items[item]) for item in self.__items)
        return (max(settings.MIN_ORDER, sum_order))
    
    def calculate_time(self) -> float:
        return sum(settings.GARMENT_WEIGHT[item] * self.__items[item] * settings.KILOGRAM_PER_HOUR for item in self.__items.keys())
    
    @Logger.log_record
    def add_items(self, items:dict) -> None:
        for item in items:
            item_cut = str(item).replace("-", "")
            if item_cut in settings.PRISE_LIST.keys():
                self.__items[item_cut] = items[item]
                self.__amount_items += items[item]
                self.weight += settings.GARMENT_WEIGHT[item_cut] * items[item]

            
    @Logger.log_record
    def __insert_to_sql(self) -> None:
        self.__sql_orders_connector.add((self.__ID, self.__email_client, self.__phone_client, self.__cost, self.__amount_items, self.__notes, False))
    
    def order_summary(self) -> None:
        self.__sender.order_summary(self.__ID, self.__items, int(self.calculate_cost()), int(self.calculate_time()))
        self.__insert_to_sql()
        LaundryGui.popup_window(f"Your order has been successfully received!\nThe washing will be finished in {round(self.calculate_time(), 2)} hours.\nWe will notify you when your order is ready")

    def order_ready(self):
        self.__sender.Your_order_is_ready(self.__ID)

    @Logger.log_record
    @staticmethod
    def order_pickup(order_ID: int, email_client) -> None:
        sql_orders_connector = SqlOrders(order_ID)
        if not sql_orders_connector.get_value('order_collected'):
            sql_orders_connector.update_value("order_collected", True)
            order_cost = sql_orders_connector.get_value('order_cost')
            LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
            LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
            person = Client(email_client)
            connect_method = person.get_connect_method()
            if connect_method == "email":
                sender = EmailSender(email_client)
            else:
                phone_client = person.get_phone()
                sender = SmsSender(phone_client)
            sender.thank_you()
        else:
            LaundryGui.popup_window('Your order has already been collected')
