from abc import ABC, abstractmethod
import numpy as np
from gym_multispace.core.world_state import WorldState


# Entity object state (we store here values that in game might change mostly)
class EntityState(ABC):

    def __init__(self, pos=(-1, -1), size=1, mass=1, vel=np.zeros(WorldState.WORLD_DIM_2D)):
        # Position
        self.pos = pos

        # Size[ m]
        self.size = size

        # Mass [kg]
        self.mass = mass

        # Velocity [m/s^2]
        self.vel = vel


# Physical agent state
class AgentState(EntityState):

    def __init__(self, pos=(-1, -1), size=1, mass=1, vel=np.zeros(WorldState.WORLD_DIM_2D)):
        super().__init__(pos, size, mass, vel)
        self.max_speed = 3


# Physical special object state
class SpecialObjectState(EntityState):

    def __init__(self, pos=(-1, -1), size=1, mass=2, vel=np.zeros(WorldState.WORLD_DIM_2D)):
        super().__init__(pos, size, mass, vel)
