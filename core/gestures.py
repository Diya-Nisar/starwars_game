def is_fist(hand_landmarks):

    tips = [8, 12, 16, 20]

    folded = 0

    for tip in tips:

        tip_y = hand_landmarks.landmark[tip].y
        pip_y = hand_landmarks.landmark[tip - 2].y

        if tip_y > pip_y:
            folded += 1

    return folded >= 3


def is_open_hand(hand_landmarks):

    tips = [8, 12, 16, 20]

    open_count = 0

    for tip in tips:

        tip_y = hand_landmarks.landmark[tip].y
        pip_y = hand_landmarks.landmark[tip - 2].y

        if tip_y < pip_y:
            open_count += 1

    return open_count >= 3


def peace_sign(hand_landmarks):

    index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y

    ring_down = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
    pinky_down = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y

    return index_up and middle_up and ring_down and pinky_down