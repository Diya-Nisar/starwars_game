# ============================================
# main.py
# ============================================

import cv2
import numpy as np
import math
import time
import random
import pygame

from core.hand_tracking import process_hands, draw_landmarks
from core.gestures import is_fist, is_open_hand, peace_sign
from core.saber import toggle_saber, update_saber, draw_saber, change_color, current_color_name
from core.effects import add_shockwave, draw_shockwaves
from core.particles import create_sparks, draw_particles

from core.audio import (
    play_ignition,
    start_hum,
    stop_hum,
    play_swing,
    play_force,
    stop_all_audio,
    restart_ambience
)

from core.lightning import draw_lightning

from core.boss import (
    boss,
    spawn_boss,
    update_boss,
    draw_boss,
    boss_hits_player
)

from core.character import (
    draw_anakin,
    draw_yoda_message,
    draw_vader_boss,
    draw_sith_core
)

from core.maps import apply_map
from core.crawl import draw_crawl, reset_crawl

import core.blasters as blasters

# ============================================
# CAMERA
# ============================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ============================================
# STATES
# ============================================

CRAWL = 0
MENU = 1
COUNTDOWN = 2
PLAYING = 3
GAME_OVER = 4
WIN = 5

game_state = CRAWL

countdown_start = 0

# ============================================
# PLAYER
# ============================================

max_health = 100
health = 100

force_energy = 100

# ============================================
# GAMEPLAY
# ============================================

wave = 1

wave_duration = 30
wave_start_time = time.time()

combo = 0
combo_timer = 0

level_transition = False
level_transition_start = 0

victory_flash = 0

# ============================================
# MOVEMENT
# ============================================

prev_wrist = None
swing_speed = 0

trail_points = []

# ============================================
# STARS
# ============================================

stars = []

for _ in range(200):

    stars.append([
        random.randint(0, 1280),
        random.randint(0, 720),
        random.randint(1, 3)
    ])

# ============================================
# TIMERS
# ============================================

last_asteroid = time.time()

shake_frames = 0

# ============================================
# MAIN LOOP
# ============================================

while True:

    current_time = time.time()

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    glow_layer = np.zeros_like(frame)

    # ============================================
    # OPENING CRAWL
    # ============================================

    if game_state == CRAWL:

        done = draw_crawl(frame)

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        key = cv2.waitKey(1)

        if done or key == 32:
            game_state = MENU

        elif key == 27:
            break

        continue

    # ============================================
    # BACKGROUND MAP
    # ============================================

    frame = apply_map(frame, min(wave, 5))

    # ============================================
    # STAR OVERLAY
    # ============================================

    overlay = np.zeros_like(frame)

    for star in stars:

        cv2.circle(
            overlay,
            (star[0], star[1]),
            star[2],
            (255, 255, 255),
            -1
        )

    frame = cv2.addWeighted(frame, 0.85, overlay, 0.15, 0)

    # ============================================
    # MENU
    # ============================================

    if game_state == MENU:

        frame[:] = (0, 0, 0)

        cv2.putText(
            frame,
            "JEDI FORCE TRAINER",
            (210, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.9,
            (0, 255, 255),
            5
        )

        cv2.putText(
            frame,
            "ANAKIN'S FINAL TRIAL",
            (300, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "SURVIVE 4 WAVES",
            (400, 330),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "DEFEAT VADER AND THE SITH CORE",
            (250, 405),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            "PRESS SPACE TO START",
            (300, 610),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        frame = draw_yoda_message(
            frame,
            "Restore balance, you must."
        )

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        key = cv2.waitKey(1)

        if key == 32:

            restart_ambience()

            game_state = COUNTDOWN

            countdown_start = time.time()

            wave_start_time = time.time()

        elif key == 27:
            break

        continue

    # ============================================
    # COUNTDOWN
    # ============================================

    if game_state == COUNTDOWN:

        frame[:] = (0, 0, 0)

        elapsed = int(current_time - countdown_start)

        number = 3 - elapsed

        if number > 0:

            cv2.putText(
                frame,
                str(number),
                (560, 420),
                cv2.FONT_HERSHEY_SIMPLEX,
                7,
                (0, 255, 255),
                12
            )

        else:

            cv2.putText(
                frame,
                "BEGIN",
                (350, 420),
                cv2.FONT_HERSHEY_SIMPLEX,
                4,
                (0, 255, 0),
                8
            )

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        cv2.waitKey(1)

        if elapsed >= 3:

            game_state = PLAYING

            wave_start_time = time.time()

        continue

    # ============================================
    # TIME-BASED LEVEL TRANSITIONS
    # ============================================

    if (
        current_time - wave_start_time > wave_duration
        and not level_transition
        and not boss["active"]
        and wave < 5
    ):

        wave += 1

        wave_start_time = current_time

        wave_duration += 10

        level_transition = True

        level_transition_start = current_time

    if level_transition:

        frame[:] = (0, 0, 0)

        if wave == 2:
            location = "CORUSCANT SKIES"
        elif wave == 3:
            location = "MUSTAFAR"
        elif wave == 4:
            location = "HYPERSPACE JUMP"
        else:
            location = "DEATH STAR RUINS"

        cv2.putText(
            frame,
            f"WAVE {wave}",
            (420, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (0, 255, 255),
            6
        )

        cv2.putText(
            frame,
            location,
            (300, 430),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "PREPARE YOURSELF",
            (260, 520),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (255, 255, 255),
            2
        )

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        cv2.waitKey(1)

        if time.time() - level_transition_start > 2:

            level_transition = False

        continue

    # ============================================
    # BOSS
    # ============================================

    if wave >= 5 and not boss["active"] and game_state == PLAYING:

        spawn_boss()

    if boss["active"] and boss["health"] <= 0:

        boss["active"] = False

        victory_flash = 25

        stop_all_audio()

        game_state = WIN

    # ============================================
    # TRACKING
    # ============================================

    results = process_hands(frame)

    # ============================================
    # COMBO RESET
    # ============================================

    if time.time() - combo_timer > 2:

        combo = 0

    # ============================================
    # ASTEROIDS
    # ============================================

    if not boss["active"] and game_state == PLAYING:

        if wave == 1:
            spawn_delay = 0.9
        elif wave == 2:
            spawn_delay = 0.7
        elif wave == 3:
            spawn_delay = 0.5
        else:
            spawn_delay = 0.35

        if current_time - last_asteroid > spawn_delay:

            blasters.spawn_asteroid(w, h, wave)

            last_asteroid = current_time

    blasters.update_asteroids(frame)

    # ============================================
    # CHARACTER OVERLAY
    # ============================================

    frame = draw_anakin(frame)

    # ============================================
    # HANDS
    # ============================================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            wrist = hand_landmarks.landmark[0]
            index_base = hand_landmarks.landmark[5]

            wx, wy = int(wrist.x * w), int(wrist.y * h)
            ix, iy = int(index_base.x * w), int(index_base.y * h)

            if is_fist(hand_landmarks):

                toggle_saber(True)

                play_ignition()

                start_hum()

            if is_open_hand(hand_landmarks):

                toggle_saber(False)

                stop_hum()

            if peace_sign(hand_landmarks):

                change_color()

            update_saber()

            if prev_wrist:

                swing_speed = math.sqrt(
                    (wx - prev_wrist[0]) ** 2 +
                    (wy - prev_wrist[1]) ** 2
                )

            prev_wrist = (wx, wy)

            if swing_speed > 45:

                play_swing()

            # ============================================
            # FORCE PUSH
            # ============================================

            if (
                is_open_hand(hand_landmarks)
                and swing_speed > 30
                and force_energy > 0
            ):

                add_shockwave(wx, wy)

                play_force()

                shake_frames = 4

                force_energy -= 1

            else:

                if force_energy < 100:
                    force_energy += 0.2

            # ============================================
            # FORCE LIGHTNING
            # ============================================

            if peace_sign(hand_landmarks) and force_energy > 40:

                draw_lightning(frame, wx, wy)

                force_energy -= 0.5

                if boss["active"]:

                    dist = math.sqrt(
                        (wx - boss["x"]) ** 2 +
                        (wy - boss["y"]) ** 2
                    )

                    if dist < 250:

                        boss["health"] -= 0.3

                remaining = []

                for asteroid in blasters.asteroids:

                    dist = math.sqrt(
                        (wx - asteroid["x"]) ** 2 +
                        (wy - asteroid["y"]) ** 2
                    )

                    if dist > 250:

                        remaining.append(asteroid)

                blasters.asteroids = remaining

            # ============================================
            # DRAW SABER
            # ============================================

            end_x, end_y = draw_saber(
                frame,
                glow_layer,
                wx,
                wy,
                ix,
                iy,
                swing_speed
            )

            # ============================================
            # TRAILS
            # ============================================

            trail_points.append((end_x, end_y))

            if len(trail_points) > 12:

                trail_points.pop(0)

            for i in range(1, len(trail_points)):

                alpha = i / len(trail_points)

                cv2.line(
                    glow_layer,
                    trail_points[i - 1],
                    trail_points[i],
                    (255, 255, 255),
                    int(12 * alpha)
                )

            # ============================================
            # ASTEROID COLLISION
            # ============================================

            hit = blasters.check_asteroid_collision(
                end_x,
                end_y,
                wx,
                wy,
                create_sparks
            )

            if hit:

                combo += 1

                combo_timer = time.time()

                shake_frames = 3

            # ============================================
            # BOSS DAMAGE
            # ============================================

            if boss["active"]:

                dist_to_boss = math.sqrt(
                    (end_x - boss["x"]) ** 2 +
                    (end_y - boss["y"]) ** 2
                )

                if dist_to_boss < 140:

                    boss["health"] -= 1

                    shake_frames = 5

            draw_landmarks(frame, hand_landmarks)

    # ============================================
    # DAMAGE
    # ============================================

    if blasters.asteroid_hit_player(w):

        health -= 10

        shake_frames = 8

    if boss_hits_player():

        health -= 1

        shake_frames = 6

    if health <= 0:

        stop_all_audio()

        game_state = GAME_OVER

    # ============================================
    # DRAW
    # ============================================

    update_boss()

    if boss["active"]:

        frame = draw_vader_boss(
            frame,
            boss["x"],
            boss["y"]
        )

        frame = draw_sith_core(
            frame,
            boss["x"],
            boss["y"] - 130
        )

    draw_boss(frame)

    blasters.draw_asteroids(frame)

    draw_particles(frame)

    draw_shockwaves(frame)

    frame = cv2.addWeighted(
        frame,
        1.0,
        glow_layer,
        0.8,
        0
    )

    # ============================================
    # VICTORY FLASH
    # ============================================

    if victory_flash > 0:

        flash = np.full_like(frame, 255)

        alpha = victory_flash / 25

        frame = cv2.addWeighted(
            frame,
            1 - alpha,
            flash,
            alpha,
            0
        )

        shake_frames = 12

        victory_flash -= 1

    # ============================================
    # SHAKE
    # ============================================

    if shake_frames > 0:

        shake_x = random.randint(-8, 8)
        shake_y = random.randint(-8, 8)

        M = np.float32([
            [1, 0, shake_x],
            [0, 1, shake_y]
        ])

        frame = cv2.warpAffine(
            frame,
            M,
            (frame.shape[1], frame.shape[0])
        )

        shake_frames -= 1

    # ============================================
    # HUD
    # ============================================

    cv2.rectangle(frame, (20, 20), (320, 50), (80, 80, 80), -1)

    cv2.rectangle(
        frame,
        (20, 20),
        (20 + int((health / max_health) * 300), 50),
        (0, 255, 0),
        -1
    )

    cv2.rectangle(frame, (20, 70), (320, 100), (80, 80, 80), -1)

    cv2.rectangle(
        frame,
        (20, 70),
        (20 + int(force_energy * 3), 100),
        (255, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"SCORE: {blasters.score}",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"WAVE: {wave}",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    if not boss["active"] and wave < 5:

        remaining_time = max(
            0,
            int(wave_duration - (current_time - wave_start_time))
        )

        cv2.putText(
            frame,
            f"NEXT WAVE: {remaining_time}s",
            (20, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    cv2.putText(
        frame,
        f"COMBO x{combo}",
        (900, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "ANAKIN",
        (980, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # ============================================
    # STORY POPUPS
    # ============================================

    if wave == 1 and game_state == PLAYING:

        frame = draw_yoda_message(
            frame,
            "Train you, I will."
        )

    elif wave == 3 and game_state == PLAYING:

        frame = draw_yoda_message(
            frame,
            "Fear is the path to darkness."
        )

    elif boss["active"]:

        frame = draw_yoda_message(
            frame,
            "Face him, you must."
        )

    # ============================================
    # WIN SCREEN
    # ============================================

    if game_state == WIN:

        stop_all_audio()

        frame[:] = (0, 0, 0)

        cv2.putText(
            frame,
            "THE FORCE IS WITH YOU",
            (110, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 255),
            5
        )

        cv2.putText(
            frame,
            "SITH CORE DESTROYED",
            (260, 390),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            f"FINAL SCORE: {blasters.score}",
            (370, 500),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "PRESS R TO RESTART",
            (300, 620),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        key = cv2.waitKey(1)

        if key == ord("r"):

            health = 100
            force_energy = 100
            wave = 1
            wave_duration = 30
            wave_start_time = time.time()
            combo = 0
            victory_flash = 0
            blasters.score = 0
            blasters.asteroids.clear()
            boss["active"] = False
            reset_crawl()
            game_state = MENU

        elif key == 27:
            break

        continue

    # ============================================
    # GAME OVER
    # ============================================

    if game_state == GAME_OVER:

        frame[:] = (0, 0, 0)

        cv2.putText(
            frame,
            "THE JEDI HAS FALLEN",
            (150, 320),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            5
        )

        cv2.putText(
            frame,
            f"FINAL SCORE: {blasters.score}",
            (380, 450),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "PRESS R TO RESTART",
            (300, 620),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        cv2.imshow("STAR WARS FORCE TRAINER", frame)

        key = cv2.waitKey(1)

        if key == ord("r"):

            health = 100
            force_energy = 100
            wave = 1
            wave_duration = 30
            wave_start_time = time.time()
            combo = 0
            victory_flash = 0
            blasters.score = 0
            blasters.asteroids.clear()
            boss["active"] = False
            reset_crawl()
            game_state = MENU

        elif key == 27:
            break

        continue

    # ============================================
    # SHOW
    # ============================================

    cv2.imshow("STAR WARS FORCE TRAINER", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()

cv2.destroyAllWindows()