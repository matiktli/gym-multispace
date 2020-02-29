from abc import ABC, abstractmethod
import cv2
import numpy as np


class VisualObject(ABC):

    def __init__(self, pos: tuple, color):
        self.pos = pos
        self.color = color
        self.color = Renderer.get_color_by_txt(self.color)['bgr']
        self.pos = Renderer.get_pos_from_array(self.pos)
        self.tag = '<>'

    def render(self, image):
        return self.render_internal(image)

    @abstractmethod
    def render_internal(self, image):
        raise NotImplementedError()


class CircleVisualObject(VisualObject):

    def __init__(self, pos, color, radius):
        super().__init__(pos, color)
        self.radius = radius

    def render_internal(self, image):
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        return cv2.circle(image,
                          pos_int,
                          int(self.radius[0]),
                          self.color, -1)


# Perform scalling operations world to visual representation
class Scaler():

    def __init__(self, world_real_size: tuple, world_visual_size: tuple):
        self.vector_r_to_v = np.zeros(2)
        self.vector_r_to_v[0] = world_visual_size[0] / world_real_size[0]
        self.vector_r_to_v[1] = world_visual_size[1] / world_real_size[1]

    def scale_object(self, v_object):
        v_object.radius = v_object.radius * self.vector_r_to_v
        v_object.pos = v_object.pos * self.vector_r_to_v
        return v_object


class Renderer():

    COLORS = [
        {
            'txt': 'blue',
            'bgr': (255, 0, 0)
        }, {
            'txt': 'green',
            'bgr': (0, 255, 0)
        }, {
            'txt': 'red',
            'bgr': (0, 0, 255)
        }, {
            'txt': 'gray',
            'bgr': (100, 100, 100)
        }
    ]

    @staticmethod
    def get_color_by_txt(c_txt):
        if isinstance(c_txt, tuple):
            return c_txt
        result_list = list(
            filter(lambda color: color['txt'] == c_txt, Renderer.COLORS))
        if len(result_list) == 0:
            raise Exception(f'Color: {c_txt} is not supported!')
        return result_list[0]

    @staticmethod
    def get_pos_from_array(array_pos):
        return tuple(array_pos)

    WINDOW_SIZE = (500, 500)
    WINDOW_NAME = 'Game render'

    def __init__(self, world_size):
        # Initialise scaler
        self.window_size = Renderer.WINDOW_SIZE
        self.window_name = Renderer.WINDOW_NAME
        self.scaler = Scaler(world_size, self.window_size)
        self.objects_to_render = []
        # Reset renderer state
        self.reset()

    def add_object_to_frame(self, visual_object):
        if self.scaler:
            visual_object = self.scaler.scale_object(visual_object)

        self.objects_to_render.append(visual_object)

    def render(self, return_rgb_array=False):
        for v_obj in self.objects_to_render:
            if isinstance(v_obj, CircleVisualObject):
                self.image = v_obj.render(self.image)
            else:
                raise NotImplementedError(
                    'Only Circle object rendering is supported for now')
        # Return image or display depend on mode
        if return_rgb_array:
            return self.image
        else:
            cv2.imshow(self.WINDOW_NAME, self.image)
            cv2.waitKey(1)
        self.reset()

    def reset(self):
        self.objects_to_render = []
        self.image = 255 * np.ones(
            (self.window_size[0], self.window_size[1], 3), np.uint8)
