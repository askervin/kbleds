#!/usr/bin/python2

"""kbled - control keyboard leds
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
        fcntl.ioctl(self._tty_fd, KDGETLED, self._buf, True)
        return ord(self._buf.tolist()[0])

    def set_state(self, state):
        fcntl.ioctl(self._tty_fd, KDSETLED, state)
