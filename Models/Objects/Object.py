from abc import ABC, abstractmethod
from Models.Vector3D import Vector3D
from Models.Material import Material
class Object(ABC):
    # an abstract base class for all objects in the scene
    # it defines the basic properties and methods that all objects should have
    # such as color, material, and intersection methods
    def __init__(self, color: Vector3D, shininess: float = 10.0):
        self.color = color 
        self.material = Material(color, shininess=shininess)    
    @abstractmethod
    def intersect(self, ray) -> tuple:
        pass
    
    @abstractmethod
    def get_surface_properties(self, point: Vector3D) -> tuple:
        pass