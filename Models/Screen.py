import numpy as np
from Models.Pixel import Pixel
from Models.Vector3D import Vector3D
import math
class Screen:
    # Screen for 3D scene ray tracing.
    # Defines the screen's position, orientation, and projection parameters used to generate 
    # rays for rendering the scene from a specific viewpoint.
    def __init__(self, position_vector, look_at_vector, up_vector, fov, aspect_ratio, width, height):
        # Initialize screen with position, orientation, and projection parameters.
        self.position = position_vector
        self.look_at = look_at_vector
        self.up = up_vector
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.width = width
        self.height = height
        # Initialize pixels with black color
        self.pixels = [[Pixel(i, j, Vector3D(0, 0, 0)) for j in range(height)] for i in range(width)]
        # Default pixel size (in world units)
        # 2.0 because screen goes from -1 to 1 (width of 2)
        self.pixel_width = 2.0 / width
        self.pixel_height = 2.0 / height

    def set_position(self, position_vector):
        # Set the screen's position in 3D space.
        self.position = position_vector

    def set_look_at(self, look_at_vector):
        # Set the point the screen is looking at in 3D space.
        self.look_at = look_at_vector
    
    def set_up(self, up_vector):
        # Set the up direction for the screen.
        self.up = up_vector

    def set_fov(self, fov):
        # Set the field of view for the screen.
        self.fov = fov

    def set_aspect_ratio(self, aspect_ratio):
        # Set the aspect ratio for the screen.
        self.aspect_ratio = aspect_ratio

    def get_pixel(self, x, y):
        # Get the pixel at the specified coordinates.
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[x][y]
        else:
            raise IndexError(f"Pixel coordinates ({x}, {y}) out of bounds")

    def set_pixel_color(self, x, y, color):
        # Set the color of the pixel at the specified coordinates.
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x][y].set_color(color)
        else:
            raise IndexError(f"Pixel coordinates ({x}, {y}) out of bounds")
