import csv
import sys
import Interface_Creator
import time

import pygame as pg

from ast import literal_eval


class InterfaceComponents:

    def __init__(self):
        self.text_comp = []
        self.button_comp = []
        self.total = []

    def import_ui(self, filename, current_tab):
        try:
            with open("./" + filename) as file:
                reader = csv.reader(file, delimiter=',')

                for row in reader:
                    if '#' in row[0]:
                        component_attributes = row
                        tab_column = row.index("Tab")
                    else:
                        if int(row[tab_column]) != int(current_tab):
                            continue

                        file = self.ImportComponent()
                        file.get_components(component_attributes, row)

                        if file.type == 'Text':
                            font = pg.font.SysFont(file.font, int(file.font_size))
                            text_width, text_height = font.size(file.text)
                            file.hit_box = (text_width + 4, text_height + 4)
                            self.text_comp.append(file)

                        self.total.append(file)

        except FileNotFoundError:
            print("UI components file not found")
            raise SystemExit

    def draw_text(self, possible_surfaces):
        for text_obj in self.text_comp:
            # Creating font
            font = pg.font.SysFont(text_obj.font, int(text_obj.font_size))

            # Selecting surface
            index_surface = 0
            for i, surface in enumerate(possible_surfaces):
                if surface == text_obj.surface.strip().replace(" ", "_").lower():
                    index_surface = i

            # Drawing text
            text = font.render(text_obj.text, True, literal_eval(text_obj.main_color))
            possible_surfaces[index_surface].blit(text, (int(text_obj.x_location), int(text_obj.y_location)))

            if text_obj.active:
                pg.draw.rect(possible_surfaces[index_surface], (180, 40, 40),
                             (int(text_obj.x_location) - 2, int(text_obj.y_location) - 2, int(text_obj.hit_box[0]), int(text_obj.hit_box[1])), 1)

    class ImportComponent:

        def __init__(self):
            self.tab = 0
            self.id = 0
            self.name = ""
            self.type = ""
            self.font = ""
            self.font_size = 0
            self.text = ""
            self.main_color = (255, 255, 255)
            self.accent_color = (255, 0, 255)
            self.surface = screen
            self.x_location = 0
            self.y_location = 0
            self.width = 0
            self.height = 0
            self.function = ""
            self.hit_box = (20, 20)
            self.active = False

        def get_components(self, component_attributes, row):
            attributes = [a for a in dir(InterfaceComponents.ImportComponent()) if not a.startswith('__')]

            for column, field in enumerate(row):
                for attribute in attributes:
                    if str(component_attributes[column].strip().replace(" ", "_").lower()) == attribute:
                        try:
                            self.__dict__[attribute] = str(field)

                        except ValueError:
                            self.__dict__[attribute] = "Unknown"
                            print(f"Value Error! '{attribute}' was not read correctly!")


# Setup Pygame window
pg.init()
mainClock = pg.time.Clock()

pg.display.set_caption('B09')
screen = pg.display.set_mode((1280, 720))

main_font = pg.font.SysFont(None, 20)

# Testing
file_name = 'UI_Components.csv'
components = InterfaceComponents()
components.import_ui(file_name, 0)
print(components.__dict__)


def main_menu(a):
    state = {'getting_pressed': False}
    while True:

        screen.fill((0, 0, 0))

        components.draw_text([screen])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_SPACE:
                    start = time.time()
                    a += 4
                    test = Interface_Creator.InterfaceUpdate(components.text_comp[0], ["font_size", a], components, file_name)
                    test.update()
                    print(f'Time elapsed = {time.time() - start}')
                elif event.key == pg.K_s:
                    test = Interface_Creator.InterfaceUpdate(components.text_comp[0], ["font_size", a], components, file_name)
                    test.save()

            if event.type == pg.MOUSEBUTTONDOWN:
                interact = Interface_Creator.Interact(components)
                interact.check_selection(event)
                print('click')

        # if pg.mouse.get_pressed()[0]:
        #     if state['getting_pressed']:
        #
        #     else:



        pg.display.update()
        mainClock.tick(60)


main_menu(20)


