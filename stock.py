from mysql_database import SqlMaterial
from messenger import EmailSender, SmsSender
from log import Logger
import settings

class StockMaterial:
    def __init__(self, name: str, amount: int = None) -> None:
        self.__name = name
        self.__alert = settings.ALERT_MANAGER[self.__name]
        self.__sql_material_connector = SqlMaterial(f"stock {self.__name}")
        self.__check_data_material()
        self.__amount = amount
        self.__update_obj_amount()
        self.__set_messenger()

    def __check_data_material(self) -> None:
        if not self.__sql_material_connector.check_existence():
            self.__sql_material_connector.add((f"stock {self.__name}", 0))

    def __update_obj_amount(self) -> None:
        if not self.__amount:
            self.__amount = self.__sql_material_connector.get_value("material_value")


    def __set_messenger(self):
        if settings.MSG_MANAGER == "email":
            self.__messenger = EmailSender(settings.EMAIL_MANAGER)
        else:
            self.__messenger = SmsSender(settings.NUMBER_PHONE_MANAGER)

    def __update_db_amount(self) -> None:
        self.__sql_material_connector.update_value("material_value", self.__amount)
    
    def __alert_manager(self):
        subject = f"{self.__name} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {self.__name} as soon as possible.\nGreetings and have a wonderful day"
        self.__messenger.any_msg(subject, body)

    def get_material(self, remainder: int) -> int:
        to_fill = settings.FULL_CONTAINER_MACHINE[self.__name] - remainder
        print(self.__amount)
        amount_get = max(0, min(to_fill, self.__amount))
        self.__amount -= amount_get
        self.__update_db_amount()
        if self.__amount < self.__alert:
            self.__alert_manager()
        return amount_get
    
    def return_material(self, amount: int) -> None:
        self.__amount += int(amount)
        self.__update_db_amount()



if __name__ == '__main__':
    material = StockMaterial("powder")
