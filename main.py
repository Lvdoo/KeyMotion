import camera
import mapping
import interaction
import audio
import send_data
import hardware_controls
from fingers_detection import *

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]
active_notes = {finger : None for finger in FINGERS}
coms = send_data.UdpComms(ip="127.0.0.1", port=8000)
controls = hardware_controls.HardwareControls(port="COM4", baudrate=115200)

with HandLandmarker.create_from_options(options) as landmarker: 
    video = camera.open_camera()
    while True :
        for message in controls.read_messages():
            if message == "COLOR|NEXT":
                coms.send("COLOR|NEXT")
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

        for finger in FINGERS:
            pressed_note = pressed_key[finger]
            current_note = keys[finger]
            active_note = active_notes[finger]

            # Nouvel appui détecté
            if pressed_note is not None:
                coms.send(f"{pressed_note}|PRESS")
                active_notes[finger] = pressed_note

            # Le doigt a quitté la touche qu'il maintenait
            elif active_note is not None and current_note != active_note:
                coms.send(f"{active_note}|RELEASE")
                active_notes[finger] = None

        audio.update_sound(keys, pressed_key)
        annoted_image = draw_finger(rgb_frame, finger_pos)

        bgr_image = cv.cvtColor(annoted_image, cv.COLOR_RGB2BGR)
        cv.imshow('frame', bgr_image)

        if cv.waitKey(1) & 0xFF == 27 :
            break
    
    camera.release_video(video)
    coms.close()
    controls.close()