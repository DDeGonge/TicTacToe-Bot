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
            _ = input('Press enter to start game...')

            # Future improvements can happen here
            bot_first = True  # random.choice([True, False])
            game_function = 'standard'  # random.choice(GAMETYPES)

            # Start game
            if game_function == 'standard':
                standard_game(scarabot, cam, spkr, bot_first = bot_first)
            elif game_function == 'meme':
                meme_game(scarabot, cam, spkr, bot_first = bot_first)

            scarabot.park()
                
    except Exception as e:
        raise e


if __name__=='__main__':
    main()
