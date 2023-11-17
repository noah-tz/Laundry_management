from log import Logger
from mysql_database import SqlClients

from typing import Type


class Manager:
    def __init__(self, email: str) -> None:
        self._sql_manager_connector = SqlClients(email)
        data_of_manager = self._sql_manager_connector.get_details()[0]
        self._phone_manager = data_of_manager[5]
        self._email_manager = data_of_manager[6]
        self._password = data_of_manager[7]
        self._connect_method = data_of_manager[8]

    def add_manager()

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
