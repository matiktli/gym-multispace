

# Physic engine of the world
class PhysicEngine:

    # Apply forces coresponding to actions taken by agents
    def apply_actions_forces(self, world, entities_forces):
        # Apply forces from interactions between objects
        # Action passed into the Engine is already in dim of the world
        for i, agent in enumerate(world.objects_all):
            if agent.can_move:
                # todo2 - noise?
                entities_forces[i] = agent.action.move_act
        return entities_forces

    def apply_physical_interaction_forces(self, world, entities_forces):
        # TODO calculate interactions
        pass

    # Calculate new state of entities/world after all forces applied
    def calculate_new_state(self, world, entities_forces):
        # TODO calculate new state of the world
        pass


# Simple wrapper for equations since I am bad at remembering them
class Equations:

    @staticmethod
    def todo():
        pass
