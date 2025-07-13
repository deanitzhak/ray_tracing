from Models.Vector3D import Vector3D
from Models.Objects.Ray import Ray
BIAS = 1e-4  
class Scene:
    # the Phong midel is used for shading/lighting
    # is basded on some calculations
    # the furmula is:
    # I = k_a * I_a + k_d * I_d * max(0, N . L) + k_s * I_s * max(0, R . V)^n
    # where:
    # I = intensity of the light
    # k_a = ambient coefficient
    # I_a = intensity of the ambient light
    # k_d = diffuse coefficient
    # I_d = intensity of the diffuse light
    # N = normal vector of the surface
    # L = light vector (from the surface to the light)
    # V = view vector (from the surface to the camera)
    # R = reflection vector (from the light to the camera)
    # n = shininess coefficient (specular exponent)
    # the light is a vector, so we need to use the dot product
    def __init__(self):
        self.objects = []
        self.lights = []
        self.point_lights = []
        self.ambient_light = None
        self.background_color = Vector3D(0, 0, 0)  
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def add_light(self, light):
        self.lights.append(light)
        
    def add_point_light(self, point_light):
        # the ponint of light-point formula is different from the light formula
        # so we need to add a new list for point lights
        self.point_lights.append(point_light)
    
    def set_ambient_light(self, ambient):
        self.ambient_light = ambient
        
    def find_nearest_intersection(self, ray):
        # it may be better if no skip it and rander recognize it as plane
        # For regular objects (positive radius)
        nearest_object = None
        nearest_t = float('inf')
        nearest_point = None
        nearest_normal = None
        # Process foreground objects first (positive radius)
        # so if the redius is negative, we skip it
        # this is to avoid the background objects being hit firstq
        for obj in self.objects:
            if hasattr(obj, 'radius') and obj.radius < 0:
                # it may be as a plane, in the firsr scene its good for now 
                continue
            # Check intersection with the ray
            # so what is obj.intersect(ray) ?
            # it is a method that checks if the ray intersects with the object
            # it returns a tuple of (hit, t, hit_point, normal)
            # where hit is a boolean indicating if the ray intersects with the object
            # t is the distance from the ray origin to the intersection point
            hit, t, hit_point, normal = obj.intersect(ray)
            # If there is an intersection and it's closer than the current nearest
            # intersection, update the nearest object and its properties
            # so what is hit and t < nearest_t ?
            # it is checking if the ray hit the object and if the distance t is less than the current nearest_t
            # if hit is True, it means the ray intersects with the object
            if hit and t < nearest_t:
                nearest_object = obj
                nearest_t = t
                nearest_point = hit_point
                nearest_normal = normal
        # If no foreground hit, find the FARTHEST background object (negative radius)
        # This creates a more consistent background from multiple spheres
        if nearest_object is None:
            farthest_object = None
            farthest_t = -float('inf') 
            # nearest_point = None
            for obj in self.objects:
                if not hasattr(obj, 'radius') or obj.radius >= 0:
                    continue
                # Check intersection with the ray
                # so what is obj.intersect(ray) ?  
                # it is a method that checks if the ray intersects with the object
                # it returns a tuple of (hit, t, hit_point, normal)
                # where hit is a boolean indicating if the ray intersects with the object   
                # # t is the distance from the ray origin to the intersection point
                # # so we need to check if the ray intersects with the object
                # # # if it does, we need to update the farthest_object and farthest_t
                # # # if it does not, we need to skip it    
                hit, t, hit_point, normal = obj.intersect(ray)
                if hit and t > farthest_t:  
                    farthest_object = obj
                    farthest_t = t
                    nearest_point = hit_point  
                    nearest_normal = normal
            # If no foreground hit, use the farthest background object
            # so what is nearest_object = farthest_object ?            
            nearest_object = farthest_object
            nearest_t = farthest_t if farthest_object else float('inf')
        # return the nearest object, its intersection distance, hit point, and normal
        # so we return nearest_object, nearest_t, nearest_point, nearest_normal
        return nearest_object, nearest_t, nearest_point, nearest_normal
        
    def is_in_shadow(self, P, L, max_dist):
        # so what is the perpose of this method ?
        # it is to check if the point P is in shadow of any object
        # it does this by casting a shadow ray from the point P in the direction of the light L
        # and checking if it intersects with any object
        # if it does, it means that the point P is in shadow
        # and if it does not, it means that the point P is not in shadow
        # so what is max_dist ?
        # it is the maximum distance to check for intersection
        # it is used to limit the distance of the shadow ray
        # Create a shadow ray from point P in the direction of light L

        # so what is BIAS ?
        # # it is a small value to avoid self-intersection
        # # it is used to offset the origin of the shadow ray slightly away from the surface point P
        # # to avoid self-intersection issues
        # if the intersection point is very close to the surface point P
        # it will cause self-intersection issues
        # and get get infinite distance and rcursion 
        origin = P.add(L.scalar_multiply(BIAS))
        shadow_ray = Ray(origin, L)
        for obj in self.objects:
            hit, t, _, _ = obj.intersect(shadow_ray)
            if hit and 0 < t < max_dist:
                return True
        return False

    def calculate_phong_lighting(self, P, N, V, material):
        # the calculate_phong_lighting method computes the color at point P
        # based on the Phong reflection model
        # and the formula:
        # I = k_a * I_a + k_d * I_d * max(0, N . L) + k_s * I_s * max(0, R . V)^n
        # where:
        # I = intensity of the light
        # k_a = ambient coefficient
        # I_a = intensity of the ambient light
        # k_d = diffuse coefficient
        # I_d = intensity of the diffuse light
        # N = normal vector of the surface
        # L = light vector (from the surface to the light)
        # V = view vector (from the surface to the camera)
        col = Vector3D(0,0,0)
        if self.ambient_light:
            amb = self.ambient_light.intensity.hadamard(material.diffuse_color)
            col = amb.scalar_multiply(material.ambient_coef)
        # For every light (directional + point)
        for light in (self.lights + self.point_lights):
            L = light.get_direction(P)
            dist = light.get_distance(P)
            if self.is_in_shadow(P, L, dist):
                continue
            # Diffuse
            lam = max(0.0, N.dot_product(L))
            diff = light.get_intensity(P)\
                       .hadamard(material.diffuse_color)\
                       .scalar_multiply(material.diffuse_coef * lam)
            # Specular
            R = L.scalar_multiply(-1).reflect(N)
            sf = max(0.0, V.dot_product(R)) ** material.shininess
            spec = light.get_intensity(P).scalar_multiply(material.specular_coef * sf)
            col = col.add(diff).add(spec)
        return col.clamp()
