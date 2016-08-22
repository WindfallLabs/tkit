# -*- coding: utf-8 -*-
"""status_example.py: double-click executable that displays the StatusLine
object.
Author: Garin Wally; Aug 2016

"""

from time import sleep

from tkit.cli import StatusLine, wait


status = StatusLine()
print(__doc__)

status.write("Run important task...")
sleep(2)
status.success()

status.write("Shotgun a beer...")
status.success()

status.write("Get a hot date...")
sleep(3)
status.failure()

status.custom("COMPLETE", "cyan")

wait()
