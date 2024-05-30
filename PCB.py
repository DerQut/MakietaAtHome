import pygame

import GUIDisplay
import GUIUtils
import LogicElements
import assets
import parser

SIZE = 0
COLOUR = 1
INVERSION = 3


class Motherboard:

    def __init__(self, in_count: int, out_count: int, com_count: int, slot_resolution: int):

        self.in_count = in_count
        self.out_count = out_count
        self.com_count = com_count

        self.ins = []
        self.outs = []
        self.coms = []

        self.slot_resolution = slot_resolution
        self.tick_tempo = 15
        self.current_tick = 0

        self.programming = []

        self.saved_outs = []

        self.next_db_id = 0

        while len(self.ins) < self.in_count:
            self.ins.append(LogicElements.Pin(True, False, True))

        while len(self.outs) < self.out_count:
            self.outs.append(LogicElements.Pin(True, True, False))

        while len(self.coms) < self.com_count:
            self.coms.append(LogicElements.Pin(True, True, True))

        self.daughterboards = []

    def update_pin_colour(self, logic_element: LogicElements.Pin, colour):
        for daughterboard in self.daughterboards:
            for component in daughterboard.components:
                if component.logic_element == logic_element:
                    component.change_colour(colour)

    def program(self, sequence):
        self.programming = sequence
        self.current_tick = self.tick_tempo * len(self.programming)

    def give_db_id(self):
        self.next_db_id = self.next_db_id + 1
        return self.next_db_id - 1

    def send_programming(self):
        if self.current_tick >= self.tick_tempo * len(self.programming):
            return 1
        index = 0
        out_cache = []
        if self.current_tick:
            index = int(self.current_tick/self.tick_tempo)
        i = 0
        while i < self.in_count:
            self.ins[i].internal_state = self.programming[index][-i-1]
            i = i + 1

        for out in self.outs:
            out_cache.append(out.internal_state)

        if self.current_tick >= 2:
            self.saved_outs.append(out_cache)

        self.current_tick = self.current_tick + 1
        return 0


class Daughterboard(GUIDisplay.Sublayer):

    def __init__(self, master: GUIDisplay.Layer, motherboard: Motherboard, size: tuple, position: tuple, bg_colour=assets.MacColoursDark.side_bar_inactive_colour, is_visible=True):
        super().__init__(master, (size[0]*motherboard.slot_resolution, size[1]*motherboard.slot_resolution), position, bg_colour, is_visible)

        self.motherboard = motherboard

        self.components = []
        self.paddings = []

        self.db_id = motherboard.give_db_id()

        i = 0
        while i < self.motherboard.in_count:
            colour = assets.Colours.white
            if len(self.motherboard.ins[i].masters):
                colour = self.motherboard.ins[i].masters[0].on_colour
            new = Component(self, (1, 1), (1, 1+i), colour, self.motherboard.ins[i])
            i = i + 1

        i = 0
        while i < self.motherboard.out_count:
            colour = assets.MacColoursDark.blue
            if len(self.motherboard.outs[self.motherboard.out_count-i-1].masters):
                colour = self.motherboard.outs[self.motherboard.out_count-i-1].masters[0].on_colour
            new = Component(self, (1, 1), (1, size[1]-2-i), colour, self.motherboard.outs[self.motherboard.out_count-i-1])
            i = i + 1

        i = 0
        while i < self.motherboard.com_count:
            colour = assets.Colours.white
            if len(self.motherboard.coms[i].masters):
                colour = self.motherboard.coms[i].masters[0].on_colour
            new = Component(self, (1, 1), (size[0]-2, 0.5*(size[1]-self.motherboard.com_count)+i), colour, self.motherboard.coms[i])
            i = i + 1

        self.motherboard.daughterboards.append(self)

    def update_textures(self):
        for component in self.components:
            component.sprite_file = component.logic_element.textures[component.logic_element.is_inverted]
            pixel_size = (0.85 * component.size[0], 0.85 * component.size[1])
            if not isinstance(component.logic_element, LogicElements.FlipFlop):
                component.texture = pygame.transform.scale(component.sprite_file, (min(pixel_size[0], pixel_size[1]), min(pixel_size[0], pixel_size[1])))
            else:
                component.texture = pygame.transform.scale(component.sprite_file, (pixel_size[0], pixel_size[1]))

    def delete(self):

        for component in self.components:
            if isinstance(component, LogicElements.Pin):
                continue

            for out in self.motherboard.outs:
                if component.logic_element in out.inputs:
                    out.disconnect(0)
                    out.internal_state = False
            for com in self.motherboard.coms:
                if component in com.inputs:
                    com.disconnect(0)
                    com.internal_state = False

            component.delete()

        for padding in self.paddings:
            self.paddings.remove(padding)
            self.master.gui_objects.remove(padding)

        self.motherboard.daughterboards.remove(self)
        self.window.all_layers.remove(self)
        self.master.sublayers.remove(self)
        self.master.gui_objects.remove(self)

        for daughterboard in self.motherboard.daughterboards:
            if daughterboard.db_id > self.db_id:
                daughterboard.position = (daughterboard.position[0], daughterboard.position[1] - self.size[1])
                for padding in daughterboard.paddings:
                    padding.position = (padding.position[0], padding.position[1] - self.size[1])



class Component(GUIUtils.Button):

    def __init__(self, daughterboard: Daughterboard, size: tuple, position: tuple, fill_colour: tuple, logic_element: LogicElements.Gate, is_visible=True):
        super().__init__(daughterboard, (size[0]*daughterboard.motherboard.slot_resolution, size[1]*daughterboard.motherboard.slot_resolution), (position[0]*daughterboard.motherboard.slot_resolution, position[1]*daughterboard.motherboard.slot_resolution), button_id=GUIUtils.Button.get_id(), fill_colour=fill_colour, is_visible=is_visible)

        self.logic_element = logic_element

        self.logic_element.masters.append(self)

        self.on_colour = fill_colour
        self.off_colour = (self.on_colour[0] * 0.5, self.on_colour[1] * 0.5, self.on_colour[2] * 0.5)

        self.fill_colour = self.on_colour

        self.sprite_file = self.logic_element.textures[self.logic_element.is_inverted]

        self.daughterboard = daughterboard
        self.daughterboard.components.append(self)

        self.inlets = []
        self.outlets = []

        pixel_size = (0.85*self.size[0], 0.85*self.size[1])
        if not isinstance(self.logic_element, LogicElements.FlipFlop):
            self.texture = pygame.transform.scale(self.sprite_file, (min(pixel_size[0], pixel_size[1]), min(pixel_size[0], pixel_size[1])))
        else:
            self.texture = pygame.transform.scale(self.sprite_file, (pixel_size[0], pixel_size[1]))

        if not (isinstance(self.logic_element, LogicElements.Pin) and not self.logic_element.has_input):
            i = self.size[1]/(self.logic_element.max_inputs+1)
            while len(self.inlets) < self.logic_element.max_inputs:
                new = Inlet(self, (self.position[0]-0.25*self.daughterboard.motherboard.slot_resolution, self.position[1]+(len(self.inlets)+1)*i-0.125*self.daughterboard.motherboard.slot_resolution), len(self.inlets), (0.25*self.daughterboard.motherboard.slot_resolution, 0.25*self.daughterboard.motherboard.slot_resolution))

        if not (isinstance(self.logic_element, LogicElements.Pin) and not self.logic_element.has_output):
            new = Outlet(self, (self.position[0]+self.size[0], self.position[1]+0.5*(self.size[1]-0.5*self.daughterboard.motherboard.slot_resolution)), 1, (self.daughterboard.motherboard.slot_resolution*0.25, self.daughterboard.motherboard.slot_resolution*0.5))

    def draw(self):
        if not self.is_visible:
            return 1

        self.fill_colour = self.on_colour
        if not self.logic_element.external_state:
            self.fill_colour = self.off_colour
        pygame.draw.rect(self.daughterboard.surface, self.fill_colour, self.rect)

        border_thickness = 0.5*(self.size[0]-self.texture.get_width())

        missing_height = 0.5*(self.size[1] - self.texture.get_height())
        missing_width = self.texture.get_width()

        temp_rect = pygame.rect.Rect(self.position[0]+border_thickness, self.position[1]+border_thickness, missing_width, missing_height-border_thickness)

        pygame.draw.rect(self.daughterboard.surface, assets.Colours.black, temp_rect)

        temp_rect = temp_rect.move(0, temp_rect.height + self.texture.get_height())

        pygame.draw.rect(self.daughterboard.surface, assets.Colours.black, temp_rect)

        self.layer.surface.blit(self.texture, (self.position[0]+border_thickness, self.position[1]+0.5*(self.size[1]-self.texture.get_height())))

    def delete(self):
        if (not isinstance(self.logic_element, LogicElements.Pin)) and self.logic_element not in self.daughterboard.motherboard.coms:
            self.logic_element.delete()
        else:
            self.logic_element.disconnect(0)

        self.daughterboard.components.remove(self)
        self.daughterboard.gui_objects.remove(self)

        for inlet in self.inlets:
            self.daughterboard.gui_objects.remove(inlet)

        for outlet in self.outlets:
            self.daughterboard.gui_objects.remove(outlet)

    def update_io_colours(self):

        for inlet in self.inlets:
            if self.logic_element.inputs[inlet.inlet_id] is None:
                inlet.fill_colour = self.off_colour
            else:
                for master in self.logic_element.inputs[inlet.inlet_id].masters:
                    inlet.fill_colour = master.fill_colour
        for outlet in self.outlets:
            outlet.fill_colour = self.fill_colour

    def change_colour(self, new_colour):

        self.on_colour = new_colour
        self.off_colour = (self.on_colour[0] * 0.5, self.on_colour[1] * 0.5, self.on_colour[2] * 0.5)

        for component in self.daughterboard.components:
            if isinstance(component.logic_element, LogicElements.HiddenBuffer) and component.logic_element.inputs[0].masters[0] == self:
                component.on_colour = new_colour
                component.off_colour = (self.on_colour[0] * 0.5, self.on_colour[1] * 0.5, self.on_colour[2] * 0.5)
                component.update_io_colours()

        self.update_io_colours()

    def change_parameter(self, parameter):

        if parameter == COLOUR:
            new_colour = parser.get_colour(self.on_colour)
            self.change_colour(new_colour)
            if isinstance(self.logic_element, LogicElements.Pin) and self.logic_element.is_built_in:
                self.daughterboard.motherboard.update_pin_colour(self.logic_element, new_colour)

        elif parameter == INVERSION:
            self.logic_element.is_inverted = not self.logic_element.is_inverted
            if isinstance(self.logic_element, LogicElements.FlipFlop):
                self.logic_element.is_rising_edge = not self.logic_element.is_rising_edge

        elif parameter == SIZE:
            ...


class Inlet(GUIUtils.Button):

    def __init__(self, component: Component, position: tuple, inlet_id: int, size=(16, 16)):
        super().__init__(component.daughterboard, size, position, GUIUtils.Button.get_id(), fill_colour=component.fill_colour, is_visible=True)

        self.component = component
        self.daughterboard = component.daughterboard
        self.inlet_id = inlet_id

        self.component.inlets.append(self)

    def draw(self):
        super().draw()

        if self.inlet_id == 2 and isinstance(self.component.logic_element, LogicElements.FlipFlop):
            point1 = (self.position[0]+2*self.size[0], self.position[1]-0.25*self.daughterboard.motherboard.slot_resolution)
            point2 = (self.position[0]+2*self.size[0]+0.33*self.daughterboard.motherboard.slot_resolution, self.position[1]+0.5*self.size[1])
            point3 = (self.position[0]+2*self.size[0], self.position[1]+0.25*self.daughterboard.motherboard.slot_resolution+self.size[1])
            pygame.draw.polygon(self.daughterboard.surface, self.fill_colour, (point1, point2, point3), width=5)

            if not self.component.logic_element.is_rising_edge:

                pygame.draw.circle(self.component.daughterboard.surface, self.fill_colour, (self.position[0]+0.5*self.size[0]-0.5*self.daughterboard.motherboard.slot_resolution+10, self.position[1]+0.5*self.size[1]), 0.4*self.daughterboard.motherboard.slot_resolution, width=5)


class Outlet(GUIUtils.Button):

    def __init__(self, component: Component, position: tuple, outlet_id: int, size=(32, 32)):
        super().__init__(component.daughterboard, size, position, GUIUtils.Button.get_id(), fill_colour=component.fill_colour, is_visible=True)

        self.component = component
        self.outlet_id = outlet_id

        self.component.outlets.append(self)
