from ast import literal_eval
import csv
import pygame as pg


class InterfaceUpdate:

    def __init__(self, component, change, all_components, filename):
        self.component = component
        self.change = change
        self.all_components = all_components
        self.filename = filename

    def update_text(self):
        if self.change[0] in {"font", "text", "surface", "function"}:
            self.component.__dict__[self.change[0]] = str(self.change[1])
        elif self.change[0] in {"tab", "id", "font_size", "x_location", "y_location", "width", "height"}:
            self.component.__dict__[self.change[0]] = int(self.change[1])
        elif self.change[0] in {"main_color", "accent_color"}:
            self.component.__dict__[self.change[0]] = literal_eval(self.change[1])
        else:
            print(f"Updating text failed, variable '{self.change[0]}' not known")

    def update(self):
        # Update component
        if self.component.type == "Text":
            self.update_text()

    def save(self):
        attributes = [a for a in dir(self.all_components.total[0]) if not a.startswith('__')]

        # Gather attributes from csv file for correct placement
        try:
            with open("./" + self.filename) as file:
                reader = csv.reader(file, delimiter=',')

                for row in reader:
                    if '#' in row[0]:
                        component_attributes = row

        except FileNotFoundError:
            print("UI components file not found")
            raise SystemExit

        # Reassemble the file
        export_list = []
        comp_id = 0
        while comp_id < len(self.all_components.total):
            for comp in self.all_components.total:
                comp_list = []
                if int(comp.id) == int(comp_id):
                    for column in range(len(component_attributes)):
                        if column == 0:
                            comp_list.append('')
                        else:
                            for attribute in attributes:
                                if str(component_attributes[column].strip().replace(" ", "_").lower()) == attribute:
                                    comp_list.append(self.all_components.total[comp_id].__dict__[attribute])

                    export_list.append(comp_list)

            comp_id += 1

        # Overwrite file
        component_attributes[0] = '#'
        try:
            with open(self.filename, 'w+', newline='') as file:
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                wr.writerow(component_attributes)
                for i in range(len(export_list)):
                    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                    wr.writerow(export_list[i])

            print("Saved!")

        except FileNotFoundError and PermissionError:
            print("Error saving!")


class Interact:

    def __init__(self, all_components, ui):
        self.all_components = all_components
        self.ui = ui

    def check_selection(self, event, state):
        top_hit = False
        for component in self.all_components.total[::-1]:
            if int(component.surface) != 1 and component.lock == "False":
                component.active = False
                component.color = component.main_color

                rect = pg.Rect(int(int(component.x_location) * state['scale'] - 2 + int(state['scroll_x'])),
                               int(int(component.y_location) * state['scale'] - 2 + int(state['scroll_y'])),
                               int(component.hit_box[0]), int(component.hit_box[1]))
                try:
                    if rect.collidepoint((event.pos[0] - self.ui.location_screen[0], event.pos[1] - self.ui.location_screen[1])) and not top_hit and component.text != 'EDIT':
                        if component.active and state['deactivate']:
                            component.active = False
                            component.color = component.main_color
                        else:
                            component.active = True
                            component.color = '(255, 40, 40)'

                        top_hit = True
                    elif state['deactivate']:
                        component.active = False
                        component.color = component.main_color

                except AttributeError:
                    pass

    def move_selection(self, event, mouse_start_position, components_start_positions, state):
        for i, component in enumerate(self.all_components.total):
            if int(component.surface) != 1:
                component_start_position = [int(components_start_positions[i][0] * state['scale'] + int(state['scroll_x'])),
                                            int(components_start_positions[i][1] * state['scale'] + int(state['scroll_y']))]
                rect = pg.Rect(component_start_position[0] - 2, component_start_position[1] - 2, int(component.hit_box[0]), int(component.hit_box[1]))
                try:
                    if rect.collidepoint((mouse_start_position[0] - self.ui.location_screen[0], mouse_start_position[1] - self.ui.location_screen[1])) and component.active:
                        component.x_location = str(components_start_positions[i][0] + int((event.pos[0] - mouse_start_position[0]) * (1 / state['scale'])))
                        component.y_location = str(components_start_positions[i][1] + int((event.pos[1] - mouse_start_position[1]) * (1 / state['scale'])))
                        if int(component.y_location) < 0:
                            component.y_location = str(0)
                except AttributeError:
                    pass

    def edit_text(self, event):
        if event.type == pg.KEYDOWN:
            for component in self.all_components.total:
                if component.active:
                    if event.key == pg.K_BACKSPACE:
                        component.text = component.text[:-1]
                    elif event.key == pg.K_DELETE:
                        component.text = ''
                    elif event.key != pg.K_TAB and event.key != pg.K_RETURN:
                        component.text += event.unicode
