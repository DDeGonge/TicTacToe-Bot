__version__ = '0.1.0'

import time
import Config as cfg
import random
from SerialDevice import *
from ScaraDriver import *
# from CameraDriver import *
from OtherStuff import *


def main():
    try:
        serdev = SerialDevice()
        scarabot = Scara(serdev)
        cam = Camera()
        cam.start_camera()

        while True:
            button_input = True
            if button_input:
                bot_first = random.choice([True, False])
                game_function = random.choice(GAMETYPES)
                scarabot.speak_opener(bot_first)

                if game_function == 'standard':
                    standard_game(scarabot, cam, bot_first = bot_first)
                elif game_function == 'meme':
                    meme_game(scarabot, cam, bot_first = bot_first)
                
    except Exception as e:
        raise e

def test():
    sd = SerialDevice()
    scara = Scara(sd)
    
    scara.zero()
    scara.enable()
    scara.send_gcode('test.g')
    scara.disable()

if __name__=='__main__':
    # main()
    test()
