__version__ = '0.1.0'

import numpy as np
import math
import Config as cfg
from time import sleep

class Move(object):
    def __init__(self, score = None, xindex = None, yindex = None):
        self.x = xindex
        self.y = yindex
        self.score = score

    def update(self, newmove):
        self.x = newmove.x
        self.y = newmove.y
        self.score = newmove.score


class TacBoard(object):
    def __init__(self):
        self.board = np.zeros((3,3))  # 0 is no move, 1 is bot, -1 is user
        self.winners = None  # Flat array with start and end of winning set

    def get_free_space_vector(self):
        ret_vec = []
        for row in self.board:
            ret_vec += [True if v == 0 else False for v in row]
        return ret_vec

    def get_winner_coords(self):
        p0 = [math.floor(self.winners[0] / 3), self.winners[0] % 3]
        p1 = [math.floor(self.winners[1] / 3), self.winners[1] % 3]
        return p0, p1

    def user_move(self, user_move_index):
        self.board[math.floor(user_move_index / 3), user_move_index % 3] = -1

    def bot_move(self, botmove):
        self.board[botmove.x, botmove.y] = 1

    def get_best_move(self):
        if cfg.DEBUG_MODE:
            print(self.board)
        return self._calc_move(self.board, 1)

    def get_worst_move(self):
        # For the memes....
        return self._calc_move(self.board, 1, worst=True)

    def _calc_move(self, board_array, player, worst=False):
        # Worst move for AI does minmin instead of minmax search
        if worst == True or player == -1:
            best_move = Move(np.inf)
        else:
            best_move = Move(-np.inf)

        moves = self.possible_moves(board_array)

        # Check if game is over
        score = self.win_check(board_array)
        if len(moves) == 0 or not score == 0:
            best_move.score = score
            return best_move

        # Otherwise do minmax search
        for move in moves:
            board_copy = board_array.copy()
            board_copy[move.y][move.x] = player
            test_move = self._calc_move(board_copy, -1 * player, worst=worst)
            test_move.x = move.x
            test_move.y = move.y

            if (worst == True and test_move.score < best_move.score) or \
                    (worst == False and player == 1 and test_move.score > best_move.score) or \
                    (worst == False and player == -1 and test_move.score < best_move.score):
                best_move.update(test_move)

        return best_move

    def possible_moves(self, board_array=None):
        if board_array is None:
            board_array = self.board

        return [Move(None, x, y) for x in range(3) for y in range(3) if board_array[y, x] == 0]

    def win_check(self, board_array=None):
        """ Return 0 if no win, 1 if bot win, -1 if user win """
        if board_array is None:
            board_array = self.board

        def check_set(oneset):
            if sum(oneset) == -3:
                return -1
            elif sum(oneset) == 3:
                return 1
            return 0

        for row in range(3):
            setresult = check_set(board_array[row])
            if setresult is not 0:
                self.winners = [row, row + 2]
                return setresult

        for col in range(3):
            setresult = check_set(board_array[:,col])
            if setresult is not 0:
                self.winners = [col, col + 6]
                return setresult

        diag1 = ([board_array[0,0], board_array[1,1], board_array[2,2]], [0, 8])
        diag2 = ([board_array[0,2], board_array[1,1], board_array[2,0]], [2, 6])

        for diagset, winset in [diag1, diag2]:
            setresult = check_set(diagset)
            if setresult is not 0:
                self.winners = winset
                return setresult
        
        return 0


# Standalone mode for testing
if __name__=='__main__':
    tacgame = TacBoard()
    tacgame.user_move(0,0)
    tacgame.bot_move(1,1)
    tacgame.user_move(1,0)
    nextmove = tacgame.get_best_move()
    # nextmove = tacgame.get_worst_move()
    print(nextmove.x, nextmove.y, nextmove.score)
    print(tacgame.get_free_space_vector())
