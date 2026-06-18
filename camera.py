import time
import cv2 as cv

def open_camera():
    """
    Open the default camera and create a video capture stream.

    Returns:
        vide (cv.VideoCapture):
            OpenCV video capture object used to read frames
            from the webcam.
    """

    video = cv.VideoCapture(0)
    video.set(cv.CAP_PROP_FRAME_WIDTH, 1080)
    video.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not video.isOpened():
        print("Can't access camera !")
        exit()

    return video


def read_frame(video):
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

    frame = cv.flip(frame, 1)
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


def release_video(video):
    """
    Release the video capture stream and close all OpenCV windows.

    Args:
        video (cv.VideoCapture):
            OpenCV video capture object to release.
    """

    video.release()
    cv.destroyAllWindows()