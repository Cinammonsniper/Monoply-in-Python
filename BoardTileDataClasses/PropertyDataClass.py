from dataclasses import dataclass
from enum import Enum




class Colour(Enum):
    BROWN = 1
    LIGHTBLUE = 2
    PINK = 3
    ORANGE = 4
    RED = 5
    YELLOW = 6
    GREEN = 7
    PURPLE = 8


@dataclass
class PropertyData:
    name: str
    price: str
    rents: list[int]
    build_cost: int
    mortgage_value: int
    in_set : int
    houses = 0 
    colour: Colour
    pos:int