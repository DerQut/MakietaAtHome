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

main_window = GUIDisplay.Window(fps_cap=0)

bg_layer = GUIDisplay.ScrollingLayer(main_window, (1920-480, 1080), (480, 0), Colours.black, y_scroll_speed=45)
circuit_board = GUIObjects.Image(bg_layer, (0, 0), "assets/circuit_board_2.png")
circuit_board.can_move = False

side_bar = GUIDisplay.Layer(main_window, (480, 1080), (0, 0), MacColoursDark.side_bar_inactive_colour)
test_button2 = GUIUtils.RoundedLabelledButton(side_bar, (128, 64), (128, 720), 0, 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Test")

main_board = PCB.Motherboard(8, 8, 13, 40)


selected_output = None
current_tool = PCB.COLOUR


def get_not_db(is_visible=False):

    x_pos = 0.5*(bg_layer.size[0] - 24*main_board.slot_resolution) + bg_layer.position[0]
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (bg_layer.size[1] - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards) - 1].position[
                    1] + 22 * main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos - 2*main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos + 21*main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 21), (x_pos, y_pos), is_visible=is_visible)

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

    x_pos = 0.5 * (bg_layer.size[0] - 24 * main_board.slot_resolution) + bg_layer.position[0]
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (bg_layer.size[1] - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards)-1].position[1] + 22*main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos - 2*main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos + 21*main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 21), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 2:
        new = PCB.Component(daughterboard, (2, 4), (6, 1+i*4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 1 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        i = i + 1


def get_jk_db(is_visible=False):

    x_pos = 0.5 * (bg_layer.size[0] - 24 * main_board.slot_resolution) + bg_layer.position[0]
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (bg_layer.size[1] - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards) - 1].position[
                    1] + 22 * main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution),
                              (0, y_pos - 2 * main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution),
                              (0, y_pos + 21 * main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 21), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 2:
        new = PCB.Component(daughterboard, (2, 4), (6, 1 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (3, 4), (16, 1 + i * 4), MacColours.yellow, LogicElements.JKFlipFlop())
        new = PCB.Component(daughterboard, (3, 4), (16, 12 + i * 4), MacColours.yellow, LogicElements.JKFlipFlop())
        i = i + 1


def get_d_db(is_visible=False):

    x_pos = 0.5 * (bg_layer.size[0] - 24 * main_board.slot_resolution) + bg_layer.position[0]
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (bg_layer.size[1] - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards) - 1].position[
                    1] + 22 * main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution),
                              (0, y_pos - 2 * main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution),
                              (0, y_pos + 21 * main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 21), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 2:
        new = PCB.Component(daughterboard, (2, 4), (6, 1 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), MacColours.yellow, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (3, 4), (16, 1 + i * 4), MacColours.yellow, LogicElements.DFlipFlop())
        new = PCB.Component(daughterboard, (3, 4), (16, 12 + i * 4), MacColours.yellow, LogicElements.DFlipFlop())
        i = i + 1


def create(id):

    if id == 1:
        get_not_db(True)
    elif id == 2:
        get_nand_db(True)
    elif id == 3:
        get_jk_db(True)
    elif id == 4:
        get_d_db(True)


#get_not_db(True)
#get_nand_db(True)
get_jk_db(True)
get_d_db(True)


def button_action(button_id):

    global selected_output

    for layer in main_window.all_layers:
        for element in layer.gui_objects:
            if isinstance(element, GUIUtils.Button):
                if element.button_id == button_id:

                    if element.button_id == 0:

                        create(parser.get_value("Nowa makieta", "Wybierz szablon:\n1- NOT + NOR\n2- NAND\n3- NAND + JK\n4- NAND + D", 0))

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:
            for component in daughterboard.components:

                if component.button_id == button_id and not isinstance(component.logic_element, LogicElements.Pin):
                    component.change_parameter(PCB.INVERSION)

                for inlet in component.inlets:
                    if inlet.button_id == button_id:
                        if isinstance(selected_output, LogicElements.Gate):
                            for master in selected_output.masters:
                                if master.daughterboard == component.daughterboard:
                                    component.logic_element.inputs[inlet.inlet_id] = selected_output
                                    selected_output = None
                        else:
                            component.logic_element.disconnect(inlet.inlet_id)

                for outlet in component.outlets:
                    if outlet.button_id == button_id:
                        selected_output = component.logic_element

            daughterboard.update_textures()


def loop_action(mouse_pos):

    LogicElements.Gate.in_tick()
    LogicElements.Gate.out_tick()

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:

            for component in daughterboard.components:
                component.update_io_colours()

                if component.logic_element == selected_output:
                    for master in selected_output.masters:
                        if master.daughterboard.is_visible:
                            pygame.draw.line(main_window.screen, master.fill_colour, mouse_pos, (master.outlets[0].position[0] + daughterboard.position[0] + 0.5*master.outlets[0].size[0], master.outlets[0].position[1] + daughterboard.position[1] + 0.5*master.outlets[0].size[1]), 3)

                for inlet in component.inlets:
                    if component.logic_element.inputs[inlet.inlet_id] is not None:
                        for master in component.logic_element.inputs[inlet.inlet_id].masters:
                            if master.daughterboard == component.daughterboard and master.daughterboard.is_visible:
                                pygame.draw.line(main_window.screen, master.fill_colour, (inlet.position[0]+daughterboard.position[0]+0.5*inlet.size[0], inlet.position[1]+daughterboard.position[1]+0.5*inlet.size[1]), (master.outlets[0].position[0] + daughterboard.position[0] + 0.5*master.outlets[0].size[0], master.outlets[0].position[1] + daughterboard.position[1] + 0.5*master.outlets[0].size[1]), width=3)


def event_action(events, mouse_pos):
    global selected_output

    for event in events:

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if selected_output is not None:
                    selected_output = None
                    return -1
                for daughterboard in main_board.daughterboards:
                    if daughterboard.is_visible and daughterboard.mouse_check(mouse_pos):
                        for component in daughterboard.components:
                            if component.mouse_check(mouse_pos):
                                component.change_parameter(current_tool)
                                return 0
                        daughterboard.bg_colour = parser.get_colour(daughterboard.bg_colour)
                        return 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_output = None
            elif event.key == pygame.K_TAB:
                for daughterboard in main_board.daughterboards:
                    daughterboard.is_visible = not daughterboard.is_visible
