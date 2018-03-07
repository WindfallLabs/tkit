# -*- coding: utf-8 -*-
"""
aside.py -- Glorified Print-statements for process messaging.
Author: Garin Wally; 2016


"""

from __future__ import print_function

import re
import sys
import traceback

import colorama
from termcolor import cprint, COLORS, colored

# Python 3 compatibility
if sys.version.startswith("3"):
    raw_input = input


__all__ = ["show_colors",
           "wait",
           "handle_ex",
           "nix",
           "nix_process",
           "status",
           "status_process"]

colorama.init()

# =============================================================================
# TEXT ATTRIBUTES

# I believe Windows only supports bold
BOLD = (None, ["bold"])

# Nix Prefixes
PFX = {
    "processing": colored("......", "white", *BOLD),
    "done": colored("  OK  ", "green", *BOLD),
    "fail": colored(" FAIL ", "red", *BOLD),
    "info": colored(" INFO ", "cyan", *BOLD),
    "warn": colored(" WARN ", "yellow", *BOLD)
    }


# =============================================================================
# UTILS

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


# =============================================================================
# MESSAGE CLASSES

class Status(object):
    """Status messages and colors."""
    def __init__(self, disable_colors=False):
        """Set defaults."""
        self._disabled_colors = disable_colors
        self._spacing = 40
        self._last_len = 0
        self.text_attrs = BOLD
        if disable_colors:
            self._success_msg = "[DONE]"
            self._fail_msg = "[FAILED]"
        else:
            self._success_msg = colored("[DONE]", "green", *self.text_attrs)
            self._fail_msg = colored("[FAILED]", "red", *self.text_attrs)

    def set_spacing(self, spacing=40):
        """Sets spacing of status message."""
        self._spacing = spacing

    def set_success(self, success_msg="[DONE]", color="green"):
        """Change the session's default success message and color."""
        if color:
            msg = colored(success_msg, color, *self.text_attrs)
            self._success_msg = msg
        else:
            self._success_msg = success_msg

    def set_fail(self, fail_msg="[FAILED]", color="red"):
        """Change the session's default fail message and color."""
        if color:
            msg = colored(fail_msg, color, *self.text_attrs)
            self._fail_msg = msg
        else:
            self._fail_msg = fail_msg

    def _place_elipses(self):
        """Counts and prints elipses."""
        # If no message precedes the status, don't use elipses
        if self._last_len == 0:
            self._last_len = self._spacing
        # Print the elipses if a processing message shares the line
        print("".ljust(self._spacing-self._last_len, "."), end="")
        try:
            # For consoles that do not support flush
            sys.stdout.flush()
        except AttributeError:
            pass

        # Reset processing message length
        self._last_len = 0
        return

    def success(self):
        """Print the success message."""
        self._place_elipses()
        print(self._success_msg)

    def failure(self):
        """Print the fail message."""
        self._place_elipses()
        print(self._fail_msg)

    def custom(self, custom_msg, color='white', wait_for_user=False):
        """Print a custom message."""
        self._place_elipses()
        if color.lower() == "white" or self._disabled_colors:
            print(custom_msg)
        else:
            cprint(custom_msg, color, *self.text_attrs)
        if wait_for_user:
            wait()

    def write(self, message):
        """Write a processing message.

            Args:
                message (str): string to be printed (e.g. "Processing...")

            Usage:
                >>> self.begin("Causing error..."); self.success()
                Causing error...
                Press <Enter> to exit.
        """
        # Save the process message length for use in status object
        self._last_len = len(message)
        # Print message; flush forces the print to occur
        print(message, end="")
        try:
            # For consoles that do not support flush
            sys.stdout.flush()
        except AttributeError:
            pass
        return


class Nix(object):
    """*nix-style status messages."""
    def __init__(self, disable_colors=False):
        """Set defaults."""
        self.last_msg = ""
        self._spaces = 2
        self._disabled_colors = disable_colors

    def _make(self, pfx):
        """Formats the output message."""
        pfx = "[{}]".format(PFX[pfx])
        return "{prefix}{spaces}{msg}".format(
            prefix=pfx, spaces=" "*self._spaces, msg=self.last_msg)

    def write(self, message):
        """Take action message from user."""
        self.last_msg = message

        print(self._make("processing"), end="\r")

    def ok(self, message=None):
        """Return the 'OK' message."""
        if message:
            self.last_msg = message
        print(self._make("done"))

    def fail(self, message=None):
        """Return the 'FAIL' message."""
        if message:
            self.last_msg = message
        print(self._make("fail"))

    def info(self, message):
        """Return an 'INFO' message."""
        self.last_msg = message
        print(self._make("info"))

    def warn(self, message):
        """Return a 'WARN' message."""
        self.last_msg = message
        print(self._make("warn"))


class Message(object):
    """Use:

        with Message('Doing stuff...'):
            do_stuff()

    """
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        nix.write(self.message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            nix.fail()
            #cprint(''.join(traceback.format_exception_only(type(e), e)), "red", None, ["bold"])
            traceback.print_exc()
            raw_input("Press <Enter> to exit")
            return
        nix.ok()
        return



# =============================================================================
# DECORATORS

def status_process(func):
    """Wraps a process/function with naked try/except and 'Status' messages.
    Args:
        func (function): function to be wrapped
    Returns a process/function decorated with Status-style messages.
    Use:
        >>> @status_decorator
        >>> def my_process():
        >>>     '''My doc.
        >>>     Msg:
        >>>         Doing stuff...'''
        >>>     import time
        >>>     time.sleep(2)
        >>>     return "Some Value"  # This won't usually print
        Doing stuff.............................[1m[32m[DONE][0m
        'Some Value'

    """
    status = Status()

    def wrapper(*args, **kwargs):
        try:
            if func.__doc__ and re.findall("(?i)msg:", func.__doc__):
                d = func.__doc__
                msg = re.findall("(?i)msg:\n(.*)", d)[0].lstrip()
            else:
                msg = func.__name__
            status.write(msg)
            # Execute wrapped function
            out = func(*args, **kwargs)
            status.success()
        except:  # Naked exception, who knows what will come through that door
            status.failure()
            handle_ex()
        try:
            return out
        except UnboundLocalError:
            pass
    return wrapper


def nix_process(func):
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


# =============================================================================
# IMPORTABLE OBJECTS

status = Status()
nix = Nix()
