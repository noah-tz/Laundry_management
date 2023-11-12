from mysql_database import MysqlDatabase
from messenger import Messenger
from log import Logger
import settings


class StockManager:
    _email_manager = "laundrythecity034@gmail.com"
    @staticmethod
    def check_data_machine(number_room: int, number_machine: int, material: str) -> None:
        if not MysqlDatabase.check_equipment_execute(f"{material}, room {number_room} machine {number_machine}"):
            MysqlDatabase.add_type_equipment(f"{material}, room {number_room} machine {number_machine}", 0)
    
    @staticmethod
    def check_data_stock(material: str) -> None:
        if not MysqlDatabase.check_equipment_execute(f"stock {material}"):
            MysqlDatabase.add_type_equipment(f"stock {material}", 0)

    @Logger.log_record
    @staticmethod
    def adding_material(material: str, amount: int) -> None:
        StockManager.check_data_stock(material)
        MysqlDatabase.update_equipment_value(material, MysqlDatabase.get_equipment_value(material) + amount)

    @Logger.log_record
    @staticmethod
    def filling_machine(number_room: int, number_machine: int, material: str, max: int, remainder) -> int:
        material_stock = MysqlDatabase.get_equipment_value(f"stock {material}")
        machine_material_stock = MysqlDatabase.get_equipment_value(f"{material}, room {number_room} machine {number_machine}")
        print(type(material_stock))
        print(type(machine_material_stock))
        amount_filling = min(material_stock, max - remainder)
        MysqlDatabase.update_equipment_value(f"stock {material}", material_stock - amount_filling)
        MysqlDatabase.update_equipment_value(f"{material}, room {number_room} machine {number_machine}", machine_material_stock + amount_filling)
        if MysqlDatabase.get_equipment_value(f"{material}, room {number_room} machine {number_machine}") < max:
            StockManager.material_filling_alert(material)
        return amount_filling

    
    @staticmethod
    def material_filling_alert(material):
        subject = f"{material} in stock refill alert"
        body = f"Hello and greetings\nThe system recognized that it is necessary to fill in {material} as soon as possible.\nGreetings and have a wonderful day"
        Messenger.any_msg(StockManager._email_manager, subject, body)

