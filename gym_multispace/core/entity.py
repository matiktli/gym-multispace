from abc import ABC, abstractmethod
import gym_multispace.core.entity_state as states
import gym_multispace.core.action as actions


# Entity is representing part of space in the world
class Entity(ABC):

    def __init__(self):

        # Set representation in that is `object_type_symbol`_`number` like: a_1, o_1.
        self.uuid = None

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

    def __init__(self, uuid=None, agent_type=None, agent_team=None, view_range=None, action_callback=None):
        super().__init__()
        self.uuid = uuid
        self.can_move = True
        self.can_grab = True
        self.state = states.AgentPhysicalState()
        self.action_callback = action_callback
        self.type = agent_type
        self.team = agent_team
        self.view_range = view_range

        # Initialise agent action
        self.action = actions.AgentAction()


# Special Object is occuping quadrant's space, sharing its state
class SpecialObject(Entity):

    def __init__(self, uuid=None, object_type=None):
        super().__init__()
        self.uuid = uuid
        self.state = states.SpecialObjectPhysicalState()
        self.type = object_type
