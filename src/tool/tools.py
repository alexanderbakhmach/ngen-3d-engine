import numpy as np
import math


def matrix_multiply(matrix_a, matrix_b):
    result = []

    for i in range(len(matrix_b)): 
        total = 0

        for j in range(len(matrix_a)): 
            total += matrix_a[j] * matrix_b[j][i]

        result.append(total)

    return result


def matrix_transponse(matrix):
    return list(map(list, zip(*matrix))) 


def matrix_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


def matrix_determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0

    for c in range(len(matrix)):
        mc = matrix_minor(matrix, 0 , c)
        determinant += ((-1) ** c) * matrix[0][c] * matrix_determinant(mc)

    return determinant


def matrix_inverse(matrix):
    determinant = matrix_determinant(matrix)

    if determinant == 0:
        raise ValueError('Matrix can not be inverted. Determinant = 0.')

    if len(matrix) == 2:
        return [[matrix[1][1] / determinant, -1 * matrix[0][1] / determinant],
                [-1 * matrix[1][0] / determinant, matrix[0][0] / determinant]]

    cofactors = []

    for r in range(len(matrix)):
        cofactor_row= []

        for c in range(len(matrix)):
            minor = matrix_minor(matrix, r, c)

            cofactor_row.append(((-1) ** (r + c)) * matrix_determinant(minor))
        
        cofactors.append(cofactor_row)
    
    cofactors = matrix_transponse(cofactors)
    
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    
    return cofactors


def calc_rotation_matrix(x_angle_deg, y_angle_deg, z_angle_deg):
    x_angle_rad = math.radians(x_angle_deg)
    y_angle_rad = math.radians(y_angle_deg)
    z_angle_rad = math.radians(z_angle_deg)

    rotation_matrix_x = np.array([[1, 0, 0, 0],
                                  [0, math.cos(x_angle_rad), -math.sin(x_angle_rad), 0],
                                  [0, math.sin(x_angle_rad), math.cos(x_angle_rad), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_y = np.array([[math.cos(y_angle_rad), 0, -math.sin(y_angle_rad), 0],
                                  [0, 1, 0, 0],
                                  [math.sin(y_angle_rad), 0, math.cos(y_angle_rad), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_z = np.array([[math.cos(z_angle_rad), -math.sin(z_angle_rad), 0, 0],
                                  [math.sin(z_angle_rad), math.cos(z_angle_rad), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_xy = np.matmul(rotation_matrix_x, rotation_matrix_y)

    return np.matmul(rotation_matrix_xy, rotation_matrix_z)

def calc_translation_matrix(move_x, move_y, move_z):
    return np.array([[1, 0, 0, move_x],
                     [0, 1, 0, move_y],
                     [0, 0, 1, move_z],
                     [0, 0, 0, 1]])


def calc_scaling_matrix(x, y, z):
    return np.array([[x, 0, 0, 0],
    	             [0, y, 0, 0],
    	             [0, 0, z, 0],
    	             [0, 0, 0, 1]])

def calc_projection_matrix(field_of_view_angle_deg, aspect_ratio, far, near):
    field_of_view_angle_rad = math.radians(field_of_view_angle_deg)
    field_of_view = 1.0 / math.tan(field_of_view_angle_rad / 2.0)  

    return np.array([[field_of_view * aspect_ratio, 0, 0, 0],
                     [0, field_of_view, 0, 0],
                     [0, 0, (far + near) / (far - near), 1],
                     [0, 0, (2 * near * far) / (near - far), 0]])


def normals_to_degrees(normals):
    # The normal is the projection of the sinle sized vector on the each of coordinates.
    # So the normal_x =  single_size_vector_scalar * cos(angle_to_x_axe) = 1 * cos(angle_to_x_axe)
    # So the normal_x = cos(angle_to_x_axe).
    # So the angle_to_x_axe_degrees = degrees(arccos(angle_to_x_axe))
    return np.degrees(np.arccos(normals[:,:]))


def degrees_to_normals(degrees):
    # The normal is the projection of the sinle sized vector on the each of coordinates.
    # So the normal_x =  single_size_vector_scalar * cos(angle_to_x_axe) = 1 * cos(angle_to_x_axe)
    # So the normal_x = cos(angle_to_x_axe).
    # So the angle_to_x_axe_degrees = degrees(arccos(angle_to_x_axe))
    return np.round(np.cos(np.radians(degrees[:,:])), 3)


def parametrical_line_point(point, normal, distance):
    normal_a = normal[0]
    normal_b = normal[1]
    normal_c = normal[2]
    x = point[0]
    y = point[1]
    z = point[2]

    new_point_x = x + normal_a * distance 
    new_point_y = y + normal_b * distance 
    new_point_z = z + normal_c * distance 

    return np.array([new_point_x, new_point_y, new_point_z, 1])