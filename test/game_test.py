import gym
import gym_multispace
from gym_multispace.env_util import create_env

scenario_path = '../gym_multispace/scenarios/sample_scenario.py'
env = create_env(scenario_path)
initial_observation = env.reset()

print("STARTING GAME")
for i in range(10):
    move_act_space = env.action_space[0]
    obs_n, rew_n, done_n, info_n = env.step(action_n=[move_act_space.sample()])
    env.render(mode='human')
