import entity as entity
import world_engine as engine


# Multi agent word representation
class World():

    def __init__(self, agents=None, special_objects=None):
        self.agents = agents
        self.special_objects = special_objects
        self.engine = engine.PhysicEngine()

    # Update state of the world
    def step(self):
        pass

    # Return all objects in the world
    @property
    def objects_all(self):
        pass

    # Return all agents in the world
    @property
    def objects_agents_all(self):
        pass

    # Return agents in the world controlled by model
    @property
    def objects_agents_ai(self):
        pass

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
