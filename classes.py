import pygame as pg
from time import sleep
from threading import Thread
import math


# Purely Questionnaire Text-type
class DecorativeText:

    def __init__(self, parent, rect, fontsize=32, fontcolor='black', text='', padding=20, font=None):
        self.parent = parent
        self.color = fontcolor
        self.font = pg.font.Font(None, fontsize)
        self.rect = pg.Rect(rect)
        self.padding = padding
        self.text = text

    def blit(self):
        txt_surface = self.font.render(self.text, True, self.color)
        text_rendering = txt_surface.get_rect(center=(self.rect.width / 2, self.rect.top + (self.rect.height / 2)))
        text_rendering.right = self.rect.right - self.padding
        # Resize the box if the text is too long.
        # Blit the text.
        self.parent.blit(txt_surface, text_rendering)
        # Blit the input_box rect.
        self.rect = pg.draw.rect(self.parent, self.color, self.rect, 2)


# Broad button class
class Button:

    def __init__(self, screen, rect, text, function, *args, fontsize=32, font=None):
        self.text = text
        self.screen = screen
        self.function = function
        self.rect = pg.Rect(rect)
        self.lock = False
        self.variables = args
        self.clicked = False
        self.active_color = 'black'
        self.inactive_color = 'darkgrey'
        self.color = self.inactive_color
        self.text_subsurface = self.screen.subsurface(rect)
        if font:
            self.font = pg.font.SysFont(font, int(fontsize))
        else:
            self.font = pg.font.Font(None, int(fontsize))
        self.render_text()

    def blit(self, pos=None):
        if self.clicked:
            self.color = self.active_color
        else:
            self.color = self.inactive_color
        button = pg.draw.rect(self.screen, 'grey', self.rect)
        border = pg.draw.rect(self.screen, self.color, self.rect, width=1)
        text = self.text_subsurface.blit(self.text_rendering, self.text_rect)

    def render_text(self, text=None, addon=None):
        if text:
            self.text = text
        self.text_rendering = self.font.render((self.text + addon) if addon else self.text, True, 'black')
        self.text_rect = self.text_rendering.get_rect(center=(self.rect.width / 2, self.rect.height / 2))

    def refresh_variables(self, *args):
        self.variables = args

    def set_function(self, function):
        self.function = function

    def on_click(self):
        if not self.lock:
            t1 = Thread(target=self.click_function, daemon=True)
            t1.start()

    def click_function(self):
        self.clicked = True
        sleep(0.1)
        self.clicked = False
        if self.variables:
            self.function(*self.variables)
        else:
            self.function()


# General Centered text
class CenteredText:

    def __init__(self, screen, parent, fontsize=32, text='', font=None):
        self.parent = parent
        self.rect = pg.Rect(self.parent.left, self.parent.top, self.parent.width, self.parent.height)
        print(self.parent.left, self.parent.top, self.parent.width, self.parent.height)
        self.entity = screen.subsurface(self.rect)
        self.font = pg.font.SysFont(font if font else None, int(fontsize), )
        self.text = str(text)

    def blit(self, text=None):
        if text:
            self.text = str(text)
        self.text_surface = self.font.render(self.text, True, 'black')
        text_rect = self.text_surface.get_rect(center=(self.parent.width / 2, self.parent.height / 2))
        self.entity.blit(self.text_surface, text_rect)


# Circle that changes color when clicked
class InteractiveCircle:

    def __init__(self, screen, mid_rect, radius, possible_colors, current_color=None, data=None):
        self.screen = screen
        self.input_library_location = None
        self.data = data
        self.mid_rect = mid_rect
        self.color_list = possible_colors
        self.radius = radius
        self.color_indicator = 0
        if current_color:
            self.color = current_color
        else:
            self.color = self.color_list[0]

        for indicator, color in enumerate(self.color_list):
            if self.color == color:
                self.color_indicator = indicator
        self.blit()

    def blit(self):
        self.rect = pg.draw.circle(self.screen, self.color, self.mid_rect, self.radius)
        border = pg.draw.circle(self.screen, 'black', self.mid_rect, self.radius, width=1)

    def on_click(self):
        if self.color_indicator + 1 <= len(self.color_list) - 1:
            self.color_indicator += 1

        else:
            self.color_indicator = 0
        self.color = self.color_list[self.color_indicator]
        if self.data:
            self.data.currently_selected_colors[self.input_library_location] = self.color


# RGB circle that registers color on click
class RgbPicker:

    def __init__(self, parent, loc, radius):
        self.parent = parent
        self.loc = loc
        self.radius = radius
        self.mouse_pos = None
        self.rect = pg.draw.circle(parent, 'black', loc, radius, width=1)
        self.color = [0, 0, 0]
        midpoint = (parent.get_width() / 2, parent.get_height() / 2)
        self.img_location = midpoint[0] - radius, midpoint[1] - radius
        img_size = radius * 2, radius * 2
        self.img = pg.image.load('images/rgb.png')
        self.img = pg.transform.scale(self.img, img_size)

    def blit(self):
        self.parent.blit(self.img, self.img_location)
        if self.mouse_pos:
            self.mouse_location_circle = pg.draw.circle(self.parent, 'black',
                                                        [self.mouse_pos[0], self.mouse_pos[1]],
                                                        radius=10, width=1)

    def get_pos(self, pos):
        dist = math.hypot(pos[0] - self.loc[0], pos[1] - self.loc[1])
        if dist > self.radius:
            print('NO')
            return
        self.mouse_pos = pos
        color = self.compare_pos(dist)
        return color

    def compare_pos(self, distance_from_midpoint=None):
        calc = 0
        _trigger = False
        if self.mouse_pos[1] < self.loc[1]:
            angle = 0
            calc_side = 'upper'
            if self.mouse_pos[0] < self.loc[0]:
                d = self.upper_left()
                side = 'left'
            else:
                d = self.upper_right()
                side = 'right'
        else:
            angle = 90
            calc_side = 'lower'
            if self.mouse_pos[0] < self.loc[0]:
                d = self.lower_left()
                side = 'left'
            else:
                d = self.lower_right()
                side = 'right'

        if distance_from_midpoint > self.radius:
            return [255, 255, 255]
        try:
            if calc_side == 'upper':
                calc = d[0] / d[1]
            elif calc_side == 'lower':
                calc = d[1] / d[0]
        except ZeroDivisionError:
            _trigger = True
        angle += math.degrees(math.atan(calc))
        if _trigger:
            angle = 180
        calc_list = []
        self.color = self.decide_color(angle, distance_from_midpoint, side=side)
        for value in self.color:
            calc = 255 - value
            calc_list.append(int(calc))
        if distance_from_midpoint <= self.radius + 2:
            for num, calc in enumerate(calc_list):
                try:
                    addon = calc * (distance_from_midpoint / self.radius)
                    if addon > calc:
                        addon = calc
                    self.color[num] = self.color[num] + (calc - addon)
                except ZeroDivisionError:
                    value = 0
        if self.color == None:
            self.color = [255, 255, 255]
        return self.color

    def upper_left(self):
        """d == x / y"""
        d = self.loc[0] - self.mouse_pos[0], self.loc[1] - self.mouse_pos[1]
        return d

    def upper_right(self):
        """d == x / y"""
        d = self.mouse_pos[0] - self.loc[0], self.loc[1] - self.mouse_pos[1]
        return d

    def lower_left(self):
        """d == y / x"""
        d = self.loc[0] - self.mouse_pos[0], self.mouse_pos[1] - self.loc[1]
        return d

    def lower_right(self):
        """d == y / x"""
        d = self.mouse_pos[0] - self.loc[0], self.mouse_pos[1] - self.loc[1]
        return d

    def decide_color(self, degrees, distance, side='left'):
        if side == 'left':
            self.color = [255, 0, 0]
            color_indicator = 2
            calc_var = 1
            for degrees in range(int(degrees)):
                self.color[color_indicator] += 4.25 * calc_var
                if self.color[color_indicator] == 0:
                    color_indicator = 1
                    calc_var *= -1
                if self.color[color_indicator] == 255:
                    color_indicator = 0
                    calc_var *= -1
            return self.color
        elif side == 'right':
            self.color = [255, 0, 0]
            color_indicator = 1
            calc_var = 1
            for degrees in range(int(degrees)):
                self.color[color_indicator] += 4.25 * calc_var
                if self.color[color_indicator] == 0:
                    color_indicator = 2
                    calc_var *= -1
                if self.color[color_indicator] == 255:
                    if not color_indicator - 1 < 0:
                        color_indicator = color_indicator - 1
                    else:
                        color_indicator = 2
                    calc_var *= -1
            return self.color
        else:
            print('error')

    def blit_circle(self):
        for x in range(self.parent.get_width()):
            for y in range(self.parent.get_height()):
                pos = (x, y)
                if self.rect.collidepoint(pos):
                    color = self.get_pos(pos)
                    pg.draw.rect(self.parent, color, (x, y, 1, 1))


# Input text class
class InputText:

    def __init__(self, parent, rect, personal_range=None, numeric_only=None, text=None):
        self.parent = parent
        self.inactive_color = 'grey'
        self.active_color = 'black'
        self.invalid_color = 'red'
        self.font = pg.font.Font(None, 32)
        self.rect = pg.Rect(rect)
        if personal_range:
            self.personal_range = personal_range
        else:
            self.personal_range = []
        if numeric_only:
            self.numeric_only = True
        else:
            self.numeric_only = False
        if text:
            self.text = str(text)
        else:
            self.text = ''
        self.list = []
        self.active = False

    def blit(self):
        # Render the current text.
        if self.active:
            color = self.active_color
        else:
            color = self.inactive_color
        if not self.text == '':
            if not self.text.isnumeric() and self.numeric_only:
                color = self.invalid_color
            elif self.text.isnumeric() and not self.numeric_only:
                color = self.invalid_color
            if self.personal_range and self.text.isnumeric():
                if not self.personal_range[0] <= int(self.text) <= self.personal_range[1]:
                    color = self.invalid_color
        white_space = pg.draw.rect(self.parent, 'white', self.rect)
        txt_surface = self.font.render(self.text, True, color)
        txt_rendering = txt_surface.get_rect(center=((self.rect.left + (self.rect.width / 2),
                                                      self.rect.top + (self.rect.height / 2))))
        # Resize the box if the text is too long.
        # Blit the text.
        self.parent.blit(txt_surface, txt_rendering)
        # Blit the input_box rect.
        self.rect = pg.draw.rect(self.parent, color, self.rect, 2)

    def on_click(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def update(self):
        self.personal_range = []


# Popup with an inputbar
class InputPopup:

    def __init__(self, screen, size, text):
        self.screen = screen
        self.active = False
        self.interactables = []
        self.blitables = []
        padding = 5
        x, y = self.screen.get_width() / 2 - size[0] / 2, self.screen.get_height() / 2 - size[1] / 2
        self.text = text
        self.rect = pg.Rect(x, y, size[0], size[1])
        question_rect = pg.Rect(self.screen.get_width() / 2 - size[0] / 2 + padding, self.rect.top + padding,
                                self.rect.width - (2 * padding), 50)
        question = CenteredText(screen, question_rect, 32, text)
        self.blitables.append(question)
        input_rect = pg.Rect(question_rect.left, question_rect.bottom + padding, self.rect.width - (2 * padding), 50)
        self.input = InputText(screen, *input_rect)
        self.interactables.append(self.input)
        button_rect = self.rect.left + padding, self.rect.bottom - size[1] / 4 - padding, (size[0] - 3 * padding) / 2, \
                      size[1] / 4
        button = Button(screen, button_rect, 'cancel', self.quit)
        self.interactables.append(button)
        button_rect = button.rect.right + padding, self.rect.bottom - size[1] / 4 - padding, (
                size[0] - 3 * padding) / 2, size[1] / 4
        button = Button(screen, button_rect, 'save', self.save)
        self.interactables.append(button)

    def blit(self):
        if self.active:
            pg.draw.rect(self.screen, 'white', self.rect)
            for item in self.blitables:
                item.blit()
            for item in self.interactables:
                item.blit()

    def on_click(self, pos):
        for item in self.interactables:
            if item.rect.collidepoint(pos):
                item.on_click()

    def save(self):
        if not self.input.text == '':
            self.answer = self.input.text
            self.active = False
        else:
            return

    def quit(self):
        self.active = False

    def init_pop(self):
        self.active = True
        self.text = ''


# List class
class InputList:

    def __init__(self, screen, parent, choices, fontsize=24, font=None):
        self.screen = screen
        self.parent = parent
        self.fontsize = fontsize
        self._remove_trigger = False
        self.font = font
        try:
            self.parent_rect = parent.rect
        except:
            self.parent_rect = parent
        self.active = False
        self.choices = choices
        self.active_point = None
        self.create_text_locations(choices)

    def create_text_locations(self, list):
        self.text_locations = []
        self.box_locations = []
        height, width = 30 * len(list), self.parent_rect.width
        x, y = self.parent_rect.left, self.parent_rect.bottom - height
        self.rect = pg.Rect(x, y, width, height)
        for num, text in enumerate(list):
            rect = pg.Rect(self.rect.left, self.rect.top + (num * 30), self.rect.width, 30)
            text = CenteredText(self.screen, rect, self.fontsize, text)
            self.text_locations.append(text)
            box_rect = pg.Rect(rect.right - (rect.width * 0.1), self.rect.top + (num * 30), rect.width * 0.1,
                               rect.height)
            self.box_locations.append(box_rect)

    def blit(self):
        if self.active:
            try:
                self.parent.lock = True
            except AttributeError:
                pass
            pg.draw.rect(self.screen, 'white', self.rect)
            for num, items in enumerate(self.text_locations):
                if num == self.active_point:
                    pg.draw.rect(self.screen, 'lightblue', items.rect)
                items.blit()
                pg.draw.rect(self.screen, 'black', items.rect, width=1)
            for num, items in enumerate(self.box_locations):
                pg.draw.rect(self.screen, 'black', items, width=1)
        else:
            try:
                self.parent.lock = False
            except AttributeError:
                pass

    def on_click(self, pos):
        for num, items in enumerate(self.text_locations):
            if items.rect.collidepoint(pos):
                self.active_point = num
        if any(box.collidepoint(pos) for box in self.box_locations):
            self._remove_trigger = True
        else:
            self._remove_trigger = False

    def update_list(self, list):
        self.choices = list
        self.create_text_locations(list)

    def init_list(self):
        self.active = True


# General 'cancel/confirm' popup
class Popup:

    def __init__(self, screen, size, text):
        self.screen = screen
        self.size = size
        self.proceed = False
        self.active = False
        self.buttons = []
        self.text = text
        padding = 5
        self.rect = pg.Rect((screen.get_width() / 2 - self.size[0] / 2), (screen.get_height() / 2 - self.size[1] / 2),
                            size[0], size[1])
        button_rect = self.rect.right - (self.rect.width * .4) - padding, self.rect.top + self.rect.height - (
                self.rect.height * .3) - padding, self.rect.width * .4, self.rect.height * .3
        self.proceed = Button(screen, button_rect, 'proceed', self.cont)
        button_rect = self.rect.left + padding, self.rect.top + self.rect.height - (self.rect.height * .3) - padding, \
                      self.rect.width * .4, self.rect.height * .3
        self.cancel = Button(screen, button_rect, 'cancel', self.cancel)
        self.buttons.append(self.cancel)
        self.buttons.append(self.proceed)
        text_placement = pg.Rect(self.screen.get_width() / 2 - size[0] / 2 + padding, self.rect.top + padding,
                                 self.rect.width - (2 * padding), 50)
        self.text = CenteredText(screen, text_placement, 32, text)

    def blit(self):
        if self.active:
            pg.draw.rect(self.screen, 'white', self.rect)
            pg.draw.rect(self.screen, 'black', self.rect, width=1)
            self.text.blit()
            for buttons in self.buttons:
                buttons.blit()

    def on_click(self, pos):
        if self.active:
            for items in self.buttons:
                if items.rect.collidepoint(pos):
                    items.on_click()

    def refresh_text(self, text=None, addon=None):
        i = 1

    def cancel(self):
        self.active = False

    def cont(self):
        self.active = False
        self.proceed = True

    def init_pop(self):
        self.proceed = False
        self.active = True


# RGB tab for the RGB cirlce
class RGBPickerTab:

    def __init__(self, screen, parent, parent_rect, design=None):
        self.screen = screen
        self.parent = parent
        self.rect = pg.Rect(parent_rect)
        self.subsurface = self.screen.subsurface(self.rect)
        self.blitlist = []
        self.textlist = []
        self.font = design.font if design else None
        self.active = False
        self.prepare()

    def blit(self):
        if not self.active:
            return
        self.subsurface.fill('white')
        for items in self.blitlist:
            items.blit()
        pg.draw.rect(self.subsurface, self.color_circle.color, self.color_preview_rect)
        pg.draw.rect(self.subsurface, 'black', self.color_preview_rect, width=1)
        for num, items in enumerate(self.textlist):
            code = int(self.color_circle.color[num])
            items.blit(str(code))
        pg.draw.rect(self.screen, 'black', self.rect, width=1)

    def on_click(self, pos, addon=None):
        if not self.rect.collidepoint(pos):
            self.parent.tab_active = False
            self.active = False
        pos = pos[0] - self.rect.left, pos[1] - self.rect.top
        color = self.color_circle.get_pos(pos)
        if color == None:
            color = [255, 255, 255]

    def prepare(self):
        width, height = self.rect.width, self.rect.height
        color_circle_tab_rect = 0, 0, width * .75, height * 1
        color_circle_tab = pg.draw.rect(self.subsurface, 'black', color_circle_tab_rect, width=1)
        self.color_circle_location_subsurface = self.subsurface.subsurface(color_circle_tab_rect)
        self.rgb_values_rect = color_circle_tab.right, 0, width * .25, height * 0.75
        self.rgb_values_tab = pg.draw.rect(self.subsurface, 'black', self.rgb_values_rect, width=1)
        self.color_preview_rect = color_circle_tab.right, self.rgb_values_tab.bottom, width * .25, height * 0.25
        color_preview = pg.draw.rect(self.subsurface, 'black', self.color_preview_rect, width=1)
        self.prepare_color_circle(color_circle_tab)
        self.prepare_rgb_values(self.rgb_values_tab)

    def prepare_color_circle(self, parent):
        width, height = parent.width, parent.height
        radius = min(width, height)
        radius /= 2
        self.color_circle = RgbPicker(self.color_circle_location_subsurface, (width / 2, height / 2), radius)
        self.blitlist.append(self.color_circle)

    def prepare_rgb_values(self, parent):
        for num in range(3):
            calc_rect = parent.left, parent.top + (num * (parent.height / 3)), parent.width / 2, parent.height / 3
            name_rect = pg.draw.rect(self.subsurface, 'black', calc_rect, width=1)
            calc_rect = parent.left + (parent.width / 2), parent.top + (
                    num * (parent.height / 3)), parent.width / 2, parent.height / 3
            value_rect = pg.draw.rect(self.subsurface, 'black', calc_rect, width=1)
            name = self.subsurface.subsurface(parent.left, parent.top + (num * (parent.height / 3)), parent.width / 2,
                                              parent.height / 3)
            value = self.subsurface.subsurface(parent.left + (parent.width / 2),
                                               parent.top + (num * (parent.height / 3)), parent.width / 2,
                                               parent.height / 3)
            if num == 0:
                text = 'r'
            elif num == 1:
                text = 'g'
            else:
                text = 'b'
            text = CenteredText(self.subsurface, name_rect, 20, text, self.font)
            self.blitlist.append(text)
            text = CenteredText(self.subsurface, value_rect, 20, str(self.color_circle.color[num]), font=self.font)
            self.textlist.append(text)
