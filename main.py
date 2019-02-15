#!/usr/bin/env python3
import asyncio
from random import randint
from evdev import ecodes, InputDevice, UInput, categorize, uinput

TRACKING_ID_MIN = 1989
TRACKING_ID_MAX = TRACKING_ID_MIN + 1000

# exclusively handle input device during 3fd
# this would prevent default DE handling of 3-finger gestures,
# which is useful in cases where they can't be configured,
# but this feature is still buggy: sometimes the drag gets "stuck."
GRAB = False

# todo - get this from a config file or stdin
input_device_path = '/dev/input/event14'


def set_lock(in_dev, lock):
    '''Grab or ungrab the input device for exclusive handling.

    Useful to prevent triggering DE defined gestures. Still buggy.

    :param in_dev: The source trackpad InputDevice
    :param lock: Boolean, whether to set or release lock
    '''
    if lock:
        try:
            in_dev.grab()
        except IOError:
            print('cannot grab device; may already be grabbed')
    else:
        try:
            in_dev.ungrab()
        except IOError:
            print('cannot ungrab device; may already be ungrabbed')


def send_3fd_frame(in_dev, sur_dev, start=False):
    '''Send an entire event frame representing the start / stop of 3fd.

    :param in_dev: The source trackpad InputDevice
    :param sur_dev: The surrogate UInput device
    :param start: Boolean, whether to start or stop 3fd
    '''
    tracking_id = -1
    click_val = 0
    if start:
        tracking_id = randint(TRACKING_ID_MIN, TRACKING_ID_MAX)
        click_val = 1

    if GRAB:
        set_lock(in_dev, start)

    # to fake multitouch events, even if it's just one touch,
    # we need to fake these events as well.
    sur_dev.write(ecodes.EV_ABS, ecodes.ABS_MT_TRACKING_ID, tracking_id)
    sur_dev.write(ecodes.EV_KEY, ecodes.BTN_TOUCH, click_val)
    sur_dev.write(ecodes.EV_KEY, ecodes.BTN_TOOL_FINGER, click_val)
    sur_dev.write(ecodes.EV_ABS, ecodes.ABS_PRESSURE, 155 * click_val)

    # this is the actual click event
    sur_dev.write(ecodes.EV_KEY, ecodes.BTN_LEFT, click_val)
    sur_dev.syn()


async def handler(in_dev, sur_dev):
    '''The asyncio handler.'''
    is_drag_start_frame = False
    is_drag_end_frame = False
    is_dragging_3 = False

    async for event in in_dev.async_read_loop():
        if event.type == ecodes.EV_SYN:
            if is_drag_start_frame:
                send_3fd_frame(in_dev, sur_dev, start=True)
                is_drag_start_frame = False
            elif is_drag_end_frame:
                send_3fd_frame(in_dev, sur_dev, start=False)
                is_drag_end_frame = False
            elif is_dragging_3:
                sur_dev.syn()

        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_TOOL_TRIPLETAP:
                event = categorize(event)
                is_drag_start_frame = not is_dragging_3 and event.keystate == 1
                is_drag_end_frame = is_dragging_3 and event.keystate == 0
                is_dragging_3 = event.keystate == 1

        elif is_dragging_3 and event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                sur_dev.write(ecodes.EV_ABS, ecodes.ABS_MT_POSITION_X,
                              event.value)
                sur_dev.write(ecodes.EV_ABS, ecodes.ABS_X, event.value)
            elif event.code == ecodes.ABS_Y:
                sur_dev.write(ecodes.EV_ABS, ecodes.ABS_MT_POSITION_Y,
                              event.value)
                sur_dev.write(ecodes.EV_ABS, ecodes.ABS_Y, event.value)
            elif event.code == ecodes.ABS_MT_SLOT and event.value == 0:
                sur_dev.write(ecodes.EV_ABS, ecodes.ABS_MT_SLOT, 0)

    sur_dev.close()


# get input device and create surrogate uinput device
try:
    input_device = InputDevice(input_device_path)
    surrogate_device = UInput.from_device(input_device, name=input_device.name,
                                          version=3)
except uinput.UInputError:
    print('/dev/uinput not available; try the following:')
    print('sudo chmod 666 /dev/uinput')
    print('sudo modprobe uinput')
    exit(1)

# start handling async events
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler(input_device, surrogate_device))
except KeyboardInterrupt:
    exit(0)
