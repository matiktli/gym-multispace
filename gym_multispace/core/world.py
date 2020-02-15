import world_engine as engine
import world_state as state
import entity as ent


# Multi agent word representation
class World():

    WORLD_DIM = 2

    def __init__(self, agents=None, special_objects=None):
        self.world_dim = World.WORLD_DIM
        self.agents = agents
        self.special_objects = special_objects
        self.state = state.WorldState()
        self.engine = engine.PhysicEngine(self.state)
        self.is_discrete = True
        self.is_shared_reward = False

    # Update state of the world
    def step(self):
        # Get actions from callback to agents decision makers
        self.agents = self.__set_agents_actions_from_callback(self.agents)
        # After actions come responses from environment
        self.__perform_world_actions(self.agents)

    def __set_agents_actions_from_callback(self, agents):
        for agent in agents:
            # Pass agent and world to agent action callback func
            agent.action = agent.action_callback(agent, self)
        return agents

    def __perform_world_actions(self, agents):
        pass

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
        return [agent for agent in self.agents if agent.action_callback is not None]

    # Return agents in the world controlled by world script
    @property
    def objects_agents_script(self):
        pass

    # Return all special objects in the world
    @property
    def objects_special_all(self):
        pass

    # Return special objects in the world, of type: @type
    @property
    def objects_special_type(self, type):
        pass
