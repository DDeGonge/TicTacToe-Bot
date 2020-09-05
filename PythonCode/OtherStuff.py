__version__ = '0.1.0'

import Config as cfg
import random
import math
from Gameplay import *
from ScaraDriver import *

GAMETYPES = ['standard', 'meme']

def standard_game(scarabot, cam, spkr, bot_first: bool):
    spkr.play_opener()
    scarabot.draw_board()
    game = TacBoard()
    turn = 0 if bot_first else 1
    fasttrack = False  # Bot goes until wins

    while True:
        if turn == 0:
            # Pick random corner for first move
            first_move = Move(xindex=random.randint(0,1)*2, yindex=random.randint(0,1)*2)
            game.bot_move(first_move)
            scarabot.draw_move(first_move)
        elif fasttrack is True or turn % 2 == 0:
            # Bot turn
            scarabot.unpark()
            bot_best_move = game.get_best_move()
            if cfg.DEBUG_MODE:
                print('bot move:', bot_best_move.x, bot_best_move.y)
            game.bot_move(bot_best_move)
            scarabot.draw_move(bot_best_move)
        else:
            # Player turn
            scarabot.park()
            if turn >= 5:
                bot_win_possible = game.is_bot_win_possible()
            else:
                bot_win_possible = True

            cam.locate_user_move_prep()
            spkr.play_users_turn()
            if bot_win_possible is False:
                if random.randint(0,1) == 0:
                    swat(cam, scarabot, spkr, n=2)
                else:
                    distract(cam, spkr)
                fasttrack = True
            else:
                _ = input('Press enter after moved. TODO auto detect this or something idk...')
                user_move_index = cam.locate_user_move(game.get_free_space_vector())
                if cfg.DEBUG_MODE:
                    print('user_move_index:', user_move_index)
                game.user_move(user_move_index)

        if cfg.DEBUG_MODE:
            print('Turn:', turn)

        game_result = game.win_check(report_tie=True)
        if cfg.DEBUG_MODE:
            print('Game Result:', game_result)

        if game_result == 1:
            spkr.play_compliment()
            scarabot.draw_win_line(game)
            return
        elif game_result == 2:
            # Tie, should be impossible
            return
        elif game_result == -1:
            # This should also be impossible but idk..
            return

        turn += 1


def meme_game(scarabot, cam, spkr, bot_first: bool):
    print("one day this will exist. But for now, I am the meme.")

def distract(cam, spkr):
    timeout_s = 60
    t_start = time.time()
    cam.locate_user_move_prep()
    while time.time() < t_start + timeout_s:
        if cam.identify_motion():
            spkr.play_distract()
            time.sleep(2)
            return

def swat(cam, bot, spkr, n=1):
    """ Swat away user hand when seen n times """
    timeout_s = 60
    swats = 0
    t_start = time.time()
    cam.locate_user_move_prep()
    while time.time() < t_start + timeout_s:
        if cam.identify_motion():
            bot.absolute_move(-20,40,700)
            bot.absolute_move(130,60,700)
            bot.absolute_move(-40,70,700)
            bot.park()
            swats += 1

            if swats >= n:
                spkr.play_taunt()
                return

            spkr.play_users_turn()
            
