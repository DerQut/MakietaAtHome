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

    def draw(self):

        if self.is_visible:

            pygame.draw.rect(self.layer.surface, self.fill_colour, self.rect, self.width)

    def update(self):
        self.rect = pygame.rect.Rect(self.position, self.size)

    def move_by(self, x=0, y=0):

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
