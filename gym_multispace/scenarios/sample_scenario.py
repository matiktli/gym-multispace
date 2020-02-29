from gym_multispace.scenario import BaseScenario
from gym_multispace.core.entity import Agent, SpecialObject
from gym_multispace.core.world import World
import numpy as np


# Test scenario
class Scenario(BaseScenario):

    def generate_world(self):
        print('GENERATING WORLD')
        world = World()
        world.state.size = (10, 10)
        world.is_reward_shared = False
        world.is_discrete = True
        world.agents = [Agent(), Agent(), Agent()]
        world.special_objects = [
            SpecialObject(), SpecialObject(), SpecialObject(), SpecialObject(), SpecialObject()]

        for i, agent in enumerate(world.agents):
            agent.can_grab = False
            agent.uuid = f'a_{i}'
            agent.view_range = np.inf
            agent.state.mass = 1
        for i, special_obj in enumerate(world.special_objects):
            special_obj.uuid = f'o_{i}'
            agent.state.mass = 2

        return world

    def reset_world(self, world):
        print('RESETING WORLD')
        center_p = tuple([x / 2 for x in world.state.size])
        for i, agent in enumerate(world.agents):
            agent.state.pos = (center_p[0] + i, center_p[1] - i)

        for i, special_obj in enumerate(world.special_objects):
            special_obj.state.pos = (center_p[0] - i, center_p[1] + i)

    def get_reward(self, agent, world):
        print('REWARDING AGENT')
        return 1.0

    def get_observation(self, agent, world):
        # Simple observation of agent position
        print('OBSERVING WORLD')
        return np.zeros(0)
