# STAR WARS FORCE TRAINER

A cinematic gesture-controlled Star Wars inspired game built using Python, OpenCV, MediaPipe, and Pygame.

Use your hand as a lightsaber to:

* slice asteroids
* use Force powers
* survive escalating waves
* defeat the Sith Core boss

---

# FEATURES

* Real-time hand tracking
* Lightsaber combat
* Asteroid slicing system
* Force push ability
* Force lightning
* Combo system
* Wave progression
* Boss fight
* Cinematic sound effects
* Dynamic health and force bars
* Motion trails and screen shake
* Starfield background
* Gesture recognition using MediaPipe

---

# CONTROLS

| Gesture      | Action                         |
| ------------ | ------------------------------ |
| Fist ✊       | Ignite lightsaber              |
| Open palm ✋  | Force push                     |
| Peace sign ✌ | Change saber color + lightning |
| ESC          | Quit game                      |

---

# GAME OBJECTIVE

Survive 5 increasingly difficult waves of asteroids.

In the final wave:

* fight the Sith Core boss
* destroy its red core using your lightsaber

Win condition:

```text
THE FORCE IS WITH YOU
```

Lose condition:

```text
THE JEDI HAS FALLEN
```

---

# PROJECT STRUCTURE

```text
starwars_force_project/
│
├── assets/
│   └── sounds/
│       ├── ambience.wav
│       ├── explosion.wav
│       ├── force.wav
│       ├── hum.wav
│       ├── ignition.wav
│       └── swing.wav
│
├── core/
│   ├── audio.py
│   ├── blasters.py
│   ├── boss.py
│   ├── effects.py
│   ├── gestures.py
│   ├── hand_tracking.py
│   ├── lightning.py
│   ├── particles.py
│   └── saber.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# INSTALLATION

## 1. Clone or download the project

```bash
git clone <repo-url>
```

OR simply download and extract the ZIP.

---

# 2. Create virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Add sound files

Inside:

```text
assets/sounds/
```

Add:

```text
ambience.wav
explosion.wav
force.wav
hum.wav
ignition.wav
swing.wav
```

---

# 5. Run the game

```bash
python main.py
```

---

# REQUIREMENTS.TXT

Create a file named:

```text
requirements.txt
```

Paste:

```text
opencv-python
numpy
mediapipe
pygame
```

---

# IMPORTANT NOTES

## Webcam Access

The game requires webcam permissions.

If the camera does not open:

* close Zoom/Teams/Discord
* allow camera permissions
* restart terminal

---

# PYTHON VERSION

Recommended:

```text
Python 3.11
```

Python 3.13 may cause MediaPipe compatibility issues.

---

# PERFORMANCE TIPS

For smoother gameplay:

* use good lighting
* keep webcam stable
* use 720p camera resolution
* close heavy background applications

---

# TROUBLESHOOTING

## MediaPipe Error

If you get:

```text
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

Install compatible versions:

```bash
pip uninstall mediapipe
pip install mediapipe==0.10.14
```

---

# SOUND ISSUES

If sound lags:

* reduce background apps
* use headphones
* ensure WAV files are short

---

# FUTURE IMPROVEMENTS

Planned upgrades:

* better lightsaber bloom
* dual sabers
* Death Star background
* hologram UI
* cinematic intro crawl
* voice lines
* advanced boss attacks
* force slow-motion effects

---

# CREDITS

Built with:

* Python
* OpenCV
* MediaPipe
* Pygame

Inspired by the Star Wars universe.

---

# MAY THE FORCE BE WITH YOU
