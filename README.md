Draggy
====

Enable three- or four-finger drag on touchpads.

### Usage

To use this script, pass it the path of the touchpad device to enable gestures on:

`draggy /dev/input/event14`

You can find the path with `libinput list-devices` (look for the device with the `gesture` capability, not necessarily the one with `Trackpad` in its name).

The script enables three-finger drag by default. Four-finger drag is available with the `-c` or `--count` flags:

`draggy -c 4 /dev/input/event14`

### Dependencies

* Python 3
* [python-evdev](https://python-evdev.readthedocs.io/en/latest/): `sudo pip install evdev`
* libinput

The script also needs `/dev/uinput` access. To temporarily enable, run `sudo chmod 0666 /dev/uinput`. To permanently enable, copy `40-uinput.rules` to `/etc/udev/rules.d`, ensure your user is in the `uinput` group, and restart your machine. The `uinput` module is builtin to some kernels, but if yours does not include it you will have to load it with `sudo modprobe uinput`.

### Autostarting

No fancy install script yet. Use DE tools or XDG-autostart to call the script on login.

### LICENSE

Copyright (C) 2019 Dave Riedstra. This program is distributed under the terms of the GNU General Public License.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
