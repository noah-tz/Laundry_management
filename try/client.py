from order import Order
from messenger import Messenger
from log import Logger
from mysql_database import SqlClients
from washing_machine import WashingRoom

from gui import LaundryGui
from typing import Dict
import PySimpleGUI as sg


class Client:
    clients = {}
    def __init__(self, name: str, family: str, city: str, street: str, house_number: int, number_pone: str, email: str, message_type: str) -> None:
        self.number_pone:str = number_pone
        self.name: str = name
        self.family = family
        self.city = city
        self.street = street
        self.house_number = house_number
        self.email = email
        self.orders: Dict[int, Order] = {}
        self.message_type = message_type
    
    @Logger.log_record
    @staticmethod
    def create_object_client(email: str):
        database_connector = SqlClients()
        client_details = database_connector.get_details(email)
        person = Client(client_details[0], client_details[1], client_details[2], client_details[3], client_details[4], client_details[5], email, client_details[6])
        Client.clients[email] = person
        return person

    def open_order(self, items: dict) -> Order:
        new_order = Order(self.email, items)
        self.orders[new_order.ID] = new_order
        return new_order






if __name__ == '__main__':
    noah = Client("0527184022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
    noah.open_order()