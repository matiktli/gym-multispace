from abc import ABC, abstractmethod
import entity_state as state


# Quadrant is representing part of space in the world
class Quadrant(ABC):

    def __init__(self):
        self.state = state.QuadrantPhysicalState()


# Agent is occuping quadrant's space, sharing its state
class Agent(Quadrant):

    def __init__(self, action_callback=None):
        super().__init__()
        self.state = state.AgentPhysicalState()
        self.action_callback = action_callback


# Special Object is occuping quadrant's space, sharing its state
class SpecialObject(Quadrant):

    def __init__(self):
        super().__init__()
        self.state = state.SpecialObjectPhysicalState()
