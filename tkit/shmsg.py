# -*- coding: utf-8 -*-
"""
shmsg - Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making console-based
tools look better.
"""

from __future__ import print_function
import sys
import time
import traceback
import urllib
import urllib2

import colorama
from termcolor import cprint, COLORS, colored


colorama.init()

BOLD = (None, ["bold"])


def show_colors():
    """Displays available text colors."""
    all_colors = " ".join([colored(name, name) for name in COLORS.keys()])
    cprint(all_colors)


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


def send_text(cell_number, message):
    """Sends a text message via textbelt.com"""
    url = 'http://textbelt.com/text'
    fail_msg = "send_text failed: "

    # Non-string phone number error
    if not isinstance(cell_number, str) or not cell_number.isdigit():
        raise AttributeError(
            fail_msg + "Input cell_number must be a numeric string")

    # Non-string/list message error
    if isinstance(message, list):
        text_content = '\n'.join([i for i in message])
    elif isinstance(message, str):
        text_content = message
    else:
        raise AttributeError(
            fail_msg + "Input message must be a string or list")

    # Prepares communication with textbelt.com
    values = {'message': text_content, 'number': cell_number}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)

    # Attempts to send request
    try:
        urllib2.urlopen(req)

    # Catches and relabels send errors
    except:
        try:
            # Check if textbelt.com site is down
            urllib2.urlopen('http://www.google.com', timeout=2)
            error_msg = "Possible problem with site: " + url
            raise urllib2.URLError(fail_msg + error_msg)

        except urllib2.URLError:
            # Assume internet connection failure
            error_msg = "No Internet connection"
            raise urllib2.URLError(fail_msg + error_msg)
    return


def get_error(red=True):
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
            return colored(msg, "red", *BOLD)
        return msg
    return ""


class _StatusMsgs(object):
    """Status messages and colors."""
    def __init__(self):
        """Set defaults."""
        self._spacing = 40
        self._proc_len = 0
        self._success_msg = colored("[DONE]", "green", *BOLD)
        self._fail_msg = colored("[FAILED]", "red", *BOLD)

    def set_spacing(self, spacing=40):
        """Sets spacing of status message."""
        self._spacing = spacing

    def set_success(self, success_msg="[DONE]", color="green"):
        """Change the session's default success message and color."""
        msg = colored(success_msg, color, *BOLD)
        self._success_msg = msg

    def set_fail(self, fail_msg="[FAILED]", color="red"):
        """Change the session's default fail message and color."""
        msg = colored(fail_msg, color, *BOLD)
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

    def custom(self, custom_msg, color='white'):
        """Print a custom message."""
        self._place_elipses()
        cprint(custom_msg, color, *BOLD)

    def write(self, string):
        """Create a processing message.

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


MSG = _StatusMsgs()


# TESTS
if __name__ == '__main__':
    # STATUS TESTS
    # Success
    MSG.write("Success...")
    time.sleep(2)
    MSG.success()
    # Fail
    MSG.write("Fail...")
    time.sleep(2)
    MSG.failure()
    # Custom
    MSG.write("Custom...")
    time.sleep(2)
    MSG.custom("[COMPLETE]", 'cyan')
    # Change default fail
    MSG.set_fail("OMG!")
    MSG.write("New fail default...")
    time.sleep(2)
    MSG.failure()

    # TEST ERROR
    fprint("Intentional Error:\t", "")
    try:
        raise Exception("Test Error")
    except Exception:
        cprint(get_error())

    fprint("Testing Complete", wait_for_enter=True)
