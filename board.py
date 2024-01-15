import pygame

import rules


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
        self.text_surface = self.font.render(self.text, True, 'white')
        text_rect = self.text_surface.get_rect(center=(self.parent.width / 2, self.parent.height / 2))
        self.entity.blit(self.text_surface, text_rect)


class RouletteBoard:

    def __init__(self, screen, loc, width, height):
        self.blits = []
        self.numbers = []
        self.text = []
        self.screen = screen
        zero_width = width / 13
        self.rect = pygame.Rect(loc[0], loc[1], width, height)
        upper_part = self._upper_part((self.rect.left + zero_width, self.rect.top), width - zero_width,
                                      (height * .25))
        zero_rect = self._zero((self.rect.left, upper_part.bottom), zero_width, (height * .5))
        middle_part = self._middle_part((zero_rect.right, upper_part.bottom), (width - zero_width), (height * .5))
        lower_part = self._lower_part((self.rect.left + zero_width, middle_part.bottom), width - zero_width,
                                      (height * .25))

    def _upper_part(self, loc, width, height):
        upper_part_rect = pygame.Rect(loc[0], loc[1], width, height)
        manque_rect = pygame.Rect(loc[0], loc[1], (width / 3), height)
        impair_rect = pygame.Rect(manque_rect.right, loc[1], (width / 3), height)
        rouge_rect = pygame.Rect(impair_rect.right, loc[1], (width / 3), height)
        manque_text = CenteredText(self.screen, manque_rect, 24, "Manque 1-18")
        impair_text = CenteredText(self.screen, impair_rect, 24, "Impair odd")
        rouge_text = CenteredText(self.screen, rouge_rect, 24, "Red")
        self.blits.append(manque_rect)
        self.blits.append(impair_rect)
        self.blits.append(rouge_rect)
        self.text.append(manque_text)
        self.text.append(impair_text)
        self.text.append(rouge_text)
        return upper_part_rect

    def _middle_part(self, loc, width, height):
        i = 3
        middle_part_rect = pygame.Rect(loc[0], loc[1], width, height)
        rows, columns = 3, 12
        block_width = width / 12
        block_height = height / 3
        for row in range(rows):
            for column in range(columns):
                x, y = loc[0] + (column * block_width), loc[1] + (row * block_height)
                block_rect = pygame.Rect(x, y, block_width, block_height)
                text = CenteredText(self.screen, block_rect, 24, str(i))
                if i in rules.Rules.rouge_color:
                    color = 'Red'
                else:
                    color = 'Black'
                self.numbers.append((block_rect, color))
                self.text.append(text)
                i += 3
                if i > 36:
                    i = i - 37
        return middle_part_rect

    def _lower_part(self, loc, width, height):
        lower_part_rect = pygame.Rect(loc[0], loc[1], width, height)
        passe_rect = pygame.Rect(loc[0], loc[1], (width / 3), height)
        pair_rect = pygame.Rect(passe_rect.right, loc[1], (width / 3), height)
        noir_rect = pygame.Rect(pair_rect.right, loc[1], (width / 3), height)
        passe_text = CenteredText(self.screen, passe_rect, 24, "Passe 19-36")
        pair_text = CenteredText(self.screen, pair_rect, 24, "Pair Even")
        noir_text = CenteredText(self.screen, noir_rect, 24, "Black")
        self.blits.append(passe_rect)
        self.blits.append(pair_rect)
        self.blits.append(noir_rect)
        self.text.append(passe_text)
        self.text.append(pair_text)
        self.text.append(noir_text)
        return lower_part_rect

    def _zero(self, loc, width, height):
        zero_rect = pygame.Rect(loc[0], loc[1], width, height)
        text = CenteredText(self.screen, zero_rect, 24, str(0))
        self.numbers.append((zero_rect, 'darkGreen'))
        self.text.append(text)
        return zero_rect

    def blit(self, screen):
        for items in self.blits:
            pygame.draw.rect(screen, '#5a5a5a', items)
            pygame.draw.rect(screen, 'white', items, width=1)
        for items in self.numbers:
            pygame.draw.rect(screen, items[1], items[0])
            pygame.draw.rect(screen, 'white', items[0], width=1)
        for items in self.text:
            items.blit()

    def on_click(self, pos):
        for items in self.text:
            if items.rect.collidepoint(pos):
                print(items.text)
