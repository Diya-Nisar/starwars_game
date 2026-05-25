# ============================================
# core/audio.py
# ============================================

import pygame
import time

# ============================================
# LOW LATENCY AUDIO
# ============================================

pygame.mixer.pre_init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=256
)

pygame.init()

pygame.mixer.init()

# ============================================
# LOAD SOUNDS
# ============================================

ignition_sound = pygame.mixer.Sound(
    "assets/sounds/ignition.wav"
)

hum_sound = pygame.mixer.Sound(
    "assets/sounds/hum.wav"
)

swing_sound = pygame.mixer.Sound(
    "assets/sounds/swing.wav"
)

explosion_sound = pygame.mixer.Sound(
    "assets/sounds/explosion.wav"
)

force_sound = pygame.mixer.Sound(
    "assets/sounds/force.wav"
)

# ============================================
# VOLUMES
# ============================================

ignition_sound.set_volume(0.35)

hum_sound.set_volume(0.10)

swing_sound.set_volume(0.18)

explosion_sound.set_volume(0.22)

force_sound.set_volume(0.20)

# ============================================
# BACKGROUND AMBIENCE
# ============================================

pygame.mixer.music.load(
    "assets/sounds/ambience.wav"
)

pygame.mixer.music.set_volume(0.05)

pygame.mixer.music.play(-1)

# ============================================
# STATE
# ============================================

hum_playing = False

last_swing = 0

last_explosion = 0

last_force = 0

last_ignition = 0

# ============================================
# FUNCTIONS
# ============================================

def play_ignition():

    global last_ignition

    current = time.time()

    if current - last_ignition > 1:

        ignition_sound.play()

        last_ignition = current


def start_hum():

    global hum_playing

    if not hum_playing:

        hum_sound.play(-1)

        hum_playing = True


def stop_hum():

    global hum_playing

    hum_sound.stop()

    hum_playing = False


def play_swing():

    global last_swing

    current = time.time()

    if current - last_swing > 0.35:

        swing_sound.play()

        last_swing = current


def play_explosion():

    global last_explosion

    current = time.time()

    if current - last_explosion > 0.2:

        explosion_sound.play()

        last_explosion = current


def play_force():

    global last_force

    current = time.time()

    if current - last_force > 0.7:

        force_sound.play()

        last_force = current


def stop_all_audio():

    stop_hum()

    pygame.mixer.music.stop()

    pygame.mixer.stop()


def restart_ambience():

    pygame.mixer.music.play(-1)