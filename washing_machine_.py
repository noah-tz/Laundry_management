from stock import StockManager
from messenger import Messenger
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
    __min_container = settings.MIN_CONTAINER
    __full_container = settings.FULL_CONTAINER
    def __init__(self, number_machine: int, number_room) -> None:
        self.number_machine = number_machine
        self.number_room = number_room
        self.stock = {"powder": 0, "softener": 0}
        self.is_active = False
        self.order: str


    def check_material_machine(self):
        result = True
        for material in self.stock.keys():
            if self.stock[material] < WashingMachine.__min_container[material] and not self.filling_material(material):
                result = False
        return result

    def filling_material(self, material: str) -> bool:
        self.stock[material] += StockManager.filling_machine(material, WashingMachine.__full_container[material], self.stock[material])
        if self.stock[material] < WashingMachine.__full_container[material]:
            StockManager.material_filling_alert(material)
        return self.stock[material] >= WashingMachine.__min_container[material]

    def start(self, order: Type[Order]) -> bool:
        if not self.check_material_machine():
            return False
        self.is_active = True
        thread_washing = threading.Thread(target= self.washing, args= (order,))
        thread_washing.start()
        return True
    
    def washing(self, order: Type[Order]) -> None:
        self.material_reduction(order)
        time.sleep(max((order.calculate_time() * (60 * 60)) / 60 * settings.MINUTE_PER_HOUR, 10))
        print("washing is finished")
        self.order_ready(order)
        self.is_active = False

    def material_reduction(self, order: Type[Order]):
        for material in self.stock.keys():
            self.stock[material] -= order.weight * settings.MATERIAL_PER_KILOGRAM[material]


    @Logger.log_record
    def order_ready(self, order: Type[Order]):
        order.is_finished = True
        self.is_full = False
        self.order = {}
        del WashingRoom.orders[order.ID]
        Messenger.Your_order_is_ready(order.email_client, order.ID)

    def close_machine(self):
        for material in self.stock.keys():
            StockManager.adding_material(material, self.stock[material])
            self.stock[material] = 0


class WashingRoom:
    orders_pending = {}
    orders = {}
    def __init__(self, number_room: int) -> None:
        self.number_room = number_room
        self.__machines = {number_machine: WashingMachine(number_machine +1, self.number_room) for number_machine in range(settings.MACHINE_PER_ROOM)}
        self.is_full = False

        
    @Logger.log_record
    def start_washing(self, order: Type[Order]):
        for machine in self.__machines.values():
            if not machine.is_active:
                if machine.number_machine == settings.MACHINE_PER_ROOM:
                    self.is_full = True
                WashingRoom.orders[order.ID] = self.number_room
                if not machine.start(order):
                    WashingRoom.orders_pending[order] = self.number_room
                    sg.popup("Oh... we're really sorry, there are materials that we currently lack. Please wait until we come to restock our inventory.\nIt may take a little time.\nYou will be notified when your order is ready.")
                return

    def order_pickup(self, email: str, ID):
        Messenger.thank_you(email)

    def close_room(self):
        for _, machine in self.__machines.items():
            machine.close_machine()

if __name__ == '__main__':
    mysql_database.MysqlDatabase.checks_database()

    mysql_database.MysqlDatabase.update_equipment_value("stock powder", 5000)
    mysql_database.MysqlDatabase.update_equipment_value("stock softener", 5000)
    a = Order("t0527184022@gmail.com", {"shirt": 1, "pants": 0, "tank top": 0, "underwear": 0, "socks": 0, "coat": 0, "hat": 0, "sweater": 0, "curtain": 0, "map": 0})
    b = WashingRoom(1)
    b.start_washing(a)
    a.order_summary()
    b.close_room()








