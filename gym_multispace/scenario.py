from gym_multispace.core.world import World
from gym_multispace.core.entity import Agent, SpecialObject

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

    @abstractmethod
    def is_done(self, world):
        return False


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
