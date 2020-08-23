__version__ = '0.1.0'

import sys
import time
import os
import cv2
import scipy.misc
import Config as cfg
import numpy as np


def preprocess_image(img):
    # Greyscale and blur
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(5,5),0)
    if cfg.DEBUG_MODE:
        debug_save_img(blur, 'rawimg.jpg')

    # Transform image perspective
    pts1 = np.float32([cfg.p0, cfg.p1, cfg.p2, cfg.p3])
    pts2 = np.float32([[0,0],[cfg.POST_TRANSFORM_RES[0],0],[0,cfg.POST_TRANSFORM_RES[1]],cfg.POST_TRANSFORM_RES])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    blur_crop = cv2.warpPerspective(blur,M,(cfg.POST_TRANSFORM_RES[0],cfg.POST_TRANSFORM_RES[1]))
    if cfg.DEBUG_MODE:
        debug_save_img(blur_crop, 'transformed.jpg')

    return blur_crop


if __name__=='__main__':
    img1 = cv2.imread(os.path.join('testimgs', 'blank.jpg'), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(os.path.join('testimgs', 'notblank.jpg'), cv2.IMREAD_GRAYSCALE)
    
    img1crop = preprocess_image(img1)
    img2crop = preprocess_image(img2)

    alldiff = np.sum(cv2.absdiff(img1crop, img2crop))

    q1_diff = np.sum(cv2.absdiff(img1crop[0:110, 0:399], img2crop[0:110, 0:399]))
    q2_diff = np.sum(cv2.absdiff(img1crop[111:245, 0:399], img2crop[111:245, 0:399]))
    q3_diff = np.sum(cv2.absdiff(img1crop[246:400, 0:399], img2crop[246:400, 0:399]))

    print(alldiff)
    print(q1_diff, q2_diff, q3_diff)

    cv2.imwrite(os.path.join('testimgs', 'blank_cropped.jpg'), img1crop)
    cv2.imwrite(os.path.join('testimgs', 'notblank_cropped.jpg'), img2crop)

    diffimg = cv2.absdiff(img1crop[111:245, 0:399], img2crop[111:245, 0:399])
    cv2.imwrite(os.path.join('testimgs', 'imdiff.jpg'), diffimg)
