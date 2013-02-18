


class Game(object):
    """
    An abstract Game object.
    """
    
    def __init__(self):
        pass

    @staticmethod
    def initial_board():
        raise NotImplementedError

    def draw_board(self):
        raise NotImplementedError


    def move_legal(self, move):
        raise NotImplementedError

    def transition(self, move, player):
        raise NotImplementedError
    
    def result(self):
        raise NotImplementedError
