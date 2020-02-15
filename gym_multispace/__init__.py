from gym_multispace.multi_agent_env import MultiAgentSpaceEnv
from gym.envs.registration import register

register(
    id='multispace-v0',
    entry_point='gym_multispace:MultiAgentSpaceEnv',
)
