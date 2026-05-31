import cv2
import math
import numpy as np

# Debug export: last computed skin mask (for visualization)
last_mask = None

class _Landmark:
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class _HandLandmarks:
    def __init__(self, landmarks):
        self.landmark = landmarks


class _HandsResult:
    def __init__(self, hand_landmarks):
        self.multi_hand_landmarks = hand_landmarks


def _skin_mask(frame):
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    lower = np.array((0, 133, 77), dtype=np.uint8)
    upper = np.array((255, 173, 127), dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask


def _find_hand_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(contour)

    # Reject contours that are too small or obviously the whole frame / background
    h_frame, w_frame = mask.shape[:2]
    frame_area = float(h_frame * w_frame)

    # Allow smaller hand blobs (smaller/zoomed-out webcams)
    if area < 1500:
        return None

    # If the detected blob covers almost the entire frame it's likely a false positive
    if area > frame_area * 0.7:
        return None

    return contour


def _count_extended_fingers(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    if hull is None or len(hull) < 3:
        return 0

    defects = cv2.convexityDefects(contour, hull)
    if defects is None:
        return 0

    finger_count = 0
    contour_len = cv2.arcLength(contour, True)

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])

        a = math.dist(start, end)
        b = math.dist(start, far)
        c = math.dist(end, far)

        if b * c == 0:
            continue

        angle = math.degrees(math.acos(max(-1.0, min(1.0, (b * b + c * c - a * a) / (2 * b * c)))))
        if angle < 80 and d > contour_len * 0.02:
            finger_count += 1

    return min(max(finger_count, 0), 5)


def _build_hand_landmarks(frame, contour, finger_count):
    x, y, w, h = cv2.boundingRect(contour)
    if h == 0 or w == 0:
        return []

    # Determine pose state for synthetic landmarks.
    is_open = finger_count >= 3
    is_peace = finger_count == 2

    def finger_y(position, extended):
        if extended:
            if position == 'tip':
                return y + h * 0.18
            if position == 'dip':
                return y + h * 0.26
            if position == 'pip':
                return y + h * 0.35
            if position == 'mcp':
                return y + h * 0.45
        else:
            if position == 'tip':
                return y + h * 0.45
            if position == 'dip':
                return y + h * 0.38
            if position == 'pip':
                return y + h * 0.35
            if position == 'mcp':
                return y + h * 0.45
        return y + h * 0.5

    def finger_points(offset, extended):
        return [
            _Landmark(x + w * offset, finger_y('mcp', extended)),
            _Landmark(x + w * offset, finger_y('pip', extended)),
            _Landmark(x + w * offset, finger_y('dip', extended)),
            _Landmark(x + w * offset, finger_y('tip', extended)),
        ]

    extended = {
        'index': is_open or is_peace,
        'middle': is_open or is_peace,
        'ring': is_open and not is_peace,
        'pinky': is_open and not is_peace,
        'thumb': is_open,
    }

    wrist = _Landmark(x + w * 0.5, y + h * 0.95)
    thumb = [
        _Landmark(x + w * 0.12, y + h * 0.65),
        _Landmark(x + w * 0.15, y + h * 0.55),
        _Landmark(x + w * 0.18, y + h * 0.40),
        _Landmark(x + w * 0.20, y + h * (0.22 if extended['thumb'] else 0.42)),
    ]
    index = finger_points(0.28, extended['index'])
    middle = finger_points(0.45, extended['middle'])
    ring = finger_points(0.62, extended['ring'])
    pinky = finger_points(0.80, extended['pinky'])

    landmarks = [
        wrist,
        thumb[0],
        thumb[1],
        thumb[2],
        thumb[3],
        index[0],
        index[1],
        index[2],
        index[3],
        middle[0],
        middle[1],
        middle[2],
        middle[3],
        ring[0],
        ring[1],
        ring[2],
        ring[3],
        pinky[0],
        pinky[1],
        pinky[2],
        pinky[3],
    ]

    h_frame, w_frame = frame.shape[:2]
    # Normalize and clamp landmark coordinates to [0,1]
    normalized = []
    for l in landmarks:
        nx = l.x / float(w_frame) if w_frame else 0.0
        ny = l.y / float(h_frame) if h_frame else 0.0
        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))
        normalized.append(_Landmark(nx, ny, l.z))

    return normalized


def process_hands(frame):
    global last_mask
    mask = _skin_mask(frame)
    last_mask = mask.copy()
    contour = _find_hand_contour(mask)
    if contour is None:
        return _HandsResult([])

    finger_count = _count_extended_fingers(contour)
    landmarks = _build_hand_landmarks(frame, contour, finger_count)

    if not landmarks:
        return _HandsResult([])

    result = _HandsResult([_HandLandmarks(landmarks)])
    # attach some debug info for callers
    try:
        area = float(cv2.contourArea(contour))
        x, y, w, h = cv2.boundingRect(contour)
        result.debug = {
            "found": True,
            "area": area,
            "bbox": (x, y, w, h),
            "finger_count": int(finger_count),
        }
    except Exception:
        result.debug = {"found": True}

    return result


def draw_landmarks(frame, hand_landmarks):
    h, w = frame.shape[:2]
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
    ]

    for start_idx, end_idx in connections:
        start = hand_landmarks.landmark[start_idx]
        end = hand_landmarks.landmark[end_idx]
        cv2.line(
            frame,
            (int(start.x * w), int(start.y * h)),
            (int(end.x * w), int(end.y * h)),
            (0, 255, 0),
            2,
        )

    for lm in hand_landmarks.landmark:
        cv2.circle(
            frame,
            (int(lm.x * w), int(lm.y * h)),
            4,
            (0, 255, 0),
            -1,
        )

