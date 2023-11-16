import settings
from order import Order
from log import Logger

from typing import Type
import time
from typing import Type


class WashingMachine:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {"powder": 0, "softener": 0}
        self.is_active: bool = False

    def get_amount_material(self, material: str) -> int:
        return self._stock[material]
    
    def filling_material(self, material: str, amount: int) -> bool:
        self._stock[material] += amount
        return self._stock[material] >= settings.MIN_CONTAINER_MACHINE[material]

    def material_emptying(self, material: str) -> int:
        amount = self._stock[material]
        self._stock[material] = 0
        return amount

    def check_material_machine(self):
        result = True
        for material in self._stock.keys():
            if self._stock[material] < settings.MIN_CONTAINER_MACHINE[material] and not self.filling_material(material):
                result = False
        return result

    def washing(self, order: Type[Order]) -> None:
        self.material_reduction(order)
        time.sleep(max((order.calculate_time() * (60 * 60)) / 60 * settings.MINUTE_PER_HOUR, 10))
        self.is_active = False

    def material_reduction(self, order: Type[Order]):
        for material in self._stock.keys():
            self._stock[material] -= order.get_weight() * settings.MATERIAL_PER_KILOGRAM[material]










