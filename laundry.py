from order import Order
from information import StockMaterial
from washing_machine import WashingMachine
import settings
from gui import LaundryGui
from log import Logger

from typing import Type
import threading


class LaundryRoom:
    def __init__(self) -> None:
        """
        Initialize the LaundryRoom with washing machines, stock of materials, and order-related attributes.
        """
        self._machines: dict[int, WashingMachine] = {number_machine: WashingMachine()
                                                     for number_machine in range(1, settings.NUMBER_OF_MACHINES + 1)}
        self._stock: dict[str, StockMaterial] = {name_material: StockMaterial(name_material)
                                                 for name_material in settings.NAMES_MATERIAL}
        self._full = False
        self._orders_pending: list[Order] = []

    @Logger.log_record
    def enter_order(self, order: Type[Order], notes: bool = True) -> None:
        """
        Attempt to enter a new order into the laundry room.
        Parameters:
        - order (Type[Order]): The order to be processed.
        - notes (bool): Flag indicating whether to display notes to the user.
        Returns:
        - None
        """
        if self._full:
            self._orders_pending.append(order)
            if notes:
                LaundryGui.popup_window("All laundry rooms are occupied. We will enter your order later.")
            return False
        else:
            self._find_machine(order, notes)
        return True
            
    def _find_machine(self, order: Order, notes: bool) -> None:
        """
        Find an available washing machine for the given order.
        Parameters:
        - order (Order): The order to be processed.
        - notes (bool): Flag indicating whether to display notes to the user.
        Returns:
        - None
        """
        for number, machine in self._machines.items():
            if not machine.is_active:
                if self._check_material_machine(number):
                    self._set_thread(number, order)
                    return True
                else:
                    self._orders_pending.append(order)
                    if notes:
                        LaundryGui.popup_window(
                            "We're sorry, some of the maintenance materials are missing.\nYour order is pending and we will notify you immediately when it is ready")
                return False
        self._full = True
        return self.enter_order(order)

    def _check_material_machine(self, number_machine: int) -> bool:
        """
        Check if the washing machine has sufficient materials for processing the order.

        Parameters:
        - number_machine (int): The number of the washing machine to be checked.

        Returns:
        - bool: True if the machine has sufficient materials, False otherwise.
        """
        result = True
        for material in settings.NAMES_MATERIAL:
            amount_material_of_machine = self._machines[number_machine].get_amount_material(material)
            if (amount_material_of_machine < settings.MIN_CONTAINER_MACHINE[material]
                    and not self._machines[number_machine].filling_material(material,
                                                                            self._stock[material].get_material(
                                                                                amount_material_of_machine))
            ):
                result = False
        return result

    def _empty_machine_material(self, number_machine: int) -> None:
        """
        Empty the materials from the washing machine back into the stock.
        Parameters:
        - number_machine (int): The number of the washing machine to be emptied.
        Returns:
        - None
        """
        for material in settings.NAMES_MATERIAL:
            self._stock[material].add_material(self._machines[number_machine].material_emptying(material))

    def _set_thread(self, number_machine: int, order: Type[Order]):
        """
        Start a new thread for washing and process the order.
        Parameters:
        - number_machine (int): The number of the washing machine.
        - order (Type[Order]): The order to be processed.
        Returns:
        - None
        """
        thread_washing = threading.Thread(target=self._start_washing, args=(number_machine, order))
        thread_washing.start()
        order.order_summary()

    def _start_washing(self, number_machine: int, order: Type[Order]) -> None:
        """
        Start the washing process for the given order.
        Parameters:
        - number_machine (int): The number of the washing machine.
        - order (Type[Order]): The order to be processed.
        Returns:
        - None
        """
        self._machines[number_machine].washing(order)
        self._finish_washing(order)

    def _finish_washing(self, order: Type[Order]):
        """
        Finish the washing process and mark the laundry room as not full.
        Parameters:
        - order (Type[Order]): The order that has been processed.
        Returns:
        - None
        """
        print("Washing is finished")
        self._full = False
        order.order_ready()
        self.initialize_pending_orders()

    @Logger.log_record
    def initialize_pending_orders(self) -> bool:
        """
        Initialize pending orders when the laundry room is not full.
        Returns:
        - bool: True if all pending orders are successfully processed, False otherwise.
        """
        while self._orders_pending:
            if self.enter_order(self._orders_pending[0], False):
                self._orders_pending.pop(0)
            else:
                return False
        return True

    @Logger.log_record
    def close_room(self):
        """
        Close the laundry room and empty materials from all washing machines.
        Returns:
        - None
        """
        for number_machine, _ in self._machines.items():
            self._empty_machine_material(number_machine)

