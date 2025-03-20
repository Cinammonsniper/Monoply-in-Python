
import pygame
from GameClass import Game
from TileScripts import Property, RailRoad, Utility, Chance, CommunityChest, Go, GoToJail, FreeParking, LuxuryTax, IncomeTax, Jail
from PlayerScript import Player
from GameGUIScripts import DrawProperty, Frame, TextBox
from OwnedPropertyViewClass import OwnedPropertyView
import random

pygame.init()


BPC = {0: [(867, 868), (1000, 1000)], 1:[(782, 868), (869, 1000)], 2: [(706, 868), (779, 1000)], 3: [(626, 868), (703, 1000)], 4:[(545,868), (622,1000)], 
        5:[(464, 868), (541, 1000)], 6:[(382, 868), (460, 1000)], 7:[(301, 868), (377, 1000)], 8:[(220, 868), (297, 1000)], 9: [(138, 868), (215, 1000)], 
        10:[(0, 868), (133, 1000)], 11:[(0, 787), (133, 864)], 12:[(0, 709), (133, 783)], 13:[(0, 626), (133, 704)], 14:[(0, 545), (133, 622)], 15:[(0, 464), (133, 540)],
        16:[(0, 381), (133, 459)], 17:[(0, 300),(133, 376)], 18:[(0, 219), (133, 295)], 19:[(0, 137), (133, 213)], 20:[(0, 0), (133, 130)], 
        21:[(138,0), (215,131)], 22:[(220,0), (297,131)], 23:[(299, 0), (377, 131)], 24:[(381, 0), (459, 131)], 25:[(462, 0), (540, 131)], 26: [(544,0), (621,131)],  
        27: [(626, 0), (703, 131)], 28: [(707, 0), (784, 131)], 29: [(788, 0), (862, 131)], 30: [(867, 0),(1000, 131)], 31:[(867, 136), (1000, 215)]  , 32: [(867, 219), (1000, 296)], 
        33: [(867, 300),(1000, 378)], 34: [(867, 381), (1000, 459)], 35:[(867, 464), (1000, 540)], 36: [(867, 545), (1000, 622)], 37: [(867, 626), (1000, 704)], 
        38: [(867, 708), (1000, 783)], 39: [(867, 787), (1000, 864)]}
PLAYER_ICONS = ["airplane", "car", "engine", "boat"]
ROTATION = {range(0, 11): 0,
            range(11, 20): 90,
            range(20, 31): 180,
            range(31, 40): 270}


def generate_hop_list(initial: int, final: int) -> dict[tuple[int, int]: int]:

    hop_list = {}

    def calculate_position(pos: int, movement: int) -> int:
        new_pos = pos + movement
        if new_pos <= 39:
            return new_pos
        else:
            return(new_pos - 40)

    def mid_point(edges: list[tuple[int, int]]):
        mpx = round(abs((edges[1][0] - edges[0][0])/2))
        mpy = round(abs((edges[0][1] - edges[1][1])/2))

        return (edges[0][0] + mpx, edges[0][1] + mpy)

    position = initial

    while position != final:
        position =  calculate_position(position, 1)
        edges = BPC[position]
        coordinates = mid_point(edges)
        cords = (coordinates[0] - 30, coordinates[1] - 30)
        if 1 <= position <= 10:
            hop_list[cords] = 0
        elif 11 <= position <= 20:
            hop_list[cords] = 270
        elif 21 <= position <= 30:
            hop_list[cords] = 180
        elif 31 <= position <= 39 or position == 0:
            hop_list[cords] = 90

    return hop_list


def calculate_size(edges: dict[tuple[int, int], int]) -> tuple[int, int]:

    x1, y1 = edges[0]
    x2, y2 = edges[1]
    return (x2 - x1, y2 - y1)



class Button:
    def __init__(self, text: str, width: int, height: int, coordinates:tuple[int, int], font:pygame.font.Font, screen:pygame.display, active: bool, command) -> None:
        self.text = text
        self.width = width
        self.height = height
        self.coordinates = coordinates
        self.font = font
        self.screen = screen
        self.active = active
        self.command = command
        self.initialize()
        self.set_state(self.active)

    def initialize(self) -> None:
        self.coordinates
        
        self.clickable = True
        self.colour = "#005F80"
        self.hover_colour = "#FF7043"
        self.bottom_colour = "#004059"
        self.text_colour = "#A6A6A6"
        self.draw_colour = self.colour
        self.allevation = 6
        self.dynamic_allevation = self.allevation
        self.orignal_y = self.coordinates[1]

        self.button_rect = pygame.Rect(self.coordinates, (self.width, self.height))

        self.button_bottom_rect = pygame.Rect(self.coordinates, (self.width, self.allevation))

        self.text_surface = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)
        self.pressed = False

    def set_state(self, state:bool):
        self.active = state
        if state is True:
            self.text_colour = "#FFFFFF"
        else:
            self.text_colour = "#A6A6A6"
        self.text_surface = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)



    def draw(self) -> None:
        
        self.button_rect.y = self.orignal_y - self.dynamic_allevation
        self.text_rect.center = self.button_rect.center

        self.button_bottom_rect.midtop = self.button_rect.midtop
        self.button_bottom_rect.height = self.button_rect.height + self.dynamic_allevation

        
        pygame.draw.rect(surface=self.screen, color=self.bottom_colour, rect=self.button_bottom_rect, border_radius=12)
        pygame.draw.rect(surface=self.screen, color=self.draw_colour, rect=self.button_rect, border_radius=12)
        self.screen.blit(self.text_surface, self.text_rect)

    def check_clicked(self, mouse_pos: int, pressed: bool):
        if self.button_rect.collidepoint(mouse_pos):
            if self.active:
                self.draw_colour = self.hover_colour
            if pressed:
                self.pressed = True
                self.dynamic_allevation = 0
            else:
                if self.pressed:
                    self.pressed = False
                    self.dynamic_allevation = self.allevation
                    if self.active:
                        return self.command
        else:
            self.dynamic_allevation = self.allevation
            self.draw_colour = self.colour
        return None

class DrawOnTile:
    def __init__(self, index: int, screen: pygame.surface.Surface, corresponding_tile, cage_img: pygame.surface.Surface) -> None:
        self.index = index
        self.screen = screen
        self.tile = corresponding_tile
        self.cage_img = cage_img
        self.initialize()
    
    def initialize(self):
        edges = BPC[self.index]
        self.players_on_tile = [] 
        self.property_level = 0 if type(self.tile) == Property else -1
        self.__rotation = ROTATION[next(r for r in ROTATION if self.index in r)]
        self.__house_obj = DrawProperty(self.screen, edges, self.__rotation)
        self.__tile_rect = pygame.Rect(edges[0], calculate_size(edges))
        self.__hover_surface = pygame.Surface(self.__tile_rect.size, pygame.SRCALPHA)
        self.__hover_surface.fill((211, 211, 211,70))
        self.__scaling_dictionary = {1:1, 2:1.75, 3:1.75, 4:2}
        self.__selection_surface = pygame.Surface(self.__tile_rect.size, pygame.SRCALPHA)
        self.__selection_surface.fill((26, 26, 26, 90))
        self.__mortgage_surface = pygame.Surface(self.__tile_rect.size, pygame.SRCALPHA)
        self.__mortgage_surface.fill((255, 69, 58, 90))
        self.pressed = False
        self.selected = False
        self.inactive = False


    def update_data(self):
        #check if the property level has been changed and if so update the property level
        if self.property_level != -1:
            if self.tile.property_level_ != self.property_level:
                self.property_level = self.tile.property_level_
                self.__house_obj.update_house_list(self.property_level)

        #check if the players on the tile have moved if so remove them from the players list and return a list of the moved players
        moved_players = []
        if self.players_on_tile != []:
            for i in range(len(self.players_on_tile)):
                if self.players_on_tile[i].pos != self.index:
                    moved_players.append(self.players_on_tile[i])
                    self.players_on_tile[i] = None
        self.players_on_tile = [player for player in self.players_on_tile if player is not None]
        return moved_players
    
    def is_ownable(self):
        return self.tile.is_ownable
    
    def return_owner(self):
        return self.tile.owner

    def is_mortgaged(self):
        if self.is_ownable():
            return self.tile.is_mortgaged
        else:
            return False 
    def is_deconstructable(self):
        return self.tile.is_deconstructable

    def draw(self) -> None:

        if self.inactive:
            self.screen.blit(self.__selection_surface, self.__tile_rect.topleft)
        elif self.is_ownable():
            if self.tile.is_mortgaged:
                self.screen.blit(self.__mortgage_surface, self.__tile_rect.topleft)
        
        if self.property_level > 0:
            self.__house_obj.draw()

        #draws the player on the tile 
        if self.players_on_tile:
            ox, oy = self.players_on_tile[0].coordinates.topleft
            x, y = ox, oy 
            scaling = 60 / self.__scaling_dictionary[len(self.players_on_tile)]
            line_break = 1
            for player in self.players_on_tile:
                img =  pygame.transform.rotate(pygame.transform.scale(player.player_img, (scaling, scaling)), player.orientation)
                if player.in_jail and self.tile.pos == 10:
                    img_rect = img.get_rect(x=x+20, y=y-20)
                    self.screen.blit(img, img_rect)
                    cage_rect = self.cage_img.get_rect(center=img_rect.center)
                    self.screen.blit(self.cage_img, cage_rect)
                else:
                    img_rect = img.get_rect(x=x, y=y)
                    self.screen.blit(img, img_rect)
                x += scaling
                line_break *= -1
                if line_break == 1:
                    y += scaling
                    x = ox
        
        

    def check_clicked(self, mouse_pos: tuple[int, int], pressed:bool) -> int:
        if self.__tile_rect.collidepoint(mouse_pos) and not self.inactive:
            #overlay a transulcent gray surface for the hover effect
            self.screen.blit(self.__hover_surface, self.__tile_rect.topleft)
            if pressed:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
                    return self.index
        
        return -1


        


            
        
        

class RenderEngine():    
    def __init__(self, game: Game) -> None:
        
        self.player_list = game.players_list
        self.game = game
        self.render_tiles_list : dict[int, DrawOnTile] = {}
        self.current_property_card_display: tuple
        self.current_player: Player
        self.ui_elements = []
        self.info_box_elements = []
        self.dice_faces = {}
        self.current_temp = []
        self.running = True
        self.initialize()

    def initialize(self) -> None:
        self.screen = pygame.display.set_mode((1900,1000))
        self.font = pygame.font.Font("assets\\fonts\\game_font_roboto_m.ttf", 32)
        self.clock = pygame.time.Clock()

        self.board_img = pygame.image.load("assets\\image assets\\monopoly_board.png")
        self.cage_image = pygame.transform.smoothscale(pygame.image.load("assets\\image assets\\cage.png"), (70,70))

        self.command_dictionary = {"buy": self._buy, 
                                   "end_turn" : self._nothing,
                                   "chance" : self._chance,
                                   "community_chest": self._community_chest,
                                   "jail_option" : self._in_jail,
                                   "move_jail" : self._move_jail}
        
        self.selection_state = False
        self.selection_func = None
        self.display_pay_fine_button = False


        for tile in self.game.board:
                tile_obj = DrawOnTile(tile.pos, self.screen, tile, self.cage_image)
                self.render_tiles_list[tile.pos] = tile_obj
                
        for i in range(1, 7):
            image = pygame.transform.smoothscale(pygame.image.load(f"assets\\dice faces\\dice_{i}.png"), (100, 100))
            self.dice_faces[i] = image

        player_icons = PLAYER_ICONS.copy()

        for player in self.player_list:
            player.player_img = pygame.transform.smoothscale(pygame.image.load(f"assets\\player icons\\{player_icons[0]}.png"), (60, 60))
            player_icons.pop(0)
            player_property_view = OwnedPropertyView(player, self.screen)
            player.owned_property_view = player_property_view
            position = player.player_img.get_rect()
            position[0] = 904
            position[1] = 907
            player.coordinates = position
            self.render_tiles_list[0].players_on_tile.append(player)

        self.current_player = self.player_list[0]

        self.create_ui_elements()
        self.update_property_card_display(1)
        self.update_information_box()





    def _buy(self):
        self.buy_button.set_state(True)

    def _nothing(self):
        self.update_information_box()

    def _chance(self):
        self.render_all()
        self.update()
        pygame.time.delay(100)
        chance = self.game._return_current_chance()
        chance_card_frame = Frame(600, 300, (200, 350), self.screen, "#FFFFFF")
        text_box = TextBox(chance, 550, 250, (225, 375), self.screen, self.font, "center", "#FFFFFF", "#000000")
        self.current_temp = [(False, chance_card_frame), (False, text_box)]
        command_key = self.game.chance_actions(chance)
        self.command_dictionary[command_key]()

    def _community_chest(self):
        self.render_all()
        self.update()
        pygame.time.delay(100)
        community_chest = self.game._return_current_community_chest()
        chance_card_frame = Frame(600, 300, (200, 350), self.screen, "#FFFFFF")
        text_box = TextBox(community_chest, 550, 250, (225, 375), self.screen, self.font, "center", "#FFFFFF", "#000000")
        self.current_temp = [(False, chance_card_frame), (False, text_box)]
        command_key = self.game.chance_actions(community_chest)
        self.command_dictionary[command_key]()

    def _in_jail(self):
        self.display_pay_fine_button = True

    def _move_jail(self):
        self.render_all()
        self.update()
        self.game._move_to_jail()
        self.end_turn_button_clicked_()

    def end_turn_button_clicked_(self):
        self.display_pay_fine_button = False
        self.current_player = self.game.end_turn()
        self.end_turn_button.set_state(False)
        self.roll_dice_button.set_state(True)
        self.buy_button.set_state(False)
        self.mortgagae_button.set_state(False)
        self.build_property_button.set_state(False)
        self.update_information_box()
        if self.selection_state:
            for tile in self.render_tiles_list.values():
                tile.inactive = False
        
    def buy_button_clicked_(self):
        self.game._tile_bought()
        self.buy_button.set_state(False)
        self.current_player.owned_property_view.refresh_property_view()
        self.update_information_box()

    def mortgage_button_clicked_(self):
        self.selection_state = True
        self.selection_func = self.game._mortgage_property
        for tile in self.render_tiles_list.values():
            if tile.is_ownable():
                if tile.return_owner() != self.current_player:
                    tile.inactive = True
                elif tile.property_level > 0 and not tile.is_deconstructable():
                        tile.inactive = True
                else:
                    continue
            else:
                tile.inactive = True

    def build_button_clicked_(self):
        if not self.selection_state:
            self.selection_state = True
            self.selection_func = self.game._build_on_tile
            tiles = [tile for tile in self.game.board if tile.is_ownable]
            player_tiles = [tile for tile in tiles if tile.owner == self.current_player]
            player_tiles_buildable = [tile for tile in player_tiles if tile.is_buildable]
            
            for tile in self.game.board:
                if tile not in player_tiles_buildable:
                    self.render_tiles_list[tile.pos].inactive = True
        else:
            for tile in self.render_tiles_list.values():
                tile.inactive = False
            self.selection_state = False
    
    def unmortgage_button_clicked_(self):
        if not self.selection_state:
            self.selection_state = True
            self.selection_func = self.game._unmortgage_property
            tiles = [tile for tile in self.game.board if tile.is_ownable]
            player_tiles = [tile for tile in tiles if tile.owner == self.current_player]
            player_tiles_buildable = [tile for tile in player_tiles if tile.is_mortgaged]
            for tile in self.game.board:
                if tile not in player_tiles_buildable:
                    self.render_tiles_list[tile.pos].inactive = True
        else:
            for tile in self.render_tiles_list.values():
                tile.inactive = False
            self.selection_state = False

    def pay_fine_button_clicked(self):
        self.game._fine_payed()
        self.display_pay_fine_button = False






    def update_property_card_display(self, card_no: int) -> None:
        self.property_card_frame = Frame(380, 430, (1010, 560), self.screen, colour="#FFFFFF")
        property_card = pygame.transform.smoothscale(pygame.image.load(f"assets\\property cards\\{card_no}.png"), (360, 405))
        property_card_rect = property_card.get_rect()
        property_card_rect.center = self.property_card_frame.frame_rect.center
        self.current_property_card_display = (property_card, property_card_rect)

    def create_ui_elements(self):
        
        buttons_frame = Frame(380, 530, (1010, 10), self.screen)
        text_fields_frame = Frame(480, 390, (1410, 10), self.screen)
        property_view_frame = Frame(480, 580, (1410, 410), self.screen)

        self.roll_dice_button = Button("Roll Dice" , 350, 75, (1025, 50) , self.font, self.screen, True , self.dice_rolled)
        self.buy_button = Button("Buy"             , 170, 75, (1025, 200), self.font, self.screen, False, self.buy_button_clicked_)
        self.mortgagae_button = Button("Mortgage"  , 170, 75, (1205, 200), self.font, self.screen, False, self.mortgage_button_clicked_)
        self.unmortgage_button = Button("Buy Back"         , 170, 75, (1025, 300), self.font, self.screen, False, self.unmortgage_button_clicked_)
        self.build_property_button = Button("Build", 170, 75, (1205, 300), self.font, self.screen, False, self.build_button_clicked_)
        self.end_turn_button = Button("End Turn"           , 170, 75, (1025, 400), self.font, self.screen, False, self.end_turn_button_clicked_)
        self.trade_button = Button("Trade"     , 170, 75, (1205, 400), self.font, self.screen, False, None)
        self.pay_fine_button = Button("Pay Fine"     , 170, 75, (415, 200), self.font, self.screen, True, self.pay_fine_button_clicked)

        money_label = TextBox("Money:", 150, 50, (1435, 135), self.screen, self.font, alighn="left")
        goj_label = TextBox("G.O.J cards: ", 200, 50, (1435, 235), self.screen, self.font, alighn="left")
        
        self.ui_elements.append(property_view_frame)
        self.ui_elements.append(text_fields_frame)
        self.ui_elements.append(buttons_frame)
        self.ui_elements.append(self.roll_dice_button)
        self.ui_elements.append(self.buy_button)
        self.ui_elements.append(self.mortgagae_button)

        self.ui_elements.append(self.unmortgage_button)
        self.ui_elements.append(self.build_property_button)
        self.ui_elements.append(money_label)
        self.ui_elements.append(goj_label)
        self.ui_elements.append(self.end_turn_button)
        self.ui_elements.append(self.trade_button)

    def update_information_box(self):
        self.info_box_elements = []
        player_name = TextBox(self.current_player.name, 430, 50,(1435, 35), self.screen, self.font, alighn="center")
        money_text_box = TextBox(str(self.current_player.money), 150, 50, (1645, 135), self.screen, self.font, alighn="left")
        goj_text_box = TextBox(str(self.current_player.get_out_of_jail_cards), 150, 50, (1645, 235), self.screen, self.font, alighn="left")
        self.info_box_elements.append(player_name)
        self.info_box_elements.append(money_text_box)
        self.info_box_elements.append(goj_text_box)

    def move_player(self, initial: int, player: Player) -> None:
        final = player.pos
        hop_list = generate_hop_list(initial, final)
        orientation = 0
        for coordinates in hop_list.keys():
            
            orientation = hop_list[coordinates]
            player_img = pygame.transform.rotate(player.player_img, orientation)
            self.screen.blit(player_img, player.coordinates)
            final_coords = coordinates
            
            if orientation == 0:
                while player.coordinates[0] > final_coords[0]:
                    self.screen.blit(self.board_img, player.coordinates, player.coordinates)
                    player.coordinates = player.coordinates.move(-5, 0)
                    self.screen.blit(player_img, player.coordinates)
                    pygame.display.update()
                    self.clock.tick(60)
            elif orientation == 270:
                while player.coordinates[1] > final_coords[1]:
                    self.screen.blit(self.board_img, player.coordinates, player.coordinates)
                    player.coordinates = player.coordinates.move(0, -5)
                    self.screen.blit(player_img, player.coordinates)
                    pygame.display.update()
                    self.clock.tick(60)
            elif orientation == 180:
                while player.coordinates[0] < final_coords[0]:
                    self.screen.blit(self.board_img, player.coordinates, player.coordinates)
                    player.coordinates = player.coordinates.move(+5, 0)
                    self.screen.blit(player_img, player.coordinates)
                    pygame.display.update()
                    self.clock.tick(60)
            elif orientation == 90:
                while player.coordinates[1] < final_coords[1]:
                    self.screen.blit(self.board_img, player.coordinates, player.coordinates)
                    player.coordinates = player.coordinates.move(0, +5)
                    self.screen.blit(player_img, player.coordinates)
                    pygame.display.update()
                    self.clock.tick(60)
            
        player.orientation = orientation

    def update(self) -> None:
        
        for tile in self.render_tiles_list.values():
            moved_players = tile.update_data()
            if moved_players != []:
                for player in moved_players:
                    self.move_player(tile.index, player)
                    self.render_tiles_list[player.pos].players_on_tile.append(player)


        self.screen.blit(self.current_property_card_display[0], self.current_property_card_display[1])

    def update_dice_faces(self, dice_1: int, dice_2: int):
        dice_1_image = self.dice_faces[dice_1]
        dice_2_image = self.dice_faces[dice_2]
        dice_1_rect = dice_1_image.get_rect()
        dice_1_rect.x, dice_1_rect.y = (390, 450)
        dice_2_rect = dice_2_image.get_rect()
        dice_2_rect.x, dice_2_rect.y = (510, 450)
        self.current_temp = [[dice_1_image, dice_1_rect], [dice_2_image, dice_2_rect]]


    def mouse_tracker(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        
        for element in self.ui_elements:
            if element.clickable:
                command = element.check_clicked(mouse_pos, pressed)
                if command is not None:
                    command()

        for tile in self.render_tiles_list.values():
            tile_no = tile.check_clicked(mouse_pos, pressed)
            if self.selection_state and tile_no != -1:
                self.selection_func(tile_no)
                self.update_information_box()
                self.update()
                self.build_button_clicked_()
                
            if tile_no != -1 and tile.is_ownable():
                self.update_property_card_display(tile_no)
        
        if self.display_pay_fine_button:
            command = self.pay_fine_button.check_clicked(mouse_pos, pressed)
            if command is not None:
                command()
            self.pay_fine_button.check_clicked(mouse_pos, pressed)
        

    def render_all(self):
        self.screen.blit(self.board_img, (0, 0))

        for surface_info in self.current_temp:
            if surface_info[0] is False:
                surface_info[1].draw()
            else:
                self.screen.blit(surface_info[0], surface_info[1])
        
        for tile in self.render_tiles_list.values():
            tile.draw()

        for element in self.ui_elements:
            element.draw()

        for element in self.info_box_elements:
            element.draw()

        if self.display_pay_fine_button:
            self.pay_fine_button.draw()
        
        self.property_card_frame.draw()
        self.screen.blit(self.current_property_card_display[0], self.current_property_card_display[1])

        self.current_player.owned_property_view.draw()

        

    
    def dice_rolled(self):
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            self.update_dice_faces(d1, d2)
            doubles = False
            if d1 == d2:
                doubles = True          
            command_key = self.game.start_turn((d1+d2), doubles=doubles)
            # x = int(input("enter: "))
            # command_key = self.game.start_turn(x)
            self.roll_dice_button.set_state(False)
            self.end_turn_button.set_state(True)
            if self.current_player.properties != []:
                self.mortgagae_button.set_state(True)
                self.unmortgage_button.set_state(True)
                self.build_property_button.set_state(True)
            self.command_dictionary[command_key]()




        

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    for player in self.player_list:
                        player.owned_property_view.refresh_property_view()
 
    
            self.screen.fill("#2D2D2D")
            self.mouse_tracker()
            self.render_all()
            self.mouse_tracker()
            self.update()   

            pygame.display.flip()

            self.clock.tick(60)




a_player = Player(1500, "Talha")
b_player = Player(1500, "Qasim")

a_board = Game([a_player, b_player])

#a_board.create_board()
a_board.start_game()

ga = RenderEngine(a_board)
ga.game_loop()


pygame.quit()