  
"""Simple example showing how to get gamepad events."""

# from __future__ import print_function
from inputs import get_gamepad
import numpy as np
import time

# DPAD_MAX = 32767
# translate = np.array((0.0,0.0)) # as a proportion
# tilt = np.array((0.0,0.0))
# rotate = 0
# updown = 0

def main():
    DPAD_MAX = 32767
    DPAD_SCALE = DPAD_MAX/100
    TRIG_MAX = 255
    TRIG_SCALE = TRIG_MAX/100
    translate = np.array((0.0,0.0)) # as a proportion
    tilt = np.array((0.0,0.0))
    rotateRight = 0.0
    rotateLeft = 0.0
    rotate = 0
    updown = 0

    while 1:
        events = get_gamepad()

        for event in events:
            # print(event.ev_type, event.code, event.state)

            if event.code == "ABS_X":
                translate[1] = event.state / DPAD_SCALE
            
            if event.code == "ABS_Y":
                translate[0] = event.state / DPAD_SCALE

            if event.code == "ABS_RX":
                tilt[1] = event.state / DPAD_SCALE

            if event.code == "ABS_RY":
                tilt[0] = event.state / DPAD_SCALE

            if event.code == "ABS_Z":
                rotateLeft = event.state / TRIG_SCALE
            
            if event.code == "ABS_RZ":
                rotateRight = event.state / TRIG_SCALE

            if event.code == "ABS_HAT0Y":
                if event.state == -1:
                    updown = 1
                elif event.state == 1:
                    updown = -1
                else:
                    updown = 0
        
        rotate = rotateRight - rotateLeft
        
        # print("Translate values:", translate)
        # print("Tilt values:", tilt)
        print("Rotate:", rotate)

        if updown == 1:
            print("Increase Z")
        elif updown == -1:
            print("Lower Z")
        else:
            print("Keep Z")

        print("")

        # time.sleep(0.1)
        
if __name__ == "__main__":
    main()
