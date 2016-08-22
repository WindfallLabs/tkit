# -*- coding: utf-8 -*-
"""handle_ex_example.py: double-click executable that displays the handle_ex
function.
Author: Garin Wally; Aug 2016

"""

from time import sleep

from tkit.cli import StatusLine, wait, handle_ex


status = StatusLine()
print(__doc__)

status.write("Run important task...")
sleep(2)
status.success()

status.write("Shotgun a beer...")
status.failure()

try:
    raise IOError("You spilled!")
except IOError:
    handle_ex()
