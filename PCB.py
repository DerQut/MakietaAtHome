import pygame

import GUIDisplay
import GUIObjects
import GUIUtils
import LogicElements
import assets


class Motherboard:

    def __init__(self, in_count, out_count, com_count, slot_resolution):

        self.in_count = in_count
        self.out_count = out_count
        self.com_count = com_count

        self.ins = []
        self.outs = []
        self.coms = []

        self.slot_resolution = slot_resolution

        while len(self.ins) < self.in_count:
            self.ins.append(LogicElements.Pin(True, False, True))

        while len(self.outs) < self.out_count:
            self.outs.append(LogicElements.Pin(True, True, False))

        while len(self.coms) < self.com_count:
            self.coms.append(LogicElements.Pin(True, True, True))

        self.daughterboards = []


class Daughterboard(GUIDisplay.Layer):

    def __init__(self, window, motherboard, size, position, bg_colour=assets.MacColoursDark.green, is_visible=True):
        super().__init__(window, (size[0]*motherboard.slot_resolution, size[1]*motherboard.slot_resolution), position, bg_colour, is_visible)

        self.motherboard = motherboard

        self.components = []

        i = 0
        while i < self.motherboard.in_count:
            new = Component(self, (1, 1), (1, 1+i), assets.MacColours.yellow, self.motherboard.ins[i])
            i = i + 1

        i = 0
        while i < self.motherboard.out_count:
            new = Component(self, (1, 1), (1, size[1]-2-i), assets.MacColours.yellow, self.motherboard.outs[self.motherboard.out_count-i-1])
            i = i + 1

        self.motherboard.daughterboards.append(self)

    def update_textures(self):
        for component in self.components:
            component.sprite_file = component.logic_element.textures[component.logic_element.is_inverted]
            pixel_size = 0.85 * min(component.size[0], component.size[1])
            component.texture = pygame.transform.scale(component.sprite_file, (pixel_size, pixel_size))


class Component(GUIUtils.Button):

    def __init__(self, daughterboard, size, position, fill_colour, logic_element, is_visible=True):
        super().__init__(daughterboard, (size[0]*daughterboard.motherboard.slot_resolution, size[1]*daughterboard.motherboard.slot_resolution), (position[0]*daughterboard.motherboard.slot_resolution, position[1]*daughterboard.motherboard.slot_resolution), button_id=GUIUtils.Button.get_id(), fill_colour=fill_colour, is_visible=is_visible)

        self.logic_element = logic_element

        self.logic_element.master = self

        self.on_colour = fill_colour
        self.off_colour = (self.on_colour[0] * 0.7, self.on_colour[1] * 0.7, self.on_colour[2] * 0.7)

        self.fill_colour = self.on_colour

        self.sprite_file = self.logic_element.textures[self.logic_element.is_inverted]

        self.daughterboard = daughterboard
        self.daughterboard.components.append(self)

        self.inlets = []
        self.outlets = []

        pixel_size = 0.85*min(self.size[0], self.size[1])
        self.texture = pygame.transform.scale(self.sprite_file, (pixel_size, pixel_size))

        if not (isinstance(self.logic_element, LogicElements.Pin) and not self.logic_element.has_input):
            i = self.size[1]/(self.logic_element.max_inputs+1)
            while len(self.inlets) < self.logic_element.max_inputs:
                new = Inlet(self, (self.position[0]-0.25*self.daughterboard.motherboard.slot_resolution, self.position[1]+(len(self.inlets)+1)*i-0.125*self.daughterboard.motherboard.slot_resolution), len(self.inlets), (0.25*self.daughterboard.motherboard.slot_resolution, 0.25*self.daughterboard.motherboard.slot_resolution))

    def draw(self):
        self.fill_colour = self.on_colour
        if not self.logic_element.external_state:
            self.fill_colour = self.off_colour
        pygame.draw.rect(self.daughterboard.surface, self.fill_colour, self.rect)

        self.layer.surface.blit(self.texture, (self.position[0]+0.5*(self.size[0]-self.texture.get_width()), self.position[1]+0.5*(self.size[1]-self.texture.get_height())))

    def delete(self):
        self.logic_element.delete()
        self.daughterboard.components.remove(self)
        self.daughterboard.gui_objects.remove(self)


class Inlet(GUIUtils.Button):

    def __init__(self, component, position, inlet_id, size=(16, 16)):
        super().__init__(component.daughterboard, size, position, GUIUtils.Button.get_id(), fill_colour=component.fill_colour, is_visible=True)

        self.component = component
        self.daughterboard = component.daughterboard
        self.inlet_id = inlet_id

        self.component.inlets.append(self)


class Outlet(GUIUtils.Button):
    ...
