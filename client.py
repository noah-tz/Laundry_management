from log import Logger
from auxiliary_functions import AuxiliaryFunctions
from mysql_database import SqlClients, SqlOrders
from messenger import EmailSender, SmsSender
from laundry import LaundryRoom
from gui import LaundryGui
from order import Order
from user import User

from typing import Type
import PySimpleGUI as sg


class Client(User):
    def __init__(self, email: str) -> None:
        self._email = email
        self._sql_connector = SqlClients(self._email)
        if self._sql_connector.check_existence():
            data_of_client = self._sql_connector.get_details()[0]
            self._phone = data_of_client[5]
            self._password = data_of_client[7]
            self._connect_method = data_of_client[8]
            self._sender = EmailSender(self._email) if self._connect_method == "email" else SmsSender(self._phone_client)

    def get_phone(self):
        return self._phone
    
    def get_connect_method(self):
        return self._connect_method
    
    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        laundry_gui.replace_to_client_window(self._email)
        while True:
            event, value = laundry_gui.read_window()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                self.order_pickup(value['-order number-'])
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                new_order = Order(self._email, self._phone, self._connect_method, value)
                laundry_room.enter_order(new_order)

    @Logger.log_record    
    def order_pickup(self, order_ID: int) -> None:
        sql_orders_connector = SqlOrders(order_ID)
        email_client_order = sql_orders_connector.get_value("email_client")
        if email_client_order == self._email: 
            if not sql_orders_connector.get_value('order_collected'):
                sql_orders_connector.update_value("order_collected", True)
                order_cost = sql_orders_connector.get_value('order_cost')
                LaundryGui.popup_window(f'Please complete the payment of {order_cost}\nClick OK to pay.')
                LaundryGui.popup_window(f'The payment was successful.\nOrder number {order_ID} has been collected.\nThank you!')
                self._sender.thank_you()
            else:
                LaundryGui.popup_window('Your order has already been collected')
        else:
            LaundryGui.popup_window('No order associated with you with this number was found')
    







if __name__ == '__main__':
    noah = Client("0527184022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
