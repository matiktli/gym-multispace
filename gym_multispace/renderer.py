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


class Renderer():

    WINDOW_SIZE = (500, 500)
    WINDOW_NAME = 'Game render'

    def __init__(self):
        self.window_size = Renderer.WINDOW_SIZE
        self.window_name = Renderer.WINDOW_NAME
        self.objects_to_render = []
        self.image = 255 * np.ones(
            (self.window_size[0], self.window_size[1], 3), np.uint8)

    def render(self, return_rgb_array=False):
        if return_rgb_array:
            return self.image
        else:
            cv2.imshow(self.WINDOW_NAME, self.image)
            cv2.waitKey(1)
