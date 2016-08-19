# -*- coding: utf-8 -*-

import unittest
import sys
from time import sleep
from StringIO import StringIO

from tkit.cli import StatusLine


OLD_STDOUT = sys.stdout



class TestStatus(unittest.TestCase):
    def setUp(self):
        self.status = StatusLine()
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_write(self):
        """status.write()"""
        self.status.write("Doing important task...")
        self.assertEqual(
            self.io_out.getvalue(),
            "Doing important task...")

    def test_success(self):
        """nix.success()"""
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok..................................."
             "\x1b[1m\x1b[32m[DONE]\x1b[0m\n"))

    def test_failure(self):
        """nix.failure()"""
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Will fail..............................."
             "\x1b[1m\x1b[31m[FAILED]\x1b[0m\n"))

    def test_warn(self):
        """nix.warn()"""
        self.status.custom("COMPLETE", "cyan")
        self.assertEqual(
            self.io_out.getvalue(),
            "\x1b[1m\x1b[36mCOMPLETE\x1b[0m\n")
