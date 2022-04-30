#!/usr/bin/env python3
import evdev


def get_gesture_devices(num_fingers = 3):
    '''returns a list of devices which should work with draggy'''
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]


    def dev_filter(dev):
        ec = evdev.ecodes
        caps = dev.capabilities()

        # has multitouch
        finger_key = ec.BTN_TOOL_TRIPLETAP if num_fingers == 3 else ec.BTN_TOOL_QUADTAP
        has_key = (ec.EV_KEY in caps and finger_key in caps[ec.EV_KEY]
            and ec.BTN_TOOL_FINGER in caps[ec.EV_KEY]
            and ec.BTN_TOUCH in caps[ec.EV_KEY])

        return has_key

    return list(filter(dev_filter, devices))
