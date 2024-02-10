import pygame

import GUIDisplay
import GUIObjects
import GUIUtils
import PCB
import assets

from assets import *

import LogicElements

pygame.display.init()
pygame.font.init()

main_window = GUIDisplay.Window(fps_cap=150)

bg_layer = GUIDisplay.Layer(main_window, (1920, 1080), (0, 0), Colours.black)
circuit_board = GUIObjects.Image(bg_layer, (0, 0), "assets/circuit_board_2.png")

side_bar = GUIDisplay.Layer(main_window, (480, 1080), (0, 0), MacColoursDark.side_bar_inactive_colour)
test_button2 = GUIUtils.RoundedLabelledButton(side_bar, (128, 64), (128, 720), GUIUtils.Button.get_id(), 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Test")

main_board = PCB.Motherboard(8, 8, 13, 32)
first_sub = PCB.Daughterboard(main_window, main_board, (32, 20), (688, 128))
buffer1 = PCB.Component(first_sub, (2, 2), (3, 3), assets.MacColours.yellow, LogicElements.Buffer())
buffer2 = PCB.Component(first_sub, (2, 2), (3, 6), assets.MacColours.yellow, LogicElements.Buffer())

or1 = PCB.Component(first_sub, (2, 2), (8, 3), assets.MacColours.yellow, LogicElements.ORGate(2))
and1 = PCB.Component(first_sub, (2, 2), (8, 6), assets.MacColours.yellow, LogicElements.ANDGate(2, False))

buffer1.logic_element.connect(or1.logic_element, 0)
buffer1.logic_element.connect(and1.logic_element, 0)

buffer2.logic_element.connect(or1.logic_element, 1)
buffer2.logic_element.connect(and1.logic_element, 1)


def button_action(button_id):
    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:
            for component in daughterboard.components:
                if component.button_id == button_id:
                    if not (isinstance(component.logic_element, LogicElements.Pin) and component.logic_element.is_built_in):
                        component.logic_element.is_inverted = not component.logic_element.is_inverted
            daughterboard.update_textures()


def loop_action():
    LogicElements.Gate.in_tick()
    LogicElements.Gate.out_tick()


def event_action(events, mouse_pos):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                for daughterboard in reversed(main_board.daughterboards):
                    if daughterboard.is_visible:
                        for component in reversed(daughterboard.components):
                            if component.mouse_check(mouse_pos):
                                if not(isinstance(component.logic_element, LogicElements.Pin) and component.logic_element.is_built_in):
                                    component.delete()
