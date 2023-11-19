from mysql_database import SqlMaterial, SqlSystemData, ManagerDatabase
from messenger import EmailSender, SmsSender
from log import Logger
import settings

from typing import Type



class Informer:
    def __init__(self, name: str, amount: int = None) -> None:
        if 0:
            self._connector: Type[ManagerDatabase]
            self._name_in_data: str
            self._name_column_value: str
        self._name = name
        self._check_data()
        self._amount = amount
        self._update_obj_amount()
        self._messenger = EmailSender(settings.EMAIL_MANAGER) if settings.MSG_MANAGER == "email" else SmsSender(settings.NUMBER_PHONE_MANAGER)

    def _check_data(self) -> None:
        if not self._connector.check_existence():
            self._connector.add((self._name_in_data, 0))

    def _update_obj_amount(self) -> None:
        if not self._amount:
            self._amount = self._connector.get_value(self._name_column_value)

    def _update_db_amount(self) -> None:
        self._connector.update_value(self._name_column_value, self._amount)
        



class StockMaterial(Informer):
    def __init__(self, name: str, amount: int = None) -> None:
        self._name_in_data = f"stock {name}"
        self._name_column_value = "material_value"
        self._connector = SqlMaterial(self._name_in_data)
        self._alert = settings.ALERT_MANAGER[name]
        super().__init__(name, amount)

    def _alert_manager(self):
        subject = f"{self._name} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {self._name} as soon as possible.\nGreetings and have a wonderful day"
        self._messenger.any_msg(subject, body)

    def get_material(self, remainder: int) -> int:
        to_fill = settings.FULL_CONTAINER_MACHINE[self._name] - remainder
        amount_get = max(0, min(to_fill, self._amount))
        self._amount -= amount_get
        self._update_db_amount()
        if self._amount < self._alert:
            self._alert_manager()
        return amount_get
    
    def add_material(self, amount: int) -> None:
        if amount != 0:
            self._amount += int(amount)
            self._update_db_amount()


class SystemData(Informer):
    def __init__(self, name: str, amount: int = None) -> None:
        self._name_in_data = name
        self._name_column_value = "variable_value"
        self._connector = SqlSystemData(self._name_in_data)
        super().__init__(name, amount)

    def get_value(self) -> int:
        return self._amount
    
    def change_value(self, amount_to_add: int) -> None:
        self._amount += int(amount_to_add)
        self._update_db_amount()