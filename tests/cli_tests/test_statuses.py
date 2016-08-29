# -*- coding: utf-8 -*-

import unittest
import sys
from time import sleep
from StringIO import StringIO

from tkit.cli import StatusLine, status_decorator  # TODO: replace with status


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
        """status.success()"""
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok..................................."
             "\x1b[1m\x1b[32m[DONE]\x1b[0m\n"))

    def test_failure(self):
        """status.failure()"""
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Will fail..............................."
             "\x1b[1m\x1b[31m[FAILED]\x1b[0m\n"))

    def test_custom(self):
        """status.custom()"""
        self.status.custom("COMPLETE", "cyan")
        self.assertEqual(
            self.io_out.getvalue(),
            "\x1b[1m\x1b[36mCOMPLETE\x1b[0m\n")


class TestStatus_color_disabled(unittest.TestCase):
    def setUp(self):
        self.status = StatusLine(disable_colors=True)
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_write(self):
        """no color status.write()"""
        self.status.write("Doing important task...")
        self.assertEqual(
            self.io_out.getvalue(),
            "Doing important task...")

    def test_success(self):
        """no color status.success()"""
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            "Be ok...................................[DONE]\n")

    def test_failure(self):
        """no color status.failure()"""
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            "Will fail...............................[FAILED]\n")

    def test_complete(self):
        """no color status.complete()"""
        self.status.custom("COMPLETE", "cyan")
        self.assertEqual(self.io_out.getvalue(), "COMPLETE\n")



class TestStatus_half_spacing(unittest.TestCase):
    def setUp(self):
        self.status = StatusLine(disable_colors=True)
        self.status.set_spacing(20)
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_success(self):
        """no color, half space status.success()"""
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(self.io_out.getvalue(),
                         "Be ok...............[DONE]\n")

    def test_failure(self):
        """no color, half space status.failure()"""
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(self.io_out.getvalue(),
                         "Will fail...........[FAILED]\n")

    def test_reset(self):
        """no color, reset spacing status.success"""
        self.status.set_spacing()
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok...................................[DONE]\n"))
        

class TestStatus_set_msgs(unittest.TestCase):
    def setUp(self):
        self.status = StatusLine()
        self.status.set_success(success_msg="PASS!", color="blue")
        self.status.set_fail(fail_msg="WRONG!", color="yellow")
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    def test_success(self):
        """status.success()"""
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok..................................."
             "\x1b[1m\x1b[34mPASS!\x1b[0m\n"))

    def test_failure(self):
        """status.failure()"""
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Will fail..............................."
             "\x1b[1m\x1b[33mWRONG!\x1b[0m\n"))

    def test_success_white(self):
        """status.success()"""
        self.status.set_success("PASS!", None)
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok...................................PASS!\n"))

    def test_failure_white(self):
        """status.failure()"""
        self.status.set_fail("WRONG!", None)
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Will fail...............................WRONG!\n"))

    def test_reset_success(self):
        self.status.set_success()
        self.status.write("Be ok")
        self.status.success()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Be ok..................................."
             "\x1b[1m\x1b[32m[DONE]\x1b[0m\n"))

    def test_reset_failure(self):
        self.status.set_fail()
        self.status.write("Will fail")
        self.status.failure()
        self.assertEqual(
            self.io_out.getvalue(),
            ("Will fail..............................."
             "\x1b[1m\x1b[31m[FAILED]\x1b[0m\n"))


class TestStatusDecorator(unittest.TestCase):
    def setUp(self):
        self.io_out = StringIO()
        sys.stdout = self.io_out
    def tearDown(self):
        sys.stdout = OLD_STDOUT

    @status_decorator
    def in_doc(self, stuff):
        """Has message value in __doc__.
        Args:
            stuff (str): stuff to do
        Returns stuff.
        Msg:
            Doing stuff..."""
        return stuff

    def test_in_doc(self):
        self.in_doc("Stuff to process")
        self.assertEqual(
            self.io_out.getvalue(),
            ("Doing stuff............................."
             "\x1b[1m\x1b[32m[DONE]\x1b[0m\n"))

    @status_decorator
    def not_in_doc(self, stuff):
        """Does not have message value in __doc__."""
        return stuff

    def test_not_in_doc(self):
        self.not_in_doc("Stuff to process")
        self.assertEqual(
            self.io_out.getvalue(),
            ("not_in_doc.............................."
             "\x1b[1m\x1b[32m[DONE]\x1b[0m\n"))
