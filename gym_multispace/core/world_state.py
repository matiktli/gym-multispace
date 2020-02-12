

# Representation of world physical state
class WorldState():

    def __init__(self):

        # Time in between of simulation events in seconds
        self.timestamp = 1

        # Environment friction
        self.friction = 0.10

        # Entities contact margin
        self.contact_margin = 0
