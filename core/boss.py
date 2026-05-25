import cv2
import random
import math

boss = {

    "active": False,

    "x": 1000,
    "y": 360,

    "health": 100,

    "direction": -1,

    "lasers": [],

    "phase": 1
}


def spawn_boss():

    boss["active"] = True

    boss["health"] = 100

    boss["x"] = 1000

    boss["y"] = 360

    boss["lasers"] = []


def update_boss():

    if not boss["active"]:
        return

    # ============================================
    # PHASES
    # ============================================

    if boss["health"] < 70:
        boss["phase"] = 2

    if boss["health"] < 40:
        boss["phase"] = 3

    # ============================================
    # MOVEMENT
    # ============================================

    speed = 3 + boss["phase"]

    boss["y"] += boss["direction"] * speed

    if boss["y"] < 180:
        boss["direction"] = 1

    if boss["y"] > 540:
        boss["direction"] = -1

    # ============================================
    # LASERS
    # ============================================

    if random.randint(0, 30 - boss["phase"] * 5) == 0:

        boss["lasers"].append({

            "x": boss["x"] - 120,
            "y": boss["y"],

            "vx": -15 - boss["phase"] * 2

        })

    new_lasers = []

    for laser in boss["lasers"]:

        laser["x"] += laser["vx"]

        if laser["x"] > -100:

            new_lasers.append(laser)

    boss["lasers"] = new_lasers


def draw_boss(frame):

    if not boss["active"]:
        return

    # Outer shell
    cv2.circle(
        frame,
        (boss["x"], boss["y"]),
        120,
        (40,40,40),
        -1
    )

    # Inner shell
    cv2.circle(
        frame,
        (boss["x"], boss["y"]),
        90,
        (70,70,70),
        -1
    )

    # Weak core
    cv2.circle(
        frame,
        (boss["x"], boss["y"]),
        40,
        (0,0,255),
        -1
    )

    # Glow
    cv2.circle(
        frame,
        (boss["x"], boss["y"]),
        55,
        (0,0,180),
        5
    )

    # Health bar
    cv2.rectangle(
        frame,
        (340,40),
        (940,70),
        (80,80,80),
        -1
    )

    cv2.rectangle(
        frame,
        (340,40),
        (
            340 + int(boss["health"] * 6),
            70
        ),
        (0,0,255),
        -1
    )

    cv2.putText(
        frame,
        f"SITH CORE - PHASE {boss['phase']}",
        (360,110),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        3
    )

    # ============================================
    # DRAW LASERS
    # ============================================

    for laser in boss["lasers"]:

        cv2.line(
            frame,
            (laser["x"], laser["y"]),
            (laser["x"] + 50, laser["y"]),
            (0,0,255),
            8
        )

        cv2.line(
            frame,
            (laser["x"], laser["y"]),
            (laser["x"] + 50, laser["y"]),
            (255,255,255),
            2
        )


def boss_hits_player():

    for laser in boss["lasers"]:

        if laser["x"] < 200:

            return True

    return False