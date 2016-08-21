# -*- coding: utf-8 -*-
"""display_test.py: double-click executable that displays the Nix object.
Author: Garin Wally; Aug 2016

"""

from time import sleep

from cli import Nix, wait


nix = Nix()
print(__doc__)

nix.write("Run important task")
sleep(2)
nix.ok()

nix.write("Shotgun a beer")
nix.ok()


nix.info("Computer on")


nix.write("Get a hot date")
sleep(3)
nix.fail()


nix.warn("You need a longer todo list")

wait()
