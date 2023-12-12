import settings
from order import Order

from typing import Type
import time


class WashingMachine:
    def __init__(self) -> None:
        """
        Initializes a WashingMachine object with an empty stock and inactive status.
        """
        self._stock: dict[str, int] = {"powder": 0, "softener": 0}
        self.is_active: bool = False

    def get_amount_material(self, material: str) -> int:
        """
        Retrieves the amount of a specific material in the machine's stock.
        Parameters:
        - material (str): The type of material to check.
        Returns:
        - int: The amount of the specified material in the stock.
        """
        return self._stock[material]
    
    def filling_material(self, material: str, amount: int) -> bool:
        """
        Fills a specified material into the machine's stock.
        Parameters:
        - material (str): The type of material to fill.
        - amount (int): The amount of the material to fill.
        Returns:
        - bool: True if the material has reached or exceeded the minimum container limit, False otherwise.
        """
        self._stock[material] += amount
        return self._stock[material] >= settings.MIN_CONTAINER_MACHINE[material]

    def material_emptying(self, material: str) -> int:
        """
        Empties a specified material from the machine's stock.
        Parameters:
        - material (str): The type of material to empty.
        Returns:
        - int: The amount of the material emptied from the stock.
        """
        amount = self._stock[material]
        self._stock[material] = 0
        return amount

    def check_material_machine(self) -> bool:
        """
        Checks if all materials in the machine's stock meet the minimum container requirements.
        Returns:
        - bool: True if all materials meet the minimum container requirements, False otherwise.
        """
        result = True
        for material in self._stock.keys():
            if self._stock[material] < settings.MIN_CONTAINER_MACHINE[material] and not self.filling_material(material, 0):
                result = False
        return result

    def washing(self, order: Type[Order]) -> None:
        """
        Performs the washing process for a given order.
        Parameters:
        - order (Type[Order]): The order to be washed.
        """
        self.material_reduction(order)
        time.sleep(max((order.calculate_time() * (60 * 60)) / 60 * settings.MINUTE_PER_HOUR, 10))
        self.is_active = False

    def material_reduction(self, order: Type[Order]) -> None:
        """
        Reduces the amount of materials in the machine's stock based on the given order.
        Parameters:
        - order (Type[Order]): The order for which materials are to be reduced.
        """
        for material in self._stock.keys():
            self._stock[material] -= order.get_weight() * settings.MATERIAL_PER_KILOGRAM[material]
