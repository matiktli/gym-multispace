from core.world import World
from numpy import np
from core.entity import Agent, SpecialObject
from abc import ABC, abstractmethod


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


class TestScenario(BaseScenario):

    def generate_world(self):
        world = World()
        world.agents = [Agent()]
        world.special_objects = [SpecialObject()]

        for i, agent in world.agents:
            agent.can_collide = False
            agent.can_grab = False
            agent.uuid = f'a_{i}'
            agent.view_range = np.inf

        for i, special_obj in world.special_objects:
            special_obj.uuid = f'o_{i}'
            special_obj.can_collide = False

        return world

    def reset_world(self):
        raise NotImplementedError()

    def get_reward(self, agent, world):
        raise NotImplementedError()

    def get_observation(self, agent, world):
        raise NotImplementedError()