# -*- coding: utf-8 -*-


import unittest
import mock
import sys
from time import sleep
from StringIO import StringIO

from tkit.cli._utils import *


OLD_STDOUT = sys.stdout

if sys.version.startswith("3"):
    builtin_str = 'builtins.input'
else:
    builtin_str = '__builtin__.raw_input'



class TestUtils(unittest.TestCase):
    def setUp(self):
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_show_colors(self):
        show_colors()
        expected = ("\x1b[34mblue\x1b[0m "
                    "\x1b[30mgrey\x1b[0m "
                    "\x1b[33myellow\x1b[0m "
                    "\x1b[32mgreen\x1b[0m "
                    "\x1b[36mcyan\x1b[0m "
                    "\x1b[35mmagenta\x1b[0m "
                    "\x1b[37mwhite\x1b[0m "
                    "\x1b[31mred\x1b[0m\x1b[0m\n")
        self.assertEqual(self.io_out.getvalue(), expected)

    def test_wait(self):
        with mock.patch(builtin_str, return_value='\n'):
            wait()
            self.assertEqual(self.io_out.getvalue(),
                             "\nPress <Enter> to continue\n")

    def test_handle_ex(self):
        with mock.patch(builtin_str, return_value='\n'):
            def level1():
                return level2()
            def level2():
                raise BaseException("Test Exception")
            try:
                level1()
            except:
                handle_ex()
            self.io_out.seek(0)
            full = self.io_out.readlines()
            self.assertEqual(full[0],
                             "Traceback (most recent call last):\n")
            self.assertEqual(full[-1],
                             "Press <Enter> to continue\n")
            self.assertTrue(
                "\x1b[1m\x1b[31mBaseException: Test Exception\x1b[0m\n" in full)
