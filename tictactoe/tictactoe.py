"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    ex = 0
    oh = 0 
    for row in board:
        for element in row:
            if element == X:
                ex += 1
            if element == O:
                oh += 1
    if ex == oh:
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    i = -1
    for row in board:
        i += 1
        j = -1
        for cell in row:
            j+=1
            if cell == EMPTY:
                moves.add((i,j))
    return moves
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = []

    if action not in actions(board):
        raise Exception
    
    new_board = [row[:] for row in board]
    
    i=-1
    for row in new_board:
        i += 1
        j = -1
        for cell in row:
            j+=1
            if (i,j) == action:
                new_board[i][j] = player(new_board)

    return new_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for num in range(3):
        if board[num][0] is not EMPTY and board[num][0] == board[num][1] == board[num][2]:
            return board[num][0]
        if board[0][num] is not EMPTY and board[0][num] == board[1][num] == board[2][num]:
            return board[0][num]
        if board[1][1] is not EMPTY and (board[1][1] == board[0][0] == board[2][2] or board[1][1] == board[2][0] == board[0][2]):
            return board[1][1]  
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    full = 1
    for row in board:
        for cell in row:
            if cell == EMPTY:
                full = 0
    if full == 1:
        return True
    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        move = max_v(board)[0]
        return move
    if player(board) == O:
        move = min_v(board)[0]
        return move

    raise NotImplementedError

def max_v(board):
    if terminal(board):
        return (None,utility(board))
    v = float('-inf')
    best_move = None
    for move in actions(board):
        if min_v(result(board,move))[1] > v:
            v = min_v(result(board,move))[1]
            best_move = move
    return (best_move,v)

def min_v(board):
    if terminal(board):
        return (None,utility(board))
    v = float('inf')
    best_move = None
    for move in actions(board):
        if max_v(result(board,move))[1] < v:
            v = max_v(result(board,move))[1]
            best_move = move
    return (best_move,v)
    