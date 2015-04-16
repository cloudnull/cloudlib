# Copyright 2015, Kevin Carter.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import Queue as queue
except ImportError:
    import queue
import unittest

import mock

from cloudlib import indicator


class TestBasicUtils(unittest.TestCase):
    def setUp(self):
        self.sys_patched = mock.patch('cloudlib.indicator.sys.stdout')
        self.sys = self.sys_patched.start()

        self.multi_patched = mock.patch(
            'cloudlib.indicator.multiprocessing.Process'
        )
        self.multi = self.multi_patched.start()

    def tearDown(self):
        self.sys_patched.stop()
        self.multi_patched.stop()

    def test_class_objects(self):
        spinner = indicator.Spinner()
        self.assertEqual(spinner.work_q, None)
        self.assertEqual(spinner.run, True)
        self.assertEqual(spinner.msg, None)

    def test_class_objects_msg(self):
        spinner = indicator.Spinner(msg='test')
        self.assertEqual(spinner.work_q, None)
        self.assertEqual(spinner.run, True)
        self.assertEqual(spinner.msg, 'test')

    def test_class_objects_work_q(self):
        spinner = indicator.Spinner(work_q=queue.Queue())
        self.assertEqual(isinstance(spinner.work_q, queue.Queue), True)
        self.assertEqual(spinner.run, True)
        self.assertEqual(spinner.msg, None)

    def test_run_indicator(self):
        with indicator.Spinner():
            self.sys.write.assert_called()

    def test_run_indicator_object(self):
        spinner = indicator.Spinner()
        spin = spinner.start()
        self.multi.assert_called()
        self.assertTrue(spin)
        spinner.stop()
