from mysql_database import SqlMaterial, SqlSystemData, ManagerDatabase
from messenger import EmailSender, SmsSender
from log import Logger
import settings

from typing import Type

class Informer:
    def __init__(self, name: str, amount: int = None) -> None:
        """
        Constructor for the Informer class.
        Parameters:
        - name (str): The name of the informer.
        - amount (int, optional): The initial amount. Defaults to None.
        """
        self._connector: Type[ManagerDatabase] # init in subclass
        self._name_in_data: str # init in subclass
        self._name_column_value: str # init in subclass
        self._name = name
        self._check_data()
        self._amount = amount
        self._update_obj_amount()
        self._messenger = EmailSender(settings.EMAIL_MANAGER) if settings.MSG_MANAGER == "email" else SmsSender(settings.NUMBER_PHONE_MANAGER)

    def _check_data(self) -> None:
        """
        Checks if the data for the informer exists in the database, and adds it if not.
        """
        if not self._connector.check_existence():
            self._connector.add((self._name_in_data, 0))

    @Logger.log_record
    def _update_obj_amount(self) -> None:
        """
        Updates the object's amount from the database.
        """
        if not self._amount:
            self._amount = self._connector.get_value(self._name_column_value)

    @Logger.log_record
    def _update_db_amount(self) -> None:
        """
        Updates the amount in the database.
        """
        self._connector.update_value(self._name_column_value, self._amount)

class StockMaterial(Informer):
    def __init__(self, name: str, amount: int = None) -> None:
        """
        Constructor for the StockMaterial class.

        Parameters:
        - name (str): The name of the material.
        - amount (int, optional): The initial amount. Defaults to None.
        """
        self._name_in_data = f"stock {name}"
        self._name_column_value = "material_value"
        self._connector = SqlMaterial(self._name_in_data)
        self._alert = settings.ALERT_MANAGER[name]
        super().__init__(name, amount)

    def _alert_manager(self):
        """
        Sends an alert message if the material amount is below the specified threshold.
        """
        subject = f"{self._name} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {self._name} as soon as possible.\nGreetings and have a wonderful day"
        self._messenger.any_msg(subject, body)

    @Logger.log_record
    def get_material(self, remainder: int) -> int:
        """
        Retrieves a specified amount of material from stock.
        Parameters:
        - remainder (int): The remaining space in the machine's container.
        Returns:
        - int: The amount of material retrieved.
        """
        to_fill = settings.FULL_CONTAINER_MACHINE[self._name] - remainder
        amount_get = max(0, min(to_fill, self._amount))
        self._amount -= amount_get
        self._update_db_amount()
        if self._amount < self._alert:
            self._alert_manager()
        return amount_get

    @Logger.log_record
    def add_material(self, amount: int) -> None:
        """
        Adds a specified amount of material to stock.
        Parameters:
        - amount (int): The amount of material to add.
        """
        if amount != 0:
            self._amount += int(amount)
            self._update_db_amount()

class SystemData(Informer):
    def __init__(self, name: str, amount: int = None) -> None:
        """
        Constructor for the SystemData class.
        Parameters:
        - name (str): The name of the system data.
        - amount (int, optional): The initial amount. Defaults to None.
        """
        self._name_in_data = name
        self._name_column_value = "variable_value"
        self._connector = SqlSystemData(self._name_in_data)
        super().__init__(name, amount)

    @Logger.log_record
    def get_value(self) -> int:
        """
        Retrieves the current value of the system data.
        Returns:
        - int: The current value.
        """
        return self._amount

    @Logger.log_record
    def change_value(self, amount_to_add: int) -> None:
        """
        Changes the value of the system data by adding a specified amount.
        Parameters:
        - amount_to_add (int): The amount to add to the current value.
        """
        self._amount += int(amount_to_add)
        self._update_db_amount()
