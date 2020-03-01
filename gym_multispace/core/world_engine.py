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
                print(f'Applying move_act: {agent.action.move_act}')
                entities_forces[i] = agent.action.move_act

        return entities_forces

    # Apply physical forces of environment and forces between objects
    def apply_physical_interaction_forces(self, world, entities_forces):
        # Each object interact with all other entities in the world besides of itself
        for i_a, entity_a in enumerate(world.objects_all):
            for i_b, entity_b in enumerate(world.objects_all):
                if entity_a.uuid == entity_b.uuid:
                    # Entity can not interact with itself
                    continue
                force_a = np.zeros(world.state.dim)
                force_b = np.zeros(world.state.dim)
                if entity_a.can_collide or entity_b.can_collide:
                    force_a, force_b = self.__apply_impact_force_between_entities(entity_a,
                                                                                  entity_b,
                                                                                  force_a,
                                                                                  force_b)

                force_a, force_b = self.__apply_gravitational_force_between_entities(entity_a,
                                                                                     entity_b,
                                                                                     force_a,
                                                                                     force_b)

                # Apply all interaction forces between entityes to them
                # TODO[hard] fix how forces are applied to entities
                # entities_forces[i_a] = entities_forces[i_a] + force_a
                entities_forces[i_b] = entities_forces[i_b] + force_b
        return entities_forces

    # Calculate new state of entities/world after all forces applied
    def calculate_new_state(self, world, entities_forces):
        for i, entity in enumerate(world.objects_all):
            # This check is unnecessary, at this point not forces
            # should be applyed if entity can not move
            print(f' Entity: {entity.uuid} ->  {entities_forces[i]}')
            if entity.can_move:
                # Calculate new velocity for entity
                entity.state.vel = Equations.calculate_velocity(entity.state.vel,
                                                                entities_forces[i],
                                                                entity.state.mass,
                                                                entity.state.max_speed,
                                                                world.state.friction,
                                                                world.state.timestamp)
                # Calculate new position for entity
                entity.state.pos = Equations.calculate_position(entity.state.pos,
                                                                entity.state.vel,
                                                                world.state.timestamp,
                                                                world.state.size)

    def __apply_impact_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        # Safety check on input:
        force_a = np.nan_to_num(force_a)
        force_b = np.nan_to_num(force_b)
        # If both entities can not be moved just save some time on computations
        if not (entity_a.can_be_moved and entity_b.can_be_moved):
            return force_a, force_b

        distance_between = Equations.distance(entity_a.state.pos,
                                              entity_b.state.pos)
        delta_position = Equations.delta_position(entity_a.state.pos,
                                                  entity_b.state.pos)
        distance_of_collision = Equations.min_distance(entity_a.state.size,
                                                       entity_b.state.size)
        # If entities are not with each other distances there is not collison
        if distance_between > distance_of_collision:
            return force_a, force_b

        i_force = Equations.impact_force(entity_a.state.mass,
                                         entity_b.state.mass,
                                         distance_between,
                                         entity_a.state.vel,
                                         entity_b.state.vel)
        print(
            f'1_[{entity_a.uuid} -> {entity_b.uuid}]\n  i_force: {i_force}, force_a: {force_a}, force_b: {force_b}.')
        if entity_a.can_be_moved:
            force_a = force_a + i_force
        if entity_b.can_be_moved:
            force_b = force_b - i_force
        # input(
        #     f'2_[{entity_a.uuid} -> {entity_b.uuid}]\n  i_force: {i_force}, force_a: {force_a}, force_b: {force_b}.')
        return force_a, force_b

    def __apply_gravitational_force_between_entities(self, entity_a, entity_b, force_a, force_b):
        return force_a, force_b
        # Safety check on input:
        force_a, force_b = np.nan_to_num(force_a), np.nan_to_num(force_b)
        distance_between = Equations.distance(entity_a.state.pos,
                                              entity_b.state.pos)
        g_force = Equations.gravitational_force(entity_a.state.mass,
                                                entity_b.state.mass,
                                                distance_between)

        print(
            f'1_[{entity_a.uuid} -> {entity_b.uuid}]\n  g_force: {g_force}, force_a: {force_a}, force_b: {force_b}.')
        if entity_a.can_be_moved:
            force_a = force_a + g_force
        if entity_b.can_be_moved:
            force_b = force_b - g_force

        print(
            f'2_[{entity_a.uuid} -> {entity_b.uuid}]\n  g_force: {g_force}, force_a: {force_a}, force_b: {force_b}.')
        return force_a, force_b


# Simple wrapper for equations since I am bad at remembering them
class Equations:

    GRAVITATIONAL_STATIC = 6.673 * (10 ^ -11)  # todo2 change notation

    # Delta position betwenn positions in X dim
    @staticmethod
    def delta_position(pos_a, pos_b):
        return (pos_a[0] - pos_b[0], pos_a[1] - pos_b[1])

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
        new_velocity = velocity * friction  # changed from (1-friction)
        if force is not None:
            # V(new) = V(old) + F/m * t = V(old) + a * t = V(old) + V(delta)
            new_velocity += (force / mass) * timestamp
            print(f'Force: {force}, mass: {mass}, vel: {new_velocity}')

        if max_speed is not None:
            # todo2 change to multi dim
            speed = np.sqrt(
                np.square(new_velocity[0]) + np.square(new_velocity[1]))
            if speed > max_speed:
                new_velocity = new_velocity / np.sqrt(np.square(new_velocity[0]) +
                                                      np.square(new_velocity[1])) * max_speed
        return new_velocity

    @staticmethod
    def calculate_position(position, velocity, timestamp, world_size=None):
        new_position = position + velocity * timestamp
        if world_size:
            if new_position[0] > world_size[0]:
                new_position[0] = world_size[0]
            if new_position[0] < 0:
                new_position[0] = 0
            if new_position[1] > world_size[1]:
                new_position[1] = world_size[1]
            if new_position[1] < 0:
                new_position[1] = 0
        print(f'new pos: {new_position}')
        return np.nan_to_num(new_position)

    @staticmethod
    def gravitational_force(mass_a, mass_b, distance):
        gravitational_force = (mass_a + mass_b) * \
            Equations.GRAVITATIONAL_STATIC / distance
        return np.nan_to_num(gravitational_force)

    # F = m * a    // force = mass * velocity
    @staticmethod
    def impact_force(mass_a, mass_b, distance, velocity_a, velocity_b):
        # F = 1/2 * m * v^2 / d
        impact_force = 0.5 * (mass_a + mass_b) * \
            np.power(velocity_a + velocity_b, 2) / distance
        return np.nan_to_num(impact_force)
