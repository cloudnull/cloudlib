# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

import sys
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
