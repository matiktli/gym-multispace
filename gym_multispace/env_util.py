from gym_multispace.multi_agent_env import MultiAgentSpaceEnv
from gym_multispace.scenario import load_scenario_from_file
from gym import Env


def create_env(scenario_path) -> Env:

    scenario = load_scenario_from_file(scenario_path).Scenario()
    world = scenario.generate_world()
    env = MultiAgentSpaceEnv(world=world,
                             reward_callback=scenario.get_reward,
                             observation_callback=scenario.get_observation,
                             reset_callback=scenario.reset_world)
    return env
