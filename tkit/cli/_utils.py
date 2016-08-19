# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function
import sys
import re
import time
import traceback

import colorama
from termcolor import cprint, COLORS, colored

__all__ = ["show_colors", "wait", "handle_ex", "GetError"]

colorama.init()


def show_colors():
    """Displays available text colors."""
    all_colors = " ".join([colored(name, name) for name in COLORS.keys()])
    cprint(all_colors)


def wait():
    """Python-version agnostic wait-for-input function."""
    if sys.version.split()[0].startswith("2"):
        input = raw_input
    input("Press <Enter> to continue")
    return


class GetError(object):
    """Emulation of system traceback, includes line number."""
    def __init__(self, red=True, wait=False):
        self.err = None
        self.msg = None
        self.line = None
        self.red = red
        self.full_msg = self.get_msg()
        print(self.full_msg)
        if wait:
            self._wait()

    def get_msg(self):
        exc_traceback = exc_traceback = sys.exc_info()[2]
        if exc_traceback:
            tb_lines = traceback.format_exc().splitlines()
            self.err = "Uh oh" #tb_lines[-1].split()[0]
            self.msg = " ".join(tb_lines[-1].split()[1:])
            self.line = "Line {}".format(exc_traceback.tb_lineno)
            return "{}: {} ({})".format(self.err, self.msg, self.line)
        return None

    def _wait(self):
        """Python-version agnostic wait-for-input function."""
        if sys.version.split()[0].startswith("2"):
            input = raw_input
        input("Press <Enter> to continue")
        return


def handle_ex(e):
    print("\n")
    ex = type(e).__name__
    _n, msg, line = sys.exc_info()
    msg = "{}: {}; Line: {}".format(ex, msg.message, line.tb_lineno)
    print(colored(msg, "red", None, ["bold"]))
    print("")
    raw_input("Press <Enter> to exit.")
    sys.exit(1)
