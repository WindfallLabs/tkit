# -*- coding: utf-8 -*-
"""
shmsg.py - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making cli-based
script tools look better.
"""

from __future__ import print_function

import sys

import colorama
from termcolor import cprint, colored

from tkit.cli import wait

__all__ = ["StatusLine"]

colorama.init()


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
