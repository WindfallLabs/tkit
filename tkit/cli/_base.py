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

__all__ = ["show_colors", "GetError", "StatusLine"]

colorama.init()


def show_colors():
    """Displays available text colors."""
    all_colors = " ".join([colored(name, name) for name in COLORS.keys()])
    cprint(all_colors)

'''
def fprint(string, end="\n", flush=True, wait_for_enter=False):
    """Force print. Use end="" for processing messages.

        Args:
            string (str): string to be printed
            end (str): end-of-string string; like 'print' uses "\n" by default
            flush (bool): use sys.stdout.flush() to force the print
            wait_for_enter (bool): hangs until <Enter> keypress after print;
                useful for error messages and in combination with sys.exit().

        Usage:
            >>> fprint("Causing error...", "", True)
            Causing error...
            Press <Enter> to exit.
    """
    # Print string; flush forces the print to occur
    print(string, end=end)
    if flush:
        sys.stdout.flush()
    if wait_for_enter:
        raw_input("Press <Enter> to exit.")
    return


def get_error(red=True, wait=True):
    """Simple, logging-friendly traceback message.
    Returns error message and line number.

        Usage:
            >>> try:
            ...     raise Exception("Intentional Error")
            ... except:
            ...     fprint(get_error()))
            Exception: Intentional Error; Line: 2
    """
    exc_traceback = sys.exc_info()[2]
    if exc_traceback:
        tb_lines = traceback.format_exc().splitlines()
        msg = "{0}; Line: {1}\n".format(tb_lines[-1],
                                        str(exc_traceback.tb_lineno))
        if red:
            return colored(msg, "red", None, ["bold"])
        return msg
    return ""
'''


class GetError(object):
    """Considerate traceback: prints errors in red and waits for keypress by
    default."""
    def __init__(self, red=True, wait=False):
        self.msg = self.get_msg()
        if self.msg:
            print(self.__repr__())
        if wait:
            raw_input("Press <Enter> to continue")

    def get_msg(self):
        exc_traceback = sys.exc_info()[2]
        if exc_traceback:
            tb_lines = traceback.format_exc().splitlines()
            msg = "{0}; Line: {1}".format(tb_lines[-1],
                                          str(exc_traceback.tb_lineno))
            return msg
        else:
            return None

    def __repr__(self):
        if self.msg:
            return colored(self.msg, "red", None, ["bold"])
        return "None"


class StatusLine(object):
    """Status messages and colors."""
    def __init__(self):
        """Set defaults."""
        self._spacing = 40
        self._proc_len = 0
        self._bold = (None, ["bold"])
        self._success_msg = colored("[DONE]", "green", *self._bold)
        self._fail_msg = colored("[FAILED]", "red", *self._bold)

    def set_spacing(self, spacing=40):
        """Sets spacing of status message."""
        self._spacing = spacing

    def set_success(self, success_msg="[DONE]", color="green"):
        """Change the session's default success message and color."""
        msg = colored(success_msg, color, *self._bold)
        self._success_msg = msg

    def set_fail(self, fail_msg="[FAILED]", color="red"):
        """Change the session's default fail message and color."""
        msg = colored(fail_msg, color, *self._bold)
        self._fail_msg = msg

    def _test(self):
        """Displays the success and fail status messages."""
        self.write("Success")
        time.sleep(1)
        self.success()

        self.write("Failure")
        time.sleep(1)
        self.failure()

    def bold_off(self):
        """Turns bold/bright colored text off."""
        if self._bold[1]:
            self._bold = (None, None)

    def bold_on(self):
        """Turns bold/bright colored text on. Default: on."""
        if not self.bold[1]:
            self._bold = (None, ["bold"])

    def _place_elipses(self):
        """Counts and prints elipses."""
        # If no message precedes the status, don't use elipses
        if self._proc_len == 0:
            self._proc_len = self._spacing
        # Print the elipses if a processing message shares the line
        print("".ljust(self._spacing-self._proc_len, "."), end="")
        sys.stdout.flush()

        # Reset processing message length
        self._proc_len = 0
        return

    def success(self):
        """Print the success message."""
        self._place_elipses()
        cprint(self._success_msg)

    def failure(self):
        """Print the fail message."""
        self._place_elipses()
        cprint(self._fail_msg)

    def custom(self, custom_msg, color='white', wait=False):
        """Print a custom message."""
        self._place_elipses()
        cprint(custom_msg, color, *self._bold)
        if wait:
            raw_input("Press <Enter> to continue.")

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
        self._proc_len = len(string)
        # Print string; flush forces the print to occur
        print(string, end="")
        sys.stdout.flush()

        return


# TESTS
if __name__ == '__main__':
    print("Testing status messages...\n")
    # STATUS TESTS
    # Success
    status = StatusLine()
    status.write("Success...")
    time.sleep(2)
    status.success()
    # Fail
    status.write("Fail...")
    time.sleep(2)
    status.failure()
    # Custom
    status.write("Custom...")
    time.sleep(2)
    status.custom("[COMPLETE]", 'cyan')
    # Change default fail
    status.bold_off()
    status.set_fail("Unbolded Red")
    status.write("set_fail...")
    time.sleep(2)
    status.failure()

    # TEST ERROR
    print("Intentional Error:")
    try:
        raise Exception("Test Error")
    except Exception:
        GetError(wait=True)
