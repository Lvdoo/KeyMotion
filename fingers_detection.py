import mediapipe as mp
import cv2 as cv
import numpy as np

last_y = {"last_thumb_y" : None,
          "last_index_y" : None,
          "last_middle_y" : None,
          "last_ring_y" : None,
          "last_pinky_y" : None}

movement_y = {
        "movement_thumb" : None,
        "movement_index" : None,
        "movement_middle" : None,
        "movement_ring" : None,
        "movement_pinky" : None
    }

BaseOption = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(base_options = BaseOption(model_asset_path = './hand_landmarker.task'),
                                running_mode = VisionRunningMode.VIDEO,
                                num_hands = 1,
                                min_hand_detection_confidence = 0.7,
                                min_hand_presence_confidence = 0.7,
                                min_tracking_confidence = 0.7)

def detect_hands(landmarker, frame, timestamp_ms) :
    """
    Detects hands in a video frame using MediaPipe Hand Landmarker.

    Args:
        landmarker (HandLandmarker):
            Initialized MediaPipe hand detector.
        frame (numpy.ndarray):
            Current video frame in RGB format.
        timestamp_ms (int):
            Timestamp of the frame in milliseconds.

    Returns:
        HandLandmarkerResult:
            Detection result containing hand landmarks.
    """

    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    hand_landmarker_result = landmarker.detect_for_video(mp_image, timestamp_ms)
    return hand_landmarker_result

def get_finger_data(result, width, height) :
    """
    Retrieves fingertip positions and computes their vertical movement.

    Args:
        result (HandLandmarkerResult):
            Hand detection result from MediaPipe.
        width (int):
            Frame width in pixels.
        height (int):
            Frame height in pixels.

    Returns:
        tuple:
            - finger_pos (dict): Fingertip coordinates.
            - movement_y (dict): Vertical movement of each finger.
    """
     
    global last_y
    finger_pos = get_fingers_pos(result, width, height)
    movement_y = get_movement(last_y, finger_pos)
    update_last_y(finger_pos)

    return finger_pos, movement_y

def draw_finger(rgb_image, finger_pos) :
    """
    Draws circles on detected fingertip positions.

    Args:
        rgb_image (numpy.ndarray):
            Input image.
        finger_pos (dict):
            Dictionary containing fingertip coordinates.

    Returns:
        annotated_image (numpy.ndarray):
            Annotated image with fingertip markers.
    """

    annotated_image = np.copy(rgb_image)
    # if index_detected == True :
    #     text = "YES"
    # else :
    #     text = "NO"
    if finger_pos["thumb_x"] is not None and finger_pos["thumb_y"] is not None :
        cv.circle(img = annotated_image, center = (finger_pos["thumb_x"], finger_pos["thumb_y"]), radius = 5, color = (255,29,141), thickness = -1)

    if finger_pos["index_x"] is not None and finger_pos["index_y"] is not None :
        cv.circle(img = annotated_image, center = (finger_pos["index_x"], finger_pos["index_y"]), radius = 5, color = (255,29,141), thickness = -1)

    if finger_pos["middle_x"] is not None and finger_pos["middle_y"] is not None :
        cv.circle(img = annotated_image, center = (finger_pos["middle_x"], finger_pos["middle_y"]), radius = 5, color = (255,29,141), thickness = -1)

    if finger_pos["ring_x"] is not None and finger_pos["ring_y"] is not None :
        cv.circle(img = annotated_image, center = (finger_pos["ring_x"], finger_pos["ring_y"]), radius = 5, color = (255,29,141), thickness = -1)

    if finger_pos["pinky_x"] is not None and finger_pos["pinky_y"] is not None :
        cv.circle(img = annotated_image, center = (finger_pos["pinky_x"], finger_pos["pinky_y"]), radius = 5, color = (255,29,141), thickness = -1)

    # cv.putText(img = keybord_image, text = f"Fingers detected : {text}", org = (50, 50), fontFace = cv.FONT_HERSHEY_COMPLEX, fontScale = 0.6, color = (255,0,0), thickness = 1)
    # cv.putText(img = keybord_image, text = f"Position : {smooth_x}, {smooth_y}", org = (50, 80), fontFace = cv.FONT_HERSHEY_COMPLEX, fontScale = 0.6, color = (255,0,0), thickness = 1)
    # cv.putText(img = keybord_image, text = f"Mouvement_y : {movement_y}", org = (50, 110), fontFace = cv.FONT_HERSHEY_COMPLEX, fontScale = 0.6, color = (255,0,0), thickness = 1)
    return annotated_image

def get_fingers_pos(result, width, height):
    """
    Extracts fingertip positions from MediaPipe landmarks.

    Args:
        result (HandLandmarkerResult):
            Hand detection result.
        width (int):
            Frame width in pixels.
        height (int):
            Frame height in pixels.

    Returns:
        finger_pos (dict):
            Dictionary containing x and y coordinates of
            thumb, index, middle, ring and pinky fingertips.
            Returns None values when no hand is detected.
    """

    hand_landmarks_list = result.hand_landmarks
    if not hand_landmarks_list:
        return {
            "thumb_x" : None,
            "thumb_y" : None,
            "index_x" : None,
            "index_y" : None,
            "middle_x" : None,
            "middle_y" : None,
            "ring_x" : None,
            "ring_y" : None,
            "pinky_x" : None,
            "pinky_y" : None}
            
    first_hand = hand_landmarks_list[0]
    finger_tips = {
        "thumb" : first_hand[4],
        "index" : first_hand[8],
        "middle" : first_hand[12],
        "ring" : first_hand[16],
        "pinky" : first_hand[20]
    }
    
    finger_pos = {
        "thumb_x" : int(finger_tips["thumb"].x * width),
        "thumb_y" : int(finger_tips["thumb"].y * height),
        "index_x" : int(finger_tips["index"].x * width),
        "index_y" : int(finger_tips["index"].y * height),
        "middle_x" : int(finger_tips["middle"].x * width),
        "middle_y" : int(finger_tips["middle"].y * height),
        "ring_x" : int(finger_tips["ring"].x * width),
        "ring_y" : int(finger_tips["ring"].y * height),
        "pinky_x" : int(finger_tips["pinky"].x * width),
        "pinky_y" : int(finger_tips["pinky"].y * height)
    }

    return finger_pos

def get_movement(last_y, finger_pos) :
    """
    Computes the vertical movement of each fingertip between
    two consecutive frames.

    Small movements below a threshold are ignored to reduce noise.

    Args:
        last_y (dict):
            Previous y-coordinates of fingertips.
        finger_pos (dict):
            Current fingertip coordinates.

    Returns:
        movement_y (dict):
            Vertical movement (delta y) for each finger.
    """
     
    global movement_y
    if  finger_pos["thumb_x"] is None or finger_pos["thumb_y"] is None or last_y["last_thumb_y"] is None :
        movement_y["movement_thumb"] = 0
    else :
        movement_y["movement_thumb"] = finger_pos["thumb_y"] - last_y["last_thumb_y"]
        if abs(movement_y["movement_thumb"]) < 3 :
            movement_y["movement_thumb"] = 0


    if  finger_pos["index_x"] is None or finger_pos["index_y"] is None or last_y["last_index_y"] is None :
        movement_y["movement_index"] = 0
    else :
        movement_y["movement_index"] = finger_pos["index_y"] - last_y["last_index_y"]
        if abs(movement_y["movement_index"]) < 3 :
            movement_y["movement_index"] = 0


    if  finger_pos["middle_x"] is None or finger_pos["middle_y"] is None or last_y["last_middle_y"] is None :
        movement_y["movement_middle"] = 0
    else :
        movement_y["movement_middle"] = finger_pos["middle_y"] - last_y["last_middle_y"]
        if abs(movement_y["movement_middle"]) < 3 :
            movement_y["movement_middle"] = 0


    if  finger_pos["ring_x"] is None or finger_pos["ring_y"] is None or last_y["last_ring_y"] is None :
        movement_y["movement_ring"] = 0
    else :
        movement_y["movement_ring"] = finger_pos["ring_y"] - last_y["last_ring_y"]
        if abs(movement_y["movement_ring"]) < 3 :
            movement_y["movement_ring"] = 0


    if  finger_pos["pinky_x"] is None or finger_pos["pinky_y"] is None or last_y["last_pinky_y"] is None :
        movement_y["movement_pinky"] = 0
    else :
        movement_y["movement_pinky"] = finger_pos["pinky_y"] - last_y["last_pinky_y"]
        if abs(movement_y["movement_pinky"]) < 3 :
            movement_y["movement_pinky"] = 0

    return movement_y

def update_last_y(finger_pos):
    """
    Updates stored fingertip y-coordinates for the next frame.

    Args:
        finger_pos (dict):
            Current fingertip coordinates.

    Returns:
        None
    """
    
    global last_y

    last_y["last_thumb_y"] = finger_pos["thumb_y"]
    last_y["last_index_y"] = finger_pos["index_y"]
    last_y["last_middle_y"] = finger_pos["middle_y"]
    last_y["last_ring_y"] = finger_pos["ring_y"]
    last_y["last_pinky_y"] = finger_pos["pinky_y"]

