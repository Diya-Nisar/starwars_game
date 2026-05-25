import cv2
import numpy as np

maps = {
    1: cv2.imread("assets/background/tatooine.jpg"),
    2: cv2.imread("assets/background/coruscant.jpg"),
    3: cv2.imread("assets/background/mustafar.jpg"),
    4: cv2.imread("assets/background/hyperspace.jpg"),
    5: cv2.imread("assets/background/deathstar.jpg"),
}


def apply_map(frame, wave):
    bg = maps.get(wave)

    if bg is None:
        return frame

    bg = cv2.resize(bg, (frame.shape[1], frame.shape[0]))

    frame = cv2.addWeighted(frame, 0.35, bg, 0.65, 0)

    return frame