import BoardTileDataClasses
from TileScripts import Property, RailRoad, Utility, Chance, CommunityChest, Go, GoToJail, FreeParking, LuxuryTax, IncomeTax, Jail
from PlayerScript import Player


def calculate_position(pos: int, movement: int) -> int:
    new_pos = pos + movement
    if new_pos < 39:
        return False, new_pos
    else:
        return True, (new_pos - 39)
    
def calculate_number_rolled(current_position: int, desired_location:int) -> int:
    if current_position == desired_location:
        return 39
    elif current_position < desired_location:
        return desired_location - current_position
    else:
        return (39 - current_position) + desired_location

def progess_array(array: list) -> list:
    new_array = [None for i in array]
    length = (len(array) - 1)
    i = 0
    while i <= length:
        if i == length:
            new_array[0] = array[i]
        else:
            new_array[i+1] = array[i]
        i += 1
    return new_array
    


class Game:

    def __init__(self, players_list = list[Player]) -> None:
        self.board = [None for _ in range(0, 40)]
        self.players_list: list[Player] = players_list
        self.create_board()

    def create_board(self) -> None:
        property_list = BoardTileDataClasses.load_properties()
        railroads_list = BoardTileDataClasses.load_railroads()
        utilities_list = BoardTileDataClasses.load_utility()
        self.community_chest, self.chance = BoardTileDataClasses.load_chance_and_communitychest()
        #for i, c in enumerate(self.community_chest):
        #    print(i)
        #    print(c)
        #    print(" ")

        

        for _property in property_list:
            self.board[_property.pos] = Property(pos=_property.pos, name=_property.name, data=_property)
        for railroad in railroads_list:
            self.board[railroad.pos] = RailRoad(pos=railroad.pos, name=railroad.name, data=railroad)
        for utility in utilities_list:
            self.board[utility.pos] = Utility(pos=utility.pos, name=utility.name, data=utility)


        self.board[0] = Go(0, "Go")
        self.board[2] = CommunityChest(2, "Community Chest")
        self.board[4] = IncomeTax(4, "Income Tax")
        self.board[7] = Chance(7, "Chance")
        self.board[10] = Jail(10, "Jail")
        self.board[17] = CommunityChest(17, "Community Chest")
        self.board[20] = FreeParking(20, "Free Parking")
        self.board[22] = Chance(22, "Chance")
        self.board[30]  = GoToJail(30, "Go To Jail")
        self.board[33]  = CommunityChest(33, "Community Chest")
        self.board[36] = Chance(36, "Chance")
        self.board[38] = LuxuryTax(38, "LuxuryTax")  

        
        self.set_index_dictionary = {BoardTileDataClasses.Colour.LIGHTBLUE : (6,8,9),
                            BoardTileDataClasses.Colour.PINK : (11,13,14),
                            BoardTileDataClasses.Colour.ORANGE : (16,18,19),
                            BoardTileDataClasses.Colour.RED: (21,23,24),
                            BoardTileDataClasses.Colour.YELLOW: (26,27,29),
                            BoardTileDataClasses.Colour.GREEN: (31,32,34),
                            BoardTileDataClasses.Colour.PURPLE: (37,39),
                            BoardTileDataClasses.Colour.BROWN: (1,3)}

    def set_parity(self, propertry_no: int) -> None:
        set_indices = self.set_index_dictionary[self.board[propertry_no].return_color()]
        highest = 0
        lowest = 5
        current = 0
        same_dictionary = {}
        same_list = []
        for index in set_indices:
            property_level = self.board[index].property_level_
            if property_level > highest:
                highest = property_level
            elif property_level < lowest:
                lowest = property_level

            if property_level in same_dictionary.keys():
                same_dictionary[property_level].append(index)
            else:
                same_dictionary[property_level] = [index]
        
        same_list = [i for i in same_dictionary.values() if len(i) >= len(set_indices) - 1][0]


        if highest == 0:
            if self.board[propertry_no].full_set_is_owned is False:
                for index in set_indices:
                    self.board[index].is_buildable = False
                    self.board[index].is_deconstructable = False
        elif len(set_indices) == len(same_list) and highest > 0:
            for index in same_list:
                self.board[index].is_buildable = True
                self.board[index].is_deconstructable = True
        elif len(set_indices) == len(same_list) and highest == 0:
            for index in same_list:
                self.board[index].is_buildable = True
                self.board[index].is_deconstructable = False
        elif self.board[same_list[0]].property_level_ == highest:
            lowest_index = [i for i in set_indices if i not in same_list][0]
            self.board[lowest_index].is_buildable = True
            self.board[lowest_index].is_deconstructable = False
            for index in same_list:
                self.board[index].is_buildable = False
                self.board[index].is_deconstructable = True
        elif self.board[same_list[0]].property_level_ == lowest:
            highest_index = [i for i in set_indices if i not in same_list][0]
            self.board[highest_index].is_buildable = False
            self.board[highest_index].is_deconstructable = True
            for index in same_list:
                self.board[index].is_buildable = True
                self.board[index].is_deconstructable = False

    def check_if_set_completed(self, property_no: int) -> None:
        player = self.players_list[self.current_player_index]
        indices = [i for i in self.set_index_dictionary.values() if property_no in i][0]
        set_completed = True
        for index in indices:
            if self.board[index].owner == player and not self.board[index].is_mortgaged:
                continue
            set_completed = False
            break
        if set_completed is True:
            for i in indices:
                self.board[i].full_set_is_owned = True
        elif set_completed is False:
            for i in indices:
                self.board[i].full_set_is_owned = False
    
    def give_total_property(self, player: Player):
        hotel, house = 0, 0
        buildable_properties = [property for property in self.board if type(property) == Property]
        for buildable_property in buildable_properties:
            if buildable_property.owner == player:
                if buildable_property.property_level_ == 5:
                    hotel += 1
                else:
                    house += buildable_property.property_level_
        return (hotel, house)

        


    def start_game(self):
        self.current_player_index = 0
        self.turn_in_progress = True
        self.current_command = None
        self.current_value = None

    def start_turn(self, number_rolled: int, doubles = False, c_a_c = False) -> str:
        #self.current_player_index = (self.current_player + 1) if (self.current_player + 1) < len(self.players) else 0
        player = self.players_list[self.current_player_index]
        self.turn_in_progress = True
        if player.in_jail is True:
            if doubles is True:
                pass
            elif player.get_out_of_jail_cards > 0:
                player.get_out_of_jail_cards -= 1
            elif player.doubled_count == 3:
                player.doubled_count = 0
                status = player.decrease_balance(50)
                if status == "Banckrupt":
                #TODO add code to deal with a player going banckrupt
                    pass
            else:
                player.doubled_count += 1
                self.last_roll = number_rolled
                return "jail_option"
        self.current_command, self.current_value = self.move_current_player(number_rolled, c_a_c)
        if self.current_command == "Buyable":
            return "buy" if player.money > self.current_value else "end_turn"
        elif self.current_command == "Pay":
            status = player.decrease_balance(self.current_value)
            if status == "Banckrupt":
                #TODO add code to deal with a player going banckrupt
                pass
            return "end_turn"
        elif self.current_command == "Chance":
            self.current_chance = self.chance[-1]
            self.chance = progess_array(self.chance)
            return "chance"
        elif self.current_command == "CommunityChest":
            self.current_community_chest = self.community_chest[-1]
            self.community_chest = progess_array(self.community_chest)
            return "community_chest"
        elif self.current_command == "Move to Jail":
            return "move_jail"
        else:
            return "end_turn"

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) if (self.current_player_index + 1) < len(self.players_list) else 0
        return self.players_list[self.current_player_index]

    def move_current_player(self, movement: int, c_a_c = False) -> tuple[str, int]:
        player = self.players_list[self.current_player_index]
        pos = player.pos
        crossed_start, new_pos = calculate_position(pos, movement)
        if crossed_start:
            player.increase_balance(200)
        player.pos = new_pos
        command, value = self.board[new_pos].moved_onto_tile(player, c_a_c)
        return command, value

    def chance_actions(self, c_a_c: str) -> str:
        player = self.players_list[self.current_player_index]
        command, value = self.board[player.pos].return_command(c_a_c)
        #command, value = ("Move", 5)
        if command == "Pay":
            status = player.decrease_balance(value)
            if status == "Banckrupt":
                #TODO add code to deal with a player going banckrupt
                pass
            return "end_turn"
        elif command == "Earn":
            player.increase_balance(value)
            return "end_turn"
        elif command == "GOJ":
            player.get_out_of_jail_cards += 1
            return "end_turn"
        elif command == "Move":
            if value == -3:
                value = player.pos - 3
                player.decrease_balance(200)
            value = calculate_number_rolled(player.pos, value)
            return self.start_turn(value, True)
        elif command == "COB":
            money_owed = (len(self.players_list) - 1) * 50
            for otherplayer in self.players_list:
                if player != otherplayer:
                    otherplayer.increase_balance(50)
            status = player.decrease_balance(money_owed)
            if status == "Banckrupt":
                #TODO add code to deal with a player going banckrupt
                pass
            return "end_turn"
        elif command == "IYB":
            money_earned = ((len(self.players_list)) - 1) * 10
            for otherplayer in self.players_list:
                if player != otherplayer:
                    otherplayer.decrease_balance(10)
            player.increase_balance(money_earned)
            return "end_turn"
        elif command == "PR":
            hotel, house = self.give_total_property(player)
            money_owed = ((hotel * 100) + (house * 25)) if value == 0 else ((hotel * 115) + (house * 40))
            status = player.decrease_balance(money_owed)
            if status == "Banckrupt":
                #TODO add code to deal with a player going banckrupt
                pass
            return "end_turn"
        elif command == "Move to Jail":
            return "move_jail"

        

    def _mortgage_property(self, property_no: int) -> None:
        player = self.players_list[self.current_player_index]
        for property_ in self.board:
            if property_.is_ownable and property_.pos == property_no:
                player.increase_balance(property_.mortgage())
        self.check_if_set_completed(property_no)
        self.set_parity(property_no)
        
    
    def _unmortgage_property(self, property_no: int) -> None:
        player = self.players_list[self.current_player_index]
        for property_ in self.board:
            if property_.is_ownable and property_.pos == property_no:
                player.decrease_balance(property_.unmortgage())
        self.check_if_set_completed(property_no)
        self.set_parity(property_no)

    def _tile_bought(self):
        player = self.players_list[self.current_player_index]
        tile = self.board[player.pos]
        set_completion = tile.is_sold(player)
        if set_completion == "Set Completed":
            player = self.players_list[self.current_player_index]
            indices = [i for i in self.set_index_dictionary.values() if player.pos in i][0]
            indeces_to_check = [i for i in indices if i != player.pos]
            for i in indeces_to_check:
                self.board[i].set_completed()

        player.decrease_balance(self.current_value)
        if type(tile) == RailRoad:
            tile.recalculate_rent(player)

        self.current_command, self.current_value = ("end_turn", 0)
    
    def _fine_payed(self):
        player = self.players_list[self.current_player_index]
        status = player.decrease_balance(50)
        if status == "Banckrupt":
        #TODO add code to deal with a player going banckrupt
            pass
        self.start_turn(self.last_roll)

    def _build_on_tile(self, tile_no: int) -> None:
        self.board[tile_no].build_house()
        self.set_parity(tile_no)
    
    def _move_to_jail(self):
        player = self.players_list[self.current_player_index]
        player.in_jail = True
        player.pos = 10

    def _return_current_chance(self) -> str:
        return self.current_chance

    def _return_current_community_chest(self) -> str:
        return self.current_community_chest




            
    


"""talha = Player("1000", "Talha")

game = Game([talha])

game.board[6].is_sold(talha)
game.board[8].is_sold(talha)
game.board[9].is_sold(talha)

game.board[6].set_completed()
game.board[8].set_completed()
game.board[9].set_completed()


talha.properties = [game.board[6].data, game.board[8].data, game.board[9].data]

game.current_player_index = 0

game.board[6].log()
game.board[8].log()
game.board[9].log()

#game.board[6].build_house()
#game.board[8].build_house()
#game.board[9].build_house()
#game.board[8].build_house()
#game.board[9].build_house()
#game.board[6].build_house()
#game.board[6].build_house()
#game.board[6].build_house()

#game.board[6].sell_house()

print(" ")
print(" ")
print(" ")

game.board[8].mortgage()
game.check_if_set_completed(6)
game.set_parity(6)

game.board[6].log()
game.board[8].log()
game.board[9].log()"""