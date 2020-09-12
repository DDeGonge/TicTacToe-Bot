__version__ = '0.1.0'

import sys
import time
import os
import cv2
import scipy.misc
import Config as cfg
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

class Camera(object):
    def __init__(self, resolution=cfg.IMAGE_RESOLUTION):
        self.camera = None
        self.resolution = resolution
        self.pre_move_img = None
        self.is_enabled = False

        # pic dump stuff
        self.pic_series = 0
        self.pic_type = ''

    def locate_user_move_prep(self):
        self.pic_type = 'pre'
        image = self._capture_image()
        self.pre_move_img = self.preprocess_image(image)

    def locate_user_move(self, free_spaces):
        self.pic_type = 'post'
        image = self._capture_image()
        processed_img_new = self.preprocess_image(image)

        maxdiff = 0
        box_width = int(cfg.TAC_BOX_X / 2)
        box_height = int(cfg.TAC_BOX_Y / 2)
        zone = None
        for i, (zone_x, zone_y) in enumerate(cfg.TAC_BOX_CENTERS):
            newimg_crop = processed_img_new[zone_x - box_width:zone_x + box_width, zone_y - box_height:zone_y + box_height]
            oldimg_crop = self.pre_move_img[zone_x - box_width:zone_x + box_width, zone_y - box_height:zone_y + box_height]
            zonediff = np.sum(cv2.absdiff(newimg_crop, oldimg_crop)) / (cfg.TAC_BOX_X * cfg.TAC_BOX_Y)

            if cfg.DEBUG_MODE:
                debug_save_img(cv2.absdiff(newimg_crop, oldimg_crop), '{}_diff_zone{}.jpg'.format(self.pic_series, i))

            print(i, zonediff)

            if zonediff > maxdiff and free_spaces[i] == True:
                maxdiff = zonediff
                zone = i

        self.pic_series += 1
        return zone

    def identify_motion(self):
        image = self._capture_image()
        processed_img_new = self.preprocess_image(image)

        motion_diff = np.sum(cv2.absdiff(self.pre_move_img, processed_img_new)) / (cfg.IMAGE_RESOLUTION[0] * cfg.IMAGE_RESOLUTION[1])
        if cfg.DEBUG_MODE:
            print('identify motion diff:', motion_diff)

        if motion_diff > cfg.MOTION_MIN_CHANGE:
            return True
        return False

    def _capture_image(self):
        if not self.is_enabled:
            self.start_camera()
        rawCapture = PiRGBArray(self.camera)
        self.camera.capture(rawCapture, format="bgr")
        return rawCapture.array

    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    @staticmethod
    def _save_image(img, path):
        scipy.misc.toimage(img, cmin=0.0, cmax=...).save('path')

    def start_camera(self):
        self.camera = PiCamera()
        self.configure_camera()
        self.is_enabled = True
        time.sleep(0.1)

    def configure_camera(self):
        self.camera.rotation = cfg.IMAGE_ROTATION_DEGS
        self.camera.resolution = self.resolution
        self.camera.exposure_mode = 'off'

    def stop_camera(self):
        self.camera.close()
        self.is_enabled = False

    """ Image recognition functions """

    def preprocess_image(self, img):
        # Greyscale and blur
        if cfg.DEBUG_MODE:
            debug_save_img(img, '{}_{}_raw.jpg'.format(self.pic_series, self.pic_type))

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        if cfg.DEBUG_MODE:
            debug_save_img(blur, '{}_{}_blur.jpg'.format(self.pic_series, self.pic_type))

        # Transform image perspective
        pts1 = np.float32([cfg.p0, cfg.p1, cfg.p2, cfg.p3])
        pts2 = np.float32([[0,0],[cfg.POST_TRANSFORM_RES[0],0],[0,cfg.POST_TRANSFORM_RES[1]],cfg.POST_TRANSFORM_RES])
        M = cv2.getPerspectiveTransform(pts1,pts2)
        blur_crop = cv2.warpPerspective(blur,M,(cfg.POST_TRANSFORM_RES[0],cfg.POST_TRANSFORM_RES[1]))
        if cfg.DEBUG_MODE:
            debug_save_img(blur_crop, '{}_{}_transform.jpg'.format(self.pic_series, self.pic_type))

        return blur_crop

    @staticmethod
    def load_offset_image(filepath, filename):
        import_img = cv2.imread(os.path.join(filepath, filename))
        return cv2.cvtColor(import_img,cv2.COLOR_BGR2GRAY)


def debug_save_img(img, imgname):
    im = Image.fromarray(img)
    im.save(os.path.join('/home/pi/imgs', imgname))


if __name__=='__main__':
    c = Camera()
    c.locate_user_move_prep()
    _ = input('press enter to continue...')
    result = c.locate_user_move([True]*9)
    print(result)
