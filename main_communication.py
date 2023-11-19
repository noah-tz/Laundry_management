from gui import LaundryGui
from laundry import LaundryRoom
from user import User, Client, Manager
from mysql_database import SqlClients
from auxiliary_functions import AuxiliaryFunctions
from log import Logger
from information import SystemData
import settings

import PySimpleGUI as sg
from typing import Type


class MainCommunicator:
    def __init__(self, name_laundry) -> None:
        self._name_laundry = name_laundry
        self._laundry_room = LaundryRoom()
        self._laundry_gui = LaundryGui(self._name_laundry)

    def run(self):
        while True:
            event, values = self._laundry_gui.read_window()
            if event == sg.WIN_CLOSED:
                break
            self.handle_event(event, values)

    def handle_event(self, event, values):
        if event == '-registration-':
            self.registration(values)
            return
        user = Client(values['-email_client-']) if "client" in event else Manager(values['-email_manager-'])
        # user.sign_in(self._laundry_gui, self._laundry_room)
        # return
        if 'sign_in' in event:
            password = values['-password_client-'] if "client" in event else values['-password_manager-']
            self.sign_in(user, password)
            return
        user.password_recovery()
        
    def sign_in(self, user: Type[User], password: str):
        if user.check_existence():
            if password == user.get_password():
                user.sign_in(self._laundry_gui, self._laundry_room)
                self._laundry_gui.replace_to_enter_window()
            else:
                LaundryGui.popup_window("The password is incorrect", "password incorrect")
        else:
            LaundryGui.popup_window("There is no user with this email address", "No user found")

    @Logger.log_record
    def registration(self, values):
        sql_client_connector = SqlClients(values['-email_registration-'])
        if sql_client_connector.check_existence():
            LaundryGui.popup_window("The email address is already registered, try logging in with a username and password or click on I forgot my password", "An existing email address")
        elif AuxiliaryFunctions.is_valid_user_information(values):
            sql_client_connector.add((
                values['-name_registration-'],
                values['-family_name_registration-'],
                values['-city_registration-'],
                values['-street_registration-'],
                values['-house_number_registration-'],
                values['-phone_registration-'],
                values['-email_registration-'],
                values['-password_registration-'], 
                values['-message_type_registration-']))
            costumer_informed = SystemData("number of costumers")
            costumer_informed.change_value(1)
            LaundryGui.popup_window(f"Client named {values['-name_registration-']} {values['-family_name_registration-']} successfully created", "Customer successfully created")
    
    def end_of_program(self) -> None:
        self._laundry_room.close_room()





if __name__ == "__main__":
    main_program = MainCommunicator()
    main_program.run()