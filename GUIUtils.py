import pygame

import GUIObjects
import assets


class Button(GUIObjects.Rect):

    __free_id = 1024

    def __init__(self, layer, size, position, button_id, fill_colour=assets.MacColoursDark.blue, is_visible=True):
        super().__init__(layer, size, position, fill_colour, width=0, is_visible=is_visible)

        self.is_clicked = False
        self.button_id = button_id

    def draw(self):
        if self.is_visible:
            colour = self.fill_colour
            if self.is_clicked:
                colour = (colour[0]*0.8, colour[1]*0.8, colour[2]*0.8)

            pygame.draw.rect(self.layer.surface, colour, self.rect, self.width)

    @classmethod
    def get_id(cls):
        cls.__free_id = cls.__free_id + 1
        return cls.__free_id - 1


class LabelledButton(Button):

    def __init__(self, layer, size, position, button_id, font_size, font_colour, font_file, text, fill_colour=assets.MacColoursDark.blue, is_visible=True):
        super().__init__(layer, size, position, button_id, fill_colour, is_visible)

        self.label = GUIObjects.Text(self.layer, font_size, position, font_colour, font_file, text, is_visible)
        self.center_text()

    def center_text(self):
        self.label.position = (self.position[0] + 0.5 * (self.size[0] - self.label.texture.get_width()), self.position[1] + 0.5 * (self.size[1] - self.label.texture.get_height()))

    def change_label(self, new_label):
        self.label.text = new_label
        self.label.update()
        self.center_text()


class RoundedLabelledButton(LabelledButton):

    def __init__(self, layer, size, position, button_id, font_size, font_colour, font_file, text, fill_colour=assets.MacColoursDark.blue, corner_radius=7, border_radius=1, is_visible=True):
        super().__init__(layer, size, position, button_id, font_size, font_colour, font_file, text, fill_colour, is_visible)

        self.corner_radius = corner_radius
        self.border_radius = border_radius

    def draw(self):
        border_colour = (self.fill_colour[0]*0.8, self.fill_colour[1]*0.8, self.fill_colour[2]*0.8)
        colour = self.fill_colour
        if self.is_clicked:
            colour = border_colour

        center_rect = pygame.rect.Rect(self.position[0]+self.corner_radius, self.position[1]+self.corner_radius, self.size[0]-2*self.corner_radius, self.size[1]-2*self.corner_radius)

        pygame.draw.rect(self.layer.surface, border_colour, pygame.rect.Rect(center_rect.left, center_rect.top-self.border_radius, center_rect.width, self.border_radius))

        pygame.draw.circle(self.layer.surface, colour, (self.position[0]+self.corner_radius, self.position[1]+self.corner_radius), self.corner_radius)
        pygame.draw.circle(self.layer.surface, colour, (self.position[0] + self.corner_radius + center_rect.width, self.position[1] + self.corner_radius), self.corner_radius)
        pygame.draw.circle(self.layer.surface, colour, (self.position[0] + self.corner_radius + center_rect.width, self.position[1] + self.corner_radius + center_rect.height), self.corner_radius)
        pygame.draw.circle(self.layer.surface, colour, (self.position[0] + self.corner_radius, self.position[1] + self.corner_radius + center_rect.height), self.corner_radius)

        pygame.draw.rect(self.layer.surface, colour, pygame.rect.Rect(self.position[0], center_rect.top, self.corner_radius, center_rect.height))
        pygame.draw.rect(self.layer.surface, colour, pygame.rect.Rect(center_rect.right, center_rect.top, self.corner_radius, center_rect.height))
        pygame.draw.rect(self.layer.surface, colour, pygame.rect.Rect(self.position[0]+self.corner_radius, self.position[1], center_rect.width, self.corner_radius))
        pygame.draw.rect(self.layer.surface, colour, pygame.rect.Rect(self.position[0]+self.corner_radius, center_rect.bottom, center_rect.width, self.corner_radius))

        pygame.draw.rect(self.layer.surface, colour, center_rect)
