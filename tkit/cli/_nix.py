# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function

import re

import colorama
from termcolor import colored

from tkit.cli import handle_ex

__all__ = ["nix", "nix_decorator"]


colorama.init()


# Attributes (bold)
text_attrs = (None, ["bold"])

# Prefixes
PFX = {
    "processing": colored("......", "white", *text_attrs),
    "done": colored("  OK  ", "green", *text_attrs),
    "fail": colored(" FAIL ", "red", *text_attrs),
    "info": colored(" INFO ", "cyan", *text_attrs),
    "warn": colored(" WARN ", "yellow", *text_attrs)
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


# This is the stuff to be available in tkit.cli

nix = Nix()


def nix_decorator(func):
    """Wraps a function with naked try/except and cli.StatusLine messages."""
    nix = Nix()

    def wrapper(*args, **kwargs):
        try:
            if func.__doc__ and re.findall("(?i)msg:", func.__doc__):
                d = func.__doc__
                msg = re.findall("(?i)msg:\n(.*)", d)[0].lstrip()
            else:
                msg = func.__name__
            nix.write(msg)
            # Execute wrapped function
            out = func(*args, **kwargs)
            nix.ok()
        except:  # Naked exception, who knows what will come through that door
            nix.fail()
            handle_ex()
        try:
            return out
        except UnboundLocalError:
            pass
    return wrapper
