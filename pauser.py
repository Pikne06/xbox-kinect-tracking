# ============================================================================
# KINECT PRESENCE DETECTION - MEDIA PLAYER CONTROL
# ============================================================================
# This script uses Kinect depth sensor to detect if a person is present
# and automatically pauses/plays media based on presence detection
# ============================================================================

import time
import numpy as np
from pynput.keyboard import Key, Controller
from requests import get
import cv2
from pykinect.runtime import PyKinectRuntime
from pykinect.com import FrameSourceTypes_Depth

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize Kinect runtime with depth frame source
kinect = PyKinectRuntime(FrameSourceTypes_Depth)

# Initialize keyboard controller for media key simulation
keyboard = Controller()

# ============================================================================
# DETECTION FUNCTION
# ============================================================================

def detect():
    """
    Main detection loop that monitors depth frames and controls media playback.
    Pauses media when no person is detected, plays when person appears.
    """
    
    previous_detected = False
    media_state = None  # None, 'playing', or 'paused'
    
    try:
        print("Starting detection loop...")
        print("Warming up sensor for 2 seconds...")
        time.sleep(2)
        
        while True:
            body_detected = False
            
            # ================================================================
            # CHECK FOR NEW DEPTH FRAMES
            # ================================================================
            
            # Always get the latest frame
            depth_frame = kinect.get_last_depth_frame()
            
            if depth_frame is not None:
                # Reshape 1D depth array to 2D (424x512)
                depth_data = depth_frame.reshape((424, 512))
                # Count pixels closer than 2000mm (presence threshold)
                close_pixels = np.count_nonzero((depth_data > 0) & (depth_data < 2000))
                # Detect presence if enough close pixels detected
                body_detected = close_pixels > 500
            
            # ================================================================
            # HANDLE PRESENCE STATE CHANGES (with debouncing)
            # ================================================================
            
            # Only trigger when state actually changes
            if body_detected and not previous_detected:
                # Person just appeared
                if media_state != 'playing':
                    print("Body appeared → Playing")
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)
                    media_state = 'playing'
                previous_detected = True

            elif not body_detected and previous_detected:
                # Person just left
                if media_state != 'paused':
                    print("Body disappeared → Paused")
                    keyboard.press(Key.media_play_pause)
                    keyboard.release(Key.media_play_pause)
                    media_state = 'paused'
                previous_detected = False
            
            time.sleep(0.05)  # Fast polling
            
    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # ================================================================
        # CLEANUP
        # ================================================================
        
        kinect.close()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    detect()