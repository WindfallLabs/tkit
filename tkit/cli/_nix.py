# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function

import colorama
from termcolor import colored

__all__ = ["Nix"]


colorama.init()


# Attributes (bold)
text_attrs = (None, ["bold"])

# Prefixes
PFX = {
    "processing": colored("....", "white", *text_attrs),
    "done": colored(" OK ", "green", *text_attrs),
    "fail": colored("FAIL", "red", *text_attrs),
    "info": colored("INFO", "cyan", *text_attrs),
    "warn": colored("WARN", "yellow", *text_attrs)
    }


class Nix(object):
    """*nix-style status messages."""
    def __init__(self, disable_colors=False):
        """Set defaults."""
        self.last_msg = ""
        self._spaces = 2
        self._disabled_colors = disable_colors

    def _make(self, pfx):
        pfx = "[{}]".format(PFX[pfx])
        return "{prefix}{spaces}{msg}".format(
            prefix=pfx, spaces=" "*self._spaces, msg=self.last_msg)

    def write(self, message):
        self.last_msg = message

        print(self._make("processing"), end="\r")

    def ok(self):
        print(self._make("done"))

    def fail(self):
        print(self._make("fail"))

    def info(self, string):
        self.last_msg = string
        print(self._make("info"))

    def warn(self, string):
        self.last_msg = string
        print(self._make("warn"))
