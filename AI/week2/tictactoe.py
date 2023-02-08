"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None

og_board = []


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

    Xcount = sum(s.count(X) for s in board)
    Ocount = sum(s.count(O) for s in board)

    # If all rows are nones
    if all(None in row for row in board):
        next_turn = X
    if (Xcount > Ocount):
        next_turn = O
    else:
        next_turn = X
    return next_turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if (board[i][j] == None):
                actions.add(tuple([i, j]))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    possible = actions(board_copy)

    if action in possible:

        board_copy[action[0]][action[1]] = player(board)
        return board_copy

    else:
        raise Exception("Not a possible move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for r in [check_columns(board), check_rows(board), check_diagonals(board)]:
        if r is not None:
            return r
    return None


def check_rows(board):
    for row in board:
        if row[0] == row[1] == row[2] is not None:
            return row[0]


def check_columns(board):
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] is not None:
            return board[0][col]


def check_diagonals(board):
    if (board[0][0] == board[1][1] == board[2][2]) or (board[2][0] == board[1][1] == board[0][2]):
        if board[1][1] is not None:
            return board[1][1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    w = winner(board)
    # There is a winner X or O
    if w is not None:
        return True
    # Board is completely filled
    if all(not None in row for row in board):
        return True
    # Game is still running
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == "X":
        return 1
    elif w == "O":
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None

    if player(board) == "X":

        best_score = -float("inf")
        best_move = None

        for action in actions(board):

            new_board = result(board, action)
            score = min_max(new_board)

            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    if player(board) == "O":

        best_score = float("inf")
        best_move = None

        for action in actions(board):

            new_board = result(board, action)
            score = min_max(new_board)

            if score < best_score:
                best_score = score
                best_move = action
        return best_move


def min_max (board):

    if (terminal(board)):
        return utility(board)

    if player(board) == "X":
        best_score = -float("inf")
        for action in actions(board):

            new_board = result(board,action)
            score = min_max(new_board)
            best_score = max(best_score, score)
        return best_score

    else:
        best_score = float("inf")
        for action in actions(board):
            new_board = result(board, action)
            score = min_max(new_board)
            best_score = min(best_score, score)
        return best_score