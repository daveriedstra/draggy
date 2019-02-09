#!/usr/bin/env python3
from evdev import ecodes as e, InputDevice, UInput, categorize

# NTS - if opening /dev/uinput doesn't work,
# sudo chmod 666 /dev/uniput
# sudo modprobe uinput

# todo - get this from a config file or stdin
dev_name = '/dev/input/event14'

device = InputDevice(dev_name)
ui = UInput.from_device(device, name=device.name, version=3)

dragging = False

# todo - try out the async API
for event in device.read_loop():
    if event.type == e.EV_KEY:
        event = categorize(event)
        if event.keycode == 'BTN_TOOL_TRIPLETAP':
            dragging = event.keystate == 1
            click_val = 1 if dragging else 0

            # to fake multitouch events, even if it's just one touch,
            # we need to fake these events as well.
            # I'm not sure where ID comes from (except that it's -1
            # when the touch leaves), but my birth year happens to be in range
            ui.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, 1989 * click_val - 1)
            ui.write(e.EV_KEY, e.BTN_TOUCH, click_val)
            ui.write(e.EV_KEY, e.BTN_TOOL_FINGER, click_val)

            # this is the actual click event
            ui.write(e.EV_KEY, e.BTN_LEFT, click_val)
            ui.syn()

            # idea: temporarily grab the device to avoid passing on events
            # to the DE (handy for GNOME on Wayland)
            # if dragging:
            #     device.grab()
            # else:
            #     device.ungrab()

    elif dragging:
        if event.type == e.EV_ABS:
            if event.code == e.ABS_X:
                ui.write(e.EV_ABS, e.ABS_MT_POSITION_X, event.value)
            elif event.code == e.ABS_Y:
                ui.write(e.EV_ABS, e.ABS_MT_POSITION_Y, event.value)
        elif event.type == e.EV_SYN:
            ui.syn()

ui.close()
