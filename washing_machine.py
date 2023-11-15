from stock import StockMaterial
from messenger import EmailSender, SmsSender
import settings
from order import Order
from log import Logger

import PySimpleGUI as sg
from typing import Type
import threading
import time
import mysql_database
from typing import Type


class WashingMachine:
    def __init__(self) -> None:
        self.__stock: dict[str, int] = {"powder": 0, "softener": 0}
        self.is_active: bool = False

    def get_amount_material(self, material: str) -> int:
        return self.__stock[material]
    
    def filling_material(self, material: str, amount: int) -> bool:
        self.__stock[material] += amount
        return self.__stock[material] >= settings.MIN_CONTAINER_MACHINE[material]

    def material_emptying(self, material: str) -> int:
        amount = self.__stock[material]
        self.__stock[material] = 0
        return amount

    def check_material_machine(self):
        result = True
        for material in self.__stock.keys():
            if self.__stock[material] < settings.MIN_CONTAINER_MACHINE[material] and not self.filling_material(material):
                result = False
        return result

    def washing(self, order: Type[Order]) -> None:
        self.material_reduction(order)
        time.sleep(max((order.calculate_time() * (60 * 60)) / 60 * settings.MINUTE_PER_HOUR, 10))
        self.is_active = False

    def material_reduction(self, order: Type[Order]):
        for material in self.__stock.keys():
            self.__stock[material] -= order.weight * settings.MATERIAL_PER_KILOGRAM[material]










