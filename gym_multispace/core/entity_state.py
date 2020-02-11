from abc import ABC, abstractmethod


# Quadrant object state
class QuadrantPhysicalState(ABC):

    def __init__(self, pos=None):
        self.pos = pos


# Physical agent state
class AgentPhysicalState(QuadrantPhysicalState):

    def __init__(self, pos=None):
        super().__init__(pos)


# Physical special object state
class SpecialObjectPhysicalState(QuadrantPhysicalState):

    def __init__(self, pos=None):
        super().__init__(pos)
