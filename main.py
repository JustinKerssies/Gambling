from classes import *
import pygame
import board
import stakes
import math
import bet_button


class Window:

    def __init__(self):
        self.items = []
        pygame.init()
        screensize = 1050, 450
        self.screen = pygame.display.set_mode(screensize)
        self.roulette = board.RouletteBoard(self.screen, (300, 0), 650, 300)
        self.input = stakes.Stakes(self.screen, (0, self.roulette.rect.bottom), 950, 150)
        self.bet = bet_button.BetButton(self.screen, (950, 0), 100, 450, self.roulette, self.input)
        self.items.append(self.roulette) ; self.items.append(self.input) ; self.items.append(self.bet)

        self.running = True
        while self.running:
            self.screen.fill('darkgrey')
            self.event_check()
            self.roulette.blit(self.screen)
            self.bet.blit(self.screen)
            self.input.blit()
            pygame.draw.circle(self.screen, 'white', (150, 150), radius=120)
            pygame.display.flip()
        pygame.quit()

    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for items in self.items:
                    try:
                        if items.rect.collidepoint(pos):
                            items.on_click(pos)
                    except AttributeError:
                        pass
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                try:
                    for item in self.input.chips:
                        distance = math.hypot(pos[0] - item.center[0], pos[1] - item.center[1])
                        if distance < item.radius:
                            item.center = pos
                            return
                except AttributeError:
                    pass


if __name__ == '__main__':
    Window()
