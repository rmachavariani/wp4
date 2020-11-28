import csv


class Material:

    def __init__(self, path):
        self.path = path

        self.material_type = ""
        self.name = ""
        self.type = ""
        self.code = ""
        self.index = ""
        self.density = 0
        self.e = 0
        self.e_0 = 0
        self.e_90 = 0
        self.g = 0
        self.yield_stress = 0
        self.ult_stress = 0
        self.cr_stress = 0
        self.k = 0
        self.tau_y = 0

    def import_material(self, material_type, material_choice):
        self.material_type = material_type
        try:
            with open(f"./{self.path}.csv") as file:
                reader = csv.reader(file, delimiter=',')

                for row in reader:
                    if f'variable_name_{material_type}' in row[0]:
                        component_attributes = row

                    if (row[1].strip().lower(), row[2].strip().lower()) == (material_choice[0], material_choice[1].lower()):
                        for i, value in enumerate(row):
                            self.__dict__[component_attributes[i].strip().lower()] = value

        except FileNotFoundError:
            print("UI components file not found, make sure that 'variable_name_[metal/composite]' at start of line")
            raise SystemExit
        print(component_attributes)


def import_all_materials(path, material_types):
    try:
        with open(f"./{path}.csv") as file:
            reader = csv.reader(file, delimiter=',')

            material_list = []
            component_attributes = []

            for material_type in material_types:
                for row in reader:
                    if f'variable_name_{material_type}' in row[0]:
                        component_attributes = row

                    material_name = ""
                    material_main_type = ""
                    for i, cell in enumerate(row):
                        if component_attributes[i] == "name":
                            material_name = str(cell)

                        if component_attributes[i] == "type":
                            material_main_type = str(cell)

                        if material_name != "" and material_main_type != "":
                            material_iteration = Material(path)
                            material_iteration.import_material(str(material_type), (material_name, material_main_type))
                            material_list.append(material_iteration)

    except FileNotFoundError:
        print("UI components file not found, make sure that 'variable_name_[metal/composite]' at start of line")
        raise SystemExit
    print(component_attributes)


material = Material("material_sheet")
material.import_material("metal", ("aluminium", "7075-T6"))
print(material.density)

