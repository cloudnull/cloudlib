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

from cloudlib import tests, parse_ini


class TestConfigFileIni(unittest.TestCase):
    def setUp(self):
        self.logger_patched = mock.patch('cloudlib.parse_ini.logger.getLogger')
        self.logger = self.logger_patched.start()
        self.logger.return_value = tests.Logger()

        self.os_path_patched = mock.patch('cloudlib.parse_ini.os.path.exists')
        self.os_path = self.os_path_patched.start()
        self.os_path.return_value = True

        self.env_patched = mock.patch('cloudlib.parse_ini.os.getenv')
        self.env = self.env_patched.start()

        self.tempfile_patched = mock.patch('tempfile.mkstemp')
        self.tempfile = self.tempfile_patched.start()
        self.tempfile.return_value = ('flag', 'file')

        self.config = parse_ini.ConfigurationSetup(name='test')

    def tearDown(self):
        self.logger_patched.stop()
        self.os_path_patched.stop()
        self.env_patched.stop()
        self.tempfile_patched.stop()

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
        self.env.return_value = '/home/TestUser'
        self.config.load_config(home=True)
        self.assertEqual(self.config.config_file, '/home/TestUser/.test.ini')

    def test_sys_config_home_ext(self):
        self.env.return_value = '/home/TestUser'
        self.config.load_config(home=True, ext='cfg')
        self.assertEqual(self.config.config_file, '/home/TestUser/.test.cfg')

    def test_sys_config_ext(self):
        self.config.load_config(ext='cfg')
        self.assertEqual(self.config.config_file, '/etc/test/test.cfg')

    def test_sys_config_path_home_ext(self):
        self.config.load_config(path='/test/test/test', home=True, ext='cfg')
        self.assertEqual(self.config.config_file, '/test/test/test/test.cfg')

    def test_sys_config_not_found(self):
        self.os_path.return_value = False
        self.assertRaises(
            SystemExit,
            self.config.load_config
        )

    def test_sys_config_find_config_success(self):
        self.os_path.return_value = True
        self.assertEqual(
            self.config._find_config('test_file'),
            'test_file'
        )

    def test_sys_config_find_config_fail(self):
        self.os_path.return_value = False
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
