from Models.Vector3D import Vector3D
from Models.Scene import Scene
from Models.Camera import Camera
from Models.Screen import Screen

from Handler.ScreenHandler import ScreenHandler
from Models.Lights.DirectionalLight import DirectionalLight

BASE_PLANE_DISTANCE =               0.05  # Base distance for camera placement
EXTRA_PLANE_DISTANCE_PER_OBJECT =   0.01  # Extra distance per object for camera placement
CLOSE_CAMERA_THRESHOLD =            2.5   # Threshold for close camera adjustment 
FAR_CAMERA_THRESHOLD =              3.5   # Threshold for far camera adjustment


MIN_CAMERA_DISTANCE =               0.1   # Minimum camera distance to objects
MAX_CAMERA_DISTANCE =               0.3   # Maximum camera distance to objects
MIN_FOV =                           45.0  # Minimum FOV
MAX_FOV =                           70.0  # Maximum FOV

MIN_SPHERE_BOUNDARY_DISTANCE =      0.02  # MINIMUM distance from sphere boundary
ADD_SPHERE_DISTANCE =               0.08  # MAXIMUM ADD SPHERE TO CAMERA
ADDJUSTED_CAMERA_Y =                0.2   # Increased elevation
MIN_CAMERA_Z =                      0.1   # MAX CLOSSNESS TO OBJECTS
MID_CAMERA_Z =                      0.2   # MID CAMERA Z for moderate scenes
SLIGHTLY_WIDER_FOV =                65.0  # Slightly wider FOV for better visibility
DEFAULT_CAMERA_Z =                  -1    # Default camera Z position for scenes without specific camera settings
SCREEN_WIDTH =                      800
SCREEN_HEIGHT =                     800
def calculate_adaptive_distance(original_z, object_count, max_plane_dist):
    # the point of the calculate_adaptive_distance function is to calculate the adaptive distance
    # why do we need to calculate the adaptive distance?
    # because we want to adjust the camera distance based on the scene characteristics
    # so the adaptive distance is calculated based on the original camera position
    # and the number of objects in the scene
    # the adaptive distance is calculated based on the original camera position
    # Base distance calculation - MAXIMUM CLOSENESS reduction for extreme detail
    base_distance = BASE_PLANE_DISTANCE
    # IF Original Z is to close to camera adjust it 
    if original_z <= CLOSE_CAMERA_THRESHOLD:
        # Camera is very close - moderate distance boost (same multiplier, MAXIMUM-small base)
        # This ensures cameras are not too close to objects
        # and can capture more detail without clipping
        # so the camera_multiplier is used to adjust the camera distance based on the original camera position
        camera_multiplier = 1.5 + (CLOSE_CAMERA_THRESHOLD - original_z) * 0.5
    elif original_z <= FAR_CAMERA_THRESHOLD:
        # Camera is moderately close - small distance boost (same multiplier, MAXIMUM-small base)
        # This ensures cameras are not too far from objects
        # Camera is moderately close - small distance boost (same multiplier)
        camera_multiplier = 1.2 + (FAR_CAMERA_THRESHOLD - original_z) * 0.2
    else:
        # Camera is already reasonably positioned - minimal adjustment
        camera_multiplier = 1.0 + max(0, (4.5 - original_z) * 0.1)
    # Calculate complexity multiplier based on object count
    complexity_multiplier = 1.0 + (object_count - 3) * 0.15
    # Ensure complexity multiplier is not too large
    # Calculate final adaptive distance
    adaptive_distance = base_distance * camera_multiplier * complexity_multiplier
    # APPLY MAXIMUM CLOSENESS LIMITS - force cameras to stay EXTREMELY close
    adaptive_distance = max(MIN_CAMERA_DISTANCE, min(MAX_CAMERA_DISTANCE, adaptive_distance))
    
    return adaptive_distance

def calculate_adaptive_threshold(original_z, object_count):
    # so what is the point of the calculate_adaptive_threshold function?
    # the point of this function is to calculate the adaptive threshold
    # and why do we need to calculate the adaptive threshold?
    # because we want to adjust the camera threshold based on the scene characteristics
    # Base threshold - conservative for good object visibility 
    base_threshold = 1.5
    # Adjust threshold based on camera position and complexity
    if original_z <= CLOSE_CAMERA_THRESHOLD:
        # Very close cameras need higher threshold but not extreme 
        threshold = base_threshold + (object_count - 3) * 0.2
    else:
        # Farther cameras need lower threshold 
        threshold = base_threshold * 0.8
        # result is the max of the base threshold and the calculated threshold
    # Ensure threshold is within reasonable limits
    # not too low or too high
    return max(1.0, min(3.0, threshold))

def analyze_scene_and_set_camera(scene_data):
    # the point of using this analyze function is to intelligently set the camera position
    # based on the scene geometry, ensuring it is not too close to objects
    # and has a good view of the scene
    # so in that case if the camera is too close to any object
    # the i will love to handle it by moving the camera back
    # using adaptive distance calculation based on scene characteristics
    # for example the scene2
    # e 0.0 0.0 1.0 1.0 the camera is at z=1.0
    # so if z is so close its not a good view
    # for the scene2 the camera is at z=1.0
    # another example is scene3
    # e 0.0 0.0 1.0 1.0 the camera is at z=1.0
    if scene_data['camera_params'] and len(scene_data['camera_params']) >= 3:
        original_cam = scene_data['camera_pos']
        # Calculate scene characteristics for adaptive behavior
        total_objects = len(scene_data['objects'])
        original_z = abs(original_cam.z)
        # Debug output for original camera position and total objects
        print(f"DEBUG: Original camera z={original_z}, total objects={total_objects}")
        # ANALYZE SCENE GEOMETRY FOR INTELLIGENT CAMERA PLACEMENT
        if scene_data['objects']:
            # Separate planes and spheres
            plane_objects = [obj for obj in scene_data['objects'] if len(obj) > 3 and obj[3] < 0]
            sphere_objects = [obj for obj in scene_data['objects'] if len(obj) > 3 and obj[3] > 0]
            # if the camera is not need to be adjusted
            # so initially set it to False
            # and z to original cam z
            camera_needs_adjustment = False
            suggested_z = original_cam.z
            # if the scene has planes or spheres
            if plane_objects:
                # For planes: Check if camera is too close to any plane
                # Calculate distances from camera to each plane
                # Plane objects are expected to have at least 4 elements: x, y, z, and distance
                # Assuming plane objects are in the format: [x, y, z, distance]
                # where distance is the signed distance from the plane to the camera
                # Extract distances from plane objects
                plane_distances =   [abs(obj[3]) for obj in plane_objects]
                min_plane_dist =    min(plane_distances)
                max_plane_dist =    max(plane_distances)                
                # Calculate adaptive threshold and distance based on scene characteristics
                adaptive_threshold = calculate_adaptive_threshold(original_z, total_objects)
                adaptive_distance = calculate_adaptive_distance(original_z, total_objects, max_plane_dist)
                # Check if camera is inside the "room" (inside the scene) formed by planes
                camera_to_closest_plane = abs(original_cam.z) - min_plane_dist   
                # If camera is less than adaptive threshold from closest plane, move it back
                if camera_to_closest_plane < adaptive_threshold:
                    # Move camera to a safe distance from the scene
                    # using adaptive distance calculation instead of fixed value
                    suggested_z = max_plane_dist + adaptive_distance
                    camera_needs_adjustment = True
            elif sphere_objects:
                # For spheres: Use bounding box approach
                sphere_z_positions = [obj[2] for obj in sphere_objects]
                # Sphere objects are expected to have at least 4 elements: x, y, z, and radius
                # Assuming sphere objects are in the format: [x, y, z, radius]
                # Extract radii from sphere objects
                sphere_radii = [abs(obj[3]) for obj in sphere_objects]
                # Find furthest sphere boundary
                furthest_sphere_boundary = max(z + r for z, r in zip(sphere_z_positions, sphere_radii))
                # Calculate adaptive distance for spheres
                adaptive_distance = calculate_adaptive_distance(original_z, total_objects, furthest_sphere_boundary)
                # adjust camera if too close to furthest sphere
                # Check if camera is too close to the furthest sphere boundary
                if original_cam.z - furthest_sphere_boundary < MIN_SPHERE_BOUNDARY_DISTANCE:
                    suggested_z = furthest_sphere_boundary + adaptive_distance
                    camera_needs_adjustment = True
            # Apply camera adjustment if needed
            if camera_needs_adjustment:
                scene_data['camera_pos'] = Vector3D(
                    original_cam.x, 
                    original_cam.y + ADDJUSTED_CAMERA_Y,  
                    suggested_z
                )            
                # Calculate adaptive FOV based on distance and scene complexity
                distance_ratio = (suggested_z - MIN_CAMERA_DISTANCE) / (MAX_CAMERA_DISTANCE - MIN_CAMERA_DISTANCE)
                distance_ratio = max(0.0, min(1.0, distance_ratio))  # Clamp to 0-1                
                # Adaptive FOV calculation - adjusted for closer viewing
                base_fov = SLIGHTLY_WIDER_FOV - 10      # Start with narrower base for closer cameras
                fov_adjustment = distance_ratio * 10.0 
                scene_data['fov'] = max(MIN_FOV, min(MAX_FOV, base_fov + fov_adjustment))                
            else:
                # if there is no need to adjust the camera
                # then set the fov to base value
                scene_data['fov'] = SLIGHTLY_WIDER_FOV - 5                
        # Set other defaults
        # the view dict object is used to set the camera view direction
        if not scene_data['view_dir']:
            scene_data['view_dir'] = Vector3D(0, 0, -1)
        # the up_vec object is used to set the camera up vector
        if not scene_data['up_vec']:
            scene_data['up_vec'] = Vector3D(0, 1, 0)
        # the aspect ratio is used to set the camera aspect ratio
        if not scene_data['aspect']:
            scene_data['aspect'] = 1.0
        # the resolution is used to set the camera resolution        
        if not scene_data['resolution']:
            scene_data['resolution'] = (SCREEN_WIDTH, SCREEN_HEIGHT)
        # the camera params is used to set the camera parameters   
        return 
# so what is the point for the const Variables?
# the point of these constants is to provide default lighting configurations
# and intensity multipliers for different types of lights in the ray tracer
# why do we need these constants?
# because we want consistent lighting behavior across all scenes
# and we need fallback values when scenes don't define proper lighting
DEFAULT_COMMON_DIRECTIONAL_LIGHT =  DirectionalLight(Vector3D(0, 0.5, -1), Vector3D(1, 1, 1))
# Default directional light object used as fallback when no lights are defined in scene
# Direction: (0, 0.5, -1) provides top-down diagonal lighting for good object visibility
# Intensity: (1, 1, 1) provides neutral white light that works well with all materials
# This ensures scenes always have at least one light source for proper illumination
DEFAULT_COMMON_AMBIENT_LIGHT =      Vector3D(0.1, 0.1, 0.1)
# Default ambient light intensity for global scene illumination
# Low intensity (0.1) provides subtle fill lighting without washing out shadows
# Equal RGB values (0.1, 0.1, 0.1) maintain color neutrality in ambient lighting
# This prevents completely black shadows and adds realism to the lighting model
DIRECTIONAL_PARAMS =                [0, 0.5, -1, 1.0]
# Default directional light parameters: [x, y, z, intensity_multiplier]
# Direction (0, 0.5, -1) points diagonally down for natural top-lighting effect
# Intensity multiplier 1.0 provides standard brightness without boosting
# Used when creating fallback directional lights for scenes with missing light data
DIRECTIONAL_BOOST =                 0.8
# Intensity multiplier for directional lights to balance scene illumination
# Value 0.8 provides strong but not overwhelming directional lighting
# Lower than 1.0 to prevent directional lights from dominating the scene
# This ensures directional lights contribute properly without causing overexposure
POINT_BOOST =                       1.0
# Intensity multiplier for point lights to maintain proper light falloff
# Value 1.0 provides neutral intensity scaling for point light sources
# Point lights naturally attenuate with distance, so no reduction needed
# This maintains the intended brightness of point lights as specified in scene files
DEFAULT_SOFT_ATTAENUATION =         0.02
# Default attenuation coefficient for soft lighting effects
# Lower value (0.02) creates gradual light falloff for smooth illumination
# Used for spot lights and other soft lighting types
# This provides realistic light diminishing over distance without harsh cutoffs

DEFAULT_AREA_ATTAENUATION =         0.015
# Default attenuation coefficient for area lights
# Even lower value (0.015) creates very gradual falloff for area lighting
# Area lights should have softer transitions than point lights
# This simulates the distributed nature of area light sources
CONSERVATIVE_ATTAENUATION =         0.02
# Conservative default attenuation for general purpose lighting
# Safe fallback value (0.02) that works well with most light types
# Used when light type is undefined or unrecognized
# This ensures consistent lighting behavior across different light configurations
DEFAULT_SOFT_ATTAENUATION =         0.02  
DEFAULT_AREA_ATTAENUATION =         0.015  
CONSERVATIVE_ATTAENUATION =         0.02   
def assign_intensities_properly(scene_data):
    # the point of this function is to assign intensities to lights
    # and handle cases where lights or intensities are missing
    # or where the scene is not well defined
    # so the function will check if there are lights defined in the scene
    # and if there are intensities defined
    # if not it will add a default directional light
    # for illumination
    # the total lights are the sum of directional lights and point lights
    total_lights = len(scene_data['lights']) + len(scene_data['point_lights'])
    # the total intensities are the length of the intensities list
    total_intensities = len(scene_data['intensities'])    
    # CHECK FOR MISSING LIGHTS IN SCENE
    # if the total lights is zero
    # so it means there are no lights defined in the scene
    if total_lights == 0:
        if scene_data['intensities']:
            # If there are intensities defined, create a default directional light
            # why i decide to add a default directional light
            # because it will provide some illumination to the scene
            # 0.5 is a common default direction for directional lights
            # and -1 is a common default direction for directional lights
            default_light = DirectionalLight(DEFAULT_COMMON_DIRECTIONAL_LIGHT)
            scene_data['lights'].append(default_light)
            scene_data['directional_params'].append(DIRECTIONAL_PARAMS)
        else:
            return
    # Assign to directional lights
    for i, light in enumerate(scene_data['lights']):
        if i < len(scene_data['intensities']):
            intensity_data = scene_data['intensities'][i]
        else:
            # Reuse intensities cyclically if we have more lights than intensities
            # The formula is used to assign intensities to lights
            # so what is actually happening here is that
            # if there are more lights than intensities
            # then we will reuse the intensities cyclically
            # the modulus operator is used to cycle through the intensities
            intensity_data = scene_data['intensities'][i % len(scene_data['intensities'])]
        # if statement to check if the light has intensity multiplier
        # why i chose to use biggest intensity multiplier
        # because it will provide more illumination to the scene
        multiplier = intensity_data[3] if len(intensity_data) > 3 else 1.0
        light.intensity = Vector3D(
            intensity_data[0], 
            intensity_data[1], 
            intensity_data[2]
            # boosting the intensity by a constant factor
            # multiplier * DIRECTIONAL_BOOST
        ).scalar_multiply(multiplier * DIRECTIONAL_BOOST)
        # Debug output for light directions
        if i < len(scene_data['directional_params']):
            dir_params = scene_data['directional_params'][i]
            print(f"DEBUG: Directional Light {i}: direction=({dir_params[0]}, {dir_params[1]}, {dir_params[2]}), intensity={light.intensity}")
    # Assign to point lights with conservative settings
    # so actually what is happening here is that
    # we are assigning intensities to point lights
    for i, light in enumerate(scene_data['point_lights']):
        # Use cyclical intensity assignment
        # again the modulus operator is used to cycle through the intensities
        # if there are more point lights than intensities
        intensity_data = scene_data['intensities'][i % len(scene_data['intensities'])]
        # Check if light has stored intensity multiplier from parsing
        if hasattr(light, 'intensity_multiplier'):
            multiplier = light.intensity_multiplier
        else:
            # Default multiplier if not specified
            # againnnnnnnnnnnn why i chose to use 1.0 as default multiplier
            # because it will provide a reasonable default illumination
            multiplier = intensity_data[3] if len(intensity_data) > 3 else 1.0   
        light.intensity = Vector3D(
            intensity_data[0], 
            intensity_data[1], 
            intensity_data[2]
        ).scalar_multiply(multiplier * POINT_BOOST)
        # Set conservative attenuation
        # the attenuation is used to control the light falloff
        # so the attenuation is set based on the light type
        # if the light has light_type attribute
        # so the attenuation is used to control the light falloff
        # and if the light type is spot or area
        # then the attenuation is set to a lower value
        if hasattr(light, 'light_type'):
            if light.light_type == "spot":
                light.attenuation = DEFAULT_SOFT_ATTAENUATION
            elif light.light_type == "area":
                light.attenuation = DEFAULT_AREA_ATTAENUATION
            else:
                light.attenuation = CONSERVATIVE_ATTAENUATION
        else:
            light.attenuation = CONSERVATIVE_ATTAENUATION