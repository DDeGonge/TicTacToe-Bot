__version__ = '0.1.0'

import time
import Config as cfg
import random
from SerialDevice import *
from ScaraDriver import *
from CameraDriver import *
from SpeakerDriver import *
from OtherStuff import *
from Gameplay import *


def main():
    try:
        serdev = SerialDevice()
        scarabot = Scara(serdev)
        cam = Camera()
        spkr = Speaker()

        scarabot.user_zero()
        scarabot.park()
        cam.start_camera()

        while True:
            inpt = input('Press enter to start game...')

            # Future improvements can happen here
            bot_first = True  # random.choice([True, False])
            game_function = 'standard'  # random.choice(GAMETYPES)

            if inpt == 'c':
                spkr.set_cat_mode()
            else:
                spkr.set_human_mode()

            # Start game
            if game_function == 'standard':
                standard_game(scarabot, cam, spkr, bot_first = bot_first)
            elif game_function == 'meme':
                meme_game(scarabot, cam, spkr, bot_first = bot_first)

            scarabot.park()
                
    except Exception as e:
        raise e

def stuff():
    serdev = SerialDevice()
    scarabot = Scara(serdev)
    # cam = Camera()
    spkr = Speaker()

    scarabot.user_zero()
    # cam.start_camera()
    scarabot.unpark()
    scarabot.draw_board()
    scarabot.draw_move(Move(xindex=0, yindex=0))
    scarabot.park()

    _ = input('waiting')

    scarabot.unpark()
    scarabot.draw_move(Move(xindex=1, yindex=0))
    scarabot.draw_move(Move(xindex=2, yindex=0))
    scarabot.draw_move(Move(xindex=0, yindex=1))
    scarabot.draw_move(Move(xindex=1, yindex=1))
    scarabot.draw_move(Move(xindex=2, yindex=1))
    scarabot.draw_move(Move(xindex=0, yindex=2))
    scarabot.draw_move(Move(xindex=1, yindex=2))
    scarabot.draw_move(Move(xindex=2, yindex=2))

    spkr.play_taunt()


if __name__=='__main__':
    # main()
    stuff()
