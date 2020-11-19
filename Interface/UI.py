import pygame as pg
from ast import literal_eval


def empty():
    pass


class Main:

    def __init__(self):
        self.resolution = (1280, 720)
        self.top_bar = (self.resolution[0], 50)
        self.location_screen = (0, self.top_bar[1])
        self.current_tab = 0
        self.ticks = {'global': 0}
        self.state = {'getting_pressed': False, 'click_counter': 0, 'deactivate': False, 'edit': False, 'scale': 1, 'scroll_x': 0, 'scroll_y': 0, 'deselect': False}
        self.add = {'text': False}

# class InputBox:
#
#     def __init__(self, x, y, w, h, player_num, text=''):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color_box = Color_White
#         self.color_text = Color_White
#         self.text = text
#         self.player_num = player_num
#         self.txt_surface = Font.render(text, True, self.color_text)
#         self.active = False
#
#     def handle_event(self, event, location_screen):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # If the user clicked on the input_box rect
#             # noinspection PyArgumentList
#             if self.rect.collidepoint((event.pos[0] - location_screen[0], event.pos[1] - location_screen[1])):
#                 # Toggle the active variable
#                 self.active = not self.active
#             else:
#                 if self.active and (self.text.isspace() or self.text == ''):
#                     self.text = example_names[self.player_num]
#                     self.txt_surface = Font.render(self.text, True, self.color_text)
#                 self.active = False
#
#         elif event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 elif event.key == pg.K_DELETE:
#                     self.text = ''
#                 elif event.key != pg.K_TAB and event.key != pg.K_RETURN:
#                     self.text += event.unicode
#
#                 # Re-render the text
#                 self.txt_surface = Font.render(self.text, True, self.color_text)
#
#         if self.active and self.text == example_names[self.player_num]:
#             self.text = ''
#             self.txt_surface = Font.render(self.text, True, self.color_text)
#
#     def return_input(self):
#         return self.text
#
#     def update(self):
#         # Resize the box if the text is too long
#         width = max(200, self.txt_surface.get_width()+10)
#         self.rect.w = width
#
#     def draw(self, window):
#         # Change the current color of the input box
#         # Blit inside filler rect
#         pg.draw.rect(window, Color_Soft_Red, self.rect)
#         self.color_box = Color_Light_Red if self.active else Color_White
#         # Blit the text
#         window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
#         # Blit the rect
#         pg.draw.rect(window, self.color_box, self.rect, 2)
