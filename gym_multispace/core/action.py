from enum import Enum


class AgentPhysicalAction(Enum):
    pass


# Agent taken action
class AgentAction():

    def __init__(self, physical_action=None):
        # Phisical action
        self.physical = physical_action
