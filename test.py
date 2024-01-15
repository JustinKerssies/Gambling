import pygame
import math
from classes import InputText, CenteredText


class Window:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 440))
        self.running = True
        self.colors = ['green', 'blue', 'black', 'red', 'firefox']
        self.blitables = []
        self.interactables = []
        self.shapes = []
        self.create_display(self.screen.get_width(), self.screen.get_height(), rows_columns=(2, 2))

        while self.running:
            self.event_check()
            self.blit()
            pygame.display.flip()
        for item in self.interactables:
            try:
                print(item.text)
            except AttributeError:
                pass

    def blit(self):
        self.screen.fill('white')
        for item in self.shapes:
            pygame.draw.rect(self.screen, 'black', item, width=1)
        for item in self.blitables:
            item.blit()
        for item in self.interactables:
            item.blit()
        pygame.display.flip()

    def create_display(self, width, height, rows_columns=(2, 2), ):
        width /= rows_columns[1]
        height -= 100
        amount_of_colors = len(self.colors)
        height = int(height / math.ceil((amount_of_colors / rows_columns[0])))
        print(height)
        loc = 0, 0
        for color in self.colors:
            shape = pygame.Rect(width * loc[0], height * loc[1], width, height)
            self.create_option((shape.left, shape.top, shape.width, shape.height), text=color)
            self.shapes.append(shape)
            if loc[0] == (rows_columns[1] - 1):
                loc = 0, loc[1] + 1
            else:
                loc = loc[0] + 1, loc[1]

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for item in self.interactables:
                    if item.rect.collidepoint(pos):
                        item.on_click()
                    else:
                        try:
                            item.active = False
                        except AttributeError:
                            pass
            if event.type == pygame.KEYDOWN:
                try:
                    for item in self.interactables:
                        if item.active:
                            if event.key == pygame.K_RETURN:
                                item.active = False
                            elif event.key == pygame.K_BACKSPACE:
                                item.text = item.text[:-1]
                            else:
                                item.text += event.unicode
                except AttributeError:
                    pass

    def create_option(self, rect, text=''):
        left = pygame.Rect(rect[0], rect[1], rect[2] / 2, rect[3])
        text = CenteredText(self.screen, left, text=text)
        self.blitables.append(text)
        right = pygame.Rect(rect[0] + (.5 * rect[2]), rect[1], rect[2] / 2, rect[3])
        inputtext = InputText(self.screen, (rect[0] + (.5 * rect[2]), rect[1], rect[2] / 2, rect[3]), numeric_only=True)
        self.interactables.append(inputtext)


if __name__ == '__main__':
    Window()
