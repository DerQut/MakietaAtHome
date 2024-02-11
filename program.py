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
buffer1 = PCB.Component(first_sub, (2, 2), (3, 5), assets.MacColours.yellow, LogicElements.Buffer(False))
buffer2 = PCB.Component(first_sub, (2, 2), (3, 10), assets.MacColours.yellow, LogicElements.Buffer(False))

nand1 = PCB.Component(first_sub, (2, 4), (7, 5), assets.MacColours.yellow, LogicElements.ANDGate(4, True))
nand2 = PCB.Component(first_sub, (2, 4), (7, 10), assets.MacColours.yellow, LogicElements.ANDGate(4, True))

buffer1.logic_element.connect(nand1.logic_element, 0)

def button_action(button_id):
    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:
            for component in daughterboard.components:
                if component.button_id == button_id:
                    if not (isinstance(component.logic_element, LogicElements.Pin) and component.logic_element.is_built_in):
                        component.logic_element.is_inverted = not component.logic_element.is_inverted

                for inlet in component.inlets:
                    if inlet.button_id == button_id:
                        component.logic_element.disconnect(inlet.inlet_id)

            daughterboard.update_textures()
            break


def loop_action():
    LogicElements.Gate.in_tick()
    LogicElements.Gate.out_tick()

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:

            for component in daughterboard.components:
                component.update_io_colours()
                if not (isinstance(component.logic_element, LogicElements.Pin) and not component.logic_element.has_input):
                    for inlet in component.inlets:
                        if component.logic_element.inputs[inlet.inlet_id] is not None:
                            #pygame.draw.line(main_window.screen, Colours.black, (inlet.position[0]+component.daughterboard.position[0], inlet.position[1]+component.daughterboard.position[1]), (component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[0]+component.daughterboard.position[0], component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[1]+component.daughterboard.position[1]), width=5)
                            pygame.draw.line(main_window.screen, component.logic_element.inputs[inlet.inlet_id].master.fill_colour, (inlet.position[0]+daughterboard.position[0]+0.5*inlet.size[0], inlet.position[1]+daughterboard.position[1]+0.5*inlet.size[1]), (component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[0] + daughterboard.position[0] + 0.5*component.logic_element.inputs[inlet.inlet_id].master.outlets[0].size[0], component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[1] + daughterboard.position[1] + 0.5*component.logic_element.inputs[inlet.inlet_id].master.outlets[0].size[1]), width=3)
            break


def event_action(events, mouse_pos):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                for daughterboard in reversed(main_board.daughterboards):
                    if daughterboard.is_visible:
                        for component in reversed(daughterboard.components):
                            if component.mouse_check(mouse_pos):
                                if not (isinstance(component.logic_element, LogicElements.Pin) and component.logic_element.is_built_in):
                                    component.delete()
