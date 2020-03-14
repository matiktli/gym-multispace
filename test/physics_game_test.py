import gym
import gym_multispace
from gym_multispace.env_util import create_env

scenario_path = '../gym_multispace/scenarios/physics_test_scenario.py'
env = create_env(scenario_path)
initial_observation = env.reset()
env.reset()
print("STARTING GAME")
for i in range(150):
    move_act_space = env.action_space[0]
    all_actions = []

    # 1st agent actions
    all_actions.append(0)

    # 2nd agent actions
    all_actions.append(1)

    if i > 5:
        all_actions = []
        all_actions.append(0)
        all_actions.append(3)

    if i > 14:
        all_actions = []
        all_actions.append(0)
        all_actions.append(0)

    obs_n, rew_n, done_n, info_n = env.step(action_n=all_actions)
    the_same_obs = obs_n[0]
    print(f""" 
    -----------------------------
    Step: {i}
    Agents actions: {all_actions}
    Agents rewards: {rew_n}
    Agent Observations:
        AG_Green:
            POS: {the_same_obs[0:2]}
            VEL: {the_same_obs[2:4]}
        AG_Blue:
            POS: {the_same_obs[4:6]}
            VEL: {the_same_obs[6:8]}
        SP:
            POS: {the_same_obs[8:10]}
            VEL: {the_same_obs[10:12]}
    -----------------------------
    """)
    env.render(mode='human')
