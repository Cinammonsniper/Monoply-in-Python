import BoardTileDataClasses
import pygame


class Player:
    def __init__(self, money: int, name: str) -> None:
        self.name = name
        self.money = money
        self.properties : list[BoardTileDataClasses.PropertyData, BoardTileDataClasses.RailRoadData, BoardTileDataClasses.UtilityData] = []
        self.in_jail = False
        self.orientation = 0
        self.get_out_of_jail_cards = 0
        self.pos = 0
        self.owned_property_view = None
        self.doubled_count = 0
        self.player_img: pygame.surface.Surface = None
        self.coordinates: pygame.rect.Rect = None

    def mortgage_assets(self):
        pass
    
    def decrease_balance(self, ammount: int) -> str:
        self.money -= ammount
        if self.money > 0:
            status = self.mortgage_assets()
        return status

    def passed_start(self):
        self.money += 200

    def increase_balance(self, ammount: int) -> None:
        self.money += ammount
    
