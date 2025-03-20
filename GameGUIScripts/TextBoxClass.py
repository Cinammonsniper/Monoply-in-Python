import pygame


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



class TextBox:
    def __init__(self, text: str, width, height, coordinates: tuple[int, int], screen:pygame.surface.Surface, font: pygame.font.Font, alighn: str, background_colour="#3A3A3A", text_colour="#FFFFFF") -> None:

        self.__text = text
        self.__coordinates = coordinates
        self.__screen = screen
        self.__font = font
        self.__width = width
        self.__height = height
        self.__background_colour = background_colour
        self.__alighn = alighn
        self.__text_colour = text_colour
        self.__initialize()

    def __initialize(self) -> None:
        words = self.__fit_to_size()
        self.__box_rect = pygame.Rect(self.__coordinates, (self.__width, self.__height))
        self.clickable = False
        prev_rect = self.__box_rect
        self.__text_surfaces = []
        flag = False
        for word in words:
            surface = self.__font.render(word, True, self.__text_colour)
            text_rect = surface.get_rect()

            if self.__alighn == "center":
                text_rect.midtop = prev_rect.midbottom if flag else prev_rect.midtop
            elif self.__alighn == "left":
                text_rect.topleft = prev_rect.bottomleft if flag else prev_rect.topleft
            flag = True 
            prev_rect = text_rect
            self.__text_surfaces.append((surface, text_rect))

    def __fit_to_size(self) -> None:
        words_list = make_list(self.__text, " ")
        new_word = []
        word_str = ""
        final_word_pieces = []
        i = 0
        while i <= (len(words_list) - 1):
            word = words_list[i]
            if len(new_word)  == 0:
                new_word.append(word)
            else:
                new_word.append(" ")
                new_word.append(word)
            new_word_str = "".join(new_word)
            text_surface = self.__font.render(new_word_str, True, "#FFFFFF")
            text_rect = text_surface.get_rect()
            if text_rect.width > self.__width:
                final_word_pieces.append(word_str)
                new_word = []
                word_str = ""
            elif i == len(words_list) - 1:
                final_word_pieces.append(new_word_str)
                i += 1
            else:
                word_str = new_word_str
                i+=1
        return final_word_pieces

    def draw(self):
        pygame.draw.rect(surface=self.__screen, color=self.__background_colour, rect=self.__box_rect)
        for text in self.__text_surfaces:
            surface, text_rect = text
            self.__screen.blit(surface, text_rect)