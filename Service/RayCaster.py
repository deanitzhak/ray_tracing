from Models.Vector3D import Vector3D
from Models.Objects.Ray import Ray
import math

MAX_DEPTH =         1                   # Maximum recursion depth for ray tracing
BIAS =              1e-3                # Increased bias for better shadow accuracy at distance
SPECULAR_SCALE =    0.3                 # Keep disabled for matte look
SHADOW_DIFFUSE =    0.10                # Darker shadows but not too dark
REFLECTION_SCALE =  0.8                 # Reflection scale for glossy surfaces, keep disabled
BLACK_VECTOR =      Vector3D(0, 0, 0)   # Black vector for no color contribution
AMBIENT_MULTIPLIER = 0.15               # Ambient light multiplier for more subtle ambient effects
DEFAULT_VACTOR =    Vector3D(0, 0, 0)   # Default vector for no intersection
BIAS_MULTIPLIER =   5.00                # Bias multiplier for shadow calculations
class RayCaster:
    # RayCaster class for rendering scenes using ray tracing
    # the perpose of this class is to generate rays from the camera,
    # trace them through the scene, and calculate color values based on material properties and light sources.
    def __init__(self, camera, screen, scene):
        self.camera = camera
        self.screen = screen
        self.scene = scene
        self.aspect = screen.aspect_ratio
        self.scale = math.tan(math.radians(screen.fov * 0.5))

    def generate_ray(self, i, j):
        # Generate a ray from the camera through pixel (i, j) on the screen
        # Calculate pixel coordinates in normalized device coordinates
        # Adjusted for aspect ratio and field of view
        # it can be wrong
        px = (2 * (i + 0.5) / self.screen.width - 1) * self.aspect * self.scale
        py = (1 - 2 * (j + 0.5) / self.screen.height) * self.scale
        direction = Vector3D(px, py, -1).normalize()
        return Ray(self.camera.position, direction)

    def calcAmbient(self, material):
        # Calculate ambient light contribution
        # If no ambient light is set, return black
        if not self.scene.ambient_light:
            return BLACK_VECTOR
        # the porpose of the multiplier is to make the ambient light more subtle
        ambient_intensity = self.scene.ambient_light.intensity.scalar_multiply(AMBIENT_MULTIPLIER)
        # the hadamard product is used to multiply the ambient light intensity with the material's diffuse color
        # for a more realistic ambient effect
        return ambient_intensity.hadamard(material.diffuse_color).scalar_multiply(material.ambient_coef)

    def calcDiffuse(self, P, N, material, light):
        # so the calcDiffuse method calculates the diffuse lighting contribution at point P
        # given the normal N, material properties, and light source.
        # It uses the Lambertian reflectance model, which states that the intensity of light reflected
        L = light.get_direction(P)
        lambert = max(0.0, N.dot_product(L))
        return light.get_intensity(P).hadamard(material.diffuse_color).scalar_multiply(material.diffuse_coef * lambert)

    def calcSpecular(self, P, N, V, material, light):
        return DEFAULT_VACTOR

    def shade(self, ray, depth=0):
        # the shade method is responsible for determining the color at a point of intersection
        # so if the ray intersects an object in the scene, it calculates the color based on the material properties and light sources.
        # the formula of shade calculates : color = ambient + diffuse + specular whic is sigma of the light sources 
        obj, t, P, N = self.scene.find_nearest_intersection(ray)
        # the if statement checks if there is no intersection
        if not obj:
            return self.scene.background_color
        # if the depth is greater than the maximum depth, return the background color
        mat = obj.material
        # Ambient term
        color = self.calcAmbient(mat)
        # Process each light source
        # Loop through all lights in the scene, including point lights
        # and calculate the contribution of each light to the color at point P.
        # the for loop iterates through all lights in the scene, including point lights
        # by recursively calling the in_shadow method to check if the point is in shadow
        # PSUDOCODE:
        # for each light in scene.lights + scene.point_lights:
        #     L = light.get_direction(P)
        #    light_dist = light.get_distance(P) if hasattr(light, 'get_distance') else float('inf')
        #    shadow_origin = P.add(N.scalar_multiply(BIAS * BIAS_MULTIPLIER))
        #    in_shadow = self.in_shadow(shadow_origin, L, light_dist)
        #    if in_shadow:
        #        diff = self.calcDiffuse(P, N, mat, light).scalar_multiply(SHADOW_DIFFUSE)
        #        color = color.add(diff)
        #    else:
        #        diffuse = self.calcDiffuse(P, N, mat, light)
        #        color = color.add(diffuse)
        for i, light in enumerate(self.scene.lights + self.scene.point_lights):
            L = light.get_direction(P)
            # Calculate distance to light for point lights
            # if the light has a get_distance method, it is a point light
            # and we calculate the distance from the point P to the light source.
            if hasattr(light, 'get_distance'):
                light_dist = light.get_distance(P)
            else:
                light_dist = float('inf') 
            # Shadow calculation with improved bias
            shadow_origin = P.add(N.scalar_multiply(BIAS * BIAS_MULTIPLIER))
            # so if shadow_origin is the point P offset by the normal N scaled by a bias factor
            # to avoid self-shadowing artifacts, we check if the point is in shadow
            # by calling the in_shadow method with the shadow origin, light direction, and distance to the light.
            in_shadow = self.in_shadow(shadow_origin, L, light_dist)
            if in_shadow:
                # Darker shadows
                # calculate the diffuse term for shadows
                # if the point is in shadow, we calculate the diffuse term 
                # but with a reduced intensity to simulate shadowing effects.
                # the scalar_multiply method is used to scale the diffuse term by a shadow factor
                # to make the shadows darker but not too dark.
                # This is a more subtle shadow effect
                diff = self.calcDiffuse(P, N, mat, light).scalar_multiply(SHADOW_DIFFUSE)
                # Add the shadowed diffuse term to the color
                # the add method is used to add the shadowed diffuse term to the color
                color = color.add(diff)
            else:
                # if the point is not in shadow, we calculate the diffuse term normally
                # the calcDiffuse method is called to calculate the diffuse term
                # and the result is added to the color.
                # the diffuse term is calculated using the calcDiffuse method
                diffuse = self.calcDiffuse(P, N, mat, light)
                color = color.add(diffuse)
        # Clamp and return
        return color.clamp()

    def in_shadow(self, origin, light_dir, max_dist):
        # the is shadow method checks if a point is in shadow with respect to a light source.
        # It casts a shadow ray from the point towards the light source
        # and checks for intersections with objects in the scene.
        shadow_ray = Ray(origin, light_dir)
        # Set the maximum distance for shadow ray
        for obj in self.scene.objects:
            # the hit statement checks if the shadow ray intersects with any object in the scene
            # This method checks if and where the ray hits this object.
            # PSUDOCODE:
            # for each object in scene.objects:
            #     hit, t, _, _ = obj.intersect(shadow_ray)
            # If the ray hits an object, we check the distance t
            # to determine if the intersection is within the shadow bounds.
            # If the ray hits an object, we check the distance t
            # to determine if the intersection is within the shadow bounds.
            hit, t, _, _ = obj.intersect(shadow_ray)
            # More precise shadow bounds checking
            if hit and BIAS < t < (max_dist - BIAS * 2):
                return True
        return False