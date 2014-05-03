kbleds
======

This project provides

- keyboard LED control API for Python (kbleds.py)

- command-line interface for controlling LEDs (kbleds)


Prerequisites
-------------

Linux, Python


Installing
----------

Building and installing packages on Debian and Ubuntu

    dpkg-buildpackage -uc -us
    sudo dpkg -i ../kbleds*deb

Installing without packaging:

    sudo python setup.py install


Usage
-----

See:

    kbleds --help

Example:

    sudo kbleds --leds Cs

switches on Caps lock LED (capital `C`), switches off Scroll lock LED
(lower-case `s`) and does not change Numlock LED (neither `n` nor `N`
is given). If user has read/write access to /dev/console, `sudo` is
not needed.
