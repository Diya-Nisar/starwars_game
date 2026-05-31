import cv2
import numpy as np
import time

anakin = cv2.imread("assets/characters/anakin.png", cv2.IMREAD_UNCHANGED)
yoda = cv2.imread("assets/characters/yoda.png", cv2.IMREAD_UNCHANGED)
vader = cv2.imread("assets/characters/darthvader.png", cv2.IMREAD_UNCHANGED)
sithcore = cv2.imread("assets/characters/sithcore.png", cv2.IMREAD_UNCHANGED)


def overlay_png(frame, png, x, y, scale=1.0, alpha_multiplier=1.0):
    if png is None:
        return frame

    h, w = png.shape[:2]
    new_w = int(w * scale)
    new_h = int(h * scale)

    if new_w <= 0 or new_h <= 0:
        return frame

    png = cv2.resize(png, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Normalize backgrounds to transparency:
    # - If image has 3 channels, create an alpha channel by treating near-white/near-gray
    #   uniform pixels as transparent (handles exported checkerboard backgrounds).
    # - If image already has alpha, clear alpha where the RGB looks like a uniform
    #   near-white/gray background.
    if png.shape[2] == 3:
        bgr = png
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        channel_std = np.std(bgr.astype(np.int16), axis=2)
        # uniform and bright pixels -> treat as background
        bg_mask = (channel_std < 8) & (gray >= 190)
        alpha_chan = (~bg_mask).astype(np.uint8) * 255
        png = np.dstack([bgr, alpha_chan])
    elif png.shape[2] == 4:
        bgr = png[:, :, :3]
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        channel_std = np.std(bgr.astype(np.int16), axis=2)
        bg_mask = (channel_std < 8) & (gray >= 190)
        # zero-out alpha for detected background pixels
        png[:, :, 3][bg_mask] = 0

    x1 = int(x - new_w // 2)
    y1 = int(y - new_h // 2)
    x2 = x1 + new_w
    y2 = y1 + new_h

    if x2 <= 0 or y2 <= 0 or x1 >= frame.shape[1] or y1 >= frame.shape[0]:
        return frame

    px1 = max(0, -x1)
    py1 = max(0, -y1)
    px2 = new_w - max(0, x2 - frame.shape[1])
    py2 = new_h - max(0, y2 - frame.shape[0])

    fx1 = max(0, x1)
    fy1 = max(0, y1)
    fx2 = min(frame.shape[1], x2)
    fy2 = min(frame.shape[0], y2)

    png_crop = png[py1:py2, px1:px2]

    if png_crop.shape[2] == 4:
        alpha = (png_crop[:, :, 3] / 255.0) * alpha_multiplier
    else:
        alpha = np.ones(png_crop.shape[:2]) * alpha_multiplier

    for c in range(3):
        frame[fy1:fy2, fx1:fx2, c] = (
            alpha * png_crop[:, :, c]
            + (1 - alpha) * frame[fy1:fy2, fx1:fx2, c]
        )

    return frame


def draw_hologram(frame, png, x, y, scale=1.0):
    pulse = 0.65 + 0.15 * np.sin(time.time() * 5)

    frame = overlay_png(
        frame,
        png,
        x,
        y,
        scale=scale,
        alpha_multiplier=pulse
    )

    # subtle scanline hologram effect: blend faint horizontal lines
    overlay = frame.copy()
    for row in range(0, frame.shape[0], 8):
        cv2.line(overlay, (0, row), (frame.shape[1], row), (255, 255, 255), 1)
    # blend the overlay very lightly to avoid harsh white stripes
    cv2.addWeighted(overlay, 0.06, frame, 0.94, 0, frame)

    return frame


def draw_anakin(frame):
    return draw_hologram(frame, anakin, 180, 500, scale=0.55)


def draw_yoda_message(frame, text):
    frame = draw_hologram(frame, yoda, 1100, 520, scale=0.45)

    cv2.rectangle(frame, (640, 560), (1260, 690), (0, 0, 0), -1)
    cv2.rectangle(frame, (640, 560), (1260, 690), (0, 255, 255), 2)

    cv2.putText(
        frame,
        "YODA:",
        (665, 600),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        text,
        (665, 650),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    return frame


def draw_vader_boss(frame, x, y):
    return overlay_png(frame, vader, x, y, scale=0.65, alpha_multiplier=0.9)


def draw_sith_core(frame, x, y):
    return overlay_png(frame, sithcore, x, y, scale=0.55, alpha_multiplier=0.85)