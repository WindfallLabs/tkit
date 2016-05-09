# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function
import sys
import time
import traceback

import colorama
from termcolor import cprint, COLORS, colored

__all__ = ["show_colors", "wait", "GetError", "StatusLine"]

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
    def __init__(self, red=True, key_wait=False):
        self.err = None
        self.msg = None
        self.line = None
        self.red = red
        self.full_msg = self.get_msg()
        if key_wait:
            wait()

    def get_msg(self):
        exc_traceback = exc_traceback = sys.exc_info()[2]
        if exc_traceback:
            tb_lines = traceback.format_exc().splitlines()
            self.err = tb_lines[-1].split()[0].strip(":")
            self.msg = " ".join(tb_lines[-1].split()[1:])
            self.line = "Line {}".format(exc_traceback.tb_lineno)
            return "{}: {} ({})".format(self.err, self.msg, self.line)
        return None

    def __repr__(self):
        if self.full_msg:
            if self.red:
                return colored(self.full_msg, "red", None, ["bold"])
            return self.full_msg
        else:
            return "No Error"


class StatusLine(object):
    """Status messages and colors."""
    def __init__(self, disable_colors=False):
        """Set defaults."""
        self._disabled_colors = disable_colors
        self._spacing = 40
        self._last_len = 0
        self.text_attrs = (None, ["bold"])
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
            self._success_msg = msg

    def set_fail(self, fail_msg="[FAILED]", color="red"):
        """Change the session's default fail message and color."""
        if color:
            msg = colored(fail_msg, color, *self.text_attrs)
            self._fail_msg = msg
        else:
            self._fail_msg = msg

    def _test(self):
        """Displays the success and fail status messages."""
        self.write("Success")
        time.sleep(1)
        self.success()

        self.write("Failure")
        time.sleep(1)
        self.failure()

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
        except:
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

    def custom(self, custom_msg, color='white', wait=False):
        """Print a custom message."""
        self._place_elipses()
        if color.lower() == "white" or self._disabled_colors:
            print(custom_msg)
        else:
            cprint(custom_msg, color, *self.text_attrs)
        if wait:
            raw_input("Press <Enter> to continue.")

    def nix(self, message, status=True, color="white", attrs=None):
        """Status messages that emulate Linux/Unix startup messages."""
        if status is True:
            status_msg = self._success_msg
        elif status is False:
            status_msg = self._fail_msg
        else:
            if attrs:
                status_msg = colored(status, color, *attrs)
            else:
                status_msg = colored(status, color, *self.text_attrs)

        print("{} {}".format(status_msg, message))

    def write(self, string):
        """Write a processing message.

            Args:
                string (str): string to be printed (e.g. "Processing...")

            Usage:
                >>> self.begin("Causing error..."); self.success()
                Causing error...
                Press <Enter> to exit.
        """
        # Save the process message length for use in status object
        self._last_len = len(string)
        # Print string; flush forces the print to occur
        print(string, end="")
        try:
            # For consoles that do not support flush
            sys.stdout.flush()
        except:
            pass

        return


# TESTS
if __name__ == '__main__':
    print("Testing status messages...\n")
    # STATUS TESTS
    # Success / fail
    status = StatusLine()
    status._test()

    # Change default fail
    status.bold_off()
    status.set_fail("Unbolded Red")
    status.write("set_fail...")
    time.sleep(2)
    status.failure()

    # Custom
    status.write("Custom...")
    time.sleep(2)
    status.custom("[COMPLETE]", 'cyan')

    # Nix
    status.nix(" [ OK ] ", "green", "*nix message printed.")

    # TEST ERROR
    print("\nIntentional Error:")
    try:
        raise Exception("Test Error")
    except Exception:
        GetError(wait=True)
