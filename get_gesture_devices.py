#!/usr/bin/env python3
import evdev


def get_gesture_devices():
    '''returns a list of devices which should work with draggy'''
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]


    def dev_filter(dev):
        caps = dev.capabilities()
        # 1 = EV_KEY
        # 325 = BTN_TOOL_FINGER
        return 1 in caps and caps[1].count(325) > 0

    return list(filter(dev_filter, devices))
