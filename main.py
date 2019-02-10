#!/usr/bin/env python3
import asyncio
from evdev import ecodes as e, InputDevice, UInput, categorize, uinput

# todo - get this from a config file or stdin
dev_name = '/dev/input/event14'

try:
    device = InputDevice(dev_name)
    surrogate = UInput.from_device(device, name=device.name, version=3)
except uinput.UInputError:
    print('/dev/uinput not available; try the following:')
    print('sudo chmod 666 /dev/uinput')
    print('sudo modprobe uinput')
    exit(1)


async def handler(dev, sur):
    dragging = False
    async for event in dev.async_read_loop():
        if event.type == e.EV_KEY:
            event = categorize(event)
            if event.keycode == 'BTN_TOOL_TRIPLETAP':
                dragging = event.keystate == 1
                click_val = 1 if dragging else 0

                # to fake multitouch events, even if it's just one touch,
                # we need to fake these events as well.
                # I'm not sure where ID comes from (except that it's -1
                # when the touch leaves), but my birth year happens to be valid
                sur.write(e.EV_ABS, e.ABS_MT_TRACKING_ID, 1989 * click_val - 1)
                sur.write(e.EV_KEY, e.BTN_TOUCH, click_val)
                sur.write(e.EV_KEY, e.BTN_TOOL_FINGER, click_val)

                # this is the actual click event
                sur.write(e.EV_KEY, e.BTN_LEFT, click_val)
                sur.syn()

                # idea: temporarily grab the device to avoid passing on events
                # to the DE (handy for GNOME on Wayland)
                # if dragging:
                #     dev.grab()
                # else:
                #     dev.ungrab()

        elif dragging:
            if event.type == e.EV_ABS:
                if event.code == e.ABS_X:
                    sur.write(e.EV_ABS, e.ABS_MT_POSITION_X, event.value)
                elif event.code == e.ABS_Y:
                    sur.write(e.EV_ABS, e.ABS_MT_POSITION_Y, event.value)
            elif event.type == e.EV_SYN:
                sur.syn()

    sur.close()


# start handling async events
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler(device, surrogate))
except KeyboardInterrupt:
    exit(0)
