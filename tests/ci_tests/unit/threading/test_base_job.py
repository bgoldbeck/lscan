# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

import unittest
from queue import Queue
from src.threading.base_job import *


class TestBaseJob(unittest.TestCase):

    def setUp(self):
        self.feedback_log = Queue()
        self.base_job = BaseJob(self.feedback_log)

    def tearDown(self):
        self.feedback_log = None
        self.base_job = None

    def test_do_job(self):
        with self.assertRaises(NotImplementedError) as context:
            self.base_job.do_job()
        self.assertEqual("This method is not implemented", str(context.exception))

    def test_get_work(self):
        with self.assertRaises(NotImplementedError) as context:
            self.base_job.get_work()
        self.assertEqual("This method is not implemented", str(context.exception))

    def test_get_status(self):
        self.assertEqual("", self.base_job.get_status())

    def test_put_feedback(self):
        self.base_job.put_feedback("Test Log Message")
        self.assertEqual(1, len(self.base_job.feedback_log.queue))

    def test_update_status(self):
        self.base_job.update_status("Test Update")
        self.assertEqual("Test Update", self.base_job.get_status())

    def test_go(self):
        self.assertFalse(self.base_job.is_running.is_set())
        self.base_job.go()
        self.assertTrue(self.base_job.is_running.is_set())

    def test_pause(self):
        self.assertFalse(self.base_job.is_running.is_set())
        self.base_job.go()
        self.assertTrue(self.base_job.is_running.is_set())
        self.base_job.pause()
        self.assertFalse(self.base_job.is_running.is_set())



