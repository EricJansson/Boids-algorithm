
class Agent:
    """
    The unit that will be moving around the field
    """

    def __init__(self, id, pos): ## Constructor
        """
        Initialize the unit
        """
        self.id = id
        self.pos = pos.copy()
        print("Created agent: " + self.__repr__())

    def __repr__(self):
        """
        Returns a string representation of the object.
        """
        posString = "" + str(self.pos[0])
        for i in range(len(self.pos)):
            if i == 0:
                continue
            posString += ", " + str(self.pos[i])
        return f"{self.__class__.__name__}(id={self.id}, pos({posString}))"

    def get_pos(self):
        """
        Returns a string representation of the position.
        """
        posString = "" + str(self.pos[0])
        for i in range(len(self.pos)):
            if i == 0:
                continue
            posString += ", " + str(self.pos[i])
        return posString

    def move_2D(self, pos):
        """
        Move the agent.
        """
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]

