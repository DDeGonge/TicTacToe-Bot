__version__ = '0.1.0'

import time
import Config as cfg
import random
from SerialDevice import *
from ScaraDriver import *
from CameraDriver import *
from OtherStuff import *
from Gameplay import *


def main():
    try:
        serdev = SerialDevice()
        scarabot = Scara(serdev)
        scara.zero()
        scara.enable()
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

def draw_butterfly():
    sd = SerialDevice()
    scara = Scara(sd)
    scara.user_zero()
    scara.absolute_move(20,20)
    scara.send_gcode('butter.g')

def test():
    sd = SerialDevice()
    scara = Scara(sd)
    cam = Camera()
    cam.start_camera()
    
    scara.user_zero()
    # scara.draw_board()

    # testmove = Move(xindex=0, yindex=0)
    # scara.draw_move(testmove)
    # testmove = Move(xindex=1, yindex=1)
    # scara.draw_move(testmove)
    # testmove = Move(xindex=0, yindex=2)
    # scara.draw_move(testmove)

    standard_game(scara, cam, bot_first = True)

    scara.absolute_move(0, 0)

    scara.disable()

if __name__=='__main__':
    # main()
    # test()
    draw_butterfly()
