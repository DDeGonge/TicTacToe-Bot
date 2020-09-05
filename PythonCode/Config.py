""" MECHANICAL PARAMETERS """
s0_step_per_rev = 5760
s1_step_per_rev = 3200

# default_vel_mmps = 800.0
# default_accel_mmps2 = 40000.0
default_vel_mmps = 250.0
default_accel_mmps2 = 10000.0

s0_arm_len_mm = 100.5
s1_arm_len_mm = 90.0

pen_up_pwm = 100
pen_dn_pwm = 70

x_zero_offset = 21
y_zero_offset = 141

board_center_x_mm = 60
board_center_y_mm = 50
box_size_mm = 20


""" OPERATION PARAMETERS """
gcode_folder = 'gcode'



""" CAMERA PARAMETERS """
# Cropped region corner points, consider rotation plz
p0 = [145, 115] # TL
p1 = [520, 100] # TR
p2 = [175, 400] # BL
p3 = [470, 385] # BR

IMAGE_RESOLUTION = (648,486)
IMAGE_ROTATION_DEGS = 0

POST_TRANSFORM_RES = [400,400]

TAC_BOX_CENTERS = [
    (67, 67),
    (67, 200),
    (67, 333),
    (200, 67),
    (200, 200),
    (200, 333),
    (333, 67),
    (333, 200),
    (333, 333)
]

TAC_BOX_X = 90
TAC_BOX_Y = 90

""" OPENCV PARAMETERS """
MOTION_MIN_CHANGE = 1.0



""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': s0_arm_len_mm,
    'b': s1_arm_len_mm,
    'c': s0_step_per_rev,
    'd': s1_step_per_rev,
    'e': x_zero_offset,
    'f': y_zero_offset,
    'g': pen_up_pwm,
    'h': pen_dn_pwm
}

""" DEBUG PARAMS """
DEBUG_MODE = True
