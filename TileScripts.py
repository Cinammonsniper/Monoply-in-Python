
from BoardTileDataClasses import PropertyData, RailRoadData, UtilityData, Colour
from PlayerScript import Player



class Tile(object):
    def __init__(self, pos, name) -> None:
        self.pos = pos
        self.name = name
        self.is_ownable = False
        self.is_buildable = False
        self.players_on_the_tile : list[Player] = []

    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        return None, 0

class Property(Tile):
    def __init__(self, pos, name, data: PropertyData) -> None:
        super().__init__(pos, name)
        
        self.is_ownable = True
        self.property_level_ = 0
        self.is_mortgaged = False
        self.owner : Player = None
        self.full_set_is_owned = False
        self.is_buildable = False
        self.is_deconstructable = False
        self.data = data
        self.rent = data.rents[0]
        self.colour = data.colour

    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        if self.owner == player:
            return "Owner", 0
        elif self.owner is None:
            return "Buyable", self.data.price
        elif self.owner != player:
            if self.is_mortgaged is False:
                return "Pay", self.rent
            else:
                pass
    
    def is_sold(self, player: Player):
        self.owner = player
        player.properties.append(self.data)
        in_set = self.data.in_set
        for _property in player.properties:
            if type(_property) == PropertyData:
                if _property.colour == self.colour:
                    in_set -= 1
        if in_set == 0:
            self.full_set_is_owned = True
            self.is_buildable = True
            self.rent = self.rent * 2
            return "Set Completed"
        else:
            return None
        
    def set_completed(self):
        self.set_completed = True
        self.is_buildable = True
        self.rent = self.rent * 2

    def mortgage(self):
        if self.is_deconstructable and self.property_level_ > 0:
            self.property_level_ -= 1
            return self.data.build_cost
        self.is_mortgaged = True
        return self.data.mortgage_value
    
    def unmortgage(self):
        self.is_mortgaged = False
        return (self.data.mortgage_value + (self.data.mortgage_value * 0.1))
    
    def build_house(self):
        self.property_level_ += 1
        self.data.houses = self.property_level_
        self.rent = self.data.rents[self.property_level_]
        self.is_buildable = False
        self.is_deconstructable = True

    def sell_house(self):
        self.property_level_ -= 1
        return self.data.build_cost
    
    
    def return_color(self):
        return self.data.colour
    
    def log(self):
        print("  ")
        print(self.name)
        print(f"property_level_: {self.property_level_}")
        print(f"is_mortgaged: {self.is_mortgaged}")
        print(f"full_set_is_owned: {self.full_set_is_owned}")
        print(f"is_buildable: {self.is_buildable}")
        print(f"is_deconstructable: {self.is_deconstructable}")
        print("  ")

class RailRoad(Tile):
    def __init__(self, pos, name, data: RailRoadData) -> None:
        super().__init__(pos, name)
        self.is_ownable = True
        self.is_mortgaged = False
        self.owner : Player = None
        self.data = data
        self.rent = 25
    
    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        if self.owner == player:
            return "Owner", 0
        elif self.owner is None:
            return "Buyable", self.data.price
        elif self.owner != player:
            if self.is_mortgaged is False:
                return "Pay", (self.rent if c_a_c is False else self.rent*2)
            else:
                pass
    
    def mortgage(self):
        self.is_mortgaged = True
        return self.data.mortgagae_value

    def unmortgage(self):
        self.is_mortgaged = False
        return (self.data.mortgage_value + (self.data.mortgage_value * 0.1))
        
    
    def is_sold(self, player: Player):
        self.owner = player
        player.properties.append(self.data)
        owned = 0
        for _property in player.properties:
            if _property is RailRoadData:
                owned += 1
        self.rent = self.rent * owned
        

    def recalculate_rent(self, player: Player):
        self.owner = player
        owned = 0
        for _property in player.properties:
            if _property is RailRoadData:
                owned += 1
        self.rent = self.rent * owned
    
    
    
class Utility(Tile):
    def __init__(self, pos, name, data: RailRoadData, c_a_c = False) -> None:
        super().__init__(pos, name)
        self.is_ownable = True
        self.is_mortgaged = False
        self.owner : Player = None
        self.owner_owns_pair = False
        self.data = data
    
    def moved_onto_tile(self, player: Player, c_a_c) -> tuple[str, int]:
        if self.owner == player:
            return "Owner", 0
        elif self.owner is None:
            return "Buyable", self.data.price
        elif self.owner != player:
            if self.is_mortgaged is False:
                return "Pay Calculated", 4 if self.owner_owns_pair is False else 10
            else:
                pass

    def is_sold(self, player: Player):
        self.owner = player
        player.properties.append(self.data)
        for _property in player.properties:
            if _property is UtilityData:
                self.owner_owns_pair = True 

    def mortgage(self):
        self.is_mortgaged = True
        return self.data.mortgagae_value

    def unmortgage(self):
        self.is_mortgaged = False
        return (self.data.mortgage_value + (self.data.mortgage_value * 0.1))

class CommunityChest(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)
        self.communitychest_command_dictionary = {"Advance to Go (Collect $200)" : ("Move", 0),
                                                  "Bank error in your favor. Collect $200" : ("Earn", 200),
                                                  "Doctors fee. Pay $50" : ("Pay", 50),
                                                  "From sale of stock you get $50" : ("Earn", 50),
                                                  "Get Out of Jail Free" : ("GOJ", 0),
                                                  "Go to Jail. Go directly to jail, do not pass Go, do not collect $200" : ("Move to Jail", 0),
                                                  "Holiday fund matures. Receive $100" : ("Earn", 100),
                                                  "Income tax refund. Collect $20" : ("Earn", 20),
                                                  "It is your birthday. Collect $10 from every player" : ("IYB", 10),
                                                  "Life insurance matures. Collect $100" : ("Earn", 100),
                                                  "Pay hospital fees of $100" : ("Pay", 100),
                                                  "Pay school fees of $50" : ("Pay", 50),
                                                  "Receive $25 consultancy fee" : ("Earn", 25),
                                                  "You are assessed for street repair. $40 per house. $115 per hotel" : ("PR", 1),
                                                  "You have won second prize in a beauty contest. Collect $10" : ("Earn", 10),
                                                  "You inherit $100" : ("Earn", 100)}
    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        return "CommunityChest", 0
    
    def return_command(self, community_chest: str) ->tuple[str, int]:
        return self.communitychest_command_dictionary[community_chest]

class Chance(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)
        self.chance_command_dictionary = {"Advance to Boardwalk": ("Move", 39),
                                          "Advance to Go (Collect $200)" : ("Move", 1),
                                          "Advance to Illinois Avenue. If you pass Go, collect $200": ("Move", 24),
                                          "Advance to St. Charles Place. If you pass Go, collect $200": ("Move", 11),
                                          "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled": ("Move", -100), 
                                          "Bank pays you dividend of $50": ("Earn", 50),
                                          "Get Out of Jail Free": ("GOJ", 0),
                                          "Go Back 3 Spaces": ("Move", -3),
                                          "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200": ("Move to Jail", 0),
                                          "Make general repairs on all your property. For each house pay $25. For each hotel pay $100": ("PR", 0),
                                          "Speeding fine $15": ("Pay", 15),
                                          "Take a trip to Reading Railroad. If you pass Go, collect $200": ("Move", 5),
                                          "You have been elected Chairman of the Board. Pay each player $50": ("COB", 0),
                                          "Your building loan matures. Collect $150": ("Earn", 150)}
    def moved_onto_tile(self, player: Player, c_a_c: False) -> tuple[str, int]:
        return "Chance", 0
    def return_command(self, chance: str) ->tuple[str, int]:
        return self.chance_command_dictionary[chance]
    
class GoToJail(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)
    
    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        return "Move to Jail", 0
    
class Go(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)

    def moved_onto_tile(self, player: Player, c_a_c =  False) -> tuple[str, int]:
        return super().moved_onto_tile(player)
    
class LuxuryTax(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)

    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        return "Pay", 100
    
class IncomeTax(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)

    def moved_onto_tile(self, player: Player, c_a_c = False) -> tuple[str, int]:
        ten_percent = (player.money * 0.1)
        return "Pay", ten_percent if ten_percent < 200 else 200

class FreeParking(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)

    def moved_onto_tile(self, player: Player, c_a_c =  False) -> tuple[str, int]:
        return super().moved_onto_tile(player, c_a_c)

class Jail(Tile):
    def __init__(self, pos, name) -> None:
        super().__init__(pos, name)
        self.players_in_jail: list[Player] = []
    
    def moved_onto_tile(self, player: Player, c_a_c =  False) -> tuple[str, int]:
        return super().moved_onto_tile(player, c_a_c)
    
    def put_player_in_jail(self, player: Player):
        self.players_in_jail.append(player)

    def remove_player_from_jail(self, player: Player):
        self.players_in_jail.remove(player)
    