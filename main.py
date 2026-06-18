import camera
import mapping
import interaction
import audio
import keyboard
from fingers_detection import *

with HandLandmarker.create_from_options(options) as landmarker: 
    video = camera.open_camera()
    while True :
        ret, frame = camera.read_frame(video)
        timestamp = camera.get_timestamp()
        if not ret : 
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        rgb_frame = camera.convert_to_RGB(frame)
        height, width = rgb_frame.shape[:2]
        result = detect_hands(landmarker, rgb_frame, timestamp)
        finger_pos, movement_y = get_finger_data(result, width, height)
        keys = mapping.in_touch(finger_pos)
        pressed_key = interaction.press_touch(keys, movement_y)
        audio.update_sound(keys, pressed_key)
        keyboard_image = keyboard.draw_keybord(rgb_frame,keys)
        annoted_image = draw_finger(keyboard_image, finger_pos)


        bgr_image = cv.cvtColor(annoted_image, cv.COLOR_RGB2BGR)
        cv.imshow('frame', bgr_image)

        if cv.waitKey(1) & 0xFF == 27 :
            break
    
    camera.release_video(video)