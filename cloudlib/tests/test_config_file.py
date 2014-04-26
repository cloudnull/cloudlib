# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import os
import tempfile
import unittest

import mock

from cloudlib.config_file import parse_ini
from cloudlib import tests


class TestConfigFileIni(unittest.TestCase):
    def setUp(self):
        logger = parse_ini.logging.getLogger = mock.Mock()
        logger.return_value = tests.Logger()

        self.mock_os = parse_ini.os.path.exists = mock.Mock()
        self.mock_os.return_value = True

        self.config = parse_ini.ConfigurationSetup(name='test')

    def test_sys_config(self):
        self.config.load_config()
        self.assertEqual(self.config.config_file, '/etc/test/test.ini')

    def test_sys_config_path(self):
        self.config.load_config(path='/test/test/test')
        self.assertEqual(self.config.config_file, '/test/test/test/test.ini')

    def test_sys_config_path_ext(self):
        self.config.load_config(path='/test/test/test', ext='cfg')
        self.assertEqual(self.config.config_file, '/test/test/test/test.cfg')

    def test_sys_config_path_strip_slash(self):
        self.config.load_config(path='/test/test/test/')
        self.assertEqual(self.config.config_file, '/test/test/test/test.ini')

    def test_sys_config_home(self):
        env = parse_ini.os.getenv = mock.Mock()
        env.return_value = '/home/TestUser'
        self.config.load_config(home=True)
        self.assertEqual(self.config.config_file, '/home/TestUser/.test.ini')

    def test_sys_config_home_ext(self):
        env = parse_ini.os.getenv = mock.Mock()
        env.return_value = '/home/TestUser'
        self.config.load_config(home=True, ext='cfg')
        self.assertEqual(self.config.config_file, '/home/TestUser/.test.cfg')

    def test_sys_config_ext(self):
        self.config.load_config(ext='cfg')
        self.assertEqual(self.config.config_file, '/etc/test/test.cfg')

    def test_sys_config_path_home_ext(self):
        self.config.load_config(path='/test/test/test', home=True, ext='cfg')
        self.assertEqual(self.config.config_file, '/test/test/test/test.cfg')

    def test_sys_config_not_found(self):
        self.mock_os.return_value = False
        self.assertRaises(
            SystemExit,
            self.config.load_config
        )

    def test_sys_config_find_config_success(self):
        self.mock_os.return_value = True
        self.assertEqual(
            self.config._find_config('test_file'),
            'test_file'
        )

    def test_sys_config_find_config_fail(self):
        self.mock_os.return_value = False
        self.assertRaises(
            SystemExit,
            self.config._find_config,
            'test_file'
        )

    def test_sys_config_perms(self):
        stat = parse_ini.os.stat = mock.Mock()
        stat.return_value = tests.StatResult()
        self.config.config_file = '/test/path/config.ini'
        self.assertEqual(self.config.check_perms(), True)

    def test_sys_config_perms_fail(self):
        stat = parse_ini.os.stat = mock.Mock()
        stat.return_value = tests.StatResult()
        self.config.config_file = '/test/path/config.ini'
        self.assertRaises(
            SystemExit, self.config.check_perms, '0644,0444'
        )

    def test_sys_config_config_args_parse_default_section(self):
        flag, local_file = tempfile.mkstemp()
        try:
            with open(local_file, 'wb') as f:
                f.write(tests.CONFIG_FILE)
            self.config.config_file = local_file
            args = self.config.config_args(section='default')
        except Exception as exp:
            self.fail('Failed %s' % exp)
        else:
            self.assertFalse(args.get('false_value'))
            self.assertTrue(args.get('true_value'))
            self.assertTrue(isinstance(args.get('integer_value'), int))
            self.assertTrue(isinstance(args.get('string_value'), str))
        finally:
            os.remove(local_file)

    def test_sys_config_config_args_parse_other_section(self):
        flag, local_file = tempfile.mkstemp()
        try:
            with open(local_file, 'wb') as f:
                f.write(tests.CONFIG_FILE)
            self.config.config_file = local_file
            args = self.config.config_args(section='other_section')
        except Exception as exp:
            self.fail('Failed %s' % exp)
        else:
            self.assertFalse(args.get('false_value'))
            self.assertTrue(args.get('true_value'))
            self.assertTrue(isinstance(args.get('integer_value'), int))
            self.assertTrue(isinstance(args.get('string_value'), str))
        finally:
            os.remove(local_file)
