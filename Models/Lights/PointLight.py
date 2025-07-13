from Models.Vector3D import Vector3D
import math

class PointLight:
    def __init__(self, position, intensity, attenuation=0.01):
        self.position = position
        self.intensity = intensity
        self.attenuation = attenuation
        self.light_type = "point" 

    def get_direction(self, point):
        return self.position.subtract(point).normalize()

    def get_distance(self, point):
        return self.position.subtract(point).magnitude()

    def get_intensity(self, point):
        distance = self.get_distance(point)
        # Quadratic attenuation: I = I0 / (1 + a*d + b*d²)
        # Where a = linear attenuation, b = quadratic attenuation
        linear_att = self.attenuation
        # why use 0.1 for quadratic attenuation?
        # This is a smaller value to ensure the quadratic component has less impact
        # on the overall attenuation, making the light falloff more gradual.
        quadratic_att = self.attenuation * 0.1 
        # Calculate attenuation factor
        # so what is 1.0 / (1.0 + linear_att * distance + quadratic_att * distance * distance) ?
        # It is the attenuation factor that reduces the intensity of the light
        # based on the distance from the light source
        attenuation_factor = 1.0 / (1.0 + linear_att * distance + quadratic_att * distance * distance)
        # Clamp minimum attenuation to prevent complete darkness
        attenuation_factor = max(attenuation_factor, 0.01)
        return self.intensity.scalar_multiply(attenuation_factor)