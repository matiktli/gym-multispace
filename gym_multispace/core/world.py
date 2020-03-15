import gym_multispace.core.world_engine as engine
import gym_multispace.core.world_state as state
import gym_multispace.core.entity as ent
import numpy as np


# Multi agent word representation
class World():

    def __init__(self, agents=None, special_objects=None):
        self.step_counter = 0
        self.agents = agents
        self.special_objects = special_objects
        self.state = state.WorldState()
        self.engine = engine.PhysicEngine()
        self.is_discrete = True
        self.is_shared_reward = False

    # Update state of the world
    def step(self):
        self.step_counter += 1
        # Get actions from callback for scripted (computer) agents
        self.__set_agents_actions_from_callback(
            self.objects_agents_all)

        # Perform all PHYSICAL actions in envrionemnt
        self.__proccess_physic_state()

    def __set_agents_actions_from_callback(self, agents):
        for agent in agents:
            if agent.action_callback:
                # Pass agent and world to agent action callback func
                agent.action = agent.action_callback(agent, self)
            else:
                print(f"Agent: {agent.uuid} do not have callback function!")
        return agents

    def __proccess_physic_state(self):
        # Gather actions on all entities into array.
        # Value in array is another array of forces applied in each dimension of the world
        # entities_forces = [
        #     [0.0 for _ in range(self.state.dim)] for _ in self.objects_all
        # ]
        entities_forces = [np.zeros(self.state.dim) for _ in self.objects_all]

        # Apply forces from momentum?
        self.engine.apply_force_from_momentum(self, entities_forces)

        # Apply forces coresponding to actions taken by agents
        self.engine.apply_actions_forces(self, entities_forces)

        # Apply forces from interactions between objects
        self.engine.apply_physical_interaction_forces(self, entities_forces)

        # Calculate new state of entities/world after all forces applied
        self.engine.calculate_new_state(self, entities_forces)

    # Return all objects in the world
    @property
    def objects_all(self):
        return self.agents + self.special_objects

    # Return all agents in the world
    @property
    def objects_agents_all(self):
        return self.agents

    # Return agents in the world controlled by model
    @property
    def objects_agents_ai(self):
        return [agent for agent in self.agents if agent.action_callback is None]

    # Return agents in the world controlled by world script
    @property
    def objects_agents_script(self):
        return [agent for agent in self.agents if agent.action_callback is not None]

    # Return all special objects in the world
    @property
    def objects_special_all(self):
        self.special_objects

    # Return special objects in the world, of type: @type
    @property
    def objects_special_type(self, type):
        raise NotImplementedError()
