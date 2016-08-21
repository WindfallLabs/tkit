# -*- coding: utf-8 -*-


import unittest
import sys
from time import sleep
from StringIO import StringIO

from tkit.cli import Nix


OLD_STDOUT = sys.stdout



class TestNix(unittest.TestCase):
    def setUp(self):
        self.nix = Nix()
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_write(self):
        """nix.write()"""
        self.nix.write("Doing important task")
        self.assertEqual(
            self.io_out.getvalue(),
            "[\x1b[1m\x1b[37m......\x1b[0m]  Doing important task\r")

    def test_ok(self):
        """nix.ok()"""
        self.nix.write("Be ok")
        self.io_out.seek(0)
        self.nix.ok()
        self.assertEqual(
            self.io_out.getvalue(),
            "[\x1b[1m\x1b[32m  OK  \x1b[0m]  Be ok\n")

    def test_fail(self):
        """nix.fail()"""
        self.nix.write("Dang it")
        self.io_out.seek(0)
        self.nix.fail()
        self.assertEqual(
            self.io_out.getvalue(),
            "[\x1b[1m\x1b[31m FAIL \x1b[0m]  Dang it\n")

    def test_info(self):
        """nix.info()"""
        self.nix.info("Useless information")
        self.assertEqual(
            self.io_out.getvalue(),
            "[\x1b[1m\x1b[36m INFO \x1b[0m]  Useless information\n")

    def test_warn(self):
        """nix.warn()"""
        self.nix.warn("A hopeless warning")
        self.assertEqual(
            self.io_out.getvalue(),
            "[\x1b[1m\x1b[33m WARN \x1b[0m]  A hopeless warning\n")
