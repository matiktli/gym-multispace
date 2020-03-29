

# Representation of world physical state
class WorldState():

    WORLD_DIM_2D = 2
    WORLD_SIZE_2D_SMALL = (20, 20)
    WORLD_SIZE_2D_MEDIUM = (50, 50)
    WORLD_SIZE_2D_BIG = (100, 100)

    def __init__(self):

        self.dim = WorldState.WORLD_DIM_2D

        self.size = WorldState.WORLD_SIZE_2D_SMALL

        # Time in between of simulation events in seconds
        self.timestamp = 0.1

        # Environment friction
        self.friction = 0.9

        # Entities contact margin
        self.contact_margin = 1
