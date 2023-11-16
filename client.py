from log import Logger
from mysql_database import SqlClients

from gui import LaundryGui
from typing import Dict
import PySimpleGUI as sg


class Client:
    clients = {}
    def __init__(self, email: str) -> None:
        self._sql_client_connector = SqlClients(email)
        data_of_person = self._sql_client_connector.get_details()[0]
        self._phone_client = data_of_person[5]
        self._email_client = data_of_person[6]
        self._password = data_of_person[7]
        self._connect_method = data_of_person[8]

    def get_phone(self):
        return self._phone_client
    
    def get_email(self):
        return self._email_client
    
    def get_password(self):
        return self._password
    
    def get_connect_method(self):
        return self._connect_method
    
    @Logger.log_record
    @staticmethod
    def create_object_client(email: str):
        database_connector = SqlClients(email)
        client_details = database_connector.get_details(email)
        person = Client(client_details[0], client_details[1], client_details[2], client_details[3], client_details[4], client_details[5], email, client_details[6])
        Client.clients[email] = person
        return person

    # def open_order(self, items: dict) -> Order:
    #     new_order = Order(self.email, items)
    #     self.orders[new_order.ID] = new_order
    #     return new_order






if __name__ == '__main__':
    noah = Client("0527184022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
    noah.open_order()