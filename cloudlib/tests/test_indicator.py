# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

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
        import Queue
        spinner = indicator.Spinner(work_q=Queue.Queue())
        self.assertEqual(isinstance(spinner.work_q, Queue.Queue), True)
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
