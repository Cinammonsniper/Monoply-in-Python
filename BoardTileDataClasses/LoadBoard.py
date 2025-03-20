import json
from BoardTileDataClasses.PropertyDataClass import PropertyData, Colour
from BoardTileDataClasses.RailRoadDataClass import RailRoadData
from BoardTileDataClasses.UtilityDataClass import UtilityData


def load_properties() -> list[PropertyData]:
    file = open("assets\\boarddata\\properties.json")
    properties_list = []
    properties = json.load(file)
    for property in  properties:
        _rents=[property["rent"], property["rent_1house"], property["rent_2house"], property["rent_3house"], property["rent_4house"], property["rent_hotel"]]
        property_data = PropertyData(name=property["name"], price=property["price"], rents=_rents, build_cost=property["build_cost"], mortgage_value=property["mortgage_value"], 
                                     in_set=property["in_set"], colour=Colour(property["colour"]), pos=property["pos"])
        properties_list.append(property_data)
    file.close()
    return properties_list

def load_railroads() -> list[RailRoadData]:
    file = open("assets\\boarddata\\stations.json")
    railroads_list = []
    railroads = json.load(file)
    for railroad in railroads:
        railroad_data = RailRoadData(name=railroad["name"], price=railroad["price"], mortgagae_value=railroad["mortgage_value"], pos=railroad["pos"])
        railroads_list.append(railroad_data)
    file.close()
    return railroads_list


def load_utility() -> list[UtilityData]:
    file = open("assets\\boarddata\\utilities.json")
    utilities_list = []
    utilities = json.load(file)
    for utility in utilities:
        utility_data = UtilityData(name=utility["name"], price=utility["price"], mortgagae_value=utility["mortgage_value"], pos=utility["pos"])
        utilities_list.append(utility_data)
    file.close()
    return utilities_list

def make_list(data: str, seperator: str) -> list[str]:
    array = []
    word = []
    for i, character in enumerate(data):
        if character == seperator:
            sentence = "".join(word)
            array.append(sentence)
            word = []
            continue
        elif i == (len(data) - 1):
            word.append(character)
            sentence = "".join(word)
            array.append(sentence)
            word = []
            continue
        else:
            word.append(character)
    return array

def load_chance_and_communitychest() -> tuple[list[str]]:
    with open("assets\\boarddata\\communitychest.txt", "r") as community_chest:
        text = community_chest.read()
        community_chest_cards = make_list(text, "!")
    with open("assets\\boarddata\\chance.txt", "r") as chance:
        text = chance.read()
        chance_cards = make_list(text, "!")

    return(community_chest_cards, chance_cards)

