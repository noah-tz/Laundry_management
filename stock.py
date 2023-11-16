from mysql_database import SqlMaterial
from messenger import EmailSender, SmsSender
from log import Logger
import settings

class StockMaterial:
    def __init__(self, name: str, amount: int = None) -> None:
        self._name = name
        self._alert = settings.ALERT_MANAGER[self._name]
        self._sql_material_connector = SqlMaterial(f"stock {self._name}")
        self._check_data_material()
        self._amount = amount
        self._update_obj_amount()
        self._messenger = EmailSender(settings.EMAIL_MANAGER) if settings.MSG_MANAGER == "email" else SmsSender(settings.NUMBER_PHONE_MANAGER)

    def _check_data_material(self) -> None:
        if not self._sql_material_connector.check_existence():
            self._sql_material_connector.add((f"stock {self._name}", 0))

    def _update_obj_amount(self) -> None:
        if not self._amount:
            self._amount = self._sql_material_connector.get_value("material_value")

    def _update_db_amount(self) -> None:
        self._sql_material_connector.update_value("material_value", self._amount)
    
    def _alert_manager(self):
        subject = f"{self._name} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {self._name} as soon as possible.\nGreetings and have a wonderful day"
        self._messenger.any_msg(subject, body)

    def get_material(self, remainder: int) -> int:
        to_fill = settings.FULL_CONTAINER_MACHINE[self._name] - remainder
        print(self._amount)
        amount_get = max(0, min(to_fill, self._amount))
        self._amount -= amount_get
        self._update_db_amount()
        if self._amount < self._alert:
            self._alert_manager()
        return amount_get
    
    def return_material(self, amount: int) -> None:
        self._amount += int(amount)
        self._update_db_amount()



if __name__ == '__main__':
    material = StockMaterial("powder")
