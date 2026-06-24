import cv2 as cv

KEYBOARD_X = 40
KEYBOARD_Y = 580
KEY_WIDTH = 55
KEY_HEIGHT = 60

NOTES = [
    "DO1", "RE1", "MI1", "FA1", "SOL1", "LA1", "SI1",
    "DO2", "RE2", "MI2", "FA2", "SOL2", "LA2", "SI2",
    "DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3",
    "DO4"
]

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]


def draw_keybord(image, pressed_key):
    """
    Draws the virtual piano keyboard and highlights touched notes.

    Args:
        image (numpy.ndarray):
            Image on which the keyboard is drawn.
        pressed_key (dict):
            Dictionary associating each finger with the note currently touched.

    Returns:
        image (numpy.ndarray):
            Image containing the rendered keyboard.
    """

    for i, note in enumerate(NOTES):
        x1 = KEYBOARD_X + i * KEY_WIDTH
        y1 = KEYBOARD_Y
        x2 = x1 + KEY_WIDTH
        y2 = KEYBOARD_Y + KEY_HEIGHT

        color = (230, 230, 230)

        for finger in FINGERS:
            if pressed_key[finger] == note:
                color = (153, 204, 255)

        cv.rectangle(
            img=image,
            pt1=(x1, y1),
            pt2=(x2, y2),
            color=color,
            thickness=-1
        )

        cv.rectangle(
            img=image,
            pt1=(x1, y1),
            pt2=(x2, y2),
            color=(0, 0, 0),
            thickness=1
        )

        cv.putText(
            img=image,
            text=note,
            org=(x1 + 8, y1 + 35),
            fontFace=cv.FONT_HERSHEY_COMPLEX,
            fontScale=0.35,
            color=(0, 0, 0),
            thickness=1
        )

    return image