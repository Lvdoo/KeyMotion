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

def in_touch(finger_pos) :
    """
    Determines which piano key each finger is currently touching.

    Args:
        finger_pos (dict):
            Dictionary containing the coordinates of each finger.

    Returns:
        dict:
            Dictionary mapping each finger to the corresponding piano key.
            Returns None if the finger is not touching any key.
    """
    
    keys = {}
    
    for finger in FINGERS : 
        x = finger_pos[f"{finger}_x"]
        y = finger_pos[f"{finger}_y"]

        keys[finger] = None

        if x is None or y is None:
            continue

        for i in range(1,23) : 
            if x > KEYBOARD_X + KEY_WIDTH * (i - 1) and x < KEYBOARD_X + KEY_WIDTH * i  and y > KEYBOARD_Y and y < KEYBOARD_Y + KEY_HEIGHT :
                keys[finger] = NOTES[i-1]
                break

    return keys