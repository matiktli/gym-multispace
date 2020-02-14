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
                 done_callback=None,
                 reset_callback=None
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
        self.reset_callback = reset_callback

        # Configure GymAi action spaces for agents
        self.__init_action_spaces(self.world, self.agents, self.is_discrete)
        self.time = 0

    # Action from agent > step in world > observation & reward
    def step(self, action_n):
        observation_n, reward_n, done_n, info_n = [], [], [], {'n': []}
        self.agents = self.world.objects_agents_ai

        # set agents actions
        self.__set_actions_for_agents(action_n, self.agents, self.action_space)

        # make step in world
        self.world.step()

        # record observation for each agent
        self.__record_observation_and_info_for_agents(self.agents,
                                                      self.world,
                                                      observation_n,
                                                      reward_n,
                                                      done_n,
                                                      info_n)

        # all agents get total reward in shared reward mode case
        reward = np.sum(reward_n)
        if self.is_reward_shared:
            reward_n = [reward] * self.n

        return observation_n, reward_n, done_n, info_n

    # Reset world, returning init observations for agents
    def reset(self, world):
        self.reset_callback(world)

        # record observations for each agent
        observation_n = []
        self.agents = self.world.objects_agents_ai
        for agent in self.agents:
            observation_n.append(
                self.____get_observation_from_callback(agent, world))
        return observation_n

    def render(self, mode='human', close=False):
        # TODO render
        pass

    """
    PART_1: Initialization spaces for all agents
    """

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

            # Add all action spaces for agent as batch
            if len(total_action_space) > 1:
                # all action spaces are discrete, so simplify to MultiDiscrete action space
                if all([isinstance(act_space, spaces.Discrete) for act_space in total_action_space]):
                    act_space = spaces.MultiDiscrete(
                        [[0, act_space.n - 1] for act_space in total_action_space])
                else:
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

    """
    PART_2: Setting actions for agents.
    """

    def __set_actions_for_agents(self, action_n, agents, action_space):
        for i, agent in enumerate(self.agents):
            self.____set_action_for_agent(
                action_n[i], agent, self.action_space[i])

    def ____set_action_for_agent(self, action, agent, agent_action_space):
        if agent.can_move:
            self._____set_move_action_for_agent(
                action, agent, agent_action_space)

        if agent.can_grab:
            self._____set_grab_action_for_agent(
                action, agent, agent_action_space)

    def _____set_move_action_for_agent(self, action, agent, agent_action_space):
        # TODO set move action
        pass

    def _____set_grab_action_for_agent(self, action, agent, agent_action_space):
        # TODO set grab action
        pass

    """
    PART_3: Observation, reward. Collecting data from callbacks for given policy/scenario
    """

    def __record_observation_and_info_for_agents(self, agents, world, observation_n, reward_n, done_n, info_n):
        for agent in agents:
            observation_n.append(
                self.____get_observation_from_callback(agent, world))
            reward_n.append(self.____get_reward_from_callback(agent, world))
            done_n.append(self.____get_done_from_callback(agent, world))
            info_n['n'].append(self.____get_info_from_callback(agent, world))

    # get info for an agent
    def ____get_info_from_callback(self, agent, world):
        if self.info_callback is None:
            return {}
        return self.info_callback(agent, world)

    # get observation for an agent
    def ____get_observation_from_callback(self, agent, world):
        if self.observation_callback is None:
            return np.zeros(0)
        return self.observation_callback(agent, world)

    # get if done for an agent
    def ____get_done_from_callback(self, agent, world):
        if self.done_callback is None:
            return False
        return self.done_callback(agent, world)

    # get reward for an agent
    def ____get_reward_from_callback(self, agent, world):
        if self.reward_callback is None:
            return 0.0
        return self.reward_callback(agent, world)
