# -*- coding: utf-8 -*-
from __future__ import print_function

__info__ = """
Shell Messages
Garin Wally; March 2015, April 2016

This module provides users with a toolkit of functions for making console-based
tools look better.
"""

__version__ = ("0.1.2", "wfmessages",
               """Changelog:
                - completely reconfigured status messages
                """)

import sys
import time
import traceback
import urllib
import urllib2

import colorama as _colorama


# Process Message Length (PROC_LEN)
# Global variable that allows fprint and status_msg to communicate
# See 
_PROC_LEN = 0

#SPACING = 40


_colors = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'purple': 35,
    'cyan': 36,
    'white': 37
    }


def color_str(s, color):
    """Colors input string. Requires colorama package to print correctly."""

    return ("\x1b[1;{1}m{0}\x1b[0m".format(s, _colors[color.lower()]))


def show_colors():
    c = " ".join([color_str(name, name) for name in _colors.keys()])
    cprint(c)


def cprint(s, color=None, end="\n", flush=True):
    """Color print.
    
        Args:
            s (str): string to be printed
            color (str): color of string text
            end (str): end-of-string string; like 'print' uses "\n" by default
        
        Usage:
            >>> cprint("Error", "red")
            Error # printed in red

    """
    if color:
        s = color_str(s, color)
    # Toggle colorama ON
    _colorama.init()
    # Print string; flush forces the print to occur
    print(s, end=end)
    if flush:
        sys.stdout.flush()
    # Toggle colorama OFF
    _colorama.deinit()
    return

# TODO: default end to ""?
def fprint(s, end="\n", flush=True, wait_for_enter=False):
    """Force print. Use end="" for processing messages.
    
        Args:
            s (str): string to be printed
            end (str): end-of-string string; like 'print' uses "\n" by default
            flush (bool): use sys.stdout.flush() to force the print
            wait_for_enter (bool): hangs until <Enter> keypress after print;
                useful for error messages and in combination with sys.exit().
        
        Usage:
            >>> fprint("Causing error...", "", True)
            Causing error...
            Press <Enter> to exit.
    """
    # Toggle colorama ON
    _colorama.init()
    # Print string; flush forces the print to occur
    print(s, end=end)
    if flush:
        sys.stdout.flush()
    # Save the process message length for use in status_msg()
    if end == "":
        global _PROC_LEN
        _PROC_LEN = len(s)
    if wait_for_enter:
        raw_input("Press <Enter> to exit.")
    # Toggle colorama OFF
    _colorama.deinit()
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
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_traceback:
        tb_lines = traceback.format_exc().splitlines()
        msg = "{0}; Line: {1}\n".format(tb_lines[-1],
                                        str(exc_traceback.tb_lineno))
        if red:
            return color_str(msg, "red")
        return msg
    return ""


class _StatusMsgs(object):
    """Status messages and colors."""
    def __init__(self):
        """Set defaults."""
        self._spacing = 40
        self._success_msg = color_str("[DONE]", "green")
        self._fail_msg = color_str("[FAILED]", "red")

    def set_spacing(self, spacing=40):
        self._spacing = spacing

    def set_success(self, success_msg="[DONE]", color="green"):
        """Change the session's default success message and color."""
        msg = color_str(success_msg, color)
        self._success_msg = msg

    def set_fail(self, fail_msg="[FAILED]", color="red"):
        """Change the session's default fail message and color."""
        msg = color_str(fail_msg, color)
        self._fail_msg = msg

    def _test(self):
        """Displays the success and fail status messages."""
        fprint("Success", "")
        self.success()
        fprint("Failure", "")
        self.fail()

    def _place_elipses(self):
        global _PROC_LEN
        
        # If no message precedes the status, don't use elipses
        if _PROC_LEN == 0:
            _PROC_LEN = self._spacing
        # Print the elipses if a processing message shares the line
        fprint("".ljust(self._spacing-_PROC_LEN, "."), end="")
        
        # Reset processing message length
        _PROC_LEN = 0
        return

    def success(self):
        self._place_elipses()
        cprint(self._success_msg)
        
    def fail(self):
        self._place_elipses()
        cprint(self._fail_msg)

    def custom(self, custom_msg, color='white'):
        self._place_elipses()
        cprint(custom_msg, color)


status = _StatusMsgs()

# TESTS
if __name__ == '__main__':
    # STATUS TESTS
    # Success
    fprint("Success...", "");time.sleep(2);status.success()
    # Fail
    fprint("Fail...", "");time.sleep(2);status.fail()
    # Custom
    fprint("Custom...", "");time.sleep(2);status.custom("[COMPLETE]", 'cyan')
    # Change default fail
    status.set_fail("OMG!")
    fprint("New fail default...", "");time.sleep(2);status.fail()

    # TEST ERROR
    fprint("Intentional Error:\t", "")
    try:
        raise Exception("Test Error")
    except:
        cprint(get_error())

    fprint("Testing Complete", wait_for_enter=True)

