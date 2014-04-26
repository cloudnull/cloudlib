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

from cloudlib.logger import logger
from cloudlib import tests


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log = logger.LogSetup()

    def test_logger_max_backup(self):
        self.assertEqual(self.log.max_backup, 5)

    def test_logger_max_size(self):
        self.assertEqual(self.log.max_size, 524288000)

    def test_logger_debug_logging(self):
        self.assertEqual(self.log.debug_logging, False)

    def test_logger_override_backup(self):
        log = logger.LogSetup(max_backup=10)
        self.assertEqual(log.max_backup, 10)

    def test_logger_override_max_backup(self):
        log = logger.LogSetup(max_backup=10)
        self.assertEqual(log.max_backup, 10)

    def test_logger_override_max_size(self):
        log = logger.LogSetup(max_size=10)
        self.assertEqual(log.max_size, 10485760)

    def test_logger_debug_logging_enabled(self):
        log = logger.LogSetup(debug_logging=True)
        self.assertEqual(log.debug_logging, True)

    def test_logger_return_logfile_not_root_new_log_dir(self):
        env = logger.os.getenv = mock.Mock()
        env.return_value = '/home/TestUser'
        logfile = self.log.return_logfile(
            filename='test_file', log_dir='/other'
        )
        self.assertEqual(logfile, '/home/TestUser/test_file')

    def test_logger_return_logfile_root_new_log_dir(self):
        uid = logger.os.getuid = mock.Mock()
        uid.return_value = 0
        env = logger.os.getenv = mock.Mock()
        env.return_value = '/root'
        idr = logger.os.path.isdir = mock.Mock()
        idr.return_value = True
        logfile = self.log.return_logfile(
            filename='test_file', log_dir='/other'
        )
        self.assertEqual(logfile, '/other/test_file')

    def test_logger_return_logfile_not_root(self):
        env = logger.os.getenv = mock.Mock()
        env.return_value = '/home/TestUser'
        logfile = self.log.return_logfile(filename='test_file')
        self.assertEqual(logfile, '/home/TestUser/test_file')

    def test_logger_return_logfile_root(self):
        uid = logger.os.getuid = mock.Mock()
        uid.return_value = 0
        env = logger.os.getenv = mock.Mock()
        env.return_value = '/root'
        idr = logger.os.path.isdir = mock.Mock()
        idr.return_value = True

        logfile = self.log.return_logfile(filename='test_file')
        self.assertEqual(logfile, '/var/log/test_file')

    def test_logger_return_logfile_root_log_dir_not_found(self):
        uid = logger.os.getuid = mock.Mock()
        uid.return_value = 0
        env = logger.os.getenv = mock.Mock()
        env.return_value = '/root'
        idr = logger.os.path.isdir = mock.Mock()
        idr.return_value = False

        logfile = self.log.return_logfile(
            filename='test_file', log_dir='/other'
        )
        self.assertEqual(logfile, '/root/test_file')


class TestLoggerHandlers(unittest.TestCase):
    def setUp(self):
        self.rh = logger.handlers.RotatingFileHandler = mock.Mock()
        self.sh = logger.logging.StreamHandler = mock.Mock()
        logger.logging.getLogger = tests.Logger
        logger.logging.Formatter = tests.returnstring
        self.log = logger.LogSetup()

    def test_logger_default_logger(self):
        self.log.default_logger(
            name='test_log', enable_file=False, enable_stream=False
        )
        format = '%(asctime)s - %(module)s:%(levelname)s => %(message)s'
        self.assertEqual(self.log.format, format)

    def test_logger_default_logger_new_formatter(self):
        self.log.format = '%(test)s'
        self.log.default_logger(
            name='test_log', enable_file=False, enable_stream=False
        )
        self.assertEqual(self.log.format, '%(test)s')

    def test_logger_enable_file(self):
        self.log.default_logger(
            name='test_log', enable_file=True, enable_stream=False
        )
        self.assertTrue(self.rh.called)
        self.assertFalse(self.sh.called)

    def test_logger_enable_stream(self):
        self.log.default_logger(
            name='test_log', enable_file=False, enable_stream=True
        )
        self.assertFalse(self.rh.called)
        self.assertTrue(self.sh.called)

    def test_logger_enable_stream_enable_file(self):
        self.log.default_logger(
            name='test_log', enable_file=True, enable_stream=True
        )
        self.assertTrue(self.rh.called)
        self.assertTrue(self.sh.called)

    def test_logger_set_handler(self):
        log = mock.Mock()
        handler = mock.Mock()
        self.log.set_handler(
            log=log, handler=handler
        )
        self.assertTrue(log.setLevel.called)
        self.assertTrue(handler.setFormatter.called)
        self.assertTrue(log.addHandler.called)