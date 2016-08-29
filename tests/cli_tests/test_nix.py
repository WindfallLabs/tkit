# -*- coding: utf-8 -*-


import unittest
import sys
from time import sleep
from StringIO import StringIO

import mock

from tkit.cli import nix, nix_decorator


OLD_STDOUT = sys.stdout

if sys.version.startswith("3"):
    builtin_str = 'builtins.input'
else:
    builtin_str = '__builtin__.raw_input'


class TestNix(unittest.TestCase):
    def setUp(self):
        self.nix = nix
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


class TestNixDecorator(unittest.TestCase):
    def setUp(self):
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    @nix_decorator
    def in_doc(self, stuff):
        """Has message value in __doc__.
        Args:
            stuff (str): stuff to do
        Returns stuff.
        Msg:
            Doing stuff"""
        return stuff

    def test_in_doc(self):
        self.in_doc("Stuff to process")
        self.assertEqual(
            self.io_out.getvalue(),
            ("[\x1b[1m\x1b[37m......\x1b[0m]  "
             "Doing stuff\r[\x1b[1m\x1b[32m  OK  \x1b[0m]  Doing stuff\n"))

    @nix_decorator
    def not_in_doc(self, stuff):
        """Does not have message value in __doc__."""
        return stuff

    def test_not_in_doc(self):
        self.not_in_doc("Stuff to process")
        self.assertEqual(
            self.io_out.getvalue(),
            ("[\x1b[1m\x1b[37m......\x1b[0m]  "
             "not_in_doc\r[\x1b[1m\x1b[32m  OK  \x1b[0m]  not_in_doc\n"))

    @nix_decorator
    def with_error(self):
        """Doc string.
        Msg:
            Cause error"""
        raise AttributeError("This function just isn't good enough")

    def test_error(self):
        with mock.patch(builtin_str, return_value='\n'):
            self.with_error()
        lines = self.io_out.getvalue()
        self.assertTrue(
            "This function just isn't good enough" in lines)
        self.assertTrue(
            "[\x1b[1m\x1b[31m FAIL \x1b[0m]  Cause error\n" in lines)
