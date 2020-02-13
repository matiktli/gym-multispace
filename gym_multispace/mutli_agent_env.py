import gym
from gym import error, spaces, utils
from gym.utils import seeding
from core.world import World
import numpy as np


class MultiAgentSpaceEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, world: World,
                 reward_callback=None,
                 observation_callback=None,
                 info_callback=None,
                 done_callback=None
                 ):
        self.world = world
        self.agents = world.objects_agents_ai
        self.n = len(self.agents)  # gym.Env property
        self.is_discrete = world.is_discrete  # action & input
        self.is_reward_shared = world.is_reward_shared

        # Callbacks
        self.reward_callback = reward_callback
        self.observation_callback = observation_callback
        self.info_callback = info_callback
        self.done_callback = done_callback

        # Configure GymAi action spaces for agents
        self.__init_action_spaces(self.world, self.agents, self.is_discrete)

    def step(self, action):
        # TODO step logic
        pass

    def reset(self):
        
        pass

    def render(self, mode='human', close=False):
        pass

    # Configure spaces for all agents
    def __init_action_spaces(self, world: World, agents, is_discrete):
        self.action_space = []
        self.observation_space = []
        for agent in agents:
            total_action_space = []
            # Generate move action space
            if agent.can_move:
                p_space = self.____get_physical_action_space(
                    is_discrete, agent, world)
                total_action_space.append(p_space)

            # Generate grab action space
            if agent.can_grab:
                g_space = self.____get_grab_action_space(
                    is_discrete, agent, world)
                total_action_space.append(g_space)

            if len(total_action_space) > 1:
                act_space = spaces.Tuple(total_action_space)
                self.action_space.append(act_space)
            else:
                self.action_space.append(total_action_space[0])

            # Generate observation space
            obs_dim = len(self.observation_callback(agent, world))
            obs_space = self.____get_observation_space(agent, obs_dim)
            self.observation_space.append(obs_space)

    # Define MOVE action space for agent
    def ____get_physical_action_space(self, is_discrete, agent, world):
        if is_discrete:
                # When space action is discrete our physical space have moves:
                # FORWARD, BACKWARD, LEFT, RIGHT -> 2D * 2
                # STAY -> + 1
            agent_move_action_space = spaces.Discrete(
                world.world_dim * 2 + 1)
        else:
            agent_move_action_space = spaces.Box(low=-agent.move_range,
                                                 high=+agent.move_range,
                                                 shape=(world.world_dim,),
                                                 dtype=np.float32)
        return agent_move_action_space

    # Define GRAB action space for agent
    def ____get_grab_action_space(self, is_discrete, agent, world):
        if is_discrete:
            # When space action is discrete our grab space have either: 0, 1
            agent_grab_action_space = spaces.Discrete(0)
        else:
            agent_grab_action_space = spaces.Box(low=0,
                                                 high=1,
                                                 shape=(0,),
                                                 dtype=np.float32)
        return agent_grab_action_space

    # Define observation space for agent
    def ____get_observation_space(self, agent, observation_dim):
        view_range = agent.view_range if agent.view_range is None else np.inf
        return spaces.Box(low=-view_range, high=+view_range, shape=(observation_dim,), dtype=np.float32)
