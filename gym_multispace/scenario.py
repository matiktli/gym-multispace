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
    def reset_world(self):
        raise NotImplementedError()

    # Get reward for agent base on scenario setup
    @abstractmethod
    def get_reward(self, agent, world):
        raise NotImplementedError()

    # Get observatio of world, for an agent, base on scenario setup
    @abstractmethod
    def get_observation(self, agent, world):
        raise NotImplementedError()


# Utility function to load scenarios from python file
def load_scenario_from_file(file_path):
    pathname = os.path.join(os.path.dirname(__file__), file_path)
    obj = imp.load_source('', pathname)
    return obj
