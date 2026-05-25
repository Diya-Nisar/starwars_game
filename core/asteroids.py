import cv2
    asteroids.append(asteroid)


def update_asteroids(frame):

    global asteroids

    new_asteroids = []

    for a in asteroids:

        a["x"] += a["vx"]
        a["y"] += a["vy"]

        if -100 < a["x"] < frame.shape[1] + 100:
            new_asteroids.append(a)

    asteroids = new_asteroids


def draw_asteroids(frame):

    for a in asteroids:

        cv2.circle(
            frame,
            (int(a["x"]), int(a["y"])),
            a["radius"],
            (80, 80, 80),
            -1
        )

        cv2.circle(
            frame,
            (int(a["x"]), int(a["y"])),
            a["radius"],
            (120, 120, 120),
            4
        )


def check_asteroid_collision(
    end_x,
    end_y,
    wx,
    wy,
    create_sparks
):

    global asteroids
    global score

    remaining = []

    for a in asteroids:

        dist = abs(
            (end_y - wy) * a["x"] -
            (end_x - wx) * a["y"] +
            end_x * wy -
            end_y * wx
        ) / (
            math.sqrt(
                (end_y - wy) ** 2 +
                (end_x - wx) ** 2
            ) + 1
        )

        if dist < a["radius"]:

            create_sparks(a["x"], a["y"])

            score += 1

        else:
            remaining.append(a)

    asteroids = remaining