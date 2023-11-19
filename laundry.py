from order import Order
from information import StockMaterial
from washing_machine import WashingMachine
import settings
from gui import LaundryGui

from typing import Type
import threading


class LaundryRoom:
    def __init__(self) -> None:
        self._machines: dict[int, WashingMachine] = {number_machine: WashingMachine() for number_machine in range(1, settings.NUMBER_OF_MACHINES +1)}
        self._stock: dict[str, StockMaterial] = {name_material: StockMaterial(name_material) for name_material in settings.NAMES_MATERIAL}
        self._full = False
        self._orders_pending: list[Order] = []

    def enter_order(self, order: Type[Order], notes: bool = True) -> None:
        if self._full:
            self._orders_pending.append(order)
            if notes:
                LaundryGui.popup_window("All laundry rooms are occupied. Please try again later.")
            return False
        else:
            self._find_machine(order, notes)

    def _find_machine(self, order: Order, notes: bool) -> None:
        for number, machine in self._machines.items():
            if not machine.is_active:
                if self._check_material_machine(number):
                    self._set_thread(number, order)
                    return True
                else:
                    self._orders_pending.append(order)
                    if notes:
                        LaundryGui.popup_window("We're sorry, some of the maintenance materials are missing.\nYour order is pending and we will notify you immediately when it is ready")
                return False
        self._full = True
        return self.enter_order(order)

    def _check_material_machine(self, number_machine: int) -> bool:
        result = True
        for material in settings.NAMES_MATERIAL:
            amount_material_of_machine = self._machines[number_machine].get_amount_material(material)
            if amount_material_of_machine < settings.MIN_CONTAINER_MACHINE[material] and not self._machines[number_machine].filling_material(material, self._stock[material].get_material(amount_material_of_machine)):
                result = False
        return result

    def _empty_machine_material(self, number_machine: int) -> None:
        for material in settings.NAMES_MATERIAL:
            self._stock[material].add_material(self._machines[number_machine].material_emptying(material))

    def _set_thread(self, number_machine: int, order: Type[Order]):
        thread_washing = threading.Thread(target= self._start_washing, args= (number_machine, order))
        thread_washing.start()
        order.order_summary()


    def _start_washing(self, number_machine: int, order: Type[Order]) -> None:
        self._machines[number_machine].washing(order)
        self._finish_washing(order)

    def _finish_washing(self, order: Type[Order]):
        print("washing is finished")
        self._full = False
        order.order_ready()

    def initialize_pending_orders(self) -> bool:
        while self._orders_pending:
            if self.enter_order(self._orders_pending[0], False):
                self._orders_pending.pop(0)
            else:
                return False
        return True
    
    def close_room(self):
        for number_machine, _ in self._machines.items():
            self._empty_machine_material(number_machine)

if __name__ == '__main__':
    order = Order("t0527184022@gmail.com", "0522645540", "email", {'-shirt-': 0, '-pants-': 6, '-tank top-': 0, '-underwear-': 0, '-socks-': 0, '-coat-': 0, '-hat-': 0, '-sweater-': 0, '-curtain-': 0, '-tablecloth-': 0, '-order number-': '', '-TABLE-': [], 0: '-TAB_CREATE_ORDER-'})
    laundry_room = LaundryRoom()
    laundry_room.enter_order(order)
    laundry_room.close_room()