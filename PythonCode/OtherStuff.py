__version__ = '0.1.0'

import Config as cfg
import random
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

            cam.locate_user_move()

def meme_game(scarabot, cam, bot_first: bool):
    draw_board()
