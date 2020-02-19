from enum import Enum


class ACTION(Enum):
    STAY = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4


# Agent taken action
class AgentAction():

    def __init__(self, move_act=None, grab_act=None):
        # Phisical action
        self.move_act = move_act
        self.grap_act = grab_act
