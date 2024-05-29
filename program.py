import pygame.transform
from pygame import DOUBLEBUF, RESIZABLE

import GUIDisplay
import GUIObjects
import GUIUtils
import PCB
import parser
import programator

import math

from assets import *

import LogicElements

pygame.display.init()
pygame.font.init()

main_window = GUIDisplay.Window(fps_cap=30, flags=DOUBLEBUF | RESIZABLE, resolution=(1280, 720))
pygame.display.set_icon(pygame.image.load("assets/logo.png").convert_alpha())
pygame.display.set_caption("Makieta@Home")
main_board = PCB.Motherboard(8, 8, 13, 40)

bg_layer = GUIDisplay.ScrollingLayer(main_window, (1920*2, 1080), (480, 0), Colours.black, y_scroll_speed=75, x_scroll_speed=0)
# circuit_board = GUIObjects.Image(bg_layer, (0, 0), "assets/circuit_board.png")
# circuit_board.texture = pygame.transform.scale2x(circuit_board.texture)
# circuit_board.can_move = False

side_bar = GUIDisplay.Layer(main_window, (480, 1080), (0, 0), MacColoursDark.side_bar_inactive_colour)

file_label = GUIObjects.Text(side_bar, 24, (20, 20), MacColoursDark.side_bar_colour, "assets/SFNSDisplay-Thin.otf", "Plik: _PRZEBIEG.txt")
file_reload = GUIUtils.RoundedLabelledButton(side_bar, (100, 36), (480-20-100, 20), 1, 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Odczyt")

speed_label = GUIObjects.Text(side_bar, 24, (20, 66), MacColoursDark.side_bar_colour, "assets/SFNSDisplay-Thin.otf", "Okres sygnału wejściowego:")
speed_change_button = GUIUtils.RoundedLabelledButton(side_bar, (100, 36), (480 - 20 - 100, 66), 2, 24, Colours.black, "assets/SFNSDisplay-Thin.otf", str(main_board.tick_tempo), fill_colour=Colours.white)

new_button = GUIUtils.RoundedLabelledButton(side_bar, (440, 64), (20, 1080-64-20-64-10), 0, 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Nowa makieta", fill_colour=MacColoursDark.side_bar_colour)
run_button = GUIUtils.RoundedLabelledButton(side_bar, (440, 64), (20, 1080-64-20), 3, 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Uruchom")

main_board.program(programator.complete_read("_PRZEBIEG.txt", main_board.out_count))

input_layer = GUIDisplay.ScrollingLayer(main_window, (440, 240), (20, 122+55), Colours.white, y_scroll_speed=75, x_scroll_speed=0)


input_layer_overlay = GUIDisplay.Layer(main_window, (440, 55), (20, 122), Colours.white)

id_label = GUIObjects.Text(input_layer_overlay, 24, (20, 10), Colours.black, "assets/SF-Mono-Light.otf", "id")
binary_label = GUIObjects.Text(input_layer_overlay, 24, (input_layer.size[0] - 140, 10), Colours.black, "assets/SF-Mono-Light.otf", "Binary")
decimal_label = GUIObjects.Text(input_layer_overlay, 24, (120, 10), Colours.black, "assets/SF-Mono-Light.otf", "Decimal")

underline = GUIObjects.Rect(input_layer_overlay, (420, 1), (10, 54), MacColoursDark.side_bar_colour)
vertical1 = GUIObjects.Rect(input_layer_overlay, (1, 45), (input_layer.size[0] - 140-10, 10), MacColoursDark.side_bar_colour)
vertical2 = GUIObjects.Rect(input_layer_overlay, (1, 45), (110, 10), MacColoursDark.side_bar_colour)


output_layer_overlay = GUIDisplay.Layer(main_window, (440, 55), (20, 122+55+input_layer.size[1]+20), Colours.white)
id_label_out = GUIObjects.Text(output_layer_overlay, 24, (20, 10), Colours.black, "assets/SF-Mono-Light.otf", "id")
vertical2_out = GUIObjects.Rect(output_layer_overlay, (1, 45), (110, 10), MacColoursDark.side_bar_colour)
underline_out = GUIObjects.Rect(output_layer_overlay, (420, 1), (10, 54), MacColoursDark.side_bar_colour)
graph_label = GUIObjects.Text(output_layer_overlay, 24, (120, 10), Colours.black, "assets/SF-Mono-Light.otf", "Graph")

output_layer = GUIDisplay.ScrollingLayer(main_window, (440, 902-(122+55+input_layer.size[1]+20+output_layer_overlay.size[1])), (20, 122+55+input_layer.size[1]+20+output_layer_overlay.size[1]), Colours.white, y_scroll_speed=75, x_scroll_speed=0)

selected_output = None
current_tool = PCB.COLOUR


def fill_input_layer():

    input_layer.clear()

    padding = GUIObjects.Rect(input_layer, (1, 10), (0, 0), Colours.white, is_visible=False)

    new1 = GUIObjects.Rect(input_layer, (1, 320), (input_layer.size[0] - 140 - 10, 0), MacColoursDark.side_bar_colour)
    new1.can_move = False
    new2 = GUIObjects.Rect(input_layer, (1, 320), (110, 0), MacColoursDark.side_bar_colour)
    new2.can_move = False

    y = 10
    i = 0
    for sequence in main_board.programming:
        new_label = ""
        x = input_layer.size[0] - 140
        for bit in sequence:
            new_label = new_label + str(int(bit))
        new = GUIObjects.Text(input_layer, 24, (x, y), Colours.black, "assets/SF-Mono-Light.otf", new_label)
        new = GUIObjects.Text(input_layer, 24, (20, y), Colours.black, "assets/SF-Mono-Light.otf", str(i))
        new = GUIObjects.Text(input_layer, 24, (120, y), Colours.black, "assets/SF-Mono-Light.otf", str(int(new_label, 2)))
        y = y + 33
        i = i + 1

    padding = GUIObjects.Rect(input_layer, (1, 10), (0, y), Colours.white, is_visible=False)


def pre_fill_output_layer():

    output_layer.clear()

    padding = GUIObjects.Rect(output_layer, (1, 5), (0, 0), Colours.white, is_visible=False)

    new1 = GUIObjects.Rect(output_layer, (1, output_layer.size[1]-10), (110, 0), fill_colour=MacColoursDark.side_bar_colour)
    new1.can_move = False

    y = 0
    i = 0
    for out in main_board.outs:
        new2 = GUIUtils.LabelledButton(output_layer, (90, 80), (10, y+25), 20+i, 24, MacColoursDark.side_bar_colour, "assets/SF-Mono-Light.otf", "OUT"+str(i), Colours.white)
        new3 = GUIObjects.Rect(output_layer, (output_layer.size[0]-20-111, 80), (120, y+25), MacColours.side_bar_inactive_colour)
        y = y + 100
        i = i + 1

    padding = GUIObjects.Rect(output_layer, (1, 5), (0, y+50), Colours.white, is_visible=False)


def fill_output_layer():

    if not len(main_board.outs):
        return -1

    if not len(main_board.saved_outs):
        return -2

    for out_pin in main_board.outs:
        if not len(out_pin.masters):
            return -3

    i = 0
    for obj in output_layer.gui_objects:
        if isinstance(obj, GUIObjects.Rect) and obj.is_visible and obj.size[0] > 1 and obj.size[1] > 1 and not isinstance(obj, GUIUtils.Button):
            j = 0
            rect = None
            while j < len(main_board.saved_outs):
                rect_width = obj.rect.width / len(main_board.saved_outs)
                rect_height = 5
                rect_left = j*rect_width + obj.rect.left
                rect_top = obj.rect.bottom - main_board.saved_outs[j][i] * (obj.rect.height - 5)-5
                prev_rect = rect
                rect = pygame.rect.Rect((int(rect_left), rect_top), (math.ceil(rect_width), rect_height))
                pygame.draw.rect(output_layer.surface, main_board.outs[i].masters[0].on_colour, rect)
                if j and main_board.saved_outs[j][i] != main_board.saved_outs[j-1][i]:
                    pygame.draw.rect(output_layer.surface, main_board.outs[i].masters[0].on_colour, pygame.rect.Rect(rect_left, min(rect_top, prev_rect.top), 5, max(abs(rect.top-prev_rect.bottom), abs(rect.bottom-prev_rect.top))))
                j = j + 1
            i = i + 1
        elif isinstance(obj, GUIUtils.LabelledButton):
            obj.label.font_colour = main_board.outs[i].masters[0].on_colour
            obj.label.update()
    return 0


def get_not_daughterboard(is_visible=False):

    x_pos = 0.5*(1920-480 - 24*main_board.slot_resolution) + bg_layer.position[0]
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (1080 - 20 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards)-1].position[1] + main_board.daughterboards[len(main_board.daughterboards)-1].size[1] + main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos - 2*main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos + 20*main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 20), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 6:
        new = PCB.Component(daughterboard, (2, 2), (6, 4 + i*2), Colours.white, LogicElements.Buffer(True))
        i = i + 1

    i = 0
    while i < 4:
        new = PCB.Component(daughterboard, (2, 2), (16, 1+i*2), Colours.white, LogicElements.ORGate(2, True))
        new = PCB.Component(daughterboard, (2, 2), (16, 11 + i * 2), Colours.white, LogicElements.ORGate(2, True))
        i = i + 1


def get_nand_daughterboard(is_visible=False):

    x_pos = 0.5 * (1920-480 - 24 * main_board.slot_resolution) + 480
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (1920-480 - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards)-1].position[1] + main_board.daughterboards[len(main_board.daughterboards)-1].size[1] + main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos - 2*main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2*main_board.slot_resolution), (0, y_pos + 21*main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 21), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 2:
        new = PCB.Component(daughterboard, (2, 4), (6, 1+i*4), Colours.white, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), Colours.white, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 1 + i * 4), Colours.white, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (16, 12 + i * 4), Colours.white, LogicElements.ANDGate(4, True))
        i = i + 1


def get_jk_daughterboard(is_visible=False):

    x_pos = 0.5 * (1920-480 - 24 * main_board.slot_resolution) + 480
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (1080 - 21 * main_board.slot_resolution)
    else:
        y_pos = main_board.daughterboards[len(main_board.daughterboards)-1].position[1] + main_board.daughterboards[len(main_board.daughterboards)-1].size[1] + main_board.slot_resolution

    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution), (0, y_pos - 2 * main_board.slot_resolution), is_visible=False)
    padding = GUIObjects.Rect(bg_layer, (1, 2 * main_board.slot_resolution), (0, y_pos + 21 * main_board.slot_resolution), is_visible=False)

    daughterboard = PCB.Daughterboard(bg_layer, main_board, (24, 23), (x_pos, y_pos), is_visible=is_visible)

    i = 0
    while i < 2:
        not1 = PCB.Component(daughterboard, (1, 1), (8, 4 + i * 5), Colours.white, LogicElements.HiddenBuffer(is_inverted=True), is_visible=True)
        d1 = PCB.Component(daughterboard, (3, 5), (6, 1 + i * 5), Colours.white, LogicElements.DFlipFlop(is_rising_edge=False))
        not2 = PCB.Component(daughterboard, (1, 1), (8, 15 + i * 5), Colours.white, LogicElements.HiddenBuffer(is_inverted=True), is_visible=True)
        d2 = PCB.Component(daughterboard, (3, 5), (6, 12 + i * 5), Colours.white, LogicElements.DFlipFlop(is_rising_edge=False))

        d1.logic_element.connect(not1.logic_element, 0)
        d2.logic_element.connect(not2.logic_element, 0)


        not3 = PCB.Component(daughterboard, (1, 1), (18, 4 + i * 5), Colours.white, LogicElements.HiddenBuffer(is_inverted=True), is_visible=True)
        jk1 = PCB.Component(daughterboard, (3, 5), (16, 1 + i * 5), Colours.white, LogicElements.JKFlipFlop(is_rising_edge=False))
        not4 = PCB.Component(daughterboard, (1, 1), (18, 15 + i * 5), Colours.white, LogicElements.HiddenBuffer(is_inverted=True), is_visible=True)
        jk2 = PCB.Component(daughterboard, (3, 5), (16, 12 + i * 5), Colours.white, LogicElements.JKFlipFlop(is_rising_edge=False))

        jk1.logic_element.connect(not3.logic_element, 0)
        jk2.logic_element.connect(not4.logic_element, 0)

        i = i + 1


def get_d_daughterboard(is_visible=False):

    x_pos = 0.5 * (1920-480 - 24 * main_board.slot_resolution) + 480
    if not len(main_board.daughterboards):
        y_pos = 0.33 * (1080 - 21 * main_board.slot_resolution)
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
        new = PCB.Component(daughterboard, (2, 4), (6, 1 + i * 4), Colours.white, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (2, 4), (6, 12 + i * 4), Colours.white, LogicElements.ANDGate(4, True))
        new = PCB.Component(daughterboard, (3, 4), (16, 1 + i * 4), Colours.white, LogicElements.DFlipFlop())
        new = PCB.Component(daughterboard, (3, 4), (16, 12 + i * 4), Colours.white, LogicElements.DFlipFlop())
        i = i + 1


def get_daughterboard(id):

    if id == 1:
        get_not_daughterboard(True)
    elif id == 2:
        get_nand_daughterboard(True)
    elif id == 3:
        get_jk_daughterboard(True)


def button_action(button_id):

    global selected_output

    for layer in main_window.all_layers:
        for element in layer.gui_objects:
            if isinstance(element, GUIUtils.Button):
                if element.button_id == button_id:

                    if button_id == 0:
                        get_daughterboard(parser.get_value("Nowa makieta", "Wybierz szablon:\n1- NOT + NOR\n2- NAND\n3- D + JK", 0))

                    elif button_id == 1:
                        main_board.program(programator.complete_read("_PRZEBIEG.txt", main_board.out_count))
                        fill_input_layer()

                    elif button_id == 2:
                        main_board.tick_tempo = parser.get_value("Okres sygnału wejściowego", "Zmiana okresu sygnału wejściowego", main_board.tick_tempo)
                        main_board.current_tick = main_board.tick_tempo * len(main_board.programming)
                        speed_change_button.label.text = str(main_board.tick_tempo)
                        speed_change_button.label.update()
                        speed_change_button.center_text()

                    elif button_id == 3:
                        main_board.current_tick = 0
                        main_board.saved_outs.clear()

                    elif 20+len(main_board.outs) > button_id >= 20:
                        output_layer.gui_objects[button_id*3-58].change_label(parser.get_string(f"Zmiana nazwy OUT{button_id-20}", f"Nowa nazwa dla OUT{button_id-20}", output_layer.gui_objects[button_id*3-58].label.text))

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
    fill_output_layer()
    main_board.send_programming()
    LogicElements.Gate.in_tick()
    LogicElements.Gate.out_tick()

    for daughterboard in main_board.daughterboards:
        if daughterboard.is_visible:

            for component in daughterboard.components:
                component.update_io_colours()

                if component.logic_element == selected_output:
                    for master in selected_output.masters:
                        if master.daughterboard.is_visible:
                            pygame.draw.line(daughterboard.surface, master.fill_colour, (mouse_pos[0]-daughterboard.position[0], mouse_pos[1]-daughterboard.position[1]), (master.outlets[0].position[0] + 0.5*master.outlets[0].size[0], master.outlets[0].position[1] + 0.5*master.outlets[0].size[1]), 3)

                for inlet in component.inlets:
                    if component.logic_element.inputs[inlet.inlet_id] is not None and not isinstance(component.logic_element, LogicElements.HiddenBuffer):
                        for master in component.logic_element.inputs[inlet.inlet_id].masters:
                            if master.daughterboard == component.daughterboard and master.daughterboard.is_visible:
                                pygame.draw.line(daughterboard.surface, master.fill_colour, (inlet.position[0]+0.5*inlet.size[0], inlet.position[1]+0.5*inlet.size[1]), (master.outlets[0].position[0] + 0.5*master.outlets[0].size[0], master.outlets[0].position[1] + 0.5*master.outlets[0].size[1]), width=3)


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


fill_input_layer()
pre_fill_output_layer()
