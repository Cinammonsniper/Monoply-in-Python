import pygame

class Frame:
    def __init__(self, width: int, height: int, coordinates:tuple[int, int], screen:pygame.surface.Surface, colour="#3A3A3A") -> None:
        self.__width = width
        self.__height = height
        self.__coordinates = coordinates
        self.__screen = screen
        self.__colour = colour
        self.__initialize()

    def __initialize(self) -> None:
        self.clickable = False
        self.frame_rect = pygame.Rect(self.__coordinates, (self.__width, self.__height))

    def draw(self) -> None:
        pygame.draw.rect(surface=self.__screen, color=self.__colour, rect=self.frame_rect, border_radius=8)