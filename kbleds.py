#!/usr/bin/python2

# kbleds.py - library for controlling keyboard LEDs.
#
# Copyright (C) 2018 Antti Kervinen <antti.kervinen@gmail.com>
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
import platform
import struct
import time

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

# /usr/include/linux/input-event-codes.h
event_types = {
    "EV_SYN":                  0x00,
    "EV_KEY":                  0x01,
    "EV_REL":                  0x02,
    "EV_ABS":                  0x03,
    "EV_MSC":                  0x04,
    "EV_SW":                   0x05,
    "EV_LED":                  0x11,
    "EV_SND":                  0x12,
    "EV_REP":                  0x14,
    "EV_FF":                   0x15,
    "EV_PWR":                  0x16,
    "EV_FF_STATUS":            0x17,
    "EV_MAX":                  0x1f,
    "EV_CNT":                  0x1f + 1,
}

led_codes = {
    "LED_NUML":                0x00,
    "LED_CAPSL":               0x01,
    "LED_SCROLLL":             0x02,
    "LED_COMPOSE":             0x03,
    "LED_KANA":                0x04,
    "LED_SLEEP":               0x05,
    "LED_SUSPEND":             0x06,
    "LED_MUTE":                0x07,
    "LED_MISC":                0x08,
    "LED_MAIL":                0x09,
    "LED_CHARGING":            0x0a,
    "LED_MAX":                 0x0f,
    "LED_CNT":                 0x0f + 1,
}

# struct input_event in /usr/include/linux/input.h
if platform.architecture()[0] == "32bit":
    struct_timeval = "II"
else:
    struct_timeval = "QQ"

struct_input_event = struct_timeval + 'HHi'
sizeof_input_event = struct.calcsize(struct_input_event)

def send_input_event(fd, type_, code, value):
    t = time.time()
    t_sec = int(t)
    t_usec = int(1000000*(t-t_sec))
    rv = os.write(fd, struct.pack(
        struct_input_event,
        t_sec, t_usec,
        type_, code, value))
    return rv == sizeof_input_event

class Leds(object):
    def __init__(self, tty_device=None, input_device=None):
        self._buf = array.array("c", "\x00")
        self._tty_fd = None
        self._input_fd = None
        if tty_device:
            self._tty_fd = os.open(tty_device, os.O_RDONLY)
        if input_device:
            self._input_fd = os.open(input_device, os.O_WRONLY | os.O_NONBLOCK)

    def __del__(self):
        if self._tty_fd:
            try:
                os.close(self._tty_fd)
            except OSError:
                pass
        if self._input_fd:
            try:
                os.close(self._input_fd)
            except OSError:
                pass

    def state(self):
        """returns keyboard LED state
        """
        if self._tty_fd:
            fcntl.ioctl(self._tty_fd, KDGETLED, self._buf, True)
            return ord(self._buf.tolist()[0])
        else:
            # Reading LEDs from USB keyboard not supported
            return 0

    def set_state(self, state):
        """set keyboard LED state

        Parameters:
          state (integer):
                  three least significant bits of the integer
                  (LED_SCR_BIT (LSB), LED_NUM_BIT, LED_CAP_BIT)
                  define the state of scroll, num and caps lock
                  LEDs.
        """
        if self._tty_fd:
            fcntl.ioctl(self._tty_fd, KDSETLED, state)
        if self._input_fd:
            self.set_num((state & LED_NUM) != 0)
            self.set_scroll((state & LED_SCR) != 0)
            self.set_caps((state & LED_CAP) != 0)

    def set_num(self, state):
        """set the state of the num lock LED"""
        if self._input_fd:
            send_input_event(self._input_fd,
                             event_types["EV_LED"],
                             led_codes["LED_NUML"],
                             state)
        elif self._tty_fd:
            new_state = (self.state() & ~LED_NUM) | (state << LED_NUM_BIT)
            self.set_state(new_state)

    def set_scroll(self, state):
        """set the state of the scroll lock LED"""
        if self._input_fd:
            send_input_event(self._input_fd,
                             event_types["EV_LED"],
                             led_codes["LED_SCROLLL"],
                             state)
        elif self._tty_fd:
            new_state = (self.state() & ~LED_SCR) | (state << LED_SCR_BIT)
            self.set_state(new_state)

    def set_caps(self, state):
        """set the state of the caps lock LED"""
        if self._input_fd:
            send_input_event(self._input_fd,
                             event_types["EV_LED"],
                             led_codes["LED_CAPSL"],
                             state)
        elif self._tty_fd:
            new_state = (self.state() & ~LED_CAP) | (state << LED_CAP_BIT)
            self.set_state(new_state)
