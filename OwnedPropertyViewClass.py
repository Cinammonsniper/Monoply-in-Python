import pygame
from PlayerScript import Player

class OwnedPropertyView:
    def __init__(self, player: Player, screen: pygame.surface.Surface) -> None:
        self.player : Player = player
        self.__screen = screen
        self.__initialize()

    def __initialize(self):
        self.positions = {(6,8,9)     :[1420, 420],
                          (11,13,14)  :[1655, 420],
                          (16,18,19)  :[1420, 513],
                          (21,23,24)  :[1655, 513],
                          (26,27,29)  :[1420, 606],
                          (31,32,34)  :[1655, 606],
                          (37,39)     :[1420, 699],
                          (1,3)       :[1655, 699], 
                          (5,15,25,35):[1420, 832], 
                          (12, 28)    :[1655, 832]}
        self.__cards = []
        self.__set_width = 225
    
    def refresh_property_view(self):
        self.__cards = []
        properties_list = [property.pos for property in self.player.properties]
        for property_no in properties_list:
            set_ = next((s for s in self.positions.keys() if property_no in s), None)
            if set_ is None:
                continue
            set_size = len(set_)
            card_width = round((self.__set_width - 5*(set_size)) / set_size)
            card_height = round(card_width * 1.142)
            x, y = self.positions[set_]
            for no in set_:
                if no == property_no:
                    card_image = pygame.transform.smoothscale(pygame.image.load(f"assets\\property cards\\{no}.png"), (card_width, card_height))
                    card_rect = card_image.get_rect()
                    card_rect.x, card_rect.y = x, y
                    self.__cards.append((card_image, card_rect))
                x+= card_width + 5
    
    def draw(self):
        for image_set in self.__cards:
            image, rect = image_set
            self.__screen.blit(image, rect)


