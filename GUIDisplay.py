import threading

import pygame
from pygame.locals import DOUBLEBUF, FULLSCREEN

import program
import assets

import GUIUtils


class Window:

    def __init__(self, resolution=(1920, 1080), bg_colour=assets.Colours.black, fps_cap=0, flags=DOUBLEBUF | FULLSCREEN):

        self.resolution = resolution
        self.fps_cap = fps_cap
        self.flags = flags

        self.bg_colour = bg_colour

        self.all_layers = []

        self.screen = pygame.display.set_mode(self.resolution, self.flags)
        self.main_layer = pygame.surface.Surface((1920*2, 1080*2))

        self.vertical_scale_factor = 1
        self.horizontal_scale_factor = 1

        self.is_running = True

    def pre_draw(self):

        self.screen.fill(self.bg_colour)
        self.main_layer.fill(self.bg_colour)

        for layer in self.all_layers:
            layer.pre_draw()

    def draw(self):
        for layer in self.all_layers:
            layer.draw()

        self.vertical_scale_factor = self.screen.get_height() / 1080
        rescaled_layer = pygame.transform.smoothscale_by(self.main_layer, self.vertical_scale_factor)
        self.screen.blit(rescaled_layer, (0, 0))

    def run(self):

        self.is_running = True
        clock = pygame.time.Clock()

        thread = threading.Thread(target=program.thread_action, daemon=True)
        thread.start()

        while self.is_running:

            self.pre_draw()

            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            rescaled_mouse_pos = (mouse_pos[0]/self.vertical_scale_factor, mouse_pos[1]/self.vertical_scale_factor)

            program.loop_action(rescaled_mouse_pos)

            for event in events:
                if event.type == pygame.WINDOWCLOSE:
                    self.is_running = False

                elif event.type == pygame.MOUSEWHEEL:
                    for layer in self.all_layers:
                        if isinstance(layer, ScrollingLayer):
                            if layer.mouse_check(rescaled_mouse_pos):
                                layer.scroll(event.x, event.y)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for layer in reversed(self.all_layers):
                            if layer.mouse_check(rescaled_mouse_pos) and layer.is_visible:
                                for gui_object in reversed(layer.gui_objects):
                                    if isinstance(gui_object, GUIUtils.Button):
                                        if gui_object.mouse_check(rescaled_mouse_pos):
                                            gui_object.is_clicked = True
                                            program.button_action(gui_object.button_id)
                                            break
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for layer in self.all_layers:
                            for gui_object in layer.gui_objects:
                                if isinstance(gui_object, GUIUtils.Button):
                                    gui_object.is_clicked = False

            if program.event_action(events, rescaled_mouse_pos) == pygame.WINDOWCLOSE:
                self.is_running = False

            self.draw()
            pygame.display.flip()
            clock.tick(self.fps_cap)


class Layer:

    all_layers = []

    def __init__(self, window: Window, size: tuple, position: tuple, bg_colour=assets.Colours.white, is_visible=True):

        self.window = window
        self.size = size
        self.position = position
        self.bg_colour = bg_colour
        self.is_visible = is_visible

        self.gui_objects = []

        self.surface = pygame.Surface(self.size)

        self.window.all_layers.append(self)

        self.sublayers = []

    def pre_draw(self):

        if self.is_visible:
            self.surface.fill(self.bg_colour)

            for gui_object in self.gui_objects:
                if gui_object.position[1] + gui_object.size[1] > 0:
                    gui_object.draw()

    def draw(self):
        self.window.main_layer.blit(self.surface, self.position)

    def move_by(self, x=0, y=0):
        self.position = (self.position[0]+x, self.position[1]+y)

    def mouse_check(self, mouse_pos):
        if self.position[0] <= mouse_pos[0] <= self.position[0]+self.size[0]:
            if self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]:
                return True
        return False

    def clear(self):
        self.gui_objects.clear()


class ScrollingLayer(Layer):

    def __init__(self, window: Window, size: tuple, position: tuple, bg_colour=assets.Colours.white, y_scroll_speed=30, x_scroll_speed=20, is_visible=True):
        super().__init__(window, size, position, bg_colour, is_visible)

        self.y_scroll_speed = y_scroll_speed
        self.x_scroll_speed = x_scroll_speed

    def scroll(self, x_direction, y_direction):

        can_move_up = 0
        can_move_down = 0

        can_move_left = 0
        can_move_right = 0

        for gui_object in self.gui_objects:
            if not gui_object.can_move:
                continue
            if gui_object.position[1] < 0:
                can_move_down = min(abs(gui_object.position[1]), self.y_scroll_speed)

            if gui_object.position[1]+gui_object.size[1]-self.size[1] > 0:
                can_move_up = min(abs(gui_object.position[1]+gui_object.size[1]-self.size[1]), self.y_scroll_speed)

            if gui_object.position[0] <= 0:
                can_move_right = min(abs(gui_object.position[0]), self.x_scroll_speed)

            if gui_object.position[0]+gui_object.size[0] - self.size[0] > 0:
                can_move_left = min(abs(gui_object.position[0]+gui_object.size[0]-self.size[0]), self.x_scroll_speed)

        if can_move_down and y_direction == 1:
            for gui_object in self.gui_objects:
                gui_object.move_by(y=can_move_down)

        elif can_move_up and y_direction == -1:
            for gui_object in self.gui_objects:
                gui_object.move_by(y=-can_move_up)

        if can_move_right and x_direction == -1:
            for gui_object in self.gui_objects:
                gui_object.move_by(can_move_right)

        elif can_move_left and x_direction == 1:
            for gui_object in self.gui_objects:
                gui_object.move_by(-can_move_left)


class Sublayer(Layer):

    def __init__(self, master: Layer, size: tuple, position: tuple, bg_colour=assets.Colours.white, is_visible=True):
        super().__init__(master.window, size, position, bg_colour, is_visible)

        self.can_move = True

        self.master = master
        master.sublayers.append(self)
        master.gui_objects.append(self)
