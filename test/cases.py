
cases = [

### tictactoe cases ###

    {
        'case_id': 1,
        'game': 'tictactoe',
        'history': [0,4,6,3,5,1,7,8,2],
        'result': -1,
    },
    
    {
        'case_id': 2,
        'game': 'tictactoe',
        'history': [4,3,2,6,0,1,8],
        'result': 1,
    },
    
    {
        'case_id': 3,
        'game': 'tictactoe',
        'history': [0,1,9],
        'result': 2,
    },

### checkers cases ###

    {
        'case_id': 4,
        'game': 'checkers',
        'history': [[1, 9]], # Illegal move - invalid move.
        'result': 2,
    },

    {
        'case_id': 5,
        'game': 'checkers',
        'history': [[0, 9]], # Illegal move - no piece.
        'result': 2,
    },

    {
        'case_id': 6,
        'game': 'checkers',
        'history': [[40, 33]], # Illegal move - opponent's piece.
        'result': 2,
    },

    {
        'case_id': 7,
        'game': 'checkers',
        'history': [[17, 26], [40, 32]], # Illegal move by second opponent.
        'result': 1,
    },

    {
        'case_id': 8,
        'game': 'checkers',
        # Complete game, but no multi-captures. Player 2 loses because no more move.
        'history': [[17,24],[40,33],[10,17],[49,40],[17,26],[44,37],[8,17],[42,35],[24,42],[51,33],[26,44],[53,35],[21,30],[35,26],[30,44],[26,8],[23,30],[33,26],[19,33],[40,26],[3,10],[26,17],[10,24],[56,49],[24,33],[49,42],[33,51],[60,42],[30,39],[42,35],[39,53],[55,46],[14,23],[46,39],[12,19],[39,30],[23,37],[35,26],[19,33],[62,55],[33,42],[55,46],[37,55],[58,51],[44,58]],
        'result': 1,
    },

    {
        'case_id': 16,
        'game': 'checkers',
        # Complete game with multi-captures and kings
        'history': [[17,24],[40,33],[19,28],[49,40],[12,19],[46,39],[3,12],[56,49],[10,17],[44,35],[17,26],[35,17],[8,26],[53,44],[1,10],[60,53],[10,17],[42,35],[28,42,60,46],[55,37],[24,42,56],[58,49],[56,42],[40,33],[42,24],[37,28],[21,35,53],[62,44],[24,33],[39,30],[23,37,51]],
        'result': 1,
    },

### connect four cases ###

#    {
#        'case_id': 9,
#        'game': 'connectfour',
#        'history': [],
#        'result': 0,
#    },
#    
#    {
#        'case_id': 10,
#        'game': 'connectfour',
#        'history': [
#            0,1,0,1,0,1,
#            1,0,1,0,1,0
#            ],
#        'result': 0,
#    },

    # Vertical row.
    {
        'case_id': 11,
        'game': 'connectfour',
        'history': [0,1,0,1,0,1,0],
        'result': 1,
    },

#    # Horizontal row.
#    {
#        'case_id': 12,
#       'game': 'connectfour',
#       'history': [0,0,1,1,2,2,3,3],
#       'result': 1,
#    },
#       
#    # Diagonal row.
#    {
#        'case_id': 13,
#        'game': 'connectfour',
#        'history': [0,1,1,2,2,3,2,3,3,4,3],
#        'result': 1,
#    },
#
#    # Diagonal row, player 2 wins.
#    {
#        'case_id': 14,
#        'game': 'connectfour',
#        'history': [0,0,0,0,2,2,1,3,1,1,],
#        'result': 2
#    },
#    
#    # Tie.
#    {
#        'case_id': 15,
#        'game': 'connectfour',
#        'history': [
#            0,1,0,1,0,1,
#            1,0,1,0,1,0,
#            2,3,2,3,2,3,
#            3,2,3,2,3,2,
#            4,5,4,5,4,5,
#            5,4,5,4,5,4,
#            6,6,6,6,6,6,
#            ],
#        'result': -1,
#    },

    ]

