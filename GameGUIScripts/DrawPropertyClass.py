import pygame

class DrawProperty:
    def __init__(self, screen: pygame.surface.Surface, edges: list[tuple[int, int]], rotation: int) -> None:
        self.__screen = screen
        self.__edges = edges
        self.__rotation = rotation
        self.__initialize()

    def __initialize(self):

        self.property_level = 0 #local record of the property level
        self.__house = pygame.transform.smoothscale(pygame.image.load("assets\\image assets\\house.png"), (15, 15))
        self.__hotel = pygame.transform.smoothscale(pygame.image.load("assets\\image assets\\hotel.png"), (30, 15))
        self.__hotel_flag = False 
        self.__house_list = []
        

    def update_house_list(self, property_level: int) -> None:
        
        self.property_level = property_level
        (x1, y1), (x2, y2) = self.__edges
        self.__house_list = []
        
        # Define rotation cases.
        rotation_cases = {0  : {"y_cord": y1 + 5   , "offset": ((x2 - x1) // ((self.property_level * 2) + 1))}, 
                          90 : {"x_cord": x2 - 20  , "offset": ((y2 - y1) // ((self.property_level * 2) + 1))}, 
                          180: {"y_cord": y2 - 20  , "offset": ((x2 - x1) // ((self.property_level * 2) + 1))},
                          270: {"x_cord": x1 + 5   , "offset": ((y2 - y1) // ((self.property_level * 2) + 1))}
        }

        if self.__rotation in [0, 180]:
            #Get the current rotaion case.
            rotation_case = rotation_cases[self.__rotation]

            #Generate coordinates for the houses and add them to the house list.
            if self.property_level < 5:
                x_coordinate = x1 + rotation_case["offset"]
                for _ in range(self.property_level):
                    coordinates = (x_coordinate, rotation_case["y_cord"])
                    self.__house_list.append(coordinates)
                    x_coordinate += rotation_case["offset"] * 2
            #Generate coordinates for a hotel if property level greater than 5.
            else:
                self.__hotel_flag = True
                x_coordinate = x1 + ((x2 - x1) / 2) - 16
                coordinates = (x_coordinate, rotation_case["y_cord"])
                self.__house_list.append(coordinates)

        if self.__rotation in [90, 270]:
            #Get the current rotaion case.
            rotation_case = rotation_cases[self.__rotation]

            #Generate coordinates for the houses and add them to the house list.
            if self.property_level < 5:
                y_coordinate = y1 + rotation_case["offset"]
                for _ in range(self.property_level):
                    coordinates = (rotation_case["x_cord"], y_coordinate)
                    self.__house_list.append(coordinates)
                    y_coordinate += rotation_case["offset"] * 2
            #Generate coordinates for a hotel if property level greater than 5.
            else:
                self.__hotel_flag = True
                y_coordinate = y1 + ((y2 - y1) / 2) - 16
                coordinates = (rotation_case["x_cord"], y_coordinate)
                self.__house_list.append(coordinates)
        

        
    def draw(self):
        build_transformed = pygame.transform.rotate(self.__house, self.__rotation) if self.__hotel_flag is False else pygame.transform.rotate(self.__hotel, self.__rotation)
        for cords in self.__house_list:
            self.__screen.blit(build_transformed, cords)




   