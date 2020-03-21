from gym_multispace.core.world import World
from gym_multispace.core.entity import Agent, SpecialObject
from gym_multispace.renderer import CircleVisualObject, Scaler
import cv2

from abc import ABC, abstractmethod
import imp
import os
import numpy as np


# Base scenario class to implement custom ones
class BaseScenario(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate_world(self):
        raise NotImplementedError()

    @abstractmethod
    def reset_world(self, world):
        raise NotImplementedError()

    # Get reward for agent base on scenario setup
    @abstractmethod
    def get_reward(self, agent, world):
        raise NotImplementedError()

    # Get observatio of world, for an agent, base on scenario setup
    @abstractmethod
    def get_observation(self, agent, world):
        raise NotImplementedError()

    def is_done(self, agent, world):
        return False

    def get_info(self, agent, world):
        return ["NO INFO DATA"]


# Utility function to load scenarios from python file
def load_scenario_from_file(file_path, is_absolute):
    obj = None
    if is_absolute:
        # load file from wherever
        obj = imp.load_source('', file_path)
    else:
        pathname = os.path.join(os.path.dirname(__file__), file_path)
        obj = imp.load_source('', pathname)
    return obj


class ScenarioUtils():

    @staticmethod
    def get_graphical_observation(agent, world, output_shape=(250, 250, 3)):
        image = 255 * np.ones(output_shape, np.uint8)
        scaler = Scaler(world.state.size, (output_shape[0], output_shape[1]))
        for agent in world.objects_all:
            v_obj = CircleVisualObject(
                agent.state.pos, agent.color, agent.state.size)
            v_obj = scaler.scale_object(v_obj)
            # Trick to add oppacity images in cv2
            overlay = image.copy()
            overlay = v_obj.render(overlay)
            oppacity = 0.6
            image = cv2.addWeighted(overlay,
                                    oppacity,
                                    image,
                                    1 - oppacity,
                                    0)
        return image
