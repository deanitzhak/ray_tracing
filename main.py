import sys
from Models.Vector3D       import Vector3D
from Models.Screen         import Screen
from Models.Camera         import Camera
from Models.Scene          import Scene
from Models.Objects.Sphere import Sphere
from Models.Objects.Plane  import Plane
from Models.Material       import Material
from Service.Parser        import parse_file
from Service.RayCaster     import RayCaster
from Handler.ScreenHandler import ScreenHandler
def add_lights(scene, data):
# the add light function can be use to add light sources to the scene
# or to set ambient light
# or to set point lights
# the point light formula is:
# I = I0 / (1 + a*d + b*d²)
# and the ambient light formula is:
# I = I0 * ambient_coef
    if data['ambient_light']:
        scene.set_ambient_light(data['ambient_light'])
    for dl in data['lights']:
        scene.add_light(dl)
    for pl in data['point_lights']:
        scene.add_point_light(pl)

def add_objects(scene, data):
    # the add objects function can be used to add objects to the scene
    # it can handle both spheres and planes
    # so in that case if the radius is negative it will be a plane
    # after alot of testing it was decided that the radius of the plane
    # will be the distance from the origin to the plane
    # and the normal will be the direction of the plane
    # if the radius is positive it will be a sphere
    # and the position will be the center of the sphere
    for i, (x,y,z,radius) in enumerate(data['objects']):
        # Get color and shininess for this object
        # If there are not enough colors, use default
        if i < len(data['colors']):
            # Unpack color and shininess
            # assuming colors are in the format (r, g, b, shininess)
            cr,cg,cb,shin =     data['colors'][i]
        else:
            # Default color and shininess
            # This is a fallback in case there are fewer colors than objects
            cr,cg,cb,shin =     1.0,1.0,1.0,10.0
        # Create color and material for the object
        # Using Vector3D for color and Material for shininess
        col =   Vector3D(cr,cg,cb)
        # Create material with color and shininess
        mat =   Material(col, shininess=shin)
        # Check if radius is negative or positive
        # If negative, create a plane; if positive, create a sphere
        # This is a simple way to differentiate between the two types of objects
        if radius < 0:
            # Background plane (negative radius)
            norm =          Vector3D(x,y,z).normalize()
            pl   =          Plane(norm, radius, col)
            pl.material =   mat
            scene.add_object(pl)
        else:
            # Regular sphere (positive radius)
            sph =           Sphere(Vector3D(x,y,z), radius, col)
            sph.material =  mat
            scene.add_object(sph)

def main():
    # parsing command through command line arguments
    # if no file is provided, default to 'scene1.txt'
    fn = sys.argv[1] if len(sys.argv) > 1 else 'scene1.txt'
    print(f"Loading scene file: {fn}")
    # data is parsed from the file
    # and will passed the to the parser function    
    data = parse_file(fn)
    # Extract camera and screen parameters
    cam_pos = data['camera_pos']
    look = data['view_dir']
    up = data['up_vec']
    fov = data['fov']
    asp = data['aspect']
    W, H = data['resolution']
    bg = data.get('background') or Vector3D(0.1, 0.1, 0.2)  # Dark blue default
    # ENHANCED DEBUG OUTPUT
    print(f"\n=== FINAL RENDER SETTINGS ===")
    print(f"Camera Position: {cam_pos}")
    print(f"Look Direction : {look}")
    print(f"Field of View  : {fov}")
    print(f"Resolution     : {W}x{H}")
    print(f"Background     : {bg}")
    print(f"Total Objects  : {len(data['objects'])}")
    print(f"Total Lights   : {len(data['lights']) + len(data['point_lights'])}")
    print(f"==============================\n")
    # Create screen, camera, and screen handler
    screen  = Screen(cam_pos, look, up, fov, asp, W, H)
    camera  = Camera(cam_pos, look, up, fov, asp)
    handler = ScreenHandler(screen, W, H)
    # Create and setup scene
    scene = Scene()
    scene.background_color = bg
    add_lights(scene, data)
    add_objects(scene, data)
    # Create ray caster
    caster = RayCaster(camera, screen, scene)
    # ENHANCED RENDERING with progress tracking
    hits = 0
    total_pixels = W * H
    print(f"Starting render of {total_pixels} pixels...")
    # so how this for loop works:
    # it iterates over each pixel in the screen
    # and generates a ray for each pixel
    # it then calculates the color for that pixel by calling the shade method
    # and sets the pixel color in the screen
    # PUSDOCODE:
    # for each pixel (i, j) in the screen:
    #     generate ray for pixel (i, j)
    #     calculate color for pixel (i, j) using ray
    #     set pixel color in screen 
    for j in range(H):
        if j % 100 == 0:
            print(f"Rendering row {j}/{H}")
        for i in range(W):
            # Generate ray for this pixel
            ray = caster.generate_ray(i, j)     
            # Calculate color for this pixel
            col = caster.shade(ray, depth=0) 
            # Set pixel color
            screen.set_pixel_color(i, j, col)
            # Count meaningful hits (not just background)
            if col.magnitude() > 0.1: 
                hits += 1
    # Print rendering statistics
    hit_percentage = (hits / total_pixels) * 100
    print(f"[Unified] {hits}/{total_pixels} meaningful pixels ({hit_percentage:.2f}%)")
    # Save the rendered image
    output_filename = f"render_{fn.replace('.txt', '')}.png"
    handler.save_image(output_filename)
    print(f"Image saved as: {output_filename}")

if __name__ == "__main__":
    main()