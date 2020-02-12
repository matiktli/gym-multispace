from abc import ABC, abstractmethod
import entity_state as states
import action as actions


# Entity is representing part of space in the world
class Entity(ABC):

    def __init__(self):

        # Setup entity initial physical state
        self.state = states.EntityPhysicalState()

        # If entity can move by itself
        self.can_move = False

        # If entity can be moved by other entities
        self.can_be_moved = False

        # If entity colide with other entities
        self.can_collide = True

        # If entity can be destroyed by other entities or world event
        self.can_be_destroyed = False


# Agent is occuping quadrant's space, sharing its state
class Agent(Entity):

    def __init__(self, agent_type=None, action_callback=None):
        super().__init__()
        self.state = states.AgentPhysicalState()
        self.type = agent_type
        self.action_callback = action_callback

        # Initialise agent action
        self.action = actions.AgentAction()


# Special Object is occuping quadrant's space, sharing its state
class SpecialObject(Entity):

    def __init__(self, object_type=None):
        super().__init__()
        self.state = states.SpecialObjectPhysicalState()
        self.type = object_type
