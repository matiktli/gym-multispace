import gym
import gym_multispace
from gym_multispace.env_util import create_env

scenario_path = '../gym_multispace/scenarios/attack_gate_scenario.py'
env = create_env(scenario_path)
initial_observation = env.reset()

print("STARTING GAME")
for i in range(300):
    move_act_space = env.action_space[0]
    all_actions = []
    for agent in env.world.objects_agents_ai:
        all_actions.append(move_act_space.sample())
    obs_n, rew_n, done_n, info_n = env.step(action_n=all_actions)
    print(f""" 
    -----------------------------
    Step: {i}
    Agents actions: {all_actions}
    Agents rewards: {rew_n}
    Agent Observations: {obs_n}
    -----------------------------
    """)
    env.render(mode='human')
