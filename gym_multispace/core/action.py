from enum import Enum


# Representation of action taken by agent
class ACTION(Enum):
    STAY = {'id': 0, 'vector_2d': [0.0, 0.0]}
    MOVE_UP = {'id': 1, 'vector_2d': [0.0, +1.0]}
    MOVE_DOWN = {'id': 2, 'vector_2d': [0.0, -1.0]}
    MOVE_LEFT = {'id': 3, 'vector_2d': [-1.0, 0.0]}
    MOVE_RIGHT = {'id': 4, 'vector_2d': [+1.0, 0.0]}

    @staticmethod
    def get_by_id(id):
        return list(filter(lambda act: act.value['id'] == id, list(ACTION)))[0]


# Agent taken action
class AgentAction():

    def __init__(self, move_act=None, grab_act=None):
        # Phisical action
        self.move_act = move_act  # Array with dim of the world
        self.grab_act = grab_act  #
