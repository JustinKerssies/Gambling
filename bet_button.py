import pygame


class CenteredText:

    def __init__(self, screen, parent, fontsize, text, font=None):
        self.parent = parent
        self.rect = pygame.Rect(self.parent.left, self.parent.top, self.parent.width, self.parent.height)
        self.entity = screen.subsurface(self.rect)
        self.font = pygame.font.SysFont(font if font else None, int(fontsize), )
        self.text = str(text)

    def blit(self, text=None):
        if text:
            self.text = str(text)
        self.text_surface = self.font.render(self.text, True, 'black')
        text_rect = self.text_surface.get_rect(center=(self.parent.width / 2, self.parent.height / 2))
        self.entity.blit(self.text_surface, text_rect)


class BetButton:

    def __init__(self, screen, loc, width, height, roulette, input):
        self.screen = screen
        self.roulette = roulette
        self.input = input
        self.rect = pygame.Rect(loc[0], loc[1], width, height)
        self.text = CenteredText(screen, self.rect, 32, "bet")

    def blit(self, screen):
        pygame.draw.rect(screen, 'white', self.rect)
        pygame.draw.rect(screen, 'black', self.rect, width=1)
        self.text.blit()

    def on_click(self, pos):
        for item in self.input.chips:
            for numbers in self.roulette.text:
                if numbers.rect.collidepoint(item.center):
                    print(f'{numbers.text} : {item.color}')
