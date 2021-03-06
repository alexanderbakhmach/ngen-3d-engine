import math
import numpy as np

from src.tool.tools import calc_rotation_matrix
from src.tool.tools import calc_translation_matrix
from src.tool.tools import calc_projection_matrix
from src.tool.tools import parametrical_line_point
from src.tool.tools import calc_rotation_matrix
from src.tool.tools import calc_translation_matrix
from src.tool.tools import calc_scaling_matrix
from src.tool.tools import normals_to_degrees

from src.world.worlds import world_needed
from src.model.models import ObjModel


@world_needed
class PerspectiveCamera:
    DEFAULT_SCREEN_WIDTH = 1200
    DEFAULT_SCREEN_HEIGHT = 900

    def __init__(self,
                 projective_plane_width=None,
                 projective_plane_height=None,
                 pos_x=None,
                 pos_y=None, 
                 pos_z=None,
    	         angle_x_deg=None,
    	         angle_y_deg=None,
    	         angle_z_deg=None, 
    	         field_of_view_angle_deg=None, 
    	         aspect_ratio=None,
    	         near=None,
    	         far=None):
        if projective_plane_width is None:
            projective_plane_width = self.DEFAULT_SCREEN_WIDTH

        if projective_plane_height is None:
           projective_plane_height = self.DEFAULT_SCREEN_HEIGHT

        if pos_x is None:
            pos_x = 0

        if pos_y is None:
            pos_y = 0

        if pos_z is None:
            pos_z = 0

        if angle_x_deg is None:
            angle_x_deg = 0

        if angle_y_deg is None:
            angle_y_deg = 0

        if angle_z_deg is None:
            angle_z_deg = 0

        if field_of_view_angle_deg is None:
            field_of_view_angle_deg = 30

        if aspect_ratio is None:
            aspect_ratio = 1

        if near is None:
            near = 1

        if far is None:
            far = 100
        
        self._world = None
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z
        self._pos_x_before = pos_x
        self._pos_y_before = pos_y
        self._pos_z_before = pos_z
        self._angle_x_deg = angle_x_deg
        self._angle_y_deg = angle_y_deg
        self._angle_z_deg = angle_z_deg
        self._angle_x_deg_before = angle_x_deg
        self._angle_y_deg_before = angle_y_deg
        self._angle_z_deg_before = angle_z_deg
        self._field_of_view_angle_deg = field_of_view_angle_deg
        self._aspect_ratio = aspect_ratio
        self._near = near
        self._far = far
        self._projective_plane_width = projective_plane_width
        self._projective_plane_height = projective_plane_height
        self._prev_transform = None

        self._projection_matrix = calc_projection_matrix(self._field_of_view_angle_deg,
                                                         self._aspect_ratio,
                                                         self._far,
                                                         self._near)

        self._update_matrix_for_pos()

    @property
    def world(self):
    	return self._world
    
    @world.setter
    def world(self, value):
        self._world = value

    @property
    def projective_plane_width(self):
    	return self._projective_plane_width

    @projective_plane_width.setter
    def projective_plane_width(self, value):
        self._projective_plane_width = value

    @property
    def projective_plane_height(self):
    	return self._projective_plane_height
    
    
    @projective_plane_height.setter
    def projective_plane_height(self, value):
        self._projective_plane_height = value

    @property
    def pos_x(self):
    	return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value
        self._update_matrix_for_pos()

    @property
    def pos_y(self):
    	return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value
        self._update_matrix_for_pos()

    @property
    def pos_z(self):
    	return self._pos_z

    @pos_z.setter
    def pos_z(self, value):
        self._pos_z = value
        self._update_matrix_for_pos()

    @property
    def angle_x_deg(self):
    	return self._angle_x_deg

    @angle_x_deg.setter
    def angle_x_deg(self, value):
        self._angle_x_deg = value
        self._update_matrix_for_pos()

    @property
    def angle_y_deg(self):
    	return self._angle_y_deg

    @angle_y_deg.setter
    def angle_y_deg(self, value):
        self._angle_y_deg = value
        self._update_matrix_for_pos()

    @property
    def angle_z_deg(self):
    	return self._angle_z_deg

    @angle_z_deg.setter
    def angle_z_deg(self, value):
        self._angle_z_deg = value
        self._update_matrix_for_pos()

    @property
    def field_of_view_angle_deg(self):
    	return self._field_of_view_angle_deg

    @field_of_view_angle_deg.setter
    def field_of_view_angle_deg(self, value):
        self._field_of_view_angle_deg = value

    @property
    def aspect_ratio(self):
    	return self._aspect_ratio

    @aspect_ratio.setter
    def spect_ratio(self, value):
        self._aspect_ratio = value

    def move_x(self, value):
        self._pos_x -= value
        self._update_matrix_for_move()

    def move_y(self, value):
        self._pos_y += value
        self._update_matrix_for_move()

    def move_z(self, value):
        self._pos_z += value
        self._update_matrix_for_move()

    def rotate_x(self, value):
        self._angle_x_deg += value
        self._update_matrix_for_move()

    def rotate_y(self, value):
        self._angle_y_deg += value
        self._update_matrix_for_move()

    def rotate_z(self, value):
        self._angle_z_deg += value
        self._update_matrix_for_move()

    def _update_matrix_for_move(self):
        delta_x = self._pos_x - self._pos_x_before
        delta_y = self._pos_y - self._pos_y_before
        delta_z = self._pos_z - self._pos_z_before
        delta_angle_x_deg = self._angle_x_deg - self._angle_x_deg_before
        delta_angle_y_deg = self._angle_y_deg - self._angle_y_deg_before
        delta_angle_z_deg = self._angle_z_deg - self._angle_z_deg_before
        

        tranlate_matrix = calc_translation_matrix(delta_x, delta_y, delta_z)
        rotate_matrix = calc_rotation_matrix(delta_angle_x_deg, delta_angle_y_deg, delta_angle_z_deg)

        self._transform_matrix = np.matmul(rotate_matrix, tranlate_matrix)

        if self._prev_transform is None:
            prev_tranlate_matrix = calc_translation_matrix(self._pos_x, self.pos_y, self.pos_z)
            prev_rotate_matrix = calc_rotation_matrix(self._angle_x_deg, self._angle_y_deg, self._angle_z_deg)

            self._prev_transform = np.matmul(rotate_matrix, tranlate_matrix)

        self._transform_matrix = np.matmul(self._transform_matrix, self._prev_transform)

        self._prev_transform = self._transform_matrix
        self._pos_x_before = self._pos_x
        self._pos_y_before = self._pos_y
        self._pos_z_before = self._pos_z
        self._angle_x_deg_before = self.angle_x_deg
        self._angle_y_deg_before = self.angle_y_deg
        self._angle_z_deg_before = self.angle_z_deg


    def _update_matrix_for_pos(self):
        tranlate_matrix = calc_translation_matrix(self._pos_x, self._pos_y, self._pos_z)
        rotate_matrix = calc_rotation_matrix(self._angle_x_deg, self._angle_y_deg, self._angle_z_deg)

        self._transform_matrix = np.matmul(rotate_matrix, tranlate_matrix)
        self._prev_transform = self._transform_matrix
        self._pos_x_before = self._pos_x
        self._pos_y_before = self._pos_y
        self._pos_z_before = self._pos_z
        self._angle_x_deg_before = self.angle_x_deg
        self._angle_y_deg_before = self.angle_y_deg
        self._angle_z_deg_before = self.angle_z_deg

    
    def perspective_division(self, points):
        d2_points = np.ones((points.shape[0], 2))

        for i, point in enumerate(points):
            x = point[0]
            y = point[1]
            w = point[3]

            if w > 0:
                new_x = ((x * self._projective_plane_width) / (2 * w)) + (self._projective_plane_width / 2)
                new_y = ((y * self._projective_plane_height) / (2 * w)) + (self._projective_plane_width / 2)

            else:
                new_x = np.nan
                new_y = np.nan

            d2_point = np.array([new_x, new_y])

            d2_points[i] = d2_point

        return d2_points

    def view(self, model):
        points = model.points
        normals = model._normals

        points = np.matmul(points[:,:], self._transform_matrix.T)
        normals = np.matmul(normals[:,:], np.linalg.inv(self._transform_matrix))
        points = np.matmul(points[:,:], self._projection_matrix.T)
        normals = np.matmul(normals[:,:], np.linalg.inv(self._projection_matrix))

        return self.perspective_division(points), normals


        