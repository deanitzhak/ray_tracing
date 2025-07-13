import math 
import numpy as np
import Models.Screen as Screen
import Models.Pixel as Pixel
import Models.Vector3D as Vector3D
from PIL import Image

class ScreenHandler:
    # ScreenHandler for 3D scene ray tracing.
    # Handles the screen's position, orientation, and projection parameters used to generate 
    # rays for rendering the scene from a specific viewpoint.
    def __init__(self, screen: Screen.Screen, width: int, height: int):
        # Initialize screen handler with screen object.
        self.screen = screen
        self.width = width
        self.height = height

    def print_Screen(self):
        # Print information about each pixel in the screen
        print(f"Screen dimensions: {self.width}x{self.height}")
        print(f"Pixel size: {self.screen.pixel_width:.6f}x{self.screen.pixel_height:.6f} world units")
        max_print = min(5, self.width) 
        for j in range(min(5, self.height)):  
            for i in range(max_print):
                pixel = self.screen.get_pixel(i, j)
                print(f"Pixel ({i}, {j}): Position = ({-1 + i*self.screen.pixel_width:.3f}, {1 - j*self.screen.pixel_height:.3f}), " +
                      f"Color = {pixel.get_color()}")
            
            if self.width > max_print:
                print("...")
        
        if self.height > 5:
            print("...")

    def generate_blue_image(self):
        # not in use 
        blue = Vector3D.Vector3D(0.0, 0.0, 1.0) 
        for y in range(self.height):
            for x in range(self.width):
                self.screen.set_pixel_color(x, y, blue)
    
    def generate_gradient_image(self):
        # not in use
        for y in range(self.height):
            for x in range(self.width):
                # Normalize coordinates to [0,1]
                r = x / self.width
                g = y / self.height
                b = 0.5  # Fixed blue component
                color = Vector3D.Vector3D(r, g, b)
                self.screen.set_pixel_color(x, y, color)
    
    def generate_checkerboard_image(self, size=50):
        # not in use
        for y in range(self.height):
            for x in range(self.width):
                # Determine if this is a dark or light square
                is_dark = ((x // size) + (y // size)) % 2 == 0
                
                if is_dark:
                    color = Vector3D.Vector3D(0.1, 0.1, 0.1)  # Dark gray
                else:
                    color = Vector3D.Vector3D(0.9, 0.9, 0.9)  # Light gray
                
                self.screen.set_pixel_color(x, y, color)
    
    def generate_position_based_image(self):
        # not in use
        for y in range(self.height):
            for x in range(self.width):
                # Calculate world space coordinates [-1,1]
                world_x = -1.0 + x * self.screen.pixel_width
                world_y = 1.0 - y * self.screen.pixel_height
                
                # Use these coordinates to drive the RGB values
                r = (world_x + 1) / 2  # Convert from [-1,1] to [0,1]
                g = (world_y + 1) / 2
                b = (r + g) / 2         # Just a function to create interesting colors
                
                color = Vector3D.Vector3D(r, g, b)
                self.screen.set_pixel_color(x, y, color)
        
    def save_image(self, filename="output.png"):
        # in use for saving the screen as an image file
        img = Image.new('RGB', (self.width, self.height))
        pixels = []
        
        for y in range(self.height):
            for x in range(self.width):
                color = self.screen.get_pixel(x, y).get_color()
                r = int(max(0, min(255, color.x * 255)))
                g = int(max(0, min(255, color.y * 255)))
                b = int(max(0, min(255, color.z * 255)))
                pixels.append((r, g, b))
        
        img.putdata(pixels)
        img.save(filename)

    