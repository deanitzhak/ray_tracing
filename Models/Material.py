from Models.Vector3D import Vector3D

class Material:    
    # so how the Material class works?
    # the Material class represents the material of an object in the scene
    # it is defined by its diffuse color, ambient coefficient, diffuse coefficient, specular coefficient, and shininess
    # the diffuse color is the color of the object when it is lit by a light source
    # the ambient coefficient is the coefficient of the ambient light
    # the diffuse coefficient is the coefficient of the diffuse light
    # the specular coefficient is the coefficient of the specular light 
    # the shininess is the specular exponent that controls the shininess of the object
    def __init__(self, diffuse_color: Vector3D, ambient_coef: float = 0.4, 
                diffuse_coef: float = 1.0, specular_coef: float = 0.8, 
                shininess: float = 30.0):  
        self.diffuse_color = diffuse_color
        self.ambient_coef = ambient_coef
        self.diffuse_coef = diffuse_coef
        self.specular_coef = specular_coef
        self.shininess = shininess