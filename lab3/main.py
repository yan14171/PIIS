import chess
from algos import negamax, negascout, PVS
from utils import INFINITY

def get_percentage_diff(previous, current):
    if(previous == -INFINITY):
        return 100
    try:
        percentage = abs(previous - current)/max(previous, current) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

def get_move(depth, board, searchfunc):
    legalMoves = board.legal_moves
    bestMove = None

    maxScore = -INFINITY

    for move in legalMoves:
        board.push(move)

        if searchfunc == 'negamax':
            score = negamax(depth - 1, board)
        elif searchfunc == 'negascout':
            score = negascout(depth - 1, board, -INFINITY, INFINITY)
        elif searchfunc == 'PVS':
            score = PVS(depth - 1, board, -INFINITY, INFINITY)
        board.pop()
        if score >= maxScore:
            print('Now playing: ' + str(move.uci()) + ' which is better by ' + str(int(get_percentage_diff(maxScore, score))) + ' percent')
            maxScore = score
            bestMove = move
    return bestMove

def print_board(board):
    print('\n_______________')
    print(board)
    print('\n_______________')


def main(searchfunc):
    print('_______________\nGAME START\n_______________\n')
    board = chess.Board()
    print_board(board)
    while True:
        boardChange = get_move(2, board, searchfunc)
        print('_______________\n' + str(boardChange) + '\n_______________')
        board.push(boardChange)
        print_board(board)

        move = input("Your turn:")
        board.push_san(str(move))
        print_board(board)

main('negascout')



   