from enum import Enum


# Agent taken action
class AgentAction():

    def __init__(self, move_act=None, grab_act=None):
        # Phisical action
        self.move_act = move_act
        self.grap_act = grab_act
