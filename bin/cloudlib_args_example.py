#!/usr/bin/env python
# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

import os
import sys

possible_topdir = os.path.normpath(
    os.path.join(os.path.abspath(os.getcwd()), os.pardir)
)

if os.path.exists(os.path.join(possible_topdir, 'cloudlib', '__init__.py')):
    sys.path.insert(0, possible_topdir)


from cloudlib import arguments

args = {
    'optional_args': {
        'option1': {
            'commands': ['--option1'],
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
            'title': 'SubParser Title',
            'metavar': 'SubParser Information',
            'help': 'Helpful Information',
            'subparsed_args': {
                'nested_subparsed1': {
                    'title': 'NestedSubParser Title',
                    'metavar': 'NestedSubParser Information',
                    'help': 'Helpful Information',
                    'option1': {
                        'commands': ['--option1'],
                        'default': False,
                        'action': 'store_true',
                        'help': 'Helpful Information'
                    }
                }
            },
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


a = arguments.ArgumentParserator(
    arguments_dict=args, epilog='testing epilog', title='testing title',
    detail='testing detail', description='testing description'
)

print a.arg_parser()
import sys
print sys.argv