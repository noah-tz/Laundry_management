from mysql_database import MysqlDatabase
from messenger import Messenger
from log import Logger
import settings


class InventoryManager:
    _email_manager = "laundrythecity034@gmail.com"
    @staticmethod
    def check_data_machine(number_machine: int, material: str) -> None:
        if not MysqlDatabase.check_variable_execute(f"machine washing {material} {number_machine}"):
            MysqlDatabase.insert_variable(f"machine washing {material} {number_machine}", 0)
    
    @staticmethod
    def check_data_inventory(material: str) -> None:
        if not MysqlDatabase.check_variable_execute(f"inventory {material}"):
            MysqlDatabase.insert_variable(f"inventory {material}", 0)

    @Logger.log_record
    @staticmethod
    def adding_material(material: str, amount: int) -> None:
        InventoryManager.check_data_inventory(material)
        MysqlDatabase.update_equipment_value(material, MysqlDatabase.get_equipment_value(material) + amount)

    @Logger.log_record
    @staticmethod
    def filling_machine(number_machine: int, material: str, max: int, remainder) -> int:
        amount_filling = min(MysqlDatabase.get_variable(f"machine washing {material} {number_machine}"), max - remainder)
        MysqlDatabase.update_variable(f"machine washing {material} {number_machine}", MysqlDatabase.get_variable(f"machine washing {material} {number_machine}") - amount_filling)
        if MysqlDatabase.get_variable(f"machine washing {material} {number_machine}") < max:
            InventoryManager.material_filling_alert(material)
        return amount_filling

    
    @staticmethod
    def material_filling_alert(material):
        subject = f"{material} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {material} as soon as possible.\nGreetings and have a wonderful day"
        Messenger.any_msg(InventoryManager._email_manager, subject, body)

