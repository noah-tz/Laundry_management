from inventory import InventoryManager
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
    __full_container = {"powder": 1000, "softener": 10000}
    __min_container = {"powder": 100, "softener": 1000}
    def __init__(self, number: int) -> None:
        self.number = number
        self.inventory = {"powder": 0, "softener": 0}
        self.is_active = False
        self.order: str
        self.check_data()

    # TODO to play on
    # def __del__(self) -> None:
    #     for material in self.inventory.keys():
    #         InventoryManager.adding_material(material, self.inventory[material])
    #         self.inventory[material] = 0

    def check_data(self):
        for material in self.inventory.keys():
            InventoryManager.check_data_machine(self.number, material)

    def check_material_machine(self):
        result = True
        for material in self.inventory.keys():
            if self.inventory[material] < WashingMachine.__min_container[material] and not self.filling_material(material):
                result = False
        return result

    def filling_material(self, material: str) -> bool:
        self.inventory[material] += InventoryManager.filling_machine(self.number, material, WashingMachine.__full_container[material], self.inventory[material])
        return self.inventory[material] >= WashingMachine.__min_container[material]

    def start(self, order: Type[Order]) -> bool:
        # TODO to play on
        # if not self.check_material_machine():
        #     return False
        self.is_active = True
        thread_washing = threading.Thread(target= self.washing, args= (order,))
        thread_washing.start()
        return True
    
    def washing(self, order: Type[Order]) -> None:
        time.sleep(max((order.calculate_time() * (60 * 60)) / 60 * settings.MINUTE_PER_HOUR, 10))
        print("washing is finished")
        self.order_ready(order)
        self.is_active = False

    @Logger.log_record
    def order_ready(self, order: Type[Order]):
        order.is_finished = True
        self.is_full = False
        self.order = {}
        del RoomWashing.orders[order.ID]
        Messenger.Your_order_is_ready(order.email_client, order.ID)


class RoomWashing:
    orders_pending = {}
    orders = {}
    def __init__(self, number: int) -> None:
        self.number = number
        self.__machines = {number: WashingMachine(number +1) for number in range(settings.MACHINE_PER_ROOM)}
        self.is_full = False

        
    @Logger.log_record
    def start_washing(self, order: Type[Order]):
        for machine in self.__machines.values():
            if not machine.is_active:
                if machine.number == settings.MACHINE_PER_ROOM:
                    self.is_full = True
                RoomWashing.orders[order.ID] = self.number
                if not machine.start(order):
                    RoomWashing.orders_pending[order] = self.number
                    sg.popup("Oh... we're really sorry, there are materials that we currently lack. Please wait until we come to restock our inventory.\nIt may take a little time.\nYou will be notified when your order is ready.")
                return


    def order_pickup(self, email: str, ID):
        Messenger.thank_you(email)

if __name__ == '__main__':
    mysql_database.MysqlDatabase.checks_database()
    a = Order("t0527184022@gmail.com", {"shirt": 0, "pants": 0, "tank top": 0, "underwear": 0, "socks": 0, "coat": 0, "hat": 0, "sweater": 0, "curtain": 1, "map": 0})
    b = RoomWashing(1)
    b.start_washing(a)
    a.order_summary()

    



