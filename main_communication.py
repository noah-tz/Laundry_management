from gui import Window, LaundryGui
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
    def __init__(self) -> None:
        self.__room_laundry = RoomLaundry()

    def run(self):
        entry_window = LaundryGui.make_enter_window()
        while True:
            event, values = entry_window.window.read()
            if event == sg.WIN_CLOSED:
                break
            entry_window.window.hide()
            self.handle_event(event, values)
            LaundryGui.cleaning_boxes(entry_window.window, values)
            entry_window.window.un_hide()

    def handle_event(self, event, values):
        if event == "sign in":
            self.sign_in(values['-email-'], values['-password-'])
        elif event == "sign up":
            self.sign_up()
        elif event == "forgot my password":
            self.forget_password(values['-email-'])

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
        main_client_window = LaundryGui.making_client_window(client.get_email())
        while True:
            event, value = main_client_window.window.read()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                Order.order_pickup(value['-order number-'], client.get_email())
                break
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                print(value)
                new_order = Order(client.get_email(), client.get_phone(), client.get_connect_method(), value)
                self.__room_laundry.enter_order(new_order)
                break
        main_client_window.window.close()

    @Logger.log_record
    def sign_up(self):
        registration_window = LaundryGui.making_registration_window()
        while True:
            event, values = registration_window.window.read()
            sql_client_connector = SqlClients(values['-client_email-'])
            if event == sg.WIN_CLOSED:
                registration_window.window.close()
                break
            if sql_client_connector.check_existence():
                registration_window.window.close()
                LaundryGui.popup_window("The email address is already registered, try logging in with a username and password or click on I forgot my password", "An existing email address")
                break
            if AuxiliaryFunctions.is_valid_user_information(values):
                sql_client_connector.add((values['-name-'], values['-family_name-'], values['-city-'], values['-street-'], values['-house_number-'], values['-phone-'], values['-client_email-'], values['-client_password-'], values['-message_type-']))
                registration_window.window.close()
                LaundryGui.popup_window(f"Client named {values['-name-']} {values['-family_name-']} successfully created", "Customer successfully created")
                break
        
    def forget_password(self, email):
        if AuxiliaryFunctions.is_valid_email(email):
            sql_client_connector = SqlClients(email)
            if sql_client_connector.check_existence():
                client = Client(email)
                password = client.get_password()
                sender = EmailSender(email)
                sender.password_recovery(password)
                LaundryGui.popup_window("The password has been sent to your email address", "The password has been sent")
            else:
                LaundryGui.popup_window("The email address is not yet registered. Please select the 'sign up' option to register", "No email address found")
        else:
            LaundryGui.popup_window("invalid email address")

    def end_of_program(self) -> None:
        self.__room_laundry.close_room()




if __name__ == "__main__":
    main_program = MainCommunicator()
    main_program.run()