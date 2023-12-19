from gui import LaundryGui
from laundry import LaundryRoom
from user import User, Client, Manager
from mysql_database import ManagerDatabase, SqlClients
from auxiliary_functions import AuxiliaryFunctions
from log import Logger
from information import SystemData
from messenger import EmailSender

import PySimpleGUI as sg
from typing import Type


class MainCommunicator:
    def __init__(self, name_laundry) -> None:
        """
        MainCommunicator constructor.
        Args:
        - name_laundry (str): The name of the laundry.
        """
        self._name_laundry = name_laundry
        self._laundry_room = LaundryRoom()
        self._laundry_gui = LaundryGui(self._name_laundry)

    @Logger.log_record
    def run(self):
        """
        Run the main program loop.
        This function continuously reads events from the GUI and handles them until the window is closed.
        """
        while True:
            event, values = self._laundry_gui.read_window()
            if event == sg.WIN_CLOSED:
                break
            self.handle_event(event, values)

    def handle_event(self, event, values):
        """
        Handle GUI events.
        Args:
        - event (str): The event triggered in the GUI.
        - values (dict): The values associated with the GUI elements.

        This function delegates the handling of specific events to corresponding methods.
        """
        if event == '-registration-':
            self.registration(values)
            return
        user = Client(values['-email_client-']) if "client" in event else Manager(values['-email_manager-'])
        if 'sign_in' in event:
            password_entered = values['-password_client-'] if "client" in event else values['-password_manager-']
            password = ManagerDatabase.hash_password(password_entered)
            self.sign_in(user, password)
            return

    def sign_in(self, user: Type[User], password: str):
        """
        Handle the sign-in process.
        Args:
        - user (Type[User]): An instance of the User class.
        - password (str): The password entered by the user.
        This function checks the existence of the user and verifies the password for sign-in.
        """
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
        """
        Handle the user registration process.
        Args:
        - values (dict): The values entered by the user in the registration form.
        This function performs user registration and updates the number of customers in the system.
        """
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
                ManagerDatabase.hash_password(values['-password_registration-']), 
                values['-message_type_registration-']))
            costumer_informed = SystemData("number of customers")
            costumer_informed.change_value(1)
            LaundryGui.popup_window(f"Client named {values['-name_registration-']} {values['-family_name_registration-']} successfully created", "Customer successfully created")

    def end_of_program(self) -> None:
        """
        Close the laundry room at the end of the program.
        """
        self._laundry_room.close_room()
        EmailSender.close_server()


if __name__ == "__main__":
    # Instantiate the MainCommunicator and run the program
    main_program = MainCommunicator("LaundryName")
    main_program.run()
