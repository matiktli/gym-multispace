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
        if agent.uuid == 'a_0_attacker':
            # Attacker reward is based on distance to the target entity (negative reward)
            distance_to_goal = np.sqrt(
                np.sum(np.square(agent.state.pos - world.special_objects[0].state.pos)))
            return -distance_to_goal
        elif agent.uuid == 'a_1_defender':
            attacker_agent = list(filter(
                lambda ag: ag.uuid == 'a_0_attacker', world.agents))[0]
            distance_of_attacker_to_goal = np.sqrt(
                np.sum(np.square(attacker_agent.state.pos - world.special_objects[0].state.pos)))
            # Defender reward is based on how far is the enemy from entity
            return distance_of_attacker_to_goal
        else:
            raise Exception('Wrong agent definition')

    def get_observation(self, agent, world):
        # Simple observation of all agents position
        obs = [ag.state.pos for ag in world.objects_all]
        return obs
