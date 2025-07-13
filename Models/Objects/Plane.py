import numpy as np
from Models.Vector3D import Vector3D
from Models.Objects.Object import Object 
from Models.Objects.Ray import Ray

DENOMINATOR_EPSILON = 1e-6  # Small value to avoid division by zero
class Plane(Object):   
    # the plane class is used to represent a plane in 3D space
    # it inherits from the Object class and implements the intersect method 
    def __init__(self, normal: Vector3D, d: float, color: Vector3D):
        super().__init__(color)
        self.normal = normal.normalize()  
        self.unnormalized_normal = normal
        self.d = d
        
    def intersect(self, ray: Ray) -> tuple:
        # Calculate intersection of ray with the plane
        # The plane equation is: n . (p - p0) = 0
        # where n is the normal vector, p is the point on the plane, and p0 is a point on the plane
        denominator = ray.direction.dot_product(self.normal)
        # If denominator is close to 0, ray is parallel to the plane
        if abs(denominator) < DENOMINATOR_EPSILON:
            # to perpose the ray is not intersecting the plane
            # so we return False, inf, None, None
            # inf is used to indicate that there is no intersection
            return False, float('inf'), None, None
        # Calculate t using the plane equation
        # t = -(n . p0 + d) / (n . d)
        # where n is the normal vector, p0 is the ray origin, and d is the plane constant
        # so what is self.normal.dot_product(ray.origin) ?
        # it is the dot product of the normal vector and the ray origin
        t = -(self.normal.dot_product(ray.origin) + self.d) / denominator
        # If t is negative, intersection is behind the ray origin
        # so we return False, inf, None, None
        if t < 0:
            return False, float('inf'), None, None
        # Calculate intersection point and normal
        # The intersection point is the point on the ray at distance t
        # so what is ray.point_at(t) ?
        # it is the point at distance t along the ray
        intersection_point = ray.point_at(t)
        # why to use self.normal.scalar_multiply(-1) ?
        # because the normal vector points outward from the plane
        # and we want the normal to point towards the ray origin
        normal = self.normal
        # If the denominator is positive, the normal points away from the ray origin
        # If the denominator is negative, the normal points towards the ray origin
        # so we need to invert the normal vector
        if denominator > 0:
            normal = normal.scalar_multiply(-1)  
        # Return intersection status, distance t, intersection point, and normal
        # so we return True, t, intersection_point, normal
        # True indicates that the ray intersects the plane
        # and t is the distance from the ray origin to the intersection point
        return True, t, intersection_point, normal
    
    def get_surface_properties(self, point: Vector3D) -> tuple:
        # For a plane, normal is constant regardless of hit point
        return self.normal, self.color