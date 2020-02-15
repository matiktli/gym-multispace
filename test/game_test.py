import gym
import gym_multispace
from gym_multispace.env_util import create_env

scenario_path = '../gym_multispace/scenarios/sample_scenario.py'
env = create_env(scenario_path)
