# Title: wfmessages
# Desc: Windfall messaging module
# Author: Garin Wally
# Date: March 17, 2015

from __future__ import print_function

__version__ = ("0.1.1", "wfmessages",
               """Changelog:
                - added colored text
                """)

import urllib
import urllib2
import sys
import traceback
import logging
import os
import time

import colorama


# Process Message Length (PROC_LEN)
# Global variable that allows fprint and status_msg to communicate
# See 
_PROC_LEN = 0


def fprint(s, end="\n", wait_for_enter=False):
    """Force prints a string. Use "" for processing messages.
    
        Args:
            s (str): string to be printed
            end (str): end-of-string string; like 'print' uses "\n" by default
            wait_for_enter (bool): hangs until <Enter> keypress after print;
                useful for error messages and in combination with sys.exit().
        
        Usage:
            >>> fprint("Causing error...", "", True)
            Causing error...
            Press <Enter> to exit.
    """
    # Toggle colorama ON
    colorama.init()
    # Print string; flush forces the print to occur
    print(s, end=end)
    sys.stdout.flush()
    # Save the process message length for use in status_msg()
    if end == "":
        global _PROC_LEN
        _PROC_LEN = len(s)
    if wait_for_enter:
        raw_input("Press <Enter> to exit.")
    # Toggle colorama OFF
    colorama.deinit()
    return


def color_str(s, color):
    """Colors input string. Requires colorama package to print correctly."""
    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple': 35,
        'cyan': 36,
        'white': 37
    }
    return ("\x1b[1;{1}m{0}\x1b[0m".format(s, colors[color.lower()]))


def status_msg(complete, spacing=40,
               success="[DONE]", fail="[FAILED]"):
    """Left aligns a completion status to a processing message.
    
        Args:
            complete (bool): True for success message, False for fail message
            spacing (int): distance to left-aligned edge
    
        Usage:
            >>> fprint("Doing Stuff", ""); status_msg(True)
            Doing stuff.............................[DONE]
            >>> fprint("Quite a long Doing Stuff...", ""); status_msg(False)
            Quite a long Doing Stuff................[FAILED]
    """
            
    # Left-align and fill with dots
    global _PROC_LEN
    fprint("".ljust(spacing-_PROC_LEN, "."), end="")
    
    if complete:
        fprint(color_str(success, "green"))
    else:
        fprint(color_str(fail, "red"))
    
    # Reset process length
    _PROC_LEN = 0
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


def get_error(red=False):
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


def get_scriptname(_file): # TODO: Useful???
    """Returns the __file__ name of the current script."""
    # Implement bad args    
    '''
    if not isinstance(_file, str) and os.path.exists(_file):
        raise AttributeError("This function only accepts a __file__ object")
    '''
    name = os.path.split(_file)[-1]
    return name

