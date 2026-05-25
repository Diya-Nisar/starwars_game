import cv2
import random


def draw_lightning(frame, start_x, start_y):

    x = start_x
    y = start_y

    for _ in range(15):

        nx = x + random.randint(-30,30)

        ny = y + random.randint(10,35)

        cv2.line(
            frame,
            (x,y),
            (nx,ny),
            (255,100,0),
            3
        )

        x = nx
        y = ny