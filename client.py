from order import Order
from messenger import Messenger
from log import Logger
import settings
from mysql_database import MysqlDatabase
from washing_machine import RoomWashing

from gui import LaundryGui
from typing import Dict
import PySimpleGUI as sg


class Client:
    clients = {}
    def __init__(self, name: str, family: str, city: str, street: str, house_number: int, number_pone: str, email: str, message_type: str) -> None:
        # self.subscriptions: dict = {"annual": False, "monthly": False, "daily": False}
        self.number_pone:str = number_pone
        self.name: str = name
        self.family = family
        self.city = city
        self.street = street
        self.house_number = house_number
        self.email = email
        self.orders: Dict[int, Order] = {}
        self.message_type = message_type

    @staticmethod
    def create_object_client(email: str):
        client_details = MysqlDatabase.get_client_details(email)
        person = Client(client_details[0], client_details[1], client_details[2], client_details[3], client_details[4], client_details[5], email, client_details[6])
        Client.clients[email] = person
        return person

    def sign_in(self):
        main_client_window = LaundryGui.making_client_window(self.email)
        while True:
            event, value = main_client_window.window.read()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                self.order_pickup(value['-order number-'])
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                self.open_order(value)
        main_client_window.window.close()

    @Logger.log_record
    def order_pickup(self, order_ID):
        if order_ID in self.orders.keys():
            email_client = self.orders[order_ID].email_client
        else:
            email_client = MysqlDatabase.get_value_from_table("orders", "email_client", order_ID, "order_id")
        MysqlDatabase.update("orders", "order_collected", True, "order_id", order_ID)
        Messenger.thank_you(email_client)

    def open_order(self, items: dict) -> Order:
        new_order = Order(self.email, items)
        self.orders[new_order.ID] = new_order
        return new_order






if __name__ == '__main__':
    noah = Client("0527194022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
    noah.open_order()
    MysqlDatabase.print_by_pd("orders")
    MysqlDatabase.print_by_pd("clients")