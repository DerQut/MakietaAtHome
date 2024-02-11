import pygame

import GUIDisplay
import GUIObjects
import GUIUtils
import PCB
import assets
import parser

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


selected_output = None
current_tool = PCB.COLOUR


def get_not_db(is_visible=False):

    daughterboard = PCB.Daughterboard(main_window, main_board, (24, 21), (688, 128), is_visible=is_visible)

    i = 0
    while i < 3:
        new = PCB.Component(daughterboard, (2, 2), (6, 4 + i*2), MacColours.yellow, LogicElements.Buffer(True))
        new = PCB.Component(daughterboard, (2, 2), (6, 11 + i * 2), MacColours.yellow, LogicElements.Buffer(True))
        i = i + 1

    i = 0
    while i < 4:
        new = PCB.Component(daughterboard, (2, 2), (16, 1+i*2), MacColours.yellow, LogicElements.ORGate(2, True))
        new = PCB.Component(daughterboard, (2, 2), (16, 12 + i * 2), MacColours.yellow, LogicElements.ORGate(2, True))
        i = i + 1


def get_nand_db(is_visible=False):
    daughterboard = PCB.Daughterboard(main_window, main_board, (24, 21), (688, 128), is_visible=is_visible)

    i = 0
    while i < 2:
        new = PCB.Component(daughterboard, (2, 4), (6, 1+i*4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 1 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        i = i + 1


get_nand_db()
get_not_db(True)

def button_action(button_id):

    global selected_output

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:
            for component in daughterboard.components:

                if component.button_id == button_id and not isinstance(component.logic_element, LogicElements.Pin):
                    component.change_parameter(PCB.INVERSION)

                for inlet in component.inlets:
                    if inlet.button_id == button_id:
                        print(inlet.inlet_id)
                        component.logic_element.disconnect(inlet.inlet_id)
                        component.logic_element.inputs[inlet.inlet_id] = selected_output
                        selected_output = None

                for outlet in component.outlets:
                    if outlet.button_id == button_id:
                        selected_output = component.logic_element

            daughterboard.update_textures()
            break


def loop_action(mouse_pos):

    LogicElements.Gate.in_tick()
    LogicElements.Gate.out_tick()

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:

            for component in daughterboard.components:
                component.update_io_colours()

                if component.logic_element == selected_output:
                    pygame.draw.line(main_window.screen, selected_output.master.fill_colour, mouse_pos, (selected_output.master.outlets[0].position[0] + daughterboard.position[0] + 0.5*selected_output.master.outlets[0].size[0], selected_output.master.outlets[0].position[1] + daughterboard.position[1] + 0.5*selected_output.master.outlets[0].size[1]), 3)

                for inlet in component.inlets:
                    if component.logic_element.inputs[inlet.inlet_id] is not None:
                        pygame.draw.line(main_window.screen, component.logic_element.inputs[inlet.inlet_id].master.fill_colour, (inlet.position[0]+daughterboard.position[0]+0.5*inlet.size[0], inlet.position[1]+daughterboard.position[1]+0.5*inlet.size[1]), (component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[0] + daughterboard.position[0] + 0.5*component.logic_element.inputs[inlet.inlet_id].master.outlets[0].size[0], component.logic_element.inputs[inlet.inlet_id].master.outlets[0].position[1] + daughterboard.position[1] + 0.5*component.logic_element.inputs[inlet.inlet_id].master.outlets[0].size[1]), width=3)
            break


def event_action(events, mouse_pos):
    global selected_output

    for event in events:

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                for daughterboard in reversed(main_board.daughterboards):
                    if daughterboard.is_visible:
                        for component in reversed(daughterboard.components):
                            if component.mouse_check(mouse_pos):
                                component.change_parameter(current_tool)
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_output = None
