from laundry import LaundryRoom
from gui import LaundryGui
from auxiliary_functions import AuxiliaryFunctions
from mysql_database import ManagerDatabase
from messenger import Sender

from typing import Type


class User:
    def __init__(self) -> None:
        self._sql_connector: ManagerDatabase
        self._sender: Sender
        self._email: str
        self._password: str

    def get_email(self):
        return self._email
    
    def get_password(self):
        return self._password

    def check_existence(self) -> bool:
        return self._sql_connector.check_existence()

    def sign_in(self, laundry_gui: Type[LaundryGui], laundry_room: Type[LaundryRoom] = None):
        raise NotImplementedError

    def password_recovery(self):
        if AuxiliaryFunctions.is_valid_email(self._email):
            if self._sql_connector.check_existence():
                self._sender.password_recovery(self._password)
                LaundryGui.popup_window("The password has been sent to your email address", "The password has been sent")
            else:
                LaundryGui.popup_window("The email address is not yet registered. Please select the 'sign up' option to register", "No email address found")
        else:
            LaundryGui.popup_window("invalid email address")