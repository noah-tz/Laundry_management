from gui import Window, LaundryGui
from washing_machine import WashingRoom
from client import Client
from mysql_database import MysqlDatabase
from messenger import Messenger
from auxiliary_functions import AuxiliaryFunctions
from log import Logger
import settings
from order import Order

import PySimpleGUI as sg
from typing import Type


class MainCommunicator:
    __rooms_washing: list[WashingRoom] = [WashingRoom(number +1) for number in range(settings.NUMBER_OF_ROOMS)]
    @staticmethod
    def run():
        entry_window = LaundryGui.make_enter_window()
        while True:
            event, values = entry_window.window.read()
            if event == sg.WIN_CLOSED:
                break
            entry_window.window.hide()
            MainCommunicator.handle_event(event, values)
            LaundryGui.cleaning_boxes(entry_window.window, values)
            entry_window.window.un_hide()

    @staticmethod
    def handle_event(event, values):
        if event == "sign in":
            MainCommunicator.sign_in_program(values['-email-'], values['-password-'])
        elif event == "sign up":
            MainCommunicator.sign_up()
        elif event == "forgot my password":
            MainCommunicator.forget_my_password(values['-email-'])

    @Logger.log_record
    @staticmethod
    def sign_in_program(email: str, password: str):
        if MysqlDatabase.check_client_existence(email):
            if password == MysqlDatabase.get_value_from_table("clients", "password_client", "email_client", email):
                client = Client.create_object_client(email)
                MainCommunicator.sign_in_client(client)
            else:
                LaundryGui.popup_window("The password is incorrect", "password incorrect")
        else:
            LaundryGui.popup_window("There is no customer with this email address,\nyou can choose the 'sign up' option", "No customer found")

    @staticmethod
    def sign_in_client(client: Type[Client]):
        main_client_window = LaundryGui.making_client_window(client.email)
        while True:
            event, value = main_client_window.window.read()
            if event in [sg.WIN_CLOSED, "close"]:
                break
            elif event == '-OK_TAB_ORDER_PICKUP-':
                Order.order_pickup(value['-order number-'], client.email)
                break
            elif event == 'CREATE_IN_TAB_CREATE_ORDER':
                new_order = client.open_order(value)
                if not MainCommunicator.operating_machine(new_order):
                    LaundryGui.popup_window("All laundry rooms are occupied. Please try again later.")
                break
        main_client_window.window.close()

    @Logger.log_record
    @staticmethod
    def sign_up():
        registration_window = LaundryGui.making_registration_window()
        while True:
            event, values = registration_window.window.read()
            if event == sg.WIN_CLOSED:
                registration_window.window.close()
                break
            if MysqlDatabase.check_client_existence(values['-client_email-']):
                registration_window.window.close()
                LaundryGui.popup_window("The email address is already registered, try logging in with a username and password or click on I forgot my password", "An existing email address")
                break
            if AuxiliaryFunctions.is_valid_user_information(values):
                MysqlDatabase.add_client(values['-name-'], values['-family_name-'], values['-city-'], values['-street-'], values['-house_number-'], values['-phone-'], values['-client_email-'], values['-client_password-'], values['-message_type-'])
                registration_window.window.close()
                LaundryGui.popup_window(f"Client named {values['-name-']} {values['-family_name-']} successfully created", "Customer successfully created")
                break
        
    @staticmethod
    def forget_my_password(email):
        if AuxiliaryFunctions.is_valid_email(email):
            if MysqlDatabase.check_client_existence(email):
                Messenger.password_recovery(email)
                LaundryGui.popup_window("The password has been sent to your email address", "The password has been sent")
            else:
                LaundryGui.popup_window("The email address is not yet registered. Please select the 'sign up' option to register", "No email address found")
        else:
            LaundryGui.popup_window("invalid email address")

    @Logger.log_record
    @staticmethod
    def operating_machine(order: Type[Order]) -> bool:
        for room_washing in MainCommunicator.__rooms_washing:
            if not room_washing.is_full:
                room_washing.start_washing(order)
                order.order_summary()
                return True
        return False
    
    @staticmethod
    def end_of_program() -> None:
        Messenger.email_sender.__del__()
        for machine in MainCommunicator.__rooms_washing:
            machine.close_room()




if __name__ == "__main__":
    MainCommunicator.run()