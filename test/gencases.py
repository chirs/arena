
import pickle

    ### tictactoe cases ###
tictactoe_cases = [
    {
        'name': 'tictactoe',
        'history': [0,4,6,3,5,1,7,8,2],
        'result': -1,
        },
    
    {
        'name': 'tictactoe',
        'history': [4,3,2,6,0,1,8],
        'result': 1,
        },
    
    {
        'name': 'tictactoe',
        'history': [0,1,9],
        'result': 2,
        },
    ]
        

    ### checkers cases ###


    ### connect four cases ###

connectfour_cases = [
    {
        'name': 'connectfour',
        'history': [],
        'result': 0,
        },
    
    {
        'name': 'connectfour',
        'history': [
            0,1,0,1,0,1,
            1,0,1,0,1,0
            ],
        'result': 0,
        },

    # Vertical row.
    {
        'name': 'connectfour',
        'history': [0,1,0,1,0,1,0],
        'result': 1,
        },

    # Horizontal row.
    {
        'name': 'connectfour',
        'history': [0,0,1,1,2,2,3,3],
        'result': 1,
        },
        
    # Diagonal row.
    {
        'name': 'connectfour',
        'history': [0,1,1,2,2,3,2,3,3,4,3],
        'result': 1,
        },

    # Diagonal row, player 2 wins.
    {
        'name': 'connectfour',
        'history': [0,0,0,0,2,2,1,3,1,1,],
        'result': 2
        },
    
    # Tie.
    {
        'name': 'connectfour',
        'history': [
            0,1,0,1,0,1,
            1,0,1,0,1,0,
            2,3,2,3,2,3,
            3,2,3,2,3,2,
            4,5,4,5,4,5,
            5,4,5,4,5,4,
            6,6,6,6,6,6,
            ],
        'result': -1,
        },
    ]

cases = tictactoe_cases
#cases = connectfour_cases


