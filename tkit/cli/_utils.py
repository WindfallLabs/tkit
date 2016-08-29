# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function

import sys
import traceback

import colorama
from termcolor import cprint, COLORS, colored

# Python 3 compatibility
if sys.version.startswith("3"):
    raw_input = input


__all__ = ["show_colors", "wait", "handle_ex"]

colorama.init()


def show_colors():
    """Displays available text colors."""
    all_colors = " ".join([colored(name, name) for name in COLORS.keys()])
    cprint(all_colors)


def wait():
    """Python-version agnostic wait-for-input function."""
    print("\nPress <Enter> to continue")
    raw_input()
    return


def handle_ex():
    """Catches window from closing on exceptions.
    Source: https://stackoverflow.com/questions/6086976"""
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]
    if exc is not None:
        del stack[-1]
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '   {}'.format(traceback.format_exc().lstrip())
    the_err = "".join(stackstr.split("\n")[-2:])
    print("\n".join(stackstr.split("\n")[:-2]))
    cprint(the_err, "red", None, ["bold"])
    wait()
    return
