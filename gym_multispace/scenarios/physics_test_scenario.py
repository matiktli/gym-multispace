from gym_multispace.scenario import BaseScenario
from gym_multispace.core.entity import Agent, SpecialObject
from gym_multispace.core.world import World
import numpy as np


# Test scenario
class Scenario(BaseScenario):

    def generate_world(self):
        print('GENERATING WORLD')
        world = World()
        world.state.size = (50, 50)
        world.is_reward_shared = False
        world.is_discrete = True
        world.agents = [Agent(), Agent()]
        world.special_objects = [SpecialObject()]

        for i, agent in enumerate(world.agents):
            agent.can_grab = False
            agent.uuid = f'a_{i}'
            agent.view_range = np.inf
            agent.state.mass = 3.5
            agent.state.size = 1
        for j, special_obj in enumerate(world.special_objects):
            special_obj.uuid = f'o_{j}'
            special_obj.state.mass = 3
            special_obj.state.size = 5

        world.agents[0].color = 'green'
        world.agents[1].color = 'blue'

        return world

    def reset_world(self, world):
        print('RESETING WORLD')
        center_p = tuple([x / 2 for x in world.state.size])

        world.agents[0].state.pos = (12 + 15, 12)
        world.agents[1].state.pos = (center_p[0] + 15, 1)

        for i, special_obj in enumerate(world.special_objects):
            special_obj.state.pos = (center_p[0] - i, center_p[1] + i)

    def get_reward(self, agent, world):
        return 1.0

    # observation callback function
    def get_observation(self, agent, world):
        print(f'GETTING OBS FOR AGENT: {agent.uuid}.')
        # Simple observation of all agents position
        obs = []
        for obj in world.objects_all:
            obs.append(obj.state.pos)
            obs.append(obj.state.vel)
        return np.concatenate(obs)
