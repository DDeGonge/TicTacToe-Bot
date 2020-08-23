""" MECHANICAL PARAMETERS """
s0_step_per_rev = 5760
s1_step_per_rev = 3200

default_vel_mmps = 500
default_accel_mmps2 = 5000

s0_arm_len_mm = 100.5
s1_arm_len_mm = 90

step_len_us = 1  # NOT CURRENTLY USED

x_zero_offset = 25
y_zero_offset = 150


""" OPERATION PARAMETERS """
gcode_folder = 'gcode'


""" CAMERA PARAMETERS """
# Cropped region corner points
p0 = [28, 38] # TL
p1 = [575, 33] # TR
p2 = [120, 410] # BL
p3 = [488, 408] # BR

IMAGE_RESOLUTION = (648,486)
IMAGE_ROTATION_DEGS = 0

POST_TRANSFORM_RES = [400,400]

TAC_BOX_CENTERS = [
    (100, 100),
    (100, 200),
    (100, 300),
    (200, 100),
    (200, 200),
    (200, 300),
    (300, 100),
    (300, 200),
    (300, 300)
]

TAC_BOX_X = 90
TAC_BOX_y = 90

""" OPENCV PARAMETERS """
MIN_CHANGE = 100


""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': s0_arm_len_mm,
    'b': s1_arm_len_mm,
    'c': s0_step_per_rev,
    'd': s1_step_per_rev,
    'e': x_zero_offset,
    'f': y_zero_offset
}

""" DEBUG PARAMS """
DEBUG_MODE = False
