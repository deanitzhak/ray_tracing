import numpy as np
from Models.Vector3D import Vector3D
from Models.Objects.Object import Object
from Models.Objects.Ray import Ray

class Sphere(Object):    
    # so the spere class is used to represent a sphere in 3D space
    # it inherits from the Object class and implements the intersect method
    # the sphere is defined by its center, radius and color
    def __init__(self, center: Vector3D, radius: float, color: Vector3D):
        super().__init__(color)
        self.center = center
        self.radius = radius            # Store original radius (can be negative)
        self.is_inverted = radius < 0   # Flag for inverted spheres
        self.abs_radius = abs(radius)   # Store absolute value for calculations
    
    def intersect(self, ray: Ray) -> tuple:
        # Vector from ray origin to sphere center
        oc = ray.origin.subtract(self.center)
        # Quadratic equation coefficients
        # a = |d|^2, b = 2 * (o - c) . d, c = |o - c|^2 - r^2
        # where d is the ray direction, o is the ray origin, c is the sphere center, and r is the radius
        # Calculate coefficients for the quadratic equation
        a = ray.direction.dot_product(ray.direction)
        # so what is 2.0 * oc.dot_product(ray.direction) ?
        # it is the dot product of the vector from the ray origin to the sphere center and the ray direction
        # this is used to calculate the intersection point
        b = 2.0 * oc.dot_product(ray.direction)
        c = oc.dot_product(oc) - self.abs_radius * self.abs_radius
        # Calculate discriminant
        # so what is b * b - 4 * a * c ?
        # it is the discriminant of the quadratic equation
        # if the discriminant is negative, it means that there is no intersection
        # if the discriminant is positive, it means that there are two intersections
        # if the discriminant is zero, it means that there is one intersection
        discriminant = b * b - 4 * a * c
        # No intersection if discriminant is negative
        if discriminant < 0:
            # to perpose the ray is not intersecting the sphere
            # so we return False, inf, None, None
            # inf is used to indicate that there is no intersection
            # None is used to indicate that there is no hit point or normal
            return False, float('inf'), None, None 
        # Calculate closest intersection
        # again why use 2.0 * a ?
        # because we are solving the quadratic equation for t
        # t = (-b ± sqrt(discriminant)) / (2 * a)
        # Calculate the two possible intersection points
        t = (-b - np.sqrt(discriminant)) / (2.0 * a)
        # If intersection is behind the ray origin, try the other intersection
        if t < 0: 
            t = (-b + np.sqrt(discriminant)) / (2.0 * a)
            if t < 0: 
                return False, float('inf'), None, None
        # Calculate intersection point and normal
        hit_point = ray.point_at(t)
        # Calculate the normal at the hit point
        # The normal is the vector from the sphere center to the hit point, normalized
        # so what is hit_point.subtract(self.center) ?
        # it is the vector from the sphere center to the hit point
        # and normalize it to get the unit normal vector    
        normal = hit_point.subtract(self.center).normalize()
        # For inverted spheres (negative radius), invert the normal
        if self.is_inverted:
            # so what is normal.scalar_multiply(-1) ?
            # it is the normal vector multiplied by -1 to invert it
            # this is done to get the correct normal vector for inverted spheres
            normal = normal.scalar_multiply(-1)
        # Return intersection status, distance, hit point, and normal
        # so we return True, t, hit_point, normal
        # True indicates that there is an intersection
        return True, t, hit_point, normal  
    
    def get_surface_properties(self, point: Vector3D) -> tuple:
        # Calculate the normal at the given point on the sphere
        # The normal is the vector from the sphere center to the point, normalized
        # so what is point.subtract(self.center) ?
        # it is the vector from the sphere center to the point
        # and normalize it to get the unit normal vector
        # Normalize the vector from the sphere center to the point
        normal = point.subtract(self.center).normalize()
        # For inverted spheres, invert the normal
        if self.is_inverted:
            # so what is normal.scalar_multiply(-1) ?
            # it is the normal vector multiplied by -1 to invert it
            # this is done to get the correct normal vector for inverted spheres
            normal = normal.scalar_multiply(-1)
        # Return the normal and the sphere's color
        # so we return normal, self.color
        # True indicates that there is an intersection
        # and self.color is the color of the sphere
        return normal, self.color