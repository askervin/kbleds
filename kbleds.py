#!/usr/bin/python2

# kbleds.py - library for controlling keyboard LEDs.
#
# Copyright (C) 2014 Antti Kervinen <antti.kervinen@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA


"""kbled - control keyboard LEDs
"""

import array
import fcntl
import os

# linux/kd.h
KDGETLED    = 0x4B31 # return current led state
KDSETLED    = 0x4B32 # set led state [lights, not flags]
KDGKBLED    = 0x4B64 # get led flags (not lights)
KDSKBLED    = 0x4B65 # set led flags (not lights)
LED_SCR     = 0x01   # scroll lock led
LED_NUM     = 0x02   # num lock led
LED_CAP     = 0x04   # caps lock led
LED_SCR_BIT = 0      # scroll lock led bit, 0 == LSB
LED_NUM_BIT = 1      # num lock led bit
LED_CAP_BIT = 2      # caps lock led bit

class Leds(object):
    def __init__(self, tty_device="/dev/console"):
        self._buf = array.array("c", "\x00")
        self._tty_fd = os.open(tty_device, os.O_RDONLY)

    def __del__(self):
        try:
            os.close(self._tty_fd)
        except OSError:
            pass

    def state(self):
        """returns keyboard LED state
        """
        fcntl.ioctl(self._tty_fd, KDGETLED, self._buf, True)
        return ord(self._buf.tolist()[0])

    def set_state(self, state):
        """set keyboard LED state

        Parameters:
          state (integer):
                  three least significant bits of the integer
                  (LED_SCR_BIT (LSB), LED_NUM_BIT, LED_CAP_BIT)
                  define the state of scroll, num and caps lock
                  LEDs.
        """
        fcntl.ioctl(self._tty_fd, KDSETLED, state)
