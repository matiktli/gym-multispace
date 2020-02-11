from abc import ABC, abstractmethod
from core.world import World


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
    def get_reward(self, agent, world: World):
        raise NotImplementedError()

    # Get observatio of world, for an agent, base on scenario setup
    @abstractmethod
    def get_observation(self, agent, world: World):
        raise NotImplementedError()
