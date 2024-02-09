import pygame

import GUIDisplay
import GUIObjects
import GUIUtils

from assets import *

pygame.display.init()
pygame.font.init()

main_window = GUIDisplay.Window(fps_cap=150)

bg_layer = GUIDisplay.Layer(main_window, (1920, 1080), (0, 0), MacColoursDark.bg_colour)
circuit_board = GUIObjects.Image(bg_layer, (0, 0), "assets/circuit_board_2.png")

side_bar = GUIDisplay.Layer(main_window, (480, 1080), (0, 0), MacColoursDark.side_bar_inactive_colour)
test_button2 = GUIUtils.RoundedLabelledButton(side_bar, (128, 64), (128, 720), 2, 24, Colours.white, "assets/SFPRODISPLAYMEDIUM.OTF", "Test")


def button_action(button_id):
    print(button_id)


def loop_action():
    ...


def event_action(events, mouse_pos):
    ...
