import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


def process_hands(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    return results


def draw_landmarks(frame, hand_landmarks):

    mp_draw.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS
    )