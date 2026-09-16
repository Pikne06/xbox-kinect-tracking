import time

import numpy as np
from pynput.keyboard import Controller, Key
from pykinect.com import FrameSourceTypes_Depth
from pykinect.runtime import PyKinectRuntime


kinect = PyKinectRuntime(FrameSourceTypes_Depth)
keyboard = Controller()


def detect():
    previous_detected = False
    media_state = None

    try:
        print("Starting detection loop...")
        time.sleep(2)

        while True:
            body_detected = False
            depth_frame = kinect.get_last_depth_frame()

            if depth_frame is not None:
                depth_data = depth_frame.reshape((424, 512))
                close_pixels = np.count_nonzero(
                    (depth_data > 0) & (depth_data < 2000)
                )
                body_detected = close_pixels > 500

            if body_detected and not previous_detected:
                if media_state != "playing":
                    print("Body appeared → Playing")
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)
                    media_state = "playing"
                previous_detected = True

            elif not body_detected and previous_detected:
                if media_state != "paused":
                    print("Body disappeared → Paused")
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)
                    media_state = "paused"
                previous_detected = False

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        kinect.close()


if __name__ == "__main__":
    detect()
