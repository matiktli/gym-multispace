import gym
import gym_multispace
from gym_multispace.env_util import create_env

scenario_path = '../gym_multispace/scenarios/physics_test_scenario.py'
env = create_env(scenario_path)
initial_observation = env.reset()

print("STARTING GAME")
for i in range(300):
    move_act_space = env.action_space[0]
    all_actions = []
    all_actions.append(1)
    all_actions.append(1)

    obs_n, rew_n, done_n, info_n = env.step(action_n=all_actions)
    env.render(mode='human')
