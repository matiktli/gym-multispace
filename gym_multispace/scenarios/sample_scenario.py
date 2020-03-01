from gym_multispace.scenario import BaseScenario
from gym_multispace.core.entity import Agent, SpecialObject
from gym_multispace.core.world import World
import numpy as np


# Test scenario
class Scenario(BaseScenario):

    def generate_world(self):
        print('GENERATING WORLD')
        world = World()
        world.state.size = (20, 20)
        world.is_reward_shared = False
        world.is_discrete = True
        world.agents = [Agent()]
        world.special_objects = [SpecialObject()]

        for i, agent in enumerate(world.agents):
            agent.can_grab = False
            agent.uuid = f'a_{i}'
            agent.view_range = np.inf
            agent.state.mass = 1
        for j, special_obj in enumerate(world.special_objects):
            special_obj.uuid = f'o_{j}'
            special_obj.state.mass = 1
            special_obj.state.size = 2

        return world

    def reset_world(self, world):
        print('RESETING WORLD')
        center_p = tuple([x / 2 for x in world.state.size])
        for i, agent in enumerate(world.agents):
            agent.state.pos = (center_p[0]/2 + i, center_p[1]/2 - i)

        for i, special_obj in enumerate(world.special_objects):
            special_obj.state.pos = (center_p[0] - i, center_p[1] + i)

    def get_reward(self, agent, world):
        return 1.0

    def get_observation(self, agent, world):
        # Simple observation of agent position
        return np.zeros(0)
