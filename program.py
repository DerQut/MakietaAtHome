import pygame

import GUIDisplay
import GUIObjects

import assets

main_window = GUIDisplay.Window(fps_cap=150)

left_layer = GUIDisplay.ScrollingLayer(main_window, (128, 1080), (0, 0), assets.Colours.black)

test_rect = GUIObjects.Rect(left_layer, (64, 64), (32, 32), width=3)

stripe_1 = GUIObjects.Rect(left_layer, (128, 200), (0, 0), assets.Colours.red)
stripe_2 = GUIObjects.Rect(left_layer, (128, 200), (0, 200), assets.Colours.orange)
stripe_3 = GUIObjects.Rect(left_layer, (128, 200), (0, 400), assets.Colours.yellow)
stripe_4 = GUIObjects.Rect(left_layer, (128, 200), (0, 600), assets.Colours.green)
stripe_5 = GUIObjects.Rect(left_layer, (128, 200), (0, 800), assets.Colours.cyan)
stripe_6 = GUIObjects.Rect(left_layer, (128, 200), (0, 1000), assets.Colours.blue)
stripe_7 = GUIObjects.Rect(left_layer, (128, 200), (0, 1200), assets.Colours.purple)


def loop_action():
    ...


def event_action(events, mouse_pos):

    for event in events:

        if event.type == pygame.WINDOWCLOSE:
            return pygame.WINDOWCLOSE

        elif event.type == pygame.MOUSEWHEEL:
            for layer in main_window.all_layers:
                if layer.mouse_check(mouse_pos):
                    layer.scroll(event.x, event.y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for layer in reversed(main_window.all_layers):
                    if layer.mouse_check(mouse_pos):
                        for gui_object in reversed(layer.gui_objects):
                            if gui_object.mouse_check(mouse_pos):
                                print(gui_object.fill_colour)
                                break
                        break
