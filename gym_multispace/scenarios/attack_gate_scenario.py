from gym_multispace.scenario import BaseScenario
from gym_multispace.core.entity import Agent, SpecialObject
from gym_multispace.core.world import World
import numpy as np
import random


# Test scenario
class Scenario(BaseScenario):

    def generate_world(self):
        print('GENERATING WORLD')
        world = World()
        world.state.size = (50, 50)
        world.is_reward_shared = False
        world.is_discrete = True
        world.agents = []
        world.special_objects = []

        # Create attacker agent
        attacker = Agent()
        attacker.can_grab = False
        attacker.uuid = 'a_0_attacker'
        attacker.view_range = np.inf
        attacker.state.mass = 1
        attacker.state.size = 1
        attacker.color = 'red'
        world.agents.append(attacker)

        # Create defender agent
        defender = Agent()
        defender.can_grab = False
        defender.uuid = 'a_1_defender'
        defender.view_range = np.inf
        defender.state.mass = 3
        defender.state.size = 2
        defender.color = 'green'
        world.agents.append(defender)

        # Setup objective in world
        goal = SpecialObject()
        goal.uuid = f'o_0_goal'
        goal.state.mass = 1
        goal.state.size = 3
        world.special_objects.append(goal)

        return world

    def reset_world(self, world):
        print('RESETING WORLD')
        center_p = tuple([x / 2 for x in world.state.size])

        # Place attacker most left area
        world.agents[0].state.pos = (
            2, random.randrange(0, world.state.size[1]))

        # Place deffender in the middle area
        world.agents[1].state.pos = (
            center_p[0], random.randrange(0, world.state.size[1]))

        # Place goal in the right area
        world.special_objects[0].state.pos = (
            world.state.size[0] - 2, random.randrange(0, world.state.size[1]))

    def get_reward(self, agent, world):
        # TODO[medium] implement sample reward for scenario
        return 1.0

    def get_observation(self, agent, world):
        # Simple observation of agent position
        # TODO[medium] build observation for agent
        return np.zeros(0)
