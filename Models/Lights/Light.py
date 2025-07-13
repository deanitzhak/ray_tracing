from Models.Vector3D import Vector3D
from abc import ABC, abstractmethod

class Light(ABC):    
    # An abstract base class for all light sources in the scene.
    def __init__(self, intensity: Vector3D):
        self.intensity = intensity
    
    @abstractmethod
    def get_direction(self, point: Vector3D) -> Vector3D:
        pass
    
    @abstractmethod
    def get_intensity(self, point: Vector3D) -> Vector3D:
        pass
    
    @abstractmethod
    def get_distance(self, point: Vector3D) -> float:
        pass

