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

with HandLandmarker.create_from_options(options) as landmarker_top, \
    HandLandmarker.create_from_options(options) as landmarker_front: 
    video_top, video_front = camera.open_cameras()
    fingers_detection_top = FingerDetection()
    fingers_detection_front = FingerDetection()
    cv.namedWindow("frame_top")
    cv.setMouseCallback("frame_top", camera.calibration)

    while True :
        for message in controls.read_messages():
            command, separator, value = message.partition("|")
            if not separator : 
                print("Esp32 invalid message", message)
                continue

            command = command.strip().upper()
            value = value.strip().upper()

            if command == "COLOR" and value == "NEXT" :
                coms.send("COLOR|NEXT")

            elif command == "VOLUME" :
                try : 
                    volume = int(value)
                    volume = max(0, min(100, volume))
                    volume_percent = volume / 100
                    audio.set_volume(volume_percent)

                except ValueError :
                    print("Invalid volume value", value)

        ret_top, frame_top = camera.read_frame(video_top, flip_code = -1)
        ret_front, frame_front = camera.read_frame(video_front)
        timestamp = camera.get_timestamp()
        if not ret_top or not ret_front : 
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if camera.calibration_done == False :
            cv.putText(frame_top, "Click the corners clockwise. Start with up-left", (10,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            cv.putText(frame_top, "Reset  : R", (10,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            cv.putText(frame_top, "Validate  : Enter", (10,60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
            for points in camera.calibration_points : 
                cv.circle(frame_top,(points), 5, (0,0,255), -1)
            cv.imshow('frame_top', frame_top)

        else : 
            rgb_frame_top = camera.convert_to_RGB(frame_top)
            rgb_frame_front = camera.convert_to_RGB(frame_front)
            height_top, width_top = rgb_frame_top.shape[:2]
            height_front, width_front = rgb_frame_front.shape[:2]
            result_top = detect_hands(landmarker_top, rgb_frame_top, timestamp)
            result_front = detect_hands(landmarker_front, rgb_frame_front, timestamp)
            finger_pos_top, _ = fingers_detection_top.get_finger_data(result_top, width_top, height_top)
            finger_pos_front, movement_y = fingers_detection_front.get_finger_data(result_front, width_front, height_front)
            keys = mapping.in_touch(finger_pos_top)
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
            annoted_image_top = draw_finger(rgb_frame_top, finger_pos_top)
            annoted_image_front = draw_finger(rgb_frame_front, finger_pos_front)
            bgr_image_top = cv.cvtColor(annoted_image_top, cv.COLOR_RGB2BGR)
            bgr_image_front = cv.cvtColor(annoted_image_front, cv.COLOR_RGB2BGR)
            cv.imshow('frame_top', bgr_image_top)
            cv.imshow('frame_front', bgr_image_front)

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
                
            
    camera.release_video(video_top, video_front)
    coms.close()
    controls.close()