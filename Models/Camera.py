import numpy as np
from Models.Vector3D import Vector3D

class Camera:
    #Camera for 3D scene ray tracing.
    #Defines position, orientation, and projection parameters used to generate 
    #rays for rendering the scene from a specific viewpoint.
    def __init__(self, postion_vector, look_at_vector, up_vector, fov, aspect_ratio):
        # Initialize camera with position, orientation, and projection parameters.
        self.position = postion_vector
        self.look_at = look_at_vector
        self.up = up_vector
        self.fov = fov
        self.aspect_ratio = aspect_ratio
    
    def set_position(self, position_vector):
        # Set the camera's position in 3D space.
        self.position = position_vector
    
    def set_look_at(self, look_at_vector):
        # Set the point the camera is looking at in 3D space.
        self.look_at = look_at_vector
    
    def set_up(self, up_vector):
        # Set the up direction for the camera.
        self.up = up_vector
    
    def set_fov(self, fov):
        # Set the field of view for the camera.
        # fov is the vertical field of view in degrees
        # convert it to radians for calculations
        # convert degrees to radians# fov = np.radians(fov)
        
        self.fov = fov

    
        
