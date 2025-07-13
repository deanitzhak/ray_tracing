from Models.Vector3D import Vector3D
from Models.Lights.Light import Light

class AmbientLight(Light):    
    def get_direction(self, point: Vector3D) -> Vector3D:
        return Vector3D(0, 0, 0)
    
    def get_intensity(self, point: Vector3D) -> Vector3D:
        return self.intensity
    
    def get_distance(self, point: Vector3D) -> float:
        return float('inf')