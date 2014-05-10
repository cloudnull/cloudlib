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

from cloudlib import arguments


class TestArgumentClassVars(unittest.TestCase):
    def setUp(self):
        self.args = {}

    def test_class_variables(self):
        self.arguments = arguments.ArgumentParserator(
            arguments_dict=self.args,
            env_name='test_args',
            epilog='epilog',
            title='title',
            detail='detail',
            description='description'
        )
        self.assertEqual(self.arguments.usage, '%(prog)s')
        self.assertEqual(self.arguments.env_name, 'test_args')
        self.assertEqual(self.arguments.epilog, 'epilog')
        self.assertEqual(self.arguments.title, 'title')
        self.assertEqual(self.arguments.detail, 'detail')
        self.assertEqual(self.arguments.description, 'description')


class TestArguments(unittest.TestCase):
    def setUp(self):
        self.sys_argv_original = arguments.argparse._sys.argv
        self.sys_argv = arguments.argparse._sys.argv = []
        self.print_patched = mock.patch(
            'cloudlib.arguments.argparse._sys.stderr'
        )
        self.mock_open = self.print_patched.start()

        self.args = {
            'optional_args': {
                'option1': {
                    'commands': ['--base-option1'],
                    'help': 'Helpful Information'
                }
            },
            'positional_args': {
                'possitional1': {
                    'help': 'Helpful Information',
                }
            },
            'subparsed_args': {
                'subparsed1': {
                    'help': 'Helpful Information',
                    'optional_args': {
                        'mutually_exclusive': {
                            'some_value': [
                                'option1',
                                'option2'
                            ]
                        },
                        'option1': {
                            'commands': ['--option1'],
                            'default': False,
                            'action': 'store_true',
                            'help': 'Helpful Information'
                        },
                        'option2': {
                            'commands': ['--option2'],
                            'default': False,
                            'action': 'store_true',
                            'help': 'Helpful Information'
                        },
                        'other_option3': {
                            'commands': ['--other-option3', '-O'],
                            'metavar': '[STRING]',
                            'type': str,
                            'help': 'Helpful Information'
                        }
                    }
                }
            }
        }
        self.arguments = arguments.ArgumentParserator(
            arguments_dict=self.args,
            env_name='test_args',
            epilog='epilog',
            title='title',
            detail='detail',
            description='description'
        )

    def tearDown(self):
        arguments.argparse._sys.argv = self.sys_argv_original
        self.print_patched.stop()

    def test_arg_parser_simple(self):
        arguments.argparse._sys.argv = ['app', 'subparsed1', 'testval1']
        self.assertTrue(isinstance(self.arguments.arg_parser(), dict))

    def test_arg_parser_options_simple(self):
        arguments.argparse._sys.argv = [
            'app', '--base-option1', 'testval1', 'subparsed1', 'testval2'
        ]
        self.assertTrue(isinstance(self.arguments.arg_parser(), dict))

    def test_arg_parser_options_simple_options(self):
        arguments.argparse._sys.argv = [
            'app', '--base-option1', 'testval1', 'subparsed1', '--option1',
            'testval2'
        ]
        self.assertTrue(isinstance(self.arguments.arg_parser(), dict))

    def test_arg_parser_options_simple_options_multual_exclusive(self):
        arguments.argparse._sys.argv = [
            'app', '--base-option1', 'testval1', 'subparsed1',
            '--option1', '--option2', 'testval2'
        ]
        self.assertRaises(SystemExit, self.arguments.arg_parser)

    def test_arg_parser_options_simple_more_options(self):
        arguments.argparse._sys.argv = [
            'app', '--base-option1', 'testval1', 'subparsed1',
            '--option1', '--other-option3', 'testval3', 'testval2'
        ]
        self.assertTrue(isinstance(self.arguments.arg_parser(), dict))

    def test__setup_parser(self):
        arguments.argparse._sys.argv = ['app', 'subparsed1', 'testval1']
        setup = self.arguments._setup_parser()
        parser, subparser, rargs = setup

        self.assertTrue(isinstance(setup, tuple))
        self.assertTrue(isinstance(parser, arguments.argparse.ArgumentParser))
        self.assertTrue(
            isinstance(subparser, arguments.argparse._SubParsersAction)
        )
        self.assertTrue(isinstance(rargs, list))

    def test__add_opt_argument(self):
        arguments.argparse._sys.argv = ['app', 'subparsed1', 'testval1']
        setup = self.arguments._setup_parser()
        parser, subparser, rargs = setup
        op_args = {
            'option1': {
                'commands': ['--base-option1'],
                'help': 'Helpful Information'
            }
        }
        self.arguments._add_opt_argument(op_args, parser)
