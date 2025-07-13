import math
import Vector3D as Vector3D
class Matrix:
    # This class represents a 4x4 matrix for 3D transformations including translation, rotation, scaling.
    # common matrix operations such as multiplication, transposition, and determinant calculation are also included.
    # althow this matrix is not using numpy, it is designed to be efficient for 3D graphics operations.
    def __init__(self, rows):
        # Initialize with 4 rows of 4 elements each (for 4x4 matrix)
        if len(rows) != 4 or not all(len(row) == 4 for row in rows):
            raise ValueError("Matrix must be 4x4.")
        self.rows = rows

    def __mul__(self, other):
        # Matrix multiplication: Matrix * Matrix
        if isinstance(other, Matrix):
            result = []
            for i in range(4):
                result_row = []
                for j in range(4):
                    val = sum(self.rows[i][k] * other.rows[k][j] for k in range(4))
                    result_row.append(val)
                result.append(result_row)
            return Matrix(result)

        # Matrix * Vector
        elif isinstance(other, Vector3D):
            x, y, z = other.x, other.y, other.z
            w = 1.0  # Homogeneous coordinate for translation
            result = [0, 0, 0, 0]
            for i in range(4):
                result[i] = (
                    self.rows[i][0] * x +
                    self.rows[i][1] * y +
                    self.rows[i][2] * z +
                    self.rows[i][3] * w
                )
            if result[3] != 0 and result[3] != 1:
                return Vector3D(result[0] / result[3], result[1] / result[3], result[2] / result[3])
            else:
                return Vector3D(result[0], result[1], result[2])
        else:
            raise TypeError("Unsupported multiplication.")

    def transpose(self):
        # Returns the transpose of the matrix
        return Matrix([[self.rows[j][i] for j in range(4)] for i in range(4)])

    def determinant(self):
        # Calculate the determinant of the 4x4 matrix using the rule of Sarrus or cofactor expansion
        def minor(matrix, i, j):
            return [row[:j] + row[j+1:] for k, row in enumerate(matrix) if k != i]

        if len(self.rows) != 4:
            raise ValueError("Determinant is only defined for 4x4 matrices.")

        det = 0
        for j in range(4):
            sign = (-1) ** j
            det += sign * self.rows[0][j] * Matrix(minor(self.rows, 0, j)).determinant()
        return det
    
    def minor(self, i, j):
        # Calculate the minor of the matrix by removing the i-th row and j-th column
        return Matrix([
            [self.rows[x][y] for y in range(4) if y != j]
            for x in range(4) if x != i
        ])

    def __repr__(self):
        return "\n".join(str(row) for row in self.rows)

    @staticmethod
    def identity():
        return Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def translation(tx, ty, tz):
        return Matrix([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def scaling(sx, sy, sz):
        return Matrix([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ])

    @staticmethod
    def rotation_x(theta_degrees):
        theta = math.radians(theta_degrees)
        c = math.cos(theta)
        s = math.sin(theta)
        return Matrix([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ])

    @staticmethod
    def rotation_y(theta_degrees):
        theta = math.radians(theta_degrees)
        c = math.cos(theta)
        s = math.sin(theta)
        return Matrix([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(theta_degrees):
        theta = math.radians(theta_degrees)
        c = math.cos(theta)
        s = math.sin(theta)
        return Matrix([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])
