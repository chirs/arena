


class Game(object):
    """
    An abstract Game object.
    """
    
    def __init__(self):
        pass

    def move_legal(self):
        raise NotImplementedError

    def transition(self):
        raise NotImplementedError

    def initialize(self):
        raise NotImplementedError
    
    def winner(self):
        raise NotImplementedError
