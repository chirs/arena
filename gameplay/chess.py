

from arena.gameplay.game import Game


# Need to only use coordinate system in computing positios.
# Correct coords2index to consider 2 characters per board place.


def index2coords(num):
    a, b = (num/8, num % 8)
    return (a,b)


def coords2index(coords):
    a, b = coords
    return 8*a + b



class Chess(Game):
    """
    An abstract Game object.
    """

    player_mapping = {
        1: 'w',
        2: 'b',
        }


    def __init__(self, board=None, current_player=1, moves_without_capture=0):
        self.board = board or self.initial_board()
        self.current_player = current_player
        self.moves_without_capture = moves_without_capture

        
    def copy(self):
        return 

    @staticmethod
    def initial_board():
        s = ''
        s += 'rbkbbbqbkbbbkbrb'
        s += 'pb' * 8
        s += '  ' * 32
        s += 'pw' * 8
        s += 'rwkwbwqwkwbwkwrw'
        return s

    def draw_board(self):
        s = ''
        for i in range(0,128,16):
            s += self.board[i:i+8]
            s += '\n'
        s += '=' * 8
        return s


    def get_position(self, index):
        return self.board[index:index+2]

        

    def move_legal(self, move):
        raise NotImplementedError

    def transition(self, move):

        def set_position(board, index, chars):
            l = list(board)
            l[index*2:index*2+2] = chars
            return ''.join(l)

        start_p, end_p = move

        start_chars = self.get_position(start_p)
        end_chars = self.get_position(end_p)

        if end_chars != '  ':
            moves_without_capture = self.moves_without_capture + 1
        else:
            moves_without_capture = 0
            self.moves_without_capture = 0

        board = set_position(self.board, start_p, '  ')
        board = set_position(board, end_p, start_chars)

        return Chess(board, self.opponent(), moves_without_capture)



    def opponent(self):
        return 3 - self.current_player


    def is_empty(self, position):
        return self.get_position(position) == '  '


    def get_path(self, start, end):
        print start, end
        x1, y1 = start
        x2, y2 = end


        xd = x2 - x1
        yd = y2 - y1

        if xd == 0:
            x_direction = 0
        elif xd > 0:
            x_direction = 1
        else:
            x_direction = -1

        if yd == 0:
            y_direction = 0
        elif yd > 0:
            y_direction = 1
        else:
            y_direction = -1


        if x_direction == 0 and y_direction == 0:
            return []
        else:
            # Something is wong with this recursion.
            next_position = (x1+x_direction, y1+y_direction)
            return [(x1, y1)] + self.get_path(next_position, end)


    def blocked(self, position, player):
        player_color = self.player_mapping[player]
        piece, color = self.get_position(position)

        if same_color:
            return 1
        elif opponent_color: 
            return 2
        else:
            return 0


    def unblocked_path(start, end):
        path = self.get_path(start, end)
        moves = path[1:] # Exclude start

        unblocked = []

        for i in moves:
            piece, color = self.get_position(i)
            if piece == ' ':
                unblocked.append(i)
            elif color == self.player_mapping[self.current_player()]:
                return unblocked
            else:
                unblocked.append(i)
                return unblocekd
        

    def legal_moves(self, piece, position):

        px, color = piece
        
        coords = index2coords(position)

        def knight_moves():
            x, y = coords
            opts = [(1,2),(2,1),(-1,2),(2,-1),
                    (1,-2),(-2,1),(-1,-2),(-2,-1)]

            l = [(x+a,y+b) for a,b in opts]
            return [e for e in l if not is_empty(coords2index(e))]

            
        def pawn_moves():
            x, y = coords
            if self.first_move(position):
                l = [(x, y+1), (x, y+2)]
            else:
                l = [(x, y+1)]

            l.append(self.en_passant_positions(position))
            return [e for e in l if not self.is_blocked(e)]


        def rook_moves():
            x,y = coords

            return [self.unblocked_path((x,y), (x, y+7))] + \
                [self.unblocked_path((x,y), (x, y-7))] + \
                [self.unblocked_path((x,y), (x+7, y))] + \
                [self.unblocked_path((x,y), (x-7, y))]



        def bishop_moves():
            x,y = coords

            return [self.unblocked_path((x,y), (x+7, y+7))] + \
                [self.unblocked_path((x,y), (x+7, y-7))] + \
                [self.unblocked_path((x,y), (x-7, y+7))] + \
                [self.unblocked_path((x,y), (x-7, y-7))]


        def queen_moves():
            return bishop_moves() + rook_moves()

        def king_moves():
            x,y = coords
            opts = [(0,1),(-1,1),(-1,0),(-1,-1),
                    (0,-1),(1,-1),(1,0),(1,1)]

            moves = [(x+a,y+b) for (a,b) in opts]
            



        piece_moves = {
            'k': king_moves,
            'q': queen_moves,
            'r': rook_moves,
            'b': bishop_moves,
            'p': pawn_moves,
            'k': knight_moves
            }

        move_func = piece_moves[px]
        moves = move_func()

        on_board = lambda x, y: 0 <= x < 8 and 0 <= y < 8

        return [e for e in moves if on_board(e)]


    def all_legal_moves(self):
         
        moves = []
        for piece, position in self.get_piece_positions(self.current_player):
            moves.append(self.legal_moves(piece, position))

        return moves


    def in_check(self, player):
        king_position = self.get_king_position(self.current_player)

        for piece, position in self.get_piece_positions(self.opponent()):
            if king_position in self.legal_moves(piece, position):
                return True

        return False


    def in_checkmate(self):
        if self.in_check(self.current_player):
            for move in self.legal_moves():
                board = self.transition(move)
                if not self.in_check(self.current_player):
                    return True

        return False


    def is_tie(self):
        return self.moves_without_capture > 50
    
    def result(self):

        if self.is_tie():
            return -1

        if self.in_checkmate():
            return self.opponent()

        return 0
