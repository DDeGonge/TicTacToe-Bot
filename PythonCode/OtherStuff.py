__version__ = '0.1.0'

import Config as cfg
import random
import math
from Gameplay import *
from ScaraDriver import *

GAMETYPES = ['standard', 'meme']

def standard_game(scarabot, cam, bot_first: bool):
    Scara.draw_board()
    game = TacBoard()
    turn = 0 if bot_first else 1

    while True:
        if turn % 2 == 0:
            # Bot turn
            bot_best_move = game.get_best_move()
            game.bot_move(bot_best_move.x, bot_best_move.y)
            Scara.draw_move()
        else:
            # Player turn
            cam.locate_user_move_prep()
            _ = input('Press enter after moved. TODO auto detect this or something idk...')
            user_move_index = cam.locate_user_move()
            game.user_move(math.floor(user_move_index / 3), user_move_index % 3)

        if game.win_check != 0:
            break


def meme_game(scarabot, cam, bot_first: bool):
    draw_board()
