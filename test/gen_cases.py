
import pickle

if __name__ == "__main__":

    cases = []

    ### tictactoe cases ###

    temp = {}
    temp['name'] = 'tictactoe'
    temp['history'] = [0,4,6,3,5,1,7,8,2]
    temp['result'] = -1
    cases.append(temp)

    temp = {}
    temp['name'] = 'tictactoe'
    temp['history'] = [4,3,2,6,0,1,8]
    temp['result'] = 1
    cases.append(temp)

    temp = {}
    temp['name'] = 'tictactoe'
    temp['history'] = [0,1,9]
    temp['result'] = 2
    cases.append(temp)

    ### checkers cases ###

    # ... 

    pickle.dump(cases, open("test_cases.p", "wb"))

