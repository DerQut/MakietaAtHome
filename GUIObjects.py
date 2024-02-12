import numpy

import pygame
import assets


class Rect:

    all_rects = []

    def __init__(self, layer, size, position, fill_colour=assets.Colours.black, width=0, is_visible=True):

        self.layer = layer
        self.size = size
        self.position = position
        self.fill_colour = fill_colour
        self.is_visible = is_visible
        self.width = width

        self.rect = pygame.rect.Rect(self.position, self.size)

        self.layer.gui_objects.append(self)

        Rect.all_rects.append(self)

        self.can_move = True

    def draw(self):

        if self.is_visible:

            pygame.draw.rect(self.layer.surface, self.fill_colour, self.rect, self.width)

    def update(self):
        self.rect = pygame.rect.Rect(self.position, self.size)

    def move_by(self, x=0, y=0):

        if self.can_move:
            self.position = (self.position[0]+x, self.position[1]+y)
            self.update()

    def mouse_check(self, mouse_pos):
        if self.layer.mouse_check(mouse_pos):
            if self.layer.position[0]+self.position[0] <= mouse_pos[0] <= self.layer.position[0]+self.position[0]+self.size[0]:
                if self.layer.position[1]+self.position[1] <= mouse_pos[1] <= self.layer.position[1]+self.position[1]+self.size[1]:
                    return True
        return False


class Ellipse(Rect):

    def draw(self):

        if self.is_visible:
            pygame.draw.ellipse(self.layer.surface, self.fill_colour, self.rect, self.width)


class Text:

    def __init__(self, layer, font_size, position, font_colour, font_file, text, is_visible=True):

        self.layer = layer
        self.position = position

        self.font_colour = font_colour

        self.font_size = font_size
        self.font_file = font_file
        self.text = text
        self.font = pygame.font.Font(self.font_file, self.font_size)
        self.texture = self.font.render(self.text, True, self.font_colour)

        self.is_visible = True

        self.layer.gui_objects.append(self)

    def draw(self):
        if self.is_visible:
            self.layer.surface.blit(self.texture, self.position)

    def update(self):
        self.font = pygame.font.Font(self.font_file, self.font_size)
        self.texture = self.font.render(self.text, True, self.font_colour)


class Image:

    def __init__(self, layer, position, filename, is_visible=True):

        self.filename = filename
        self.texture = pygame.image.load(filename).convert_alpha()
        self.position = position

        self.layer = layer
        self.is_visible = is_visible

        self.can_move = True

        self.size = (self.texture.get_width(), self.texture.get_height())

        self.layer.gui_objects.append(self)

    def draw(self):
        if self.is_visible:
            self.layer.surface.blit(self.texture, self.position)

    def move_by(self, x=0, y=0):
        if self.can_move:
            self.position = (self.position[0]+x, self.position[1]+y)
