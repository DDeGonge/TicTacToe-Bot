__version__ = '0.1.0'

import sys
import pygame as pg
import os
import time
import random
import Config as cfg

class Speaker(object):
    prefixes = {
        'taunt': 'taunt',
        'compliment': 'comp',
        'cat': 'meow',
        'distract': 'distr',
        'swat': 'swat',
        'opener': 'open',
        'usermove': 'move'
    }

    def __init__(self):
        self.generate_tracks()
        pg.mixer.init(cfg.freq, cfg.bitsize, cfg.channels, cfg.buffer)
        pg.mixer.music.set_volume(cfg.volume)
        self.cat_mode = False

    def set_cat_mode(self):
        self.cat_mode = True

    def set_human_mode(self):
        self.cat_mode = False

    def generate_tracks(self):
        self.tracks = {}
        files = [f for f in os.listdir(cfg.audio_path) if f.endswith('.mp3')]
        for key, value in self.prefixes.items():
            self.tracks[key] = []
            for f in files:
                if f.startswith(value):
                    self.tracks[key].append(f)

    def _play_track(self, keyname):
        if self.cat_mode is True:
            track_i = random.randint(0, len(self.tracks['cat']) - 1)
            track = self.tracks['cat'][track_i]
        else:
            track_i = random.randint(0, len(self.tracks[keyname]) - 1)
            track = self.tracks[keyname][track_i]

        # Wait for previous track to finish if still running
        # self.wait_for_sound_to_end()

        pg.mixer.music.load(os.path.join(cfg.audio_path, track))
        pg.mixer.music.play()

    def wait_for_sound_to_end(self):
        while pg.mixer.music.get_busy():
            time.sleep(0.1)

    def play_taunt(self):
        self._play_track('taunt')

    def play_compliment(self):
        self._play_track('compliment')

    def play_cat(self):
        self._play_track('cat')

    def play_distract(self):
        self._play_track('distract')

    def play_swat(self):
        self._play_track('swat')

    def play_opener(self):
        self._play_track('opener')

    def play_users_turn(self):
        self._play_track('usermove')


if __name__=='__main__':
    s = Speaker()
