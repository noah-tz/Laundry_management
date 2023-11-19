from log import Logger
from mysql_database import SqlClients
from user import User

from typing import Type


class Manager(User):
    def __init__(self, email: str) -> None:
        self._email_manager = email
        self._sql_manager_connector = SqlClients(self._email_manager)
        if self._sql_manager_connector.check_existence():
            data_of_manager = self._sql_manager_connector.get_details()[0]
            self._phone_manager = data_of_manager[5]
            self._password = data_of_manager[7]
            self._connect_method = data_of_manager[8]

    def add_manager(values: dict):
        return False


    def get_phone(self):
        return self._phone_manager
    
    def get_email(self):
        return self._email_manager
    
    def get_password(self):
        return self._password
    
    def get_connect_method(self):
        return self._connect_method
    
    


if __name__ == '__main__':
    noah = Manager("0527184022", "noah", "tzitrenboim", "bet shemesh", "miryam", 12, "t0527184022@gmail.com", "2345")
