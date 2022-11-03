from numpy import Inf
from utils import getEval

def PVS(depth, board, alpha, beta):
    best_score = -Inf
    b = beta
    if depth == 0:
        return -getEval(board)

    for move in board.legal_moves:
        board.push(move)
        score = -PVS(depth - 1, board, -b, -alpha)
        if score > best_score:
            if alpha < score < beta:
                best_score = max(score, best_score)
            else:
                best_score = -PVS(depth - 1, board, -beta, -score)

        board.pop()
        if alpha > beta:
            return alpha
        b = alpha + 1
    return best_score

def negascout(depth, board, alpha, beta):
    best_score = -Inf
    b = beta
    if depth == 0:
        return -getEval(board)

    for move in board.legal_moves:
        board.push(move)
        score = -negascout(depth - 1, board, -b, -alpha)
        if score > best_score:
            if alpha < score < beta: # check for proper values when you don't need to research
                best_score = max(score, best_score)

            else:
                #if something, do another search
                best_score = -negascout(depth - 1, board, -beta, -score)

        board.pop()
        alpha = max(score, alpha) #always choose new best score rather than alpha, not like in PVS
        if alpha > beta:
            return alpha
        b = alpha + 1
    return best_score

def negamax(depth, board):
    # Check for leaf nodes
    if depth == 0:
        finalEval = getEval(board)
        return -finalEval # return NEGated evaluation

    max = -Inf
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(depth - 1, board) #check next node
        board.pop()

        if score > max:
            max = score #just set max
    return -max