Draggy
====

Enable three- or four-finger drag on touchpads.

### Usage

Draggy will attempt to enable itself on all multitouch devices that can also send a click event (note that for the moment this means drawing tablets may be unsupported). Simply call `draggy` and it should Just Work™.

You can also pass it the path of the touchpad device to enable gestures on:

`draggy -d /dev/input/event14`

You can find the path with `libinput list-devices` (look for the device with the `gesture` capability, not necessarily the one with `Trackpad` in its name).

The script enables three-finger drag by default. Four-finger drag is available with the `-c` or `--count` option:

`draggy -c 4 -d /dev/input/event14`

### Dependencies

* Python 3
* [python-evdev](https://python-evdev.readthedocs.io/en/latest/): `sudo pip install evdev` or install `python3-evdev` package
* libinput

The script also needs `/dev/uinput` access. To temporarily enable, run `sudo chmod 0666 /dev/uinput`. To permanently enable, copy `40-uinput.rules` to `/etc/udev/rules.d`, ensure your user is in the `uinput` group, and restart your machine. The `uinput` module is builtin to some kernels, but if yours does not include it you will have to load it with `sudo modprobe uinput`.

### Installation & Removal

The script runs fine in place, but for continued use you may want to set it to auto-start. There a number of ways to do this, below is a suggestion using systemd:

1. Copy `draggy` and `get_gesture_devices.py` to `/usr/local/bin`
2. Copy `draggy.service` to `/usr/lib/systemd/system`
3. Test the unit with `systemctl start draggy.service`
4. Enable the unit to run on boot with `systemctl enable draggy.service`

Removal consists of reversing the above steps:

1. Disable the unit with `systemd disable draggy.service`
2. Remove `/usr/lib/systemd/system/draggy.service`
3. Remove `/usr/local/bin/draggy` and `/usr/local/bin/get_gesture_devices.py`

### Testing

Tested on a 2013 MacBook Air and a ThinkPad T580. If it doesn't work for you, please file an issue with as much documentation as you can so that I can try to fix it.

### LICENSE

Copyright (C) 2019-2020 Dave Riedstra. This program is distributed under the terms of the GNU General Public License.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
