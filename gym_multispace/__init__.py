from gym_multispace.mutli_agent_env import MultiAgentSpaceEnv
from gym.envs.registration import register

register(
    id='multispace-v0',
    entry_point='gym_multispace.envs:MultiAgentSpaceEnv',
)
