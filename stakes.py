import pygame
import math


class Stakes:

    def __init__(self, screen, loc, width, height):
        self.blits = []
        self.amount = {
            'green': 3,
            'blue': 1,
            'black': 1,
            'red': 1
        }
        self.chips = []
        self.screen = screen
        self.stakes_rect = pygame.Rect(loc[0], loc[1], width, height)
        self._chips(loc, width, height)
        self.blits.append(self.stakes_rect)

    def _chips(self, loc, width, height):
        columns, rows = 2, 2
        current_column, current_row = 0, 0
        sector_width, sector_height = width / (len(self.amount) / columns), height / (len(self.amount) / rows)
        for color in self.amount.keys():
            for x, chip in enumerate(range(self.amount[color])):
                radius = 20
                center = loc[0] + sector_width / 2 + sector_width * current_column + (x * radius), \
                         loc[1] + sector_height / 2 + sector_height * current_row
                chip = Chip(center, radius, color)
                self.chips.append(chip)
            current_column += 1
            if current_column == columns:
                current_column = 0
                current_row += 1

    def blit(self):
        for items in self.blits:
            pygame.draw.rect(self.screen, 'black', items, width=2)
        for items in self.chips:
            items.blit(self.screen)

    def on_hold(self, pos):
        for item in self.chips:
            distance = math.hypot(pos[0] - item.center[0], pos[1] - item.center[1])
            if distance < item.radius:
                item.center = pos
                return


class Chip:

    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def blit(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
        pygame.draw.circle(screen, 'black', self.center, self.radius, width=1)
