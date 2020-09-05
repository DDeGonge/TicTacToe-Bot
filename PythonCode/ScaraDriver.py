__version__ = '0.1.0'

import Config as cfg
import os
import time
import math

class Scara(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device
        self.x_error = 0.
        self.y_error = 0.
        self.configure()
        self.update_defaults()
        self.is_parked = False

    """ Motion stuff """

    def configure(self):
        command_string = 'C0'
        for k, v in cfg.Feather_Parameter_Chars.items():
            command_string += ' {}{}'.format(k, v)
        self.serial_device.command(command_string)

    def home(self):
        print('TODO implement this plz')

    def zero(self):
        self.serial_device.command('G92 X0 Y0')

    def enable(self):
        self.serial_device.command('M17')

    def disable(self):
        self.serial_device.command('M84')

    def user_zero(self):
        # Too lazy to implement limit switches so now I have to do this..
        self.disable()
        self.lower_pen()
        _ = input('Press enter when near zero...')
        self.enable()
        while True:
            com = input('Enter commands to move closer to zero in format "x,y", units are mm. Or press enter to continue: ')
            if com == '':
                break
            else:
                com = com.split(',')
                if len(com) == 2:
                    self.zero()
                    self.absolute_move(float(com[0]), float(com[1]))

        self.zero()
        self.raise_pen()

    def park(self):
        if self.is_parked = False:
            self.serial_device.command('G1 X-30 Y90')
            self.serial_device.command('G1 Y130')
        self.is_parked = True

    def unpark(self):
        if self.is_parked = True:
            self.serial_device.command('G1 X-30 Y90')
            self.serial_device.command('G1 X0 Y0')
        self.is_parked = False

    def raise_pen(self):
        self.serial_device.command('C2')

    def lower_pen(self):
        self.serial_device.command('C1')

    def update_defaults(self, vel = None, acc = None):
        if acc == None:
            acc = cfg.default_accel_mmps2
        if vel == None:
            vel = cfg.default_vel_mmps
        self.serial_device.command('M201 a{} v{}'.format(acc, vel))

    def absolute_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        # Calculate move
        command = 'G0 X{} Y{}'.format(xtar_mm, ytar_mm)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        self.serial_device.command(command)

    def relative_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        return self.absolute_move(xpos_mm + xtar_mm, ypos_mm + ytar_mm, velocity_mmps)

    def draw_move(self, move):
        x_center = cfg.board_center_x_mm + (move.x - 1) * cfg.box_size_mm
        y_center = cfg.board_center_y_mm + (1 - move.y) * cfg.box_size_mm
        self.absolute_move(x_center, y_center)
        self.send_gcode('draw_x.g')

    def draw_board(self):
        self.send_gcode('board.g')

    def draw_win_line(self, game):
        if game is None:
            return

        p_start, p_end = game.get_winner_coords()
        p_start_x = cfg.board_center_x_mm + (p_start[0] - 1) * cfg.box_size_mm
        p_start_y = cfg.board_center_y_mm + (1 - p_start[1]) * cfg.box_size_mm
        p_end_x = cfg.board_center_x_mm + (p_end[0] - 1) * cfg.box_size_mm
        p_end_y = cfg.board_center_y_mm + (1 - p_end[1]) * cfg.box_size_mm
        self.absolute_move(p_start_x, p_start_y)
        self.lower_pen()
        self.absolute_move(p_end_x, p_end_y)
        self.raise_pen()

    def send_gcode(self, filename):
        with open(os.path.join(cfg.gcode_folder, filename)) as f:
            while(True):
                line = f.readline().strip('\n')
                if not line:
                    break
                
                if line[0] == ';':
                    # Comments start with semicolon
                    continue

                self.serial_device.command(line)

    @property
    def is_homed(self):
        return True

    @property
    def xpos_mm(self):
        return

    @property
    def ypos_mm(self):
        return
