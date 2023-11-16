from gui import LaundryGui
from laundry import RoomLaundry
from client import Client
from mysql_database import SqlClients
from messenger import EmailSender, SmsSender
from auxiliary_functions import AuxiliaryFunctions
from log import Logger
import settings
from order import Order

import PySimpleGUI as sg
from typing import Type


class MainCommunicator:
    def __init__(self, name_laundry) -> None:
        self._name_laundry = name_laundry
        self._room_laundry = RoomLaundry()
        self._laundry_gui = LaundryGui(self._name_laundry)

    def run(self):
        while True:
            event, values = self._laundry_gui.read_window()
            if event == sg.WIN_CLOSED:
                break
            self.handle_event(event, values)
            self._laundry_gui.replace_to_enter_window()


    def handle_event(self, event, values):
        if event == "sign in":
            self.sign_in(values['-email-'], values['-password-'])
        elif event == "sign up":
            self.sign_up()
        elif event == "forgot my password":
            repeater = RepeaterPassword(values['-email-'])
            repeater.password_recovery()

    @Logger.log_record
    def sign_in(self, email: str, password: str):
        sql_client_connector = SqlClients(email)
        if sql_client_connector.check_existence():
            if password == sql_client_connector.get_value("password_client"):
                client = Client(email)
                self.sign_in_client(client)
            else:
                LaundryGui.popup_window("The password is incorrect", "password incorrect")
        else:
            LaundryGui.popup_window("There is no customer with this email address,\nyou can choose the 'sign up' option", "No customer found")

    def sign_in_client(self, client: Type[Client]):
        self._laundry_gui.replace_to_client_window(client.get_email())
        while True:
            event, value = self._laundry_gui.read_window()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                Order.order_pickup(value['-order number-'], client.get_email())
                break
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                new_order = Order(client.get_email(), client.get_phone(), client.get_connect_method(), value)
                self._room_laundry.enter_order(new_order)
                break

    @Logger.log_record
    def sign_up(self):
        self._laundry_gui.replace_to_registration_window()
        while True:
            event, values = self._laundry_gui.read_window()
            sql_client_connector = SqlClients(values['-client_email-'])
            if event == sg.WIN_CLOSED:
                break
            if sql_client_connector.check_existence():
                LaundryGui.popup_window("The email address is already registered, try logging in with a username and password or click on I forgot my password", "An existing email address")
                break
            if AuxiliaryFunctions.is_valid_user_information(values):
                sql_client_connector.add((values['-name-'], values['-family_name-'], values['-city-'], values['-street-'], values['-house_number-'], values['-phone-'], values['-client_email-'], values['-client_password-'], values['-message_type-']))
                LaundryGui.popup_window(f"Client named {values['-name-']} {values['-family_name-']} successfully created", "Customer successfully created")
                break
    
    def end_of_program(self) -> None:
        self._room_laundry.close_room()

class RepeaterPassword:
    def __init__(self, email_client) -> None:
        self.email_client = email_client

    def password_recovery(self):
        if AuxiliaryFunctions.is_valid_email(self.email_client):
            sql_client_connector = SqlClients(self.email_client)
            if sql_client_connector.check_existence():
                client = Client(self.email_client)
                password = client.get_password()
                sender = EmailSender(self.email_client)
                sender.password_recovery(password)
                LaundryGui.popup_window("The password has been sent to your email address", "The password has been sent")
            else:
                LaundryGui.popup_window("The email address is not yet registered. Please select the 'sign up' option to register", "No email address found")
        else:
            LaundryGui.popup_window("invalid email address")





if __name__ == "__main__":
    main_program = MainCommunicator()
    main_program.run()