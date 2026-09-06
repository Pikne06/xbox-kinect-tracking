#!/usr/bin/env python
"""
Gesture Data Collection Script
Records skeleton data while performing gestures for ML training
"""

import time
import csv
import warnings
import numpy as np
from pykinect.runtime import PyKinectRuntime
from pykinect.com import FrameSourceTypes_Body

warnings.filterwarnings("ignore", category=FutureWarning)

# Gesture labels
GESTURES = {
    "1": "hand_raise",
    "2": "wave",
    "3": "thumbs_up",
    "4": "point",
    "5": "idle"
}

class GestureDataCollector:
    def __init__(self):
        """Initialize Kinect and CSV file"""
        print("Initializing Kinect sensor...")
        self.kinect = PyKinectRuntime(FrameSourceTypes_Body)
        
        # CSV file setup
        self.csv_file = "gesture_training_data.csv"
        self.initialize_csv()
        
        print("✓ Kinect initialized")
        print("✓ Data will be saved to:", self.csv_file)
        
    def initialize_csv(self):
        """Create CSV with headers if it doesn't exist"""
        try:
            with open(self.csv_file, 'r'):
                print("✓ Using existing training data file")
        except FileNotFoundError:
            print("Creating new training data file...")
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Header: all joint coordinates + gesture label
                header = []
                for i in range(25):  # 25 joints in Kinect v2
                    header.extend([f"joint_{i}_x", f"joint_{i}_y", f"joint_{i}_z"])
                header.append("gesture")
                writer.writerow(header)
            print("✓ Created new training data file")
    
    def extract_skeleton_features(self, bodies):
        """Extract coordinates from all joints"""
        if bodies is None:
            return None
        
        # Find first tracked body
        for body in bodies:
            if body.is_tracked:
                joints = body.joints
                features = []
                
                # Extract X, Y, Z for each of 25 joints
                for joint in joints:
                    features.extend([joint.Position.x, joint.Position.y, joint.Position.z])
                
                return features
        
        return None
    
    def record_gesture(self, gesture_label, duration=3):
        """Record skeleton data for a gesture"""
        print(f"\n{'='*50}")
        print(f"Recording: {gesture_label}")
        print(f"Get ready in 2 seconds...")
        time.sleep(2)
        
        print(f"RECORDING (3 seconds)...")
        start_time = time.time()
        recorded_samples = []
        frame_count = 0
        
        while time.time() - start_time < duration:
            bodies = self.kinect.get_last_body_frame()
            features = self.extract_skeleton_features(bodies)
            
            if features is not None:
                recorded_samples.append(features)
                frame_count += 1
        
        # Save all recorded frames
        if recorded_samples:
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                for sample in recorded_samples:
                    row = sample + [gesture_label]
                    writer.writerow(row)
            
            print(f"✓ Saved {frame_count} frames of {gesture_label}")
            return True
        else:
            print(f"✗ No skeleton detected. Try again.")
            return False
    
    def run(self):
        """Main data collection loop"""
        try:
            print("\n" + "="*50)
            print("GESTURE DATA COLLECTION")
            print("="*50)
            print("\nAvailable Gestures:")
            for key, gesture in GESTURES.items():
                print(f"  {key}: {gesture}")
            print("  0: Quit")
            
            total_samples = 0
            
            while True:
                print("\n" + "-"*50)
                choice = input("\nChoose gesture (0-5) or 'q' to quit: ").strip()
                
                if choice == 'q' or choice == '0':
                    break
                
                if choice not in GESTURES:
                    print("Invalid choice!")
                    continue
                
                gesture = GESTURES[choice]
                
                # Record multiple samples
                num_samples = int(input(f"How many samples of '{gesture}'? (default 5): ") or "5")
                
                for i in range(num_samples):
                    print(f"\nSample {i+1}/{num_samples}")
                    if self.record_gesture(gesture):
                        total_samples += 1
                    
                    if i < num_samples - 1:
                        time.sleep(1)
            
            print("\n" + "="*50)
            print(f"✓ Data collection complete!")
            print(f"✓ Total samples recorded: {total_samples}")
            print(f"✓ Data saved to: {self.csv_file}")
            print("="*50)
            
        except KeyboardInterrupt:
            print("\n\nData collection interrupted")
        finally:
            self.kinect.close()
            print("Kinect closed")


if __name__ == "__main__":
    collector = GestureDataCollector()
    collector.run()
