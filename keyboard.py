import cv2 as cv

def draw_keybord(image, pressed_key) : 
    """
    Draws the virtual piano keyboard and highlights pressed notes.

    Args:
        image (numpy.ndarray):
            Image on which the keyboard is drawn.
        pressed_key (dict):
            Dictionary associating each finger with the note
            currently pressed.

    Returns:
        image (numpy.ndarray):
            Image containing the rendered keyboard with
            highlighted pressed notes.
    """
    fingers = ["thumb", "index", "middle", "ring", "pinky"]
    key_colors = {
        "DO":  (255,153,204),
        "RE":  (204,153,255),
        "MI":  (153,153,255),
        "FA":  (153,204,255),
        "SOL": (153,255,255),
        "LA":  (153,253,204),
        "SI":  (153,255,153),
        "DO2": (204,255,153)}
    rect_coords = {
        "DO":  ((240, 600), (315, 640)),
        "RE":  ((315, 600), (390, 640)),
        "MI":  ((390, 600), (465, 640)),
        "FA":  ((465, 600), (540, 640)),
        "SOL": ((540, 600), (615, 640)),
        "LA":  ((615, 600), (690, 640)),
        "SI":  ((690, 600), (765, 640)),
        "DO2": ((765, 600), (840, 640))}
    texts_coords = {
        "DO" : (270, 625),
        "RE" : (345, 625),
        "MI" : (420, 625),
        "FA" : (495, 625),
        "SOL" : (570, 625),
        "LA" : (645, 625),
        "SI" : (720, 625),
        "DO2" : (795, 625)}
    
    for note, (point1, point2) in rect_coords.items() :
                cv.rectangle(img = image, pt1 = point1, pt2 = point2, color = (230,230,230), thickness = -1)
                cv.rectangle(img = image, pt1 = point1, pt2 = point2, color = (0,0,0), thickness = 1)
                cv.putText(img = image, text = note, org = texts_coords[note], fontFace = cv.FONT_HERSHEY_COMPLEX, fontScale = 0.4, color = (0,0,0), thickness = 1)

    for finger in fingers :
        if pressed_key[finger] is not None : 
            cv.rectangle(img = image, pt1 = rect_coords[pressed_key[finger]][0], pt2 = rect_coords[pressed_key[finger]][1], color = key_colors[pressed_key[finger]], thickness = -1)
            cv.rectangle(img = image, pt1 = rect_coords[pressed_key[finger]][0], pt2 = rect_coords[pressed_key[finger]][1], color = (0,0,0), thickness = 1)
            cv.putText(img = image, text = pressed_key[finger], org = texts_coords[pressed_key[finger]], fontFace = cv.FONT_HERSHEY_COMPLEX, fontScale = 0.4, color = (0,0,0), thickness = 1)

    return image
