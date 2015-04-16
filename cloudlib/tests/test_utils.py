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

import unittest

from cloudlib import utils


class TestBasicUtils(unittest.TestCase):
    def test_is_int_is_int(self):
        self.assertTrue(isinstance(utils.is_int(value=1), int))

    def test_is_int_is_str(self):
        self.assertTrue(isinstance(utils.is_int(value='string'), str))

    def test_ensure_string_unicode(self):
        self.assertTrue(isinstance(utils.ensure_string(obj=u'test'), str))

    def test_ensure_string_str(self):
        self.assertTrue(isinstance(utils.ensure_string(obj='test'), str))

    def test_ensure_dict_update(self):
        test = {'test': 'value'}
        test_update = {'other': 'value'}
        return_dict = utils.dict_update(
            base_dict=test, update_dict=test_update
        )
        self.assertEqual(return_dict, {'test': 'value', 'other': 'value'})
