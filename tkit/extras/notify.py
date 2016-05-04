# -*- coding: utf-8 -*-
"""
notify.py -- Tkit Notifications
Garin Wally;

This module provides notification functions outside of the usual on-screen
messages.
"""

import urllib
import urllib2


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
            error_msg = "Possible problem with site: {}".format(url)
            raise urllib2.URLError(fail_msg + error_msg)

        except urllib2.URLError:
            # Assume internet connection failure
            error_msg = "No Internet connection"
            raise urllib2.URLError(fail_msg + error_msg)
    return
