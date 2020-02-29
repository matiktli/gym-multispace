from abc import ABC, abstractmethod
import cv2
import numpy as np


class VisualObject(ABC):

    def __init__(self, pos: tuple, color):
        self.pos = pos
        self.color = color

    def render(self, image):
        return self.render_internal(image)

    @abstractmethod
    def render_internal(self, image):
        raise NotImplementedError()


class CircleVisualObject(VisualObject):

    def __init__(self, pos, color, radius):
        super().__init__(pos, color, radius)
        self.radius = radius

    def render_internal(self, image):
        raise NotImplementedError()


# Perform scalling operations world to visual representation
class Scaler():

    def __init__(self, world_real_size: tuple, world_visual_size: tuple):
        self.vector_r_to_v = (world_visual_size[0] / world_real_size[0],
                              world_visual_size[1] / world_real_size[1])
        print(f'scaler: ', self.vector_r_to_v)


class Renderer():

    WINDOW_SIZE = (500, 500)
    WINDOW_NAME = 'Game render'

    def __init__(self, world_size):
        # Initialise scaler
        self.window_size = Renderer.WINDOW_SIZE
        self.window_name = Renderer.WINDOW_NAME
        self.scaler = Scaler(world_size, self.window_size)
        # Reset renderer state
        self.reset()

    def add_object_to_frame(self, visual_object):
        self.objects_to_render.append(visual_object)

    def render(self, return_rgb_array=False):
        # TODO[hard] take care of rendering objects
        if return_rgb_array:
            return self.image
        else:
            cv2.imshow(self.WINDOW_NAME, self.image)
            cv2.waitKey(1)

    def reset(self):
        self.objects_to_render = []
        self.image = 255 * np.ones(
            (self.window_size[0], self.window_size[1], 3), np.uint8)
