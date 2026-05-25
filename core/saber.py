# ============================================
# core/saber.py
# ============================================

import cv2
import math
import random

saber_active = False

saber_length = 220

colors = [

    ("blue", (255, 120, 0)),
    ("green", (0, 255, 0)),
    ("red", (0, 0, 255)),
    ("purple", (255, 0, 255))

]

current_color_index = 0

current_color_name = colors[current_color_index][0]


def toggle_saber(state):

    global saber_active

    saber_active = state


def update_saber():
    pass


def change_color():

    global current_color_index
    global current_color_name

    current_color_index = (
        current_color_index + 1
    ) % len(colors)

    current_color_name = colors[current_color_index][0]


def draw_saber(
    frame,
    glow_layer,
    wx,
    wy,
    ix,
    iy,
    swing_speed
):

    if not saber_active:

        return wx, wy

    dx = ix - wx
    dy = iy - wy

    mag = math.sqrt(dx * dx + dy * dy)

    if mag == 0:
        mag = 1

    dx /= mag
    dy /= mag

    end_x = int(wx + dx * saber_length)
    end_y = int(wy + dy * saber_length)

    saber_color = colors[current_color_index][1]

    # ============================================
    # MOVIE-LIKE FLICKER
    # ============================================

    brightness = random.randint(180,255)

    # ============================================
    # OUTER GLOW
    # ============================================

    cv2.line(
        glow_layer,
        (wx, wy),
        (end_x, end_y),
        saber_color,
        30
    )

    cv2.line(
        glow_layer,
        (wx, wy),
        (end_x, end_y),
        saber_color,
        22
    )

    cv2.line(
        glow_layer,
        (wx, wy),
        (end_x, end_y),
        saber_color,
        14
    )

    # ============================================
    # WHITE CORE
    # ============================================

    cv2.line(
        frame,
        (wx, wy),
        (end_x, end_y),
        (brightness, brightness, brightness),
        6
    )

    # ============================================
    # MOTION BOOST
    # ============================================

    if swing_speed > 40:

        cv2.line(
            glow_layer,
            (wx, wy),
            (end_x, end_y),
            saber_color,
            40
        )

    return end_x, end_y