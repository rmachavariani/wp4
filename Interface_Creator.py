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
        elif self.change[0] in {"tab", "font_size", "x_location", "y_location", "width", "height"}:
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

            print("Saved!!")

        except FileNotFoundError and PermissionError:
            print("Error saving!")


class Interact:

    def __init__(self, all_components):
        self.all_components = all_components

    def check_selection(self, event):
        top_hit = False
        for component in self.all_components.total[::-1]:
            rect = pg.Rect(int(component.x_location) - 2, int(component.y_location) - 2, int(component.hit_box[0]), int(component.hit_box[1]))
            if rect.collidepoint((event.pos[0], event.pos[1])) and not top_hit:
                if component.active:
                    component.active = False
                    component.main_color = '(255, 255, 255)'
                else:
                    component.active = True
                    component.main_color = '(255, 40, 40)'

                top_hit = True
            else:
                component.active = False
                component.main_color = '(255, 255, 255)'

    # def move_selection(self, event):
    #     for component in self.all_components.total[::-1]:
    #         rect = pg.Rect(int(component.x_location) - 2, int(component.y_location) - 2, int(component.hit_box[0]), int(component.hit_box[1]))
    #         if rect.collidepoint((event.pos[0], event.pos[1])):