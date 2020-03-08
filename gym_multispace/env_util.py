from gym_multispace.multi_agent_env import MultiAgentSpaceEnv, SingleAgentSpaceEnv
from gym_multispace.scenario import load_scenario_from_file
from gym import Env
from abc import ABC


def create_env(scenario_path, is_absolute=False) -> Env:

    scenario = load_scenario_from_file(scenario_path, is_absolute).Scenario()
    world = scenario.generate_world()
    env = MultiAgentSpaceEnv(world=world,
                             reward_callback=scenario.get_reward,
                             observation_callback=scenario.get_observation,
                             reset_callback=scenario.reset_world,
                             done_callback=scenario.is_done)
    return env


def create_single_env(scenario_path, is_absolute=False) -> Env:
    scenario = load_scenario_from_file(scenario_path, is_absolute).Scenario()
    world = scenario.generate_world()
    env = SingleAgentSpaceEnv(world=world,
                              reward_callback=scenario.get_reward,
                              observation_callback=scenario.get_observation,
                              reset_callback=scenario.reset_world,
                              done_callback=scenario.is_done)
    return env
