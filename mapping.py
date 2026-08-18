import json
import os
import cv2 as cv
import numpy as np

# Créer une fonction qui permet de recharger calibration dans le cas où config.json n'existe pas et donc de créer la matrice même après-coup
NOTES = [
    "DO1", "RE1", "MI1", "FA1", "SOL1", "LA1", "SI1",
    "DO2", "RE2", "MI2", "FA2", "SOL2", "LA2", "SI2",
    "DO3", "RE3", "MI3", "FA3", "SOL3", "LA3", "SI3",
    "DO4"
]

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]

MATRIX = None

if os.path.isfile("config.json") : 
    with open("config.json", "r") as f :
        data = json.load(f)

        if  data is not None and len(data) == 4 :

            KEYBOARD_UP_LEFT = data[0]
            KEYBOARD_UP_RIGHT = data[1]
            KEYBOARD_DOWN_RIGHT = data[2]
            KEYBOARD_DOWN_LEFT = data[3]

            NORMALIZE_UP_LEFT = (0,0)
            NORMALIZE_UP_RIGHT = (1,0)
            NORMALIZE_DOWN_RIGHT = (1,1)
            NORMALIZE_DOWN_LEFT = (0,1)

            CAMERA_POINTS = np.array([KEYBOARD_UP_LEFT, KEYBOARD_UP_RIGHT, KEYBOARD_DOWN_RIGHT, KEYBOARD_DOWN_LEFT], np.float32)
            NORMALIZED_POINTS = np.array([NORMALIZE_UP_LEFT, NORMALIZE_UP_RIGHT, NORMALIZE_DOWN_RIGHT, NORMALIZE_DOWN_LEFT], np.float32)

            MATRIX = cv.getPerspectiveTransform(CAMERA_POINTS, NORMALIZED_POINTS)

def normalize(x,y) :
    """
    Converts a camera point into normalized keyboard coordinates.

    Args:
        x (int):
            X coordinate of the finger in the camera frame.
        y (int):
            Y coordinate of the finger in the camera frame.

    Returns:
        tuple:
            normalized_x (float):
                Horizontal position on the keyboard, from 0 to 1.

            normalized_y (float):
                Vertical position on the keyboard, from 0 to 1.
    """

    if MATRIX is None :
        return None, None
    finger_point = np.array([[[x,y]]], np.float32)
    normalized_finger_coords = cv.perspectiveTransform(finger_point, MATRIX)
    normalized_x = normalized_finger_coords[0][0][0]
    normalized_y = normalized_finger_coords[0][0][1]

    return normalized_x, normalized_y

def in_touch(finger_pos) :
    """
    Determines which piano key each finger is currently touching.

    Args:
        finger_pos (dict):
            Dictionary containing the coordinates of each finger.

    Returns:
        dict:
            Dictionary mapping each finger to the corresponding piano key.
            Returns None if the finger is outside the keyboard.
    """
    
    keys = {}
    
    for finger in FINGERS : 
        x = finger_pos[f"{finger}_x"]
        y = finger_pos[f"{finger}_y"]

        keys[finger] = None
        
        if x is None or y is None:
            continue

        normalized_x, normalized_y = normalize(x,y)

        if normalized_x is None or normalized_y is None:
            continue

        if normalized_x >= 0 and normalized_x <= 1 and normalized_y >= 0 and normalized_y <= 1 :
            index = int(normalized_x * len(NOTES))
            if index >= len(NOTES) : 
                index = len(NOTES) - 1
            keys[finger] = NOTES[index]

    return keys