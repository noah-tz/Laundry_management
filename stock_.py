from mysql_database import MysqlDatabase
from messenger import Messenger
from log import Logger
import settings


class StockManager:
    _email_manager = "laundrythecity034@gmail.com"

    
    @staticmethod
    def check_data_stock(material: str) -> None:
        if not MysqlDatabase.check_equipment_execute(f"stock {material}"):
            MysqlDatabase.add_type_equipment(f"stock {material}", 0)

    @Logger.log_record
    @staticmethod
    def adding_material(material: str, to_fill: int) -> None:
        current_value = MysqlDatabase.get_equipment_value(f"stock {material}")
        to_update = float(current_value) + to_fill
        MysqlDatabase.update_equipment_value(f"stock {material}", to_update)

    @Logger.log_record
    @staticmethod
    def filling_machine(material: str, max: int, remainder) -> int:
        material_stock = MysqlDatabase.get_equipment_value(f"stock {material}")
        amount_filling = min(material_stock, max - remainder)
        MysqlDatabase.update_equipment_value(f"stock {material}", material_stock - amount_filling)
        return amount_filling

    
    @staticmethod
    def material_filling_alert(material):
        subject = f"{material} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {material} as soon as possible.\nGreetings and have a wonderful day"
        Messenger.any_msg(StockManager._email_manager, subject, body)

