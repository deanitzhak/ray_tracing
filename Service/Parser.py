from Models.Vector3D                import Vector3D
from Models.Lights.AmbientLight     import AmbientLight
from Models.Lights.DirectionalLight import DirectionalLight
from Models.Lights.PointLight       import PointLight
from Service.ParserServices         import analyze_scene_and_set_camera, assign_intensities_properly

def parse_file(path):
    # a struct to hold the scene data
    # its read the text file line by line 
    #e 0.0 0.0 4.0 0.0      # the e is the camera position
    #a 0.1 0.2 0.3 1.0      # the a is the ambient light
    #o 0.0 -0.5 -1.0 -3.5   # the o is an object (sphere or plane)
    #o -0.7 -0.7 -2.0 0.5 
    #o 0.6 -0.5 -1.0 0.5
    #c 0.0 1.0 1.0 10.0     # the c is the color and shininess
    #c 1.0 0.0 0.0 10.0     # which is in the format [r,g,b,shininess]
    #c 0.6 0.0 0.8 10.0     # and the index of the color is by the order of the objects
    #d 0.5 0.0 -1.0 1.0     # the d is a directional light
    #d 0.0 0.5 -1.0 0.0     # the 4th parameter is the intensity multiplier
    #p 2.0 1.0 3.0 0.6      # the p is a point light 
    #i 0.2 0.5 0.7 1.0      # the i is the intensity of the light
    #i 0.7 0.5 0.0 1.0      # the i is the intensity of the light
    scene_data = {
        'camera_pos':    None,
        'view_dir':      None,  # the view dict object is used to set the camera view direction
        'up_vec':        None,
        'fov':           None, #the FOV object is used to set the camera field of view
        'aspect':        None,
        'resolution':    None,
        'background':    None,
        'ambient_light': None,
        'camera_params': None,
        'objects':       [],   # [x,y,z,radius] or [nx,ny,nz,distance] for planes
        'colors':        [],   # [r,g,b,shininess]
        'lights':        [],   # directional lights
        'point_lights':  [],   # point lights
        'intensities':   [],   # [r,g,b,multiplier]
        'directional_params': [], # directional light parameters
        'type_of_lights':[],   # light type indicators
        'other':         []    # unrecognized commands
    }    
    # opening the file and rerading it line by line
    with open(path, 'r') as f:
        # parsing each lline 
        for line in f:
            # strip whitespace and ignore empty lines or comments
            L = line.strip()
            # if there is a comment or empty line, skip it
            if not L or L.startswith('#') or L.startswith('//'):
                continue
            # split the line into parts
            # the first part is the code, the rest are values
            parts = L.split()
            if len(parts) == 0:
                continue
            # the first part is the code what type of data it is
            # and the rest are the values
            # if the first part is not a recognized code, it will be added to the other list
            code = parts[0]
            # the calue part is the rest of the line
            vals = [float(x) for x in parts[1:]]
            if code == 'e':   # camera position
                scene_data['camera_pos'] = Vector3D(*vals[:3])
                scene_data['camera_params'] = vals
            elif code == 'v': # view direction
                # the point of normalizing is to ensure the view direction is a unit vector
                # the direction is driven by the first 3 values
                scene_data['view_dir'] = Vector3D(*vals[:3]).normalize()
            elif code == 'u':
                # u is not recognized in the txt file, but it is used to set the up vector
                # and it is normalized to ensure it is a unit vector
                # the up vector is used to define the camera orientation
                scene_data['up_vec'] = Vector3D(*vals[:3]).normalize()

            elif code == 'f': 
                # the filed view is use to set the field of view
                # it is the first value in the list
                scene_data['fov'] = vals[0]
            elif code == 't': # aspect ratio
                # the aspect ratio is the first value in the list
                # it is used to define the aspect ratio of the scene
                # i think my ratio of the filed is not best 
                scene_data['aspect'] = vals[0]

            elif code == 'r': # resolution
                # resulution is not the recognized in the txt file, but it is used to set the resolution
                # but is used to define the resolution of the scene
                scene_data['resolution'] = (int(vals[0]), int(vals[1]))

            elif code == 'b': # background color also not recognized in the txt file
                # the background color is the first 3 values in the list
                # for now the background color is not used in the scene
                # but it is used to define the background color of the scene
                scene_data['background'] = Vector3D(*vals[:3])
            elif code == 'a': # ambient light 
                # the ambient light is the first 3 values in the list
                # and the 4th value is the ambient coefficient (ka)
                # the ambient light is used to define the ambient light of the scene
                # i desdecided to use a scalar multiplication of the ambient light color
                # with the ambient coefficient to get the final ambient light color
                r, g, b = vals[:3]
                ka = vals[3] if len(vals) > 3 else 1.0
                scene_data['ambient_light'] = AmbientLight(
                    Vector3D(r, g, b).scalar_multiply(ka)
                )
            elif code == 'o':
                # object definition
                # as we can understand from the code, it can be a sphere or a plane
                # if the radius is negative, it is a plane
                # if the radius is positive, it is a sphere
                scene_data['objects'].append(vals)
                obj_type = "plane" if len(vals) > 3 and vals[3] < 0 else "sphere"

            elif code == 'c': # color + shininess
                # the color is the first 3 values in the list
                # and the 4th value is the shininess coefficient
                # the color is used to define the color of the object
                scene_data['colors'].append(vals)
                print(f"DEBUG: Added color: {vals}")

            elif code == 'd': # directional light
                dx, dy, dz = vals[:3]
                # Create light with placeholder intensity (will be set later)
                light = DirectionalLight(Vector3D(dx, dy, dz), Vector3D(1, 1, 1))
                # Use 4th value as intensity multiplier if available
                scene_data['lights'].append(light)
                # Store directional parameters for later use
                scene_data['directional_params'].append(vals)

            elif code == 'p': # point light - CONSERVATIVE PARSING
                # Point light parameters: position (px, py, pz) and optional attenuation/intensity multiplier
                # Ensure we have at least 3 values for position
                px, py, pz = vals[:3]
                # Conservative interpretation of 4th parameter
                if len(vals) > 3:
                    fourth_param = vals[3]
                    # if the fourth parameter is less than 0.1, it is treated as attenuation
                    if fourth_param < 0.1:
                        att = fourth_param
                        intensity_mult = 1.0
                        # the light type is set to point
                        light_type = "point"
                    else:  
                        # on the else section if the fourth parameter is greater than 0.1
                        # it is treated as intensity multiplier
                        # and we set the attenuation to a conservative value
                        # and the light type to normal
                        att = 0.02 
                        intensity_mult = fourth_param
                        # and it define as noraml light type
                        light_type = "normal"
                else:
                    # If no 4th parameter, use conservative defaults
                    # Attenuation is set to a conservative value
                    # i decide to use a small value for attenuation
                    # and the intensity multiplier is set to 1.0
                    att = 0.02
                    intensity_mult = 1.0
                    # and the light type is set to point
                    light_type = "point"
                
               # the point of using this if is for conservative positioning
                # If position is (0, 0, 0), use conservative positioning
                # to ensure the light is placed in a predictable location
                if px == 0.0 and py == 0.0 and pz == 0.0:
                    light_positions = [
                        Vector3D(1.0, 1.0, 0.3),    # Right elevated, moderate distance
                        Vector3D(-1.0, 1.0, 0.3),   # Left elevated, moderate distance
                        Vector3D(0.0, 0.5, 0.2)     # Center, slightly forward
                    ]
                    # initilaize the position based on the number of point lights already defined
                    # conservative positioning to avoid overlap
                    pos_idx = len(scene_data['point_lights'])
                    position = light_positions[pos_idx % len(light_positions)]
                else:
                    # else uuse the original position from the file
                    # and the position is set to the original position
                    position = Vector3D(px, py, pz)
                # Create point light with conservative settings 
                # and the intensity is set to the original intensity from the file
                # and the attenuation is set to the original attenuation from the file
                # and the light type is set to the original light type from the file
                point_light = PointLight(position, Vector3D(1, 1, 1), att)
                # the point of using this if is to set the intensity multiplier
                # if the intensity multiplier is not set, it is set to 1.0
                point_light.intensity_multiplier = intensity_mult
                point_light.light_type = light_type
                # Store the point light in the scene data
                scene_data['point_lights'].append(point_light)
            elif code == 'i': # light intensity
                # the intensity is the first 3 values in the list
                # and the 4th value is the intensity multiplier
                # the intensity is used to define the intensity of the light
                # and it is used to define the intensity of the light
                scene_data['intensities'].append(vals)

            elif code == 'l': 
                # type of light definition
                # this is used to define the type of light
                scene_data['type_of_lights'].append(vals)

            else:
                # otherwise, add to other list
                # this is used to define the other data in the scene
                scene_data['other'].append((code, vals))
    # total defined lights
    # the point of using the total defined lights is to check if there are any lights defined in the scene
    # and if there are no lights defined, we will add a default light
    total_defined_lights = len(scene_data['lights']) + len(scene_data['point_lights'])
    
    if total_defined_lights == 0:
        # iif the total light is 0, we will add a default light
        # so the default light is a directional light
        if scene_data['intensities']:
            default_light = DirectionalLight(Vector3D(0, 0.5, -1), Vector3D(1, 1, 1))
            scene_data['lights'].append(default_light)
            scene_data['directional_params'].append([0, 0.5, -1, 1.0])
        else:
            default_light = DirectionalLight(Vector3D(0, 0.5, -1), Vector3D(1, 1, 1))
            scene_data['lights'].append(default_light)
            scene_data['directional_params'].append([0, 0.5, -1, 1.0])
            scene_data['intensities'].append([0.6, 0.6, 0.6, 1.0])  # Conservative default
    # Assign intensities to lights properly
    # this function will assign the intensities to the lights properly
    # using conservative scaling to preserve original scene lighting balance
    assign_intensities_properly(scene_data)
    # Analyze scene geometry and set camera position intelligently
    # this function will analyze the scene geometry and set the camera position intelligently
    analyze_scene_and_set_camera(scene_data)
    # Print comprehensive scene data
    print("\nParsed Scene Data:")
    for key, value in scene_data.items():
        if key == "other" and value:
            print(f"  {key}:")
            for code, vals in value:
                print(f"    {code} -> {vals}")
        elif isinstance(value, list):
            print(f"  {key} ({len(value)} items):")
            for item in value:
                print(f"    - {item}")
        else:
            print(f"  {key}: {value}")
    print("END Parsed Scene Data")
    # Final light debug output
    print("\n=== LIGHT DEBUG ===")
    for i, light in enumerate(scene_data['lights']):
        print(f"Directional Light {i}: intensity={light.intensity}")
    for i, light in enumerate(scene_data['point_lights']):
        print(f"Point Light {i}: pos={light.position}, intensity={light.intensity}")
    print("===================\n")
    return scene_data