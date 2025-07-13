import numpy as np
from Models.Vector3D import Vector3D

class Pixel:
    # Pixel for 3D scene ray tracing.
    # Represents a pixel on the screen, including its position, color, and other attributes.
    def __init__(self, x: int, y: int, color: Vector3D):
        # Initialize pixel with position and color.
        self.x = x
        self.y = y
        self.color = color
        width = 1
        height = 1

    def set_color(self, color: Vector3D):
        # Set the pixel's color.
        self.color = color

    def get_color(self) -> Vector3D:
        # Get the pixel's color.
        return self.color