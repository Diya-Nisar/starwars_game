import cv2
import random

particles = []


def create_sparks(x, y):

    for _ in range(15):

        particles.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-5, 5),
            "vy": random.uniform(-5, 5),
            "life": 20
        })


def draw_particles(frame):

    global particles

    new_particles = []

    for p in particles:

        cv2.circle(
            frame,
            (int(p["x"]), int(p["y"])),
            3,
            (255, 255, 255),
            -1
        )

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["life"] -= 1

        if p["life"] > 0:
            new_particles.append(p)

    particles = new_particles