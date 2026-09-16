import time

import numpy as np
from pynput.keyboard import Controller, Key
from pykinect.com import FrameSourceTypes_Depth
from pykinect.runtime import PyKinectRuntime


DEPTH_WIDTH = 512
DEPTH_HEIGHT = 424
MAX_DISTANCE_MM = 2000
MIN_CLOSE_PIXELS = 500
POLL_INTERVAL = 0.05
STATE_CONFIRMATIONS = 5


kinect = PyKinectRuntime(FrameSourceTypes_Depth)
keyboard = Controller()


def get_presence(depth_frame):
    if depth_frame is None:
        return None

    depth_data = depth_frame.reshape((DEPTH_HEIGHT, DEPTH_WIDTH))
    close_pixels = np.count_nonzero(
        (depth_data > 0) & (depth_data < MAX_DISTANCE_MM)
    )
    return close_pixels > MIN_CLOSE_PIXELS


def toggle_media():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)


def detect():
    current_presence = None
    candidate_presence = None
    candidate_count = 0

    try:
        print("Starting detection loop...")
        time.sleep(2)

        while True:
            detected = get_presence(kinect.get_last_depth_frame())

            if detected is None:
                time.sleep(POLL_INTERVAL)
                continue

            if current_presence is None:
                current_presence = detected
                print(f"Initial state: {'present' if detected else 'absent'}")
                continue

            if detected == current_presence:
                candidate_presence = None
                candidate_count = 0
                time.sleep(POLL_INTERVAL)
                continue

            if detected != candidate_presence:
                candidate_presence = detected
                candidate_count = 1
            else:
                candidate_count += 1

            if candidate_count >= STATE_CONFIRMATIONS:
                current_presence = detected
                candidate_presence = None
                candidate_count = 0

                if detected:
                    print("Body appeared → Playing")
                else:
                    print("Body disappeared → Paused")

                toggle_media()

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        kinect.close()


if __name__ == "__main__":
    detect()
