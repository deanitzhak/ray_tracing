import math

class Vector3D:
    # This class represents a 3D vector using x, y, and z components.
    def __init__(self, x, y, z):
        # Initialize a vector with x, y, z components.
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def add(self, other):
        # Add two vectors component-wise.
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        # Subtract another vector from this one, component-wise.
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def scalar_multiply(self, scalar):
        # Multiply this vector by a scalar (single number).
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def scalar_projection(self, other):
        # The scalar projection (also called the component) of this vector onto another vector (other)
        # gives the length (as a scalar value) of this vector in the direction of 'other'.
        # It is calculated using the formula:
        #     scalar_proj = (self · other) / |other|
        # where:
        #     - self · other is the dot product of the two vectors
        #     - |other| is the magnitude (length) of the 'other' vector
        # This gives a signed value:
        #     - positive if self points in the same general direction as other,
        #     - negative if it points in the opposite direction,
        #     - zero if it's perpendicular.
        magnitude_other = other.magnitude()
        if magnitude_other == 0:
            return 0
        return self.dot_product(other) / magnitude_other

    def vector_multiply(self, other):
        # Alias for cross_product.
        return self.cross_product(other)

    def cross_product(self, other):
        # The cross product of two vectors results in a new vector that is
        # perpendicular to both original vectors.
        return Vector3D(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def dot_product(self, other):
        # The dot product (scalar product) returns a number (scalar) based on the angle between two vectors.
        # Computed as: u · v = u.x * v.x + u.y * v.y + u.z * v.z
        # It gives a measure of how much one vector extends in the direction of another.
        # If the vectors are orthogonal (perpendicular), the dot product is 0.
        # why do we need to use dot product?
        # The dot product is used in many applications, such as determining angles between vectors,
        # calculating projections, and in physics to find work done by a force.
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self):
        # The magnitude (length) of the vector, calculated using the 3D Pythagorean theorem:
        # |v| = √(x² + y² + z²)
        # where:
        # - x, y, z are the components of the vector.
        # This gives the length of the vector in 3D space.
        # so what is the purpose of magnitude?
        # The magnitude is used to understand the size of the vector,
        # which is important in many applications like physics simulations, graphics, and more.
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        # Normalize the vector (make it length 1) by dividing by its magnitude.
        # Useful for direction-only purposes.
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)

    def cosine(self, other):
        # Computes the cosine of the angle between two vectors.
        # cos(θ) = (u · v) / (|u||v|)
        mag_product = self.magnitude() * other.magnitude()
        if mag_product == 0:
            return 0
        return self.dot_product(other) / mag_product

    def sine(self, other):
        # Computes the sine of the angle between two vectors using the magnitude of their cross product.
        # sin(θ) = |u × v| / (|u||v|)
        mag_product = self.magnitude() * other.magnitude()
        if mag_product == 0:
            return 0
        return self.cross_product(other).magnitude() / mag_product

    def tangent(self, other):
        # Computes the tangent of the angle between two vectors.
        # tan(θ) = sin(θ) / cos(θ)
        cos = self.cosine(other)
        if cos == 0:
            return float('inf')
        return self.sine(other) / cos

    def reflect(self, normal):
        # Reflects the vector around a given surface normal.
        # reflection = incident - 2 * (incident · normal) * normal
        # where:
        # - incident is this vector
        # - normal is the surface normal vector
        # The normal vector should be normalized before calling this method.
        # where do i need to use this method?
        # This method is used in ray tracing or physics simulations to calculate how a vector (like light or a ball)
        dot_product = self.dot_product(normal)
        reflection = self.subtract(normal.scalar_multiply(2.0 * dot_product))
        return reflection
    
    def refract(self, normal, eta):
        # Computes the refracted vector based on Snell's law.
        # Supports total internal reflection.
        # Formula: r = (n * cos(θi) - cos(θt)) * n + v * (eta)
        # where:
        # - n is the normal vector
        # - θi is the angle of incidence
        # - θt is the angle of refraction
        # - v is the incident vector (this vector)
        # - eta is the ratio of indices of refraction (n1/n2)
        # so what is eta?
        # eta is the ratio of the indices of refraction between two media.
        # For example, if light is moving from air (n1 = 1.0) to glass (n2 = 1.5),
        # eta would be 1.0 / 1.5 = 0.6667.
        # The normal vector should be normalized before calling this method.
        cosi = max(-1, min(1, self.dot_product(normal)))
        etai = 1
        etat = eta
        n = normal
        if cosi < 0:
            cosi = -cosi
        else:
            etai, etat = etat, etai
            n = normal.scalar_multiply(-1)
        eta_ratio = etai / etat
        k = 1 - eta_ratio**2 * (1 - cosi**2)
        if k < 0:
            return Vector3D(0, 0, 0) 
        return self.scalar_multiply(eta_ratio).add(n.scalar_multiply(eta_ratio * cosi - math.sqrt(k)))

    def hadamard(self, other):
        # Element-wise multiplication between two vectors.
        # Used in shading for combining colors or light intensity.
        # so where and why do i need to use this method?
        # This method is used in graphics applications to combine colors or light intensities
        # by multiplying corresponding components of two vectors.
        # For example, if you have two RGB colors represented as vectors,
        # i can use this method to compute the resulting color by multiplying each component.
        # It returns a new vector where each component is the product of the corresponding components of the two vectors.
        return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)

    def clamp(self, min_val=0.0, max_val=1.0):
        # Clamp each component of the vector within [min_val, max_val].
        # Useful for keeping RGB or lighting values in range.
        # so what is the purpose of clamping?
        # Clamping is used to ensure that the vector components do not exceed certain limits,
        # which is especially important in graphics applications to prevent overflow or underflow.
        return Vector3D(
            max(min(self.x, max_val), min_val),
            max(min(self.y, max_val), min_val),
            max(min(self.z, max_val), min_val)
        )

    def point(self):
        # Returns the vector as a tuple (x, y, z), useful for plotting or APIs.
        return (self.x, self.y, self.z)

    def distance_to(self, other):
        # Computes the distance between this vector and another vector.
        # It uses the Euclidean distance formula:
        # distance = √((x2 - x1)² + (y2 - y1)² + (z2 - z1)²)
        return (self - other).magnitude()

    def angle_with(self, other):
        # the angel with another vector in radians.
        # It uses the cosine of the angle between the two vectors.
        cos_theta = self.cosine(other)
        return math.acos(max(-1, min(1, cos_theta)))  

    def point_at(self, t):
        # Multiplies the vector by a scalar t. Used in ray tracing to compute:
        # position = origin + direction * t
        # so where do i need to use this method?
        # It is used to find a point along the direction of the vector at distance t.
        # For example, in ray tracing, you can find the point at distance t along the ray's direction.
        return self.scalar_multiply(t)
    
    def reflect(self, normal):
        # Formula: r = v - 2(v·n)n
        # so what is v and n?
        # v is the incident vector (this vector),
        # n is the normal vector of the surface being reflected off.
        # where do i need to use this method?
        # This method is used to calculate the reflection of a vector off a surface defined by a normal vector.
        dot_product = self.dot_product(normal)
        reflected = self.subtract(normal.scalar_multiply(2.0 * dot_product))
        return reflected


    def negate(self):
        # Negates the vector (flips its direction).
        return Vector3D(-self.x, -self.y, -self.z)
    
    # Operator Overloads

    def __add__(self, other):
        # Allows usage of `+` operator
        return self.add(other)

    def __sub__(self, other):
        # Allows usage of `-` operator
        return self.subtract(other)

    def __mul__(self, scalar):
        # Allows usage of `*` operator for scalar multiplication
        return self.scalar_multiply(scalar)

    def __rmul__(self, scalar):
        # Allows scalar * vector
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        # Allows vector / scalar
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __repr__(self):
        # Nicely formats the vector when printed
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
