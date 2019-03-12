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
import queue
from src.log_messages.log_type import LogType
from src.threading.worker_state import WorkerState
from src.threading.worker_thread import WorkerThread
from src.threading.base_job import BaseJob


class TestWorkerThread(unittest.TestCase):

    def setUp(self):
        self.feedback_log = queue.Queue()  # holds messages for log
        self.job_list = [TestJob(self.feedback_log).__class__]
        self.worker_thread = WorkerThread(self.feedback_log, self.job_list)

    def tearDown(self):
        self.feedback_log = None
        self.job_list = None
        self.worker_thread = None

    def test_get_state(self):
        self.assertEqual(WorkerState.RUNNING, self.worker_thread.get_state())

    def test_put_feedback(self):
        # Adding a log message to the queue and asserting if its done correctly
        log_message = 'Conversion Test'
        log_type = LogType.INFORMATION
        initial_queue_length = len(self.worker_thread.feedback_log.queue)
        self.worker_thread.put_feedback(log_message, log_type)
        self.assertEqual(1, len(self.worker_thread.feedback_log.queue) - initial_queue_length)
        log_in_queue = self.worker_thread.feedback_log.get()
        self.assertEqual(log_message, log_in_queue.get_message())
        self.assertEqual(log_type, log_in_queue.get_message_type())

    def test_get_status(self):
        self.worker_thread.run()
        self.assertEqual('', self.worker_thread.get_status())


class TestJob(BaseJob):
    def do_job(self):
        self.is_done.set()

    def get_work(self):
        pass

