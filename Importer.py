import csv


class Material:

    def __init__(self, path):
        self.path = path

        self.material_type = ""
        self.name = ""
        self.type = ""
        self.code = ""
        self.index_12 = ""
        self.index_15 = ""
        self.density = 0
        self.e = 0
        self.e_0 = 0
        self.e_90 = 0
        self.g = 0
        self.alpha = 0
        self.yield_stress = 0
        self.ult_stress = 0
        self.cr_stress = 0
        self.k = 0
        self.tau_y = 0

    def import_material(self, material_type, material_choice):
        self.material_type = material_type
        print(f"Importing {material_type}; {material_choice[0]} {material_choice[1]}")
        try:
            with open(f"./{self.path}.csv") as file:
                reader = csv.reader(file, delimiter=',')

                for row in reader:
                    if f'variable_name_{material_type}' in row[0]:
                        component_attributes = row

                    if (row[1].strip().lower(), row[2].strip().lower()) == (material_choice[0].strip().lower(), material_choice[1].strip().lower()):
                        for i, value in enumerate(row):
                            try:
                                self.__dict__[component_attributes[i].strip().lower()] = float(value)
                            except ValueError:
                                self.__dict__[component_attributes[i].strip().lower()] = value

        except FileNotFoundError:
            print("Material sheet file not found, make sure that the right path is given")
            raise SystemExit


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
                    index_12 = False
                    index_15 = False
                    if material_type.strip().lower() == str(row[0]).strip().lower():
                        try:
                            for i, cell in enumerate(row):
                                if component_attributes[i] == "name":
                                    material_name = str(cell)

                                if component_attributes[i] == "type":
                                    material_main_type = str(cell)

                                if component_attributes[i] == "index_12":
                                    if cell != "-":
                                        index_12 = True

                                if component_attributes[i] == "index_12":
                                    if cell != "-":
                                        index_15 = True

                                if material_name != "" and material_main_type != "" and index_12 and index_15:
                                    material_iteration = Material(path)
                                    material_iteration.import_material(str(material_type), (material_name, material_main_type))
                                    material_list.append(material_iteration)
                                    break

                                if i == len(row) - 1:
                                    if not index_12 or not index_15:
                                        print(f"{material_name} was not appended: index_12 = {index_12}, index_15 = {index_15}")
                                    else:
                                        print(f"{material_name} was not appended as it does not have a type")

                        except IndexError:
                            print("Error in reading materials file")
                            raise SystemExit

    except FileNotFoundError:
        print("Material sheet file not found, make sure that the right path is given")
        raise SystemExit

    return material_list

# Test
# materials = import_all_materials("material_sheet", ("metal", "none"))
# for material in materials:
#     print(material.name, material.type)
