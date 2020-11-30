import numpy as np
import json
import math as m
import matplotlib.pyplot as plt
import time
import csv

import Importer
import Thermal_Stress
import Fastener_type
import PullThroughCheck
import Stress_Modes_Lug
import BearingCheck
import Forces
import Weight
import LugCheck

with open('data.json', 'r+') as j:
    master_json_data = json.load(j)

debug = False


def iteration(json_file, it, width, height, lug_thickness, plate_thickness, wall_thickness, hole_diameter, inner_diameter, outer_diameter, horizontal_spacing,
              margins_list, masses):

    try:
        json_data = json_file['iterations']

        int_list = list(map(int, json_data.keys()))
        last_key = sorted(int_list)[-1]
        json_data = json_data[str(last_key)]

        input_data = json_data['input']
        spacecraft_data = input_data['spacecraft']
        lug_data = input_data['lug']
        fastener_data = input_data['fastener']
        vehicle_wall_data = input_data['vehicle_wall']

        # Spacecraft data
        mmoi = spacecraft_data['mmoi']
        mass = spacecraft_data['mass']
        body_size = spacecraft_data['body_size']
        solar_panel_com = spacecraft_data['solar_panel_com']
        torques = spacecraft_data['torques']
        launch_acceleration = 5 * 9.80665

        # Plate data
        # width = float(lug_data['width_plate']) + step_sizes['width']
        # height = float(lug_data['height']) + step_sizes['height']
        # plate_thickness = float(lug_data['thickness_plate']) + step_sizes['plate_thickness']
        # wall_thickness = float(vehicle_wall_data['thickness']) + step_sizes['wall_thickness']

        if material_properties_attachment.material_type.strip().lower() == "metal":
            material_type = 1
        elif material_properties_attachment.material_type.strip().lower() == "composite":
            material_type = 2
        else:
            print(f"Material type '{material_properties_attachment.material_type}', does not exist")
            return

        # Stresses
        allowable_stress = material_properties_attachment.yield_stress
        wall_allowable_stress = material_properties_vehicle.yield_stress

        # lug_thickness = float(lug_data['thickness_lug']) + step_sizes['lug_thickness']
        lug_length = float(lug_data['length_lug'])
        lug_density = material_properties_attachment.density
        # hole_diameter = float(lug_data['hole_diameter']) + step_sizes['hole_diameter']

        # Fastener data
        # inner_diameter = float(fastener_data['inner_diameter']) + step_sizes['inner_diameter']
        # outer_diameter = float(fastener_data['outer_diameter']) + step_sizes['outer_diameter']
        # horizontal_spacing = float(fastener_data['horizontal_spacing']) + step_sizes['horizontal_spacing']
        fastener_density = material_properties_fastener.density
        area = m.pi * ((outer_diameter / 2) ** 2)

        # Calculate forces
        forces, moments = Forces.calc_forces(mmoi, mass, body_size, solar_panel_com, torques, launch_acceleration)

        edge_to_center_hole_distance = height / 2 - hole_diameter / 2

        tensile_load = forces[3][1]
        transverse_load = max(forces[3][0], forces[3][2])
        axial_load = tensile_load

        # Lug stress checks
        P_bru, P_bry, P_bush_y, shear_bearing_margin, shear_bearing_yield_margin, bushing_margin = LugCheck.check_shear_bearing(hole_diameter, lug_thickness,
                                                                                                                                edge_to_center_hole_distance,
                                                                                                                                tensile_load, material_properties_attachment.ult_stress,
                                                                                                                                material_properties_attachment.ult_stress)
        lug_list = LugCheck.check_bolt_pin_bending(hole_diameter, lug_thickness, height, edge_to_center_hole_distance, material_properties_attachment, transverse_load,
                                                   axial_load, material_properties_attachment.ult_stress, P_bru)

        try:
            P_tu_transverse = lug_list[0]
            P_ty_transverse = lug_list[1]
            ultimate_transverse_margin = lug_list[2]
            ultimate_transverse_yield_margin = lug_list[3]

            # Calculate phi from Fastener type
            phi = Fastener_type.Fastener_Type(plate_thickness, wall_thickness, inner_diameter, outer_diameter,
                                              material_properties_attachment.e, material_properties_fastener.e, material_properties_vehicle.e)

            if phi is None:
                print('Phi was not found')
                return

            # Calculate thermal stresses
            thermal_stresses = Thermal_Stress.calc_thermal_stress(material_properties_vehicle, material_properties_attachment, material_properties_fastener, phi)

            # Do bearing check
            bearing_check, coord_array, fastener_count = BearingCheck.bearing_check(height, inner_diameter, material_type, horizontal_spacing, area,
                                                                                    plate_thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces, thermal_stresses)
            # Convert coordinates from point array to python list
            new_coordinates_array = []
            for fastener_coord in coord_array:
                new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

            # Stress Modes Lug
            w_over_d = height / hole_diameter  # 1 < w_over_d < 5
            margin_lug = Stress_Modes_Lug.stress_mode_tension(material_properties_attachment, hole_diameter, lug_thickness, w_over_d, forces[3][1])

            # Pull through check
            margin_back_plate, margin_vehicle_plate = PullThroughCheck.pull_through(outer_diameter, inner_diameter, fastener_count, plate_thickness, wall_thickness,
                                                                                    allowable_stress, wall_allowable_stress, new_coordinates_array, forces[3][1], moments[3][2])

            # Mass
            mass_fastener = Weight.calc_mass_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density)
            mass_attachment = Weight.calc_mass_attachment(plate_thickness, width, height, fastener_count, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density)

            # Update json file
            # Append input to json iteration
            json_data['input']['lug']['width_plate'] = width
            json_data['input']['lug']['height'] = height
            json_data['input']['lug']['thickness_lug'] = plate_thickness
            json_data['input']['lug']['thickness_plate'] = plate_thickness
            json_data['input']['lug']['hole_diameter'] = hole_diameter
            json_data['input']['vehicle_wall']['thickness'] = wall_thickness
            json_data['input']['fastener']['inner_diameter'] = inner_diameter
            json_data['input']['fastener']['outer_diameter'] = outer_diameter
            json_data['input']['fastener']['horizontal_spacing'] = horizontal_spacing
            json_data['output']['bearing_check']['margins']['plate'] = bearing_check[0]
            json_data['output']['bearing_check']['margins']['wall'] = bearing_check[1]

            # Add pull through check
            for n, margin in enumerate(margin_back_plate):
                json_data['output']['pull_check']['margins']["plate-{}".format(n + 1)] = str(margin)

            for n, margin in enumerate(margin_vehicle_plate):
                json_data['output']['pull_check']['margins']["wall-{}".format(n + 1)] = str(margin)

            # Write back to document
            new_json_data = {str(int(last_key) + 1): json_data}

            master_json_data['iterations'].update(new_json_data)

            if debug:
                # Print to console
                rv = 5
                print(f"{it + 1}; Calculating with: width = {round(width, rv)},"
                      f" height = {round(height, rv)},"  # w
                      f" lug_thickness = {round(lug_thickness, rv)},"  # t1
                      f" plate_thickness = {round(plate_thickness, rv)},"  # t2
                      f" wall_thickness = {round(wall_thickness, rv)},"  # t3
                      f" hole_diameter = {round(hole_diameter, rv)},"  # D1
                      f" inner_diameter = {round(inner_diameter, rv)},"  # Dfi = D2
                      f" outer_diameter = {round(outer_diameter, rv)},"  # Dfo
                      f" horizontal_spacing = {round(horizontal_spacing, rv)}")

                print(f"{it + 1}; Bearing Check: {bearing_check}")
                print(f"{it + 1}; Lug Stress Check: {margin_lug}")
                print(f"{it + 1}; Pull Through Check: {margin_back_plate}, {margin_vehicle_plate}")
                print(f"{it + 1}; Shear Out Bearing Lug Check: {shear_bearing_margin}, {P_bru}")
                print(f"{it + 1}; Shear Out Bearing Yield Lug Check: {shear_bearing_yield_margin}, {P_bry}")
                print(f"{it + 1}; Bushing Lug Check: {bushing_margin}, {P_bush_y}")
                print(f"{it + 1}; Transverse Lug Check: {ultimate_transverse_margin}, {P_tu_transverse}")
                print(f"{it + 1}; Transverse Yield Lug Check: {ultimate_transverse_yield_margin}, {P_ty_transverse}")
                print(f"{it + 1}; Weight = {mass_fastener} + {mass_attachment} = {mass_fastener + mass_attachment}")

            # Graph
            all_margins = [bearing_check[0], bearing_check[1], margin_lug, margin_back_plate[0], margin_back_plate[1], margin_vehicle_plate[0], margin_vehicle_plate[1],
                           shear_bearing_margin, P_bru, shear_bearing_yield_margin, P_bry, bushing_margin, P_bush_y, ultimate_transverse_margin, P_tu_transverse,
                           ultimate_transverse_yield_margin, P_ty_transverse]

            if not None in all_margins:
                margin_details.append(all_margins)
                input_details.append([width, w_over_d, lug_thickness, plate_thickness, wall_thickness, inner_diameter, outer_diameter, horizontal_spacing])
                margins_list.append(min(all_margins))
                masses.append(float(mass_fastener + mass_attachment))

            return master_json_data

        except TypeError:
            pass

    except ValueError:
        pass


def save_data(json_file):
    try:
        with open(f'iterations_2_{material_number}.txt', 'w+', newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(
                ["Margin", "Mass", "Bearing_Check_1", "Bearing_Check_2", "Margin_Stress_Lug", "Margin_Back_Plate_1", "Margin_Back_Plate_2",
                 "Margin_Vehicle_Plate_1", "Margin_Vehicle_Plate_2", "Shear_Bearing_Margin", "P_bru", "Shear_Bearing_Yield_Margin", "P_bry",
                 "Bushing_Margin", "P_bush_y", "Ultimate_Transverse_Margin", "P_tu_transverse", "Ultimate_Transverse_Yield_Margin",
                 "P_ty_Transverse",
                 "Width", "W_over_D", "Lug_Thickness", "Plate_Thickness", "Wall_Thickness", "Inner_Diameter", "Outer_Diameter",
                 "Horizontal_Spacing",
                 "Material_Name", "Material_Type"])

            for i, mass in enumerate(mass_list):
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                wr.writerow(
                    [margin_list[i], mass_list[i], margin_details[i][0], margin_details[i][1], margin_details[i][2], margin_details[i][3],
                     margin_details[i][4],
                     margin_details[i][5], margin_details[i][6], margin_details[i][7], margin_details[i][8], margin_details[i][9],
                     margin_details[i][10],
                     margin_details[i][1], margin_details[i][12], margin_details[i][13], margin_details[i][14], margin_details[i][15],
                     margin_details[i][16],
                     input_details[i][0], input_details[i][1], input_details[i][2], input_details[i][3], input_details[i][4],
                     input_details[i][5],
                     input_details[i][6], input_details[i][7], material_details[0], material_details[1]])

        with open(f'data_iterations_2_{material_number}.json', 'w+') as j:
            json.dump(json_file, j, indent=4, sort_keys=True)

        print("Saved!")

        with open('data.json', 'r+') as j:
            json_file = json.load(j)

        return json_file

    except FileNotFoundError and PermissionError:
        print("Error saving!")


left = {"width": 0.05, "w_over_d": 1.1, "lug_thickness": 0.001, "plate_thickness": 0.0008, "wall_thickness": 0.0008,
        "inner_diameter": 0.001, "outer_diameter": 0.005, "horizontal_spacing": 0.0001}

right = {"width": 0.1, "w_over_d": 5, "lug_thickness": 0.01, "plate_thickness": 0.02, "wall_thickness": 0.02,
         "inner_diameter": 0.005, "outer_diameter": 0.01, "horizontal_spacing": 0.001}

steps = {"width": 4, "w_over_d": 4, "lug_thickness": 4, "plate_thickness": 4, "wall_thickness": 4,
         "inner_diameter": 4, "outer_diameter": 4, "horizontal_spacing": 4}

total_iterations = 1
for attribute in steps.keys():
    total_iterations *= steps[attribute]

total_iterations *= 1

print(f"Total iterations: {total_iterations}")

step = 0
material_number = 0
state = {"negative": False, "positive": False}
margin_list = []
mass_list = []
margin_details = []
input_details = []
first_iteration = True

print(f"-- Importing materials --")
material_list = Importer.import_all_materials("material_sheet", ("metal", "none"))
print(material_list[0].type, material_list[1].type, material_list[2].type, material_list[3].type, material_list[4].type, material_list[5].type, material_list[6].type)

material_properties_attachment = material_list[6]
material_properties_fastener = material_list[6]
material_properties_vehicle = material_list[6]

print(f"Material: {material_properties_attachment.name} {material_properties_attachment.type}")
material_details = [material_properties_attachment.name, material_properties_attachment.type]
material_number += 1

if not first_iteration:
    master_json_data = save_data(master_json_data)
    margin_list = []
    mass_list = []
    margin_details = []
    input_details = []
    material_details = []

for width_step in np.linspace(left['width'], right['width'], steps['width']):
    for w_over_d_step in np.linspace(left['w_over_d'], right['w_over_d'], steps['w_over_d']):
        for lug_thickness_step in np.linspace(left['lug_thickness'], right['lug_thickness'], steps['lug_thickness']):
            for plate_thickness_step in np.linspace(left['plate_thickness'], right['plate_thickness'], steps['plate_thickness']):
                for wall_thickness_step in np.linspace(left['wall_thickness'], right['wall_thickness'], steps['wall_thickness']):
                    for inner_diameter_step in np.linspace(left['inner_diameter'], right['inner_diameter'], steps['inner_diameter']):
                        for outer_diameter_step in np.linspace(left['outer_diameter'], right['outer_diameter'], steps['outer_diameter']):
                            for horizontal_spacing_step in np.linspace(left['horizontal_spacing'], right['horizontal_spacing'], steps['horizontal_spacing']):
                                if inner_diameter_step < outer_diameter_step:
                                    start_time = time.time()
                                    # Iteration
                                    hole_diameter_step = 0.01
                                    height_step = w_over_d_step * hole_diameter_step
                                    iteration_data = iteration(master_json_data, step, width_step, height_step, lug_thickness_step,
                                                               plate_thickness_step, wall_thickness_step, hole_diameter_step, inner_diameter_step,
                                                               outer_diameter_step, horizontal_spacing_step, margin_list, mass_list)

                                    step += 1

                                    if iteration_data is not None:
                                        master_json_data = iteration_data

                                    if step % 100 == 0:
                                        print(f"Step {step}; Percentage finished {round((step * 100) / total_iterations, 2)} %")

                                    if first_iteration:
                                        delta_time = time.time() - start_time
                                        print(f"expected time = {round((delta_time * total_iterations) / 60, 2)} min")
                                        first_iteration = False

save_data(master_json_data)

plt.plot(margin_list, mass_list, 'o')
plt.show()
