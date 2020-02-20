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
        for i, entity in enumerate(world.objects_all):
            # This check is unnecessary, at this point not forces
            # should be applyed if entity can not move
            if entity.can_move:
                # Calculate new velocity for entity
                entity.state.vel = Equations.calculate_velocity(entity.state.vel,
                                                                entities_forces[i],
                                                                entity.state.mass,
                                                                entity.state.max_speed,
                                                                world.state.friction,
                                                                world.timestamp)
                # Calculate new position for entity
                entity.state.pos = Equations.calculate_position(entity.state.pos,
                                                                entity.state.vel,
                                                                world.timestamp)

    def __apply_impact_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        distance_between = Equations.distance(entity_a.state.pos,
                                              entity_b.state.pos)
        delta_position = Equations.delta_position(entity_a.state.pos,
                                                  entity_b.state.pos)
        distance_of_collision = Equations.min_distance(entity_a.state.size,
                                                       entity_b.state.size)
        # TODO impl collision force
        return force_a, force_b

    def __apply_gravitational_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        # TODO impl gravitational force
        return force_a, force_b


# Simple wrapper for equations since I am bad at remembering them
class Equations:

    # Delta position betwenn positions in X dim
    @staticmethod
    def delta_position(pos_a, pos_b):
        return pos_a - pos_b

    # Distance between two positions in X dim
    @staticmethod
    def distance(pos_a, pos_b):
        d_pos = Equations.delta_position(pos_a, pos_b)
        # multidimensional pitagorean equation
        return np.sqrt(np.sum(np.square(d_pos)))

    # Distance of collision of two objects
    @staticmethod
    def min_distance(size_a, size_b):
        return size_a + size_b

    @staticmethod
    def calculate_velocity(velocity, force, mass, max_speed, friction, timestamp):
        new_velocity = velocity * (1 - friction)
        if (force is not None):
            new_velocity += (force / mass) * timestamp
        if max_speed is not None:
            # todo2 change to multi dim
            speed = np.sqrt(
                np.square(new_velocity[0]) + np.square(new_velocity[1]))
            if speed > max_speed:
                new_velocity = new_velocity / np.sqrt(np.square(new_velocity[0]) +
                                                      np.square(new_velocity)) * max_speed
        return new_velocity

    @staticmethod
    def calculate_position(position, velocity, timestamp):
        new_position = position + velocity * timestamp
        return new_position
