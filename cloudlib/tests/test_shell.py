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

from cloudlib import shell
from cloudlib import tests


class TestShell(unittest.TestCase):
    def setUp(self):
        self.logger_patched = mock.patch('cloudlib.shell.logger.getLogger')
        self.logger = self.logger_patched.start()
        self.logger.return_value = tests.Logger()

        self.communicate_patched = mock.patch(
            'cloudlib.shell.subprocess.Popen'
        )
        self.communicate = self.communicate_patched.start()

        self.mock_open_patch = mock.patch('cloudlib.shell.open', create=True)
        self.mock_open = self.mock_open_patch.start()

        self.shell = shell.ShellCommands()

    def tearDown(self):
        self.logger_patched.stop()
        self.communicate_patched.stop()
        self.mock_open_patch.stop()

    def test_run_command_success(self):
        self.communicate.return_value = tests.FakePopen()
        output, outcome = self.shell.run_command(command='test_command')
        self.assertEqual(output, 'stdout')
        self.assertEqual(outcome, True)

    def test_run_command_fail(self):
        self.communicate.return_value = tests.FakePopen(return_code=1)
        output, outcome = self.shell.run_command(command='test_command')
        self.assertEqual(output, 'stderr')
        self.assertEqual(outcome, False)

    def test_write_file(self):
        self.shell.write_file('test/file', 'test')
        file_handle = self.mock_open.return_value.__enter__.return_value
        file_handle.write.assert_called_with('test')

    def test_write_lines(self):
        contents = ['test', 'lines']
        self.shell.write_file_lines('test/file', contents)
        file_handle = self.mock_open.return_value.__enter__.return_value
        file_handle.writelines.assert_called_with(contents)

    def test_read_file(self):
        self.shell.read_file('test/file')
        file_handle = self.mock_open.return_value.__enter__.return_value
        file_handle.read.assert_called()

    def test_read_file_lines(self):
        self.shell.read_file('test/file')
        file_handle = self.mock_open.return_value.__enter__.return_value
        file_handle.readlines.assert_called()

    def test_read_large_file_lines(self):
        self.shell.read_file('test/file')
        file_handle = self.mock_open.return_value.__enter__.return_value
        file_handle.readline.assert_called()