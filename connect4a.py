from connect4base import ConnectFourBase




class ConnectFourAB(ConnectFourBase):




    def ab_search(self):
        move, score = self.max_value()
        return move

    def max_value(self):
        moves = self.legal_moves()

        results = []

        for move in moves:
            state = self.transition(move)
            
            
                



    def min_value(self):
        pass
                
            
            
