import time
import numpy as np
from pynput.keyboard import Key, Controller
from pykinect.runtime import PyKinectRuntime
from pykinect.com import FrameSourceTypes_Body


class SkeletonHandler:
    
    def __init__(self):

        self.kinect = PyKinectRuntime(FrameSourceTypes_Body)
        print("Kinect initialized for body tracking.")
    
    def get_skeletons(self):

        bodies = self.kinect.get_last_body_frame()

        if bodies is None:
            return None
        
        for body in bodies:
            if body.is_tracked:
                joints = body.joints
                skeleton = np.zeros((25, 3))

                for i, joint in enumerate(joints):
                    joint = joints[i]
                    skeleton[i] = (joint.Position.x, joint.Position.y, joint.Position.z)
                return skeleton
        return None
    
    def normalize_skeleton(self, skeleton):
        if skeleton is None:
            return None
        
        spine_base = skeleton[0]
        centered = skeleton - spine_base
        
        max_dist = np.max(np.linalg.norm(centered, axis=1))
        if max_dist > 0:
            normalized = centered / max_dist
        else:
            normalized = centered
        return normalized
    
    def close(self):
        self.kinect.close()
        print("Kinect connection closed.")
    
if __name__ == "__main__":
    handler = SkeletonHandler()
    
    print("\nWarming up sensor for 3 seconds...")
    time.sleep(3)
    
    print("Testing skeleton extraction...")
    print("Stand 1-1.5 meters away and move around a bit...\n")
    
    for i in range(10):
        bodies = handler.kinect.get_last_body_frame()
        
        print(f"Frame {i+1}:")
        print(f"  bodies = {bodies}")
        
        if bodies is not None:
            print(f"  Number of bodies: {len(bodies)}")
            for idx, body in enumerate(bodies):
                print(f"    Body {idx}: is_tracked={body.is_tracked}")
        
        skeleton = handler.get_skeletons()
        if skeleton is not None:
            print(f"  ✓ Skeleton detected!")
        else:
            print(f"  ✗ No skeleton")
        
        time.sleep(1)
    
    handler.close()
        
    
            
            
        


            