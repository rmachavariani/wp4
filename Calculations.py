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

for i in range(10):
    try:
        print(f"{i + 1}; Loading variables")
        json_data = master_json_data['iterations']

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
        width = float(lug_data['width_plate']) + 0.01
        height = float(lug_data['height']) + 0.01
        plate_thickness = float(lug_data['thickness_plate']) + 0.01
        wall_thickness = float(vehicle_wall_data['thickness'])

        if material_properties_attachment.material_type.strip().lower() == "metal":
            material = 1
        elif material_properties_attachment.material_type.strip().lower() == "composite":
            material = 2
        else:
            print(f"Material type '{material_properties_attachment.material_type}', does not exist")
            break

        # Stresses
        allowable_stress = material_properties_attachment.yield_stress
        wall_allowable_stress = material_properties_vehicle.yield_stress

        lug_thickness = float(lug_data['thickness_lug'])
        lug_length = float(lug_data['length_lug'])
        lug_density = float(lug_data['density'])
        hole_diameter = float(lug_data['hole_diameter'])

        # Fastener data
        inner_diameter = float(fastener_data['inner_diameter']) + 0.002
        outer_diameter = float(fastener_data['outer_diameter']) + 0.002
        edge_vertical = float(fastener_data['edge_vertical']) + 0.003
        horizontal_spacing = float(fastener_data['horizontal_spacing']) + 0.01
        fastener_density = float(fastener_data['density'])
        area = m.pi*((outer_diameter/2)**2)

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
        print(f"{i + 1}; Calculating with: width = {round(width, rv)},"  
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

        # Calculate thermal stresses
        thermal_stresses = Thermal_Stress.calc_thermal_stress(material_properties_vehicle, material_properties_attachment, material_properties_fastener, phi)

        # Do bearing check
        bearingCheck, coord_array, fastener_count = BearingCheck.bearing_check(height, outer_diameter, material, horizontal_spacing, area,
                                                                               plate_thickness, wall_thickness, allowable_stress, wall_allowable_stress, forces, thermal_stresses)

        print(f"{i + 1}; Bearing Check: {bearingCheck}")

        # Convert coordinates from point array to python list
        new_coordinates_array = []
        for fastener_coord in coord_array:
            new_coordinates_array.append([fastener_coord.x, fastener_coord.y])

        # Stress Modes Lug
        thickness_list = Stress_Modes_Lug.stress_mode_tension(material_properties_attachment, hole_diameter, lug_thickness, 2, forces[3][1])

        print(f"{i + 1}; Thickness list: {thickness_list}")

        # Pull through check
        margin_back_plate, margin_vehicle_plate = PullThroughCheck.pull_through(outer_diameter, inner_diameter, fastener_count, plate_thickness, wall_thickness,
                                                                                allowable_stress, wall_allowable_stress, new_coordinates_array, forces[3][1], moments[3][2])

        print(f"{i + 1}; Pull Through Check: {margin_back_plate}, {margin_vehicle_plate}")

        # Weight
        mass_fastener = Weight.calc_mass_fasteners(plate_thickness, wall_thickness, outer_diameter, fastener_density)
        mass_attachment = Weight.calc_mass_attachment(plate_thickness, width, height, fastener_count, inner_diameter, lug_thickness, lug_length, hole_diameter, lug_density)

        print(f"{i + 1}; Weight = {mass_fastener} + {mass_attachment} = {mass_fastener + mass_attachment}")

        # Update json file
        json_data['output']['bearing_check']['margins']['plate'] = bearingCheck[0]
        json_data['output']['bearing_check']['margins']['wall'] = bearingCheck[1]

        # Add pull through check
        for n, margin in enumerate(margin_back_plate):
            json_data['output']['pull_check']['margins']["plate-{}".format(n + 1)] = str(margin)

        for n, margin in enumerate(margin_vehicle_plate):
            json_data['output']['pull_check']['margins']["wall-{}".format(n + 1)] = str(margin)

        # Write back to document
        new_json_data = {str(int(last_key) + 1): json_data}

        master_json_data['iterations'].update(new_json_data)
        print("")

    except ValueError:
        print("Error occurred, moving on to the next iteration")
        continue

with open('data_iterations.json', 'w+') as j:
    json.dump(master_json_data, j, indent=4, sort_keys=True)
