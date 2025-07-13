from Models.Vector3D import Vector3D

class Ray:
    # the point of the ray is to represent a ray in 3D space
    # it is defined by its origin and direction
    # the origin is the point where the ray starts
    # the direction is the vector that points in the direction of the ray
    # the ray is used to calculate the intersection with objects in the scene
    # the point_at method is used to calculate the point at a given distance t along the ray
    def __init__(self, origin: Vector3D, direction: Vector3D):
        self.origin = origin
        self.direction = direction.normalize()
    
    def point_at(self, t: float) -> Vector3D:
        # Calculate the point at distance t along the ray
        # so what is self.direction.scalar_multiply(t) ?
        # it is the vector that points in the direction of the ray, scaled by t
        # and what is self.origin.add(...) ?
        return self.origin.add(self.direction.scalar_multiply(t))