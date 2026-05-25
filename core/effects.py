import cv2

shockwaves = []


def add_shockwave(x, y):

    shockwaves.append({
        "x": x,
        "y": y,
        "radius": 10
    })


def draw_shockwaves(frame):

    global shockwaves

    new_shockwaves = []

    for shock in shockwaves:

        cv2.circle(
            frame,
            (shock["x"], shock["y"]),
            shock["radius"],
            (255, 255, 255),
            3
        )

        shock["radius"] += 15

        if shock["radius"] < 300:
            new_shockwaves.append(shock)

    shockwaves = new_shockwaves