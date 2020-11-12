import csv
import sys
import Interface_Creator
import UI
import Functions

import pygame as pg

from ast import literal_eval

# Init UI
ui = UI.Main()


# All interface components i.e. buttons, text, menu's, etc.
class InterfaceComponents:

    def __init__(self):
        self.text_comp = []  # Text components
        self.button_comp = []  # Button components
        self.total = []  # List of all components together

    # import all interface components from csv file
    def import_ui(self, filename, current_tab):
        try:
            # Open the file
            with open("./" + filename) as file:
                reader = csv.reader(file, delimiter=',')

                # Go through all rows of the csv file
                for i, row in enumerate(reader):
                    # Leave out commented row
                    if '#' in row[0]:
                        component_attributes = row
                        tab_column = row.index("Tab")
                    else:
                        if int(row[tab_column]) != int(current_tab):  # Leave out all components not visible on tab
                            continue

                        # Get file information
                        file = self.VariableComponent()
                        file.get_components(component_attributes, row)

                        # Create text component
                        if file.type == 'Text':
                            font = pg.font.SysFont(file.font, int(file.font_size))
                            text_width, text_height = font.size(file.text)
                            file.hit_box = (text_width + 4, text_height + 4)
                            self.text_comp.append(file)

                        # Create button component
                        if file.type == 'Button':
                            file.hit_box = (int(file.width) + 4, int(file.height) + 4)
                            self.button_comp.append(file)

                        self.total.append(file)

        except FileNotFoundError:
            print("UI components file not found")
            raise SystemExit

    def update_hit_box(self, state):
        for component in self.total:
            if component.type == 'Text':
                font = pg.font.SysFont(component.font, int(int(component.font_size) * state['scale']))
                text_width, text_height = font.size(component.text)
                component.hit_box = (text_width + 4, text_height + 4)
            elif component.type == 'Button':
                component.hit_box = (int(int(component.width) * state['scale'] + 4), int(int(component.height) * state['scale'] + 4))

    def draw_text(self, possible_surfaces, state):
        for text_obj in self.text_comp:
            if (int(text_obj.surface) == 1) or text_obj.lock == "True":

                # Creating font
                font = pg.font.SysFont(text_obj.font, int(text_obj.font_size))
                # Drawing text
                text = font.render(text_obj.text, True, literal_eval(text_obj.color))
                possible_surfaces[int(text_obj.surface)].blit(text, (int(text_obj.x_location), int(text_obj.y_location)))
            else:
                # Creating font
                font = pg.font.SysFont(text_obj.font, int(int(text_obj.font_size) * state['scale']))
                # Drawing text
                text = font.render(text_obj.text, True, literal_eval(text_obj.color))
                possible_surfaces[int(text_obj.surface)].blit(text, (int(int(text_obj.x_location) * state['scale'] + int(state['scroll_x'])),
                                                                     int(int(text_obj.y_location) * state['scale']) + int(state['scroll_y'])))

    def draw_hit_box(self, possible_surfaces, state):
        for component in self.total:
            # Drawing hit_box
            if component.active:
                pg.draw.rect(possible_surfaces[int(component.surface)], (180, 40, 40),
                             (int(int(component.x_location) * state['scale'] - 2 + int(state['scroll_x'])),
                              int(int(component.y_location) * state['scale'] - 2 + int(state['scroll_y'])),
                              int(component.hit_box[0]), int(component.hit_box[1])), 1)

    class VariableComponent:

        def __init__(self):
            self.tab = 0
            self.id = 0
            self.name = ""
            self.type = ""
            self.font = "None"
            self.font_size = 40
            self.text = "New"
            self.main_color = '(255, 255, 255)'
            self.second_color = '(255, 0, 255)'
            self.surface = 0
            self.x_location = 1000
            self.y_location = 20
            self.width = 50
            self.height = 50
            self.command = ""
            self.hit_box = (20, 20)
            self.active = False
            self.lock = 'False'

            self.rect = pg.Rect(self.x_location, self.y_location, self.width, self.height)
            self.button_active = False
            self.color = self.main_color
            self.tick = 0

        def get_components(self, component_attributes, row):
            attributes = [a for a in dir(InterfaceComponents.VariableComponent()) if not a.startswith('__')]

            for column, field in enumerate(row):
                for attribute in attributes:
                    if str(component_attributes[column].strip().replace(" ", "_").lower()) == attribute:
                        try:
                            self.__dict__[attribute] = str(field)

                        except ValueError:
                            self.__dict__[attribute] = "Unknown"
                            print(f"Value Error! '{attribute}' was not read correctly!")

        # Button specific
        def handle_button_event(self, event, tick):
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect
                # noinspection PyArgumentList
                if self.rect.collidepoint((event.pos[0] - ui.location_screen[0], event.pos[1] - ui.location_screen[1])):
                    # Toggle the active variable
                    self.button_active = not self.button_active
                    # command
                    self.activate_command()
                else:
                    self.button_active = False

                if self.button_active:
                    self.tick = tick

        def activate_command(self):
            function = Functions.Main(ui)
            try:
                function.__getattribute__(self.command)()
            except AttributeError:
                pass

        def draw_button(self, window, global_tick, state):
            # Update data
            self.rect = pg.Rect(int(int(self.x_location) * state['scale'] + int(state['scroll_x'])), int(int(self.y_location) * state['scale'] + int(state['scroll_y'])),
                                int(int(self.width) * state['scale']), int(int(self.height) * state['scale']))

            font = pg.font.SysFont(self.font, int(int(self.font_size) * state['scale']))
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_width, text_height = font.size(self.text)

            self.button_active = False if global_tick - self.tick > 4 else True

            # Change the current color of the input box
            self.color = self.second_color if self.button_active else self.main_color
            # Blit the rect
            pg.draw.rect(window, literal_eval(self.color), self.rect)
            # Blit the text
            window.blit(text_surface, (int((self.rect.x + 0.5 * self.rect.w - 0.5 * text_width)),
                                       int((self.rect.y + 0.5 * self.rect.h - 0.5 * text_height))))

        def draw_static_button(self, window, global_tick, state, text_type):
            # Update data
            self.rect = pg.Rect(int(self.x_location), int(self.y_location),
                                int(self.width), int(self.height))

            font = pg.font.SysFont(self.font, int(self.font_size))
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_width, text_height = font.size(self.text)

            self.button_active = False if global_tick - self.tick > 4 else True

            # Change the current color of the input box
            if text_type == 'EDIT' and state['edit']:
                self.color = '(240, 40, 40)'
            elif text_type == 'EDIT':
                if __name__ == '__main__':
                    self.color = self.main_color
            else:
                self.color = self.second_color if self.button_active else self.main_color
            # Blit the rect
            pg.draw.rect(window, literal_eval(self.color), self.rect)
            # Blit the text
            window.blit(text_surface, (int((self.rect.x + 0.5 * self.rect.w - 0.5 * text_width)),
                                       int((self.rect.y + 0.5 * self.rect.h - 0.5 * text_height))))


# Setup Pygame window
pg.init()
mainClock = pg.time.Clock()

pg.display.set_caption('B09')
main_win = pg.display.set_mode(ui.resolution)
screen = pg.Surface((ui.resolution[0], ui.resolution[1] - ui.top_bar[1]))

# Testing
file_name = 'UI_Components.csv'
components = InterfaceComponents()
components.import_ui(file_name, 0)


def deselect():
    for component in components.total:
        if component.lock != 'EDIT':
            component.active = False
            component.color = component.main_color


def main_menu(a):
    mouse_start_position = (0, 0)
    components_start_positions = []
    ticks = ui.ticks
    state = ui.state
    while True:

        screen.fill((50, 50, 50))
        pg.draw.rect(main_win, (30, 30, 30), (0, 0, ui.top_bar[0], ui.top_bar[1]))

        interact = Interface_Creator.Interact(components, ui)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                interact.edit_text(event)

                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            if pg.key.get_pressed()[pg.K_LCTRL]:
                if pg.key.get_pressed()[pg.K_s]:
                    interface = Interface_Creator.InterfaceUpdate(components.text_comp[0], ["font_size", a], components, file_name)
                    interface.save()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        state['scale'] += 0.1
                    if event.button == 5:
                        state['scale'] -= 0.1

            elif pg.key.get_pressed()[pg.K_LALT]:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        state['scroll_x'] += 40
                    if event.button == 5:
                        state['scroll_x'] -= 40

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    state['scroll_y'] += 40
                if event.button == 5:
                    state['scroll_y'] -= 40

            # Button registration
            for button in components.button_comp:
                if button.lock:
                    button.handle_button_event(event, ticks['global'])
                elif not state['edit']:
                    button.handle_button_event(event, ticks['global'])

            # Click registration
            if state['edit']:
                if pg.mouse.get_pressed(num_buttons=3)[0]:
                    if state['getting_pressed']:
                        state['click_counter'] += 1

                        if state['click_counter'] > 0:
                            state['deactivate'] = False

                        interact.move_selection(event, mouse_start_position, components_start_positions, state)
                        interact.check_selection(event, state)
                    else:
                        try:
                            mouse_start_position = (event.pos[0], event.pos[1])
                        except AttributeError:
                            pass

                        components_start_positions = []
                        for component in components.total:
                            components_start_positions.append((int(component.x_location), int(component.y_location)))
                        state['getting_pressed'] = True

                else:
                    if state['getting_pressed']:
                        if state['click_counter'] == 0:
                            state['deactivate'] = True
                        state['getting_pressed'] = False
                        state['click_counter'] = 0

                        interact.check_selection(event, state)

                components.update_hit_box(state)

        # Buttons
        for button in components.button_comp:
            if button.lock == "True":
                button.draw_static_button(screen, ticks['global'], state, button.text)
            else:
                button.draw_button(screen, ticks['global'], state)

        if ui.state['deselect']:
            deselect()

        components.draw_text([screen, main_win], state)
        components.draw_hit_box([screen, main_win], state)

        # Add component
        # Add Text
        if ui.add['text']:
            deselect()
            new_text = components.VariableComponent()
            new_text.tab = str(ui.current_tab)
            new_text.id = str(int(components.total[-1].id) + 1)
            new_text.type = 'Text'
            new_text.name = 'Mauro'
            new_text.main_color = '(255, 255, 255)'

            font = pg.font.SysFont(new_text.font, int(new_text.font_size))
            text_width, text_height = font.size(new_text.text)
            new_text.hit_box = (text_width + 4, text_height + 4)

            components.text_comp.append(new_text)
            components.total.append(new_text)
            ui.add['text'] = False

        main_win.blit(screen, ui.location_screen)
        pg.display.flip()
        mainClock.tick(60)
        ticks['global'] += 1
        ui.state['deselect'] = False


main_menu(20)
