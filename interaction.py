is_pressed = {"thumb" : False,
            "index" : False,
            "middle" : False,
            "ring" : False,
            "pinky" : False}

def press_touch(keys, movement_y) : 
    """
    Detects when a finger presses a piano key.

    Args:
        keys (dict):
            Dictionary mapping each finger to the key currently touched.
        movement_y (dict):
            Dictionary containing the vertical movement of each finger.

    Returns:
        dict:
            Dictionary mapping each finger to the key that has been pressed.
            Returns None for fingers that did not trigger a press event.
    """
    
    global is_pressed
    pressed_key = {}
    fingers = ["thumb", "index", "middle", "ring", "pinky"]

    for finger in fingers : 
        pressed_key[finger] = None
        if  keys[finger] is None :
            is_pressed[finger] = False
            continue
    
        if movement_y[f"movement_{finger}"]  > 5 and is_pressed[finger] == False:
            pressed_key[finger] = keys[finger]
            is_pressed[finger] = True
    return pressed_key
