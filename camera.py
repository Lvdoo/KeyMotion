import time
import cv2 as cv

event = [i for i in dir(cv) if 'EVENT' in i]
calibration_points = []
calibration_done = False

def open_cameras():
    """
    Open the top and front cameras and create video capture streams.

    Returns:
        tuple:
            video_top (cv.VideoCapture):
                Capture stream for the top-view camera (finger position).
            video_front (cv.VideoCapture):
                Capture stream for the front-view camera (key press detection).
    """

    video_top = cv.VideoCapture(2, cv.CAP_DSHOW)
    video_top.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG')) 

    video_front = cv.VideoCapture(2, cv.CAP_MSMF)

    video_top.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    video_top.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    video_front.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    video_front.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not video_top.isOpened() :
        print("Can't access top camera!")
        exit()

    if not video_front.isOpened() :
            print("Can't access front camera!")
            exit()

    return video_top, video_front


def read_frame(video, flip_code = None):
    """
    Read a frame from the video stream and flip it horizontally.

    Args:
        video (cv.VideoCapture):
            OpenCV video capture object.

    Returns:
        tuple:
            ret (bool):
                True if the frame was successfully captured.
            
            frame (numpy.ndarray):
                Captured and horizontally flipped frame.
    """

    ret, frame = video.read()
    if not ret: 
        print("Can't receive frame. Exiting...")

    if flip_code is not None :
        frame = cv.flip(frame, flip_code)
    return ret, frame


def convert_to_RGB(frame):
    """
    Convert a frame from BGR format to RGB format.

    OpenCV uses BGR by default while MediaPipe and many
    deep learning libraries use RGB images.

    Args:
        frame (numpy.ndarray):
            Image frame in BGR format.

    Returns:
        rgb_frame (numpy.ndarray):
            Frame converted to RGB format.
    """

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return rgb_frame


def get_timestamp():
    """
    Get the current timestamp in milliseconds.

    Used for MediaPipe hand tracking and real-time processing.

    Returns:
        timestamp_ms (int):
            Current timestamp in milliseconds.
    """

    timestamp_ms = int(time.time() * 1000)
    return timestamp_ms


def release_video(video_top, video_front):
    """
    Release the video capture streams and close all OpenCV windows.

    Args:
        video (cv.VideoCapture):
            OpenCV video capture object to release.
    """

    video_top.release()
    video_front.release()
    cv.destroyAllWindows()


def calibration(event,x,y, flags, param) :
    """
    Register calibration points from mouse clicks.
    The function records up to four points when the left mouse
    button is clicked and calibration is not completed.

    Args:
        event (int):
            OpenCV mouse event type.
        x (int):
            Horizontal coordinate of the mouse click.
        y (int):
            Vertical coordinate of the mouse click.
        flags (int):
            OpenCV flags associated with the mouse event.
        param:
            Optional parameter passed by the OpenCV mouse callback.
    """

    global calibration_points
    if calibration_done == False :
        if event == cv.EVENT_LBUTTONDOWN and len(calibration_points) < 4 :
            calibration_points.append((x,y))