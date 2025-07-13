from Models.Vector3D import Vector3D
from Models.Lights.Light import Light

class DirectionalLight(Light):    
    # the DirectionalLight class represents a light source that emits light in a specific direction
    # it is defined by its direction and intensity
    def __init__(self, direction: Vector3D, intensity: Vector3D):
        super().__init__(intensity)
        self.direction = direction.normalize()
    
    def get_direction(self, point: Vector3D) -> Vector3D:
        return self.direction.scalar_multiply(-1)  # Negate because we want vector toward light
    
    def get_intensity(self, point: Vector3D) -> Vector3D:
        return self.intensity
    
    def get_distance(self, point: Vector3D) -> float:
        # the distance to a directional light is considered infinite
        # so we return a large value
        return float('inf')