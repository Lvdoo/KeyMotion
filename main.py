import camera
import mapping
import interaction
import audio
import send_data
import hardware_controls
from fingers_detection import *
import json
import cv2 as cv

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]
active_notes = {finger : None for finger in FINGERS}
coms = send_data.UdpComms(ip="127.0.0.1", port=8000)
controls = hardware_controls.HardwareControls(port="COM4", baudrate=115200)
final_calibration = []

with HandLandmarker.create_from_options(options) as landmarker: 
    video = camera.open_camera()
    cv.namedWindow("frame")
    cv.setMouseCallback("frame", camera.calibration)

    while True :
        for message in controls.read_messages():
            if message == "COLOR|NEXT":
                coms.send("COLOR|NEXT")
        ret, frame = camera.read_frame(video)
        timestamp = camera.get_timestamp()
        if not ret : 
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if camera.calibration_done == False :
            cv.putText(frame, "Click the corners clockwise. Start with up-left", (10,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            cv.putText(frame, "Reset  : R", (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            cv.putText(frame, "Validate  : Enter", (10,60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            for points in camera.calibration_points : 
                cv.circle(frame,(points),10,(0,0,255),-1)
            cv.imshow('frame', frame)

        else : 
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

                # New press detected
                if pressed_note is not None:
                    coms.send(f"{pressed_note}|PRESS")
                    active_notes[finger] = pressed_note

                # Finger left the key he pressed
                elif active_note is not None and current_note != active_note:
                    coms.send(f"{active_note}|RELEASE")
                    active_notes[finger] = None

            audio.update_sound(keys, pressed_key)
            annoted_image = draw_finger(rgb_frame, finger_pos)
            bgr_image = cv.cvtColor(annoted_image, cv.COLOR_RGB2BGR)
            cv.imshow('frame', bgr_image)

        key = cv.waitKey(1) & 0xFF
        if  key == 27 :
            break
        elif camera.calibration_done == False and key == ord('r') : 
            camera.calibration_points.clear()
        elif len(camera.calibration_points) == 4 and camera.calibration_done == False and key & 0xFF == 13 : 
            camera.calibration_done =  True
            final_calibration = camera.calibration_points
            json_final_calibration = json.dumps(final_calibration, indent = 4)
            with open("config.json", "w") as f :
                f.write(json_final_calibration) 
                
            
    camera.release_video(video)
    coms.close()
    controls.close()