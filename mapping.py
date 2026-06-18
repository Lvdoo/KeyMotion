KEYBOARD_X = 240
KEYBOARD_Y = 600
KEY_WIDTH = 75
KEY_HEIGHT = 40 

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
    fingers = ["thumb", "index", "middle", "ring", "pinky"]
    notes = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]

    for finger in fingers : 
        x = finger_pos[f"{finger}_x"]
        y = finger_pos[f"{finger}_y"]

        keys[finger] = None

        if x is None or y is None:
            continue

        for i in range(1,8) : 
            if x > KEYBOARD_X + KEY_WIDTH * (i - 1) and x < KEYBOARD_X + KEY_WIDTH * i  and y > KEYBOARD_Y and y < KEYBOARD_Y + KEY_HEIGHT :
                keys[finger] = notes[i-1]
                break

    return keys