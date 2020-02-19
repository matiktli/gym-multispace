import numpy as np


# Physic engine of the world
class PhysicEngine():

    # Apply forces coresponding to actions taken by agents
    def apply_actions_forces(self, world, entities_forces):
        # Apply forces from interactions between objects
        # Action passed into the Engine is already in dim of the world
        for i, agent in enumerate(world.objects_all):
            if agent.can_move:
                # todo2 - noise?
                entities_forces[i] = agent.action.move_act
        return entities_forces

    # Apply physical forces of environment and forces between objects
    def apply_physical_interaction_forces(self, world, entities_forces):
        # Each object interact with all other entities in the world besides of itself
        for i_a, entity_a in enumerate(world.objects_all):
            for i_b, entity_b in enumerate(world.objects_all):
                if entity_a is entity_b:
                    # Entity can not interact with itself
                    continue
                if not entity_a.can_collide or not entity_b.can_collide:
                    # Only collidable entities can interact
                    continue
                force_a = [0.0 for _ in range(world.state.dim)]
                force_b = [0.0 for _ in range(world.state.dim)]

                force_a, force_b = self.__apply_impact_force_between_entities(entity_a,
                                                                              entity_b,
                                                                              force_a,
                                                                              force_b)

                force_a, force_b = self.__apply_gravitational_force_between_entities(entity_a,
                                                                                     entity_b,
                                                                                     force_a,
                                                                                     force_b)

                # Apply all interaction forces between entityes to them
                entities_forces[i_a] = force_a + entities_forces[i_a]
                entities_forces[i_b] = force_b + entities_forces[i_b]
        return entities_forces

    # Calculate new state of entities/world after all forces applied
    def calculate_new_state(self, world, entities_forces):
        # TODO calculate new state of the world
        pass

    def __apply_impact_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        # TODO impl collision force
        distance = Equations.delta_distance(entity_a.state.pos, entity_b.pos)

        return force_a, force_b

    def __apply_gravitational_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        # TODO impl gravitational force
        return force_a, force_b


# Simple wrapper for equations since I am bad at remembering them
class Equations:

    # Distance between to positions in X dim
    @staticmethod
    def delta_distance(pos_a, pos_b):
        d_pos = pos_a - pos_b
        # multidimensional pitagorean equation
        return np.sqrt(np.sum(np.square(d_pos)))
