# ============================================
# core/blasters.py
# ============================================

import cv2
import random
import math

from core.audio import play_explosion

asteroids = []

score = 0


def spawn_asteroid(width, height, wave):

    side = random.choice(["left", "right"])

    if side == "left":

        x = -50

        vx = random.randint(
            3 + wave,
            6 + wave
        )

    else:

        x = width + 50

        vx = -random.randint(
            3 + wave,
            6 + wave
        )

    asteroid = {

        "x": x,

        "y": random.randint(
            100,
            height - 100
        ),

        "vx": vx,

        "vy": random.randint(-2, 2),

        "radius": random.randint(25, 50)

    }

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

        # ============================================
        # MAIN BODY
        # ============================================

        cv2.circle(
            frame,
            (int(a["x"]), int(a["y"])),
            a["radius"],
            (60,60,60),
            -1
        )

        # ============================================
        # OUTER EDGE
        # ============================================

        cv2.circle(
            frame,
            (int(a["x"]), int(a["y"])),
            a["radius"],
            (120,120,120),
            4
        )

        # ============================================
        # CRATER
        # ============================================

        cv2.circle(
            frame,
            (
                int(a["x"] - a["radius"] // 3),

                int(a["y"] - a["radius"] // 3)
            ),
            a["radius"] // 5,
            (40,40,40),
            -1
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

    hit = False

    # ============================================
    # MULTIPLE HIT POINTS ALONG SABER
    # ============================================

    hit_points = []

    for t in [0.35, 0.5, 0.65, 0.8, 0.95]:

        px = int(
            wx + (end_x - wx) * t
        )

        py = int(
            wy + (end_y - wy) * t
        )

        hit_points.append((px, py))

    for a in asteroids:

        asteroid_hit = False

        for px, py in hit_points:

            dist = math.sqrt(

                (px - a["x"])**2 +

                (py - a["y"])**2

            )

            # ============================================
            # BETTER HITBOX
            # ============================================

            hit_radius = a["radius"] * 0.7

            if dist < hit_radius:

                asteroid_hit = True

                break

        if asteroid_hit:

            create_sparks(a["x"], a["y"])

            play_explosion()

            score += 1

            # ============================================
            # SPLIT ASTEROIDS
            # ============================================

            if a["radius"] > 20:

                for _ in range(2):

                    asteroids.append({

                        "x": a["x"],

                        "y": a["y"],

                        "vx": random.randint(-6,6),

                        "vy": random.randint(-6,6),

                        "radius": a["radius"] // 2

                    })

            hit = True

        else:

            remaining.append(a)

    asteroids = remaining

    return hit


def asteroid_hit_player(width):

    global asteroids

    remaining = []

    player_hit = False

    for a in asteroids:

        if a["x"] < -100 or a["x"] > width + 100:

            player_hit = True

        else:

            remaining.append(a)

    asteroids = remaining

    return player_hit