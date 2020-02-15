from abc import ABC, abstractmethod


# Entity object state (we store here values that in game might change mostly)
class EntityState(ABC):

    def __init__(self, pos=(-1, -1), size=0, mass=0, vel=0, acc=0):
        # Position
        self.pos = pos

        # Size
        self.size = size

        # Mass
        self.mass = mass

        # Velocity
        self.vel = vel

        # Acceleration
        self.acc = acc


# Physical agent state
class AgentState(EntityState):

    def __init__(self, pos=None, size=None, mass=None, vel=None, acc=None):
        super().__init__(pos, size, mass, vel, acc)


# Physical special object state
class SpecialObjectState(EntityState):

    def __init__(self, pos=None, size=None, mass=None, vel=None, acc=None):
        super().__init__(pos, size, mass, vel, acc)
