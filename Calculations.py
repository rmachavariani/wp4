import json
import math as m

import Importer
import Thermal_Stress
import Fastener_type
import PullThroughCheck
import Stress_Modes_Lug
import BearingCheck
import Forces
import Weight

with open('data.json', 'r+') as j:
    master_json_data = json.load(j)

# Temp:
print(f"-- Importing materials --")
material_list = Importer.import_all_materials("material_sheet", ("metal", "none"))
material_properties_attachment = material_list[0]
material_properties_fastener = material_list[0]
material_properties_vehicle = material_list[4]
print(f"Done importing, starting iteration\n")


def iteration(json_file, it):
    # try:
    print(f"{it + 1}; Loading variables")
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
    width = float(lug_data['width_plate']) + step_sizes['width']
    height = float(lug_data['height'])
    plate_thickness = float(lug_data['thickness_plate'])
    wall_thickness = float(vehicle_wall_data['thickness'])

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

    lug_thickness = float(lug_data['thickness_lug'])
    lug_length = float(lug_data['length_lug'])
    lug_density = float(lug_data['density'])
    hole_diameter = float(lug_data['hole_diameter'])

    # Fastener data
    inner_diameter = float(fastener_data['inner_diameter'])
    outer_diameter = float(fastener_data['outer_diameter'])
    edge_vertical = float(fastener_data['edge_vertical'])
    horizontal_spacing = float(fastener_data['horizontal_spacing'])
    fastener_density = float(fastener_data['density'])
    area = m.pi * ((outer_diameter / 2) ** 2)

    # Append input to json iteration
    json_data['input']['lug']['width_plate'] = width
    json_data['input']['lug']['height'] = height
    json_data['input']['lug']['thickness_lug'] = plate_thickness
    json_data['input']['lug']['thickness_plate'] = plate_thickness
    json_data['input']['fastener']['inner_diameter'] = inner_diameter
    json_data['input']['fastener']['outer_diameter'] = outer_diameter
    json_data['input']['fastener']['edge_vertical'] = edge_vertical
    json_data['input']['fastener']['horizontal_spacing'] = horizontal_spacing

    rv = 5
    print(f"{it + 1}; Calculating with: width = {round(width, rv)},"
          f" height = {round(height, rv)},"  # w
          f" lug_thickness = {round(lug_thickness, rv)},"  # t1
          f" plate_thickness = {round(plate_thickness, rv)},"  # t2
          f" wall_thickness = {round(wall_thickness, rv)},"  # t3
          f" hole_diameter = {round(hole_diameter, rv)},"  # D1
          f" inner_diameter = {round(inner_diameter, rv)},"  # Dfi = D2
          f" outer_diameter = {round(outer_diameter, rv)},"  # Dfo 
          f" edge_vertical = {round(edge_vertical, rv)},"  # e1
          f" horizontal_spacing = {round(horizontal_spacing, rv)}")

    # Calculate forces
    forces, moments = Forces.calc_forces(mmoi, mass, body_size, solar_panel_com, torques, launch_acceleration)

    # Calculate phi from Fastener type
    phi = Fastener_type.Fastener_Type(plate_thickness, wall_thickness, inner_diameter, outer_diameter,
                                      material_properties_attachment.e, material_properties_fastener.e, material_properties_vehicle.e)

    if phi is None:
        print('Phi was not found')
        return

    # Calculate thermal stresses
    thermal_stresses = Thermal_Stress.calc_thermal_stress(material_properties_vehicle, material_properties_attachment, material_properties_fastener, phi)

    # Do bearing check
    bearing_check, coord_array, fastener_count = BearingCheck.bearing_check(height, outer_diameter, material_type, horizontal_spacing, area,
                                                                            plate_thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces, thermal_stresses)

    print(f"{it + 1}; Bearing Check: {bearing_check}")

    # Convert coordinates from point array to python list
    new_coordinates_array = []
    for fastener_coord in coord_array:
        new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

    # Stress Modes Lug
    w_over_d = height / hole_diameter  # 1 < w_over_d < 5
    thickness_list = Stress_Modes_Lug.stress_mode_tension(material_properties_attachment, hole_diameter, lug_thickness, w_over_d, forces[3][1])
    if not thickness_list:
        print('Thickness list could not be made')
        return

    print(f"{it + 1}; Thickness list: {thickness_list}")

    # Pull through check
    margin_back_plate, margin_vehicle_plate = PullThroughCheck.pull_through(outer_diameter, inner_diameter, fastener_count, plate_thickness, wall_thickness,
                                                                            allowable_stress, wall_allowable_stress, new_coordinates_array, forces[3][1], moments[3][2])

    print(f"{it + 1}; Pull Through Check: {margin_back_plate}, {margin_vehicle_plate}")

    # Mass
    mass_fastener = Weight.calc_mass_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density)
    mass_attachment = Weight.calc_mass_attachment(plate_thickness, width, height, fastener_count, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density)

    print(f"{it + 1}; Weight = {mass_fastener} + {mass_attachment} = {mass_fastener + mass_attachment}")

    # Update json file
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

    return master_json_data

    # except ValueError:
    #     print("Error occurred, moving on to the next iteration")


step_sizes = {"width": 0.01, "height": 0.01, "lug_thickness": 0.01, "plate_thickness": 0.01, "wall_thickness": 0.01,
              "hole_diameter": 0.01, "inner_diameter": 0.005, "outer_diameter": 0.005, "edge_vertical": 0.01, "horizontal_spacing": 0.01}

# Staring values
main_data = master_json_data['iterations']['1']['input']
width_step = float(main_data['lug']['width_plate'])
height_step = float(main_data['lug']['height'])
lug_thickness_step = float(main_data['lug']['thickness_lug'])
plate_thickness_step = float(main_data['lug']['thickness_plate'])
wall_thickness_step = float(main_data['vehicle_wall']['thickness'])
hole_diameter_step = float(main_data['lug']['hole_diameter'])
inner_diameter_step = float(main_data['fastener']['inner_diameter'])
outer_diameter_step = float(main_data['fastener']['outer_diameter'])
edge_vertical_step = float(main_data['fastener']['edge_vertical'])
horizontal_spacing_step = float(main_data['fastener']['horizontal_spacing'])

limit_values = {"width": 0.5, "height": 0.5, "lug_thickness": 0.2, "plate_thickness": 0.2, "wall_thickness": 0.2,
                "hole_diameter": 0.2, "inner_diameter": 0.01, "outer_diameter": 0.01, "edge_vertical": 0.5, "horizontal_spacing": 0.4}

i = 0
while width_step < limit_values['width']:
    width_step += step_sizes['width']
    while height_step < limit_values['height']:
        height_step += step_sizes['height']
        while lug_thickness_step < limit_values['lug_thickness']:
            lug_thickness_step += step_sizes['lug_thickness']
            while plate_thickness_step < limit_values['plate_thickness']:
                plate_thickness_step += step_sizes['plate_thickness']
                while wall_thickness_step < limit_values['wall_thickness']:
                    wall_thickness_step += step_sizes['wall_thickness']
                    while hole_diameter_step < limit_values['hole_diameter']:
                        hole_diameter_step += step_sizes['hole_diameter']
                        while inner_diameter_step < limit_values['inner_diameter']:
                            inner_diameter_step += step_sizes['inner_diameter']
                            while outer_diameter_step < limit_values['outer_diameter']:
                                outer_diameter_step += step_sizes['outer_diameter']
                                while edge_vertical_step < limit_values['edge_vertical']:
                                    edge_vertical_step += step_sizes['edge_vertical']
                                    while horizontal_spacing_step < limit_values['horizontal_spacing']:
                                        horizontal_spacing_step += step_sizes['horizontal_spacing']

                                        # Iteration
                                        iteration_data = iteration(master_json_data, i)
                                        print("")
                                        if iteration_data is not None:
                                            master_json_data = iteration_data

                                        i += 1

with open('data_iterations.json', 'w+') as j:
    json.dump(master_json_data, j, indent=4, sort_keys=True)
