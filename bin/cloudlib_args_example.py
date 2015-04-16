#!/usr/bin/env python
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


a = arguments.ArgumentParserator(
    arguments_dict=args, epilog='testing epilog', title='testing title',
    detail='testing detail', description='testing description'
)

print a.arg_parser()
import sys
print sys.argv