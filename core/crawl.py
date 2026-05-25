import cv2

crawl_y = 760

crawl_lines = [
    "A long time ago in a distant galaxy...",
    "",
    "The Sith Core has awakened.",
    "",
    "Asteroid storms ravage the galaxy.",
    "",
    "The Jedi have vanished.",
    "",
    "Only one Force wielder remains.",
    "",
    "Guided by Yoda...",
    "",
    "Anakin must restore balance."
]


def reset_crawl():
    global crawl_y
    crawl_y = 760


def draw_crawl(frame):
    global crawl_y

    frame[:] = (0, 0, 0)

    y = crawl_y

    for line in crawl_lines:
        cv2.putText(
            frame,
            line,
            (180, int(y)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        y += 55

    crawl_y -= 1.4

    if y < -50:
        return True

    return False