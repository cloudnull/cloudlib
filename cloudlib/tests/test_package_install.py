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

import mock

from cloudlib import tests
from cloudlib import package_installer


class TestPackageInstall(unittest.TestCase):
    def setUp(self):
        self.logger_patched = mock.patch(
            'cloudlib.package_installer.logger.getLogger'
        )
        self.logger = self.logger_patched.start()
        self.logger.return_value = tests.Logger()

        self.communicate_patched = mock.patch(
            'cloudlib.package_installer.shell.ShellCommands.run_command'
        )
        self.communicate = self.communicate_patched.start()
        self.communicate.return_value = ('output', 'outcome')

        self.linux_distribution_patched = mock.patch(
            'cloudlib.package_installer.platform.linux_distribution'
        )
        self.linux_distribution = self.linux_distribution_patched.start()

        fake_packages_dict = {
            'apt': {
                'packages': [
                    'someDebianPackageName'
                ],
            },
            'yum': {
                'packages': [
                    'someRHELPackageName'
                ]
            },
            'zypper': {
                'packages': [
                    'someSUSEPackageName'
                ]
            }
        }

        self.installer = package_installer.PackageInstaller(
            packages_dict=fake_packages_dict
        )

    def tearDown(self):
        self.logger_patched.stop()
        self.communicate_patched.stop()
        self.linux_distribution_patched.stop()

    def test_distro_check_debian(self):
        self.linux_distribution.return_value = ['debian']
        self.assertEqual(package_installer.distro_check(), 'apt')

    def test_distro_check_ubuntu(self):
        self.linux_distribution.return_value = ['ubuntu']
        self.assertEqual(package_installer.distro_check(), 'apt')

    def test_distro_check_redhat(self):
        self.linux_distribution.return_value = ['redhat']
        self.assertEqual(package_installer.distro_check(), 'yum')

    def test_distro_check_centos(self):
        self.linux_distribution.return_value = ['centos']
        self.assertEqual(package_installer.distro_check(), 'yum')

    def test_distro_check_suse(self):
        self.linux_distribution.return_value = ['suse']
        self.assertEqual(package_installer.distro_check(), 'zypper')

    def test_distro_check_exception(self):
        self.linux_distribution.return_value = ['failure']
        self.assertRaises(AssertionError, package_installer.distro_check)

    def test__installer_apt_custom_install_string(self):
        self.installer.distro = 'apt'
        self.installer._installer(
            package_list=['package1', 'package2'],
            install_string='test'
        )

    def test__installer_yum_custom_install_string(self):
        self.installer.distro = 'yum'
        self.installer._installer(
            package_list=['package1', 'package2'],
            install_string='test'
        )

    def test__installer_zypper_custom_install_string(self):
        self.installer.distro = 'zypper'
        self.installer._installer(
            package_list=['package1', 'package2'],
            install_string='test'
        )

    def test__installer_apt(self):
        self.installer.distro = 'apt'
        self.installer._installer(package_list=['package1', 'package2'])

    def test__installer_yum(self):
        self.installer.distro = 'yum'
        self.installer._installer(package_list=['package1', 'package2'])

    def test__installer_zypper(self):
        self.installer.distro = 'zypper'
        self.installer._installer(package_list=['package1', 'package2'])

    def test_install_debian(self):
        self.linux_distribution.return_value = ['debian']
        self.installer.install()

    def test_install_ubuntu(self):
        self.linux_distribution.return_value = ['ubuntu']
        self.installer.install()

    def test_install_rhel(self):
        self.linux_distribution.return_value = ['redhat']
        self.installer.install()

    def test_install_centos(self):
        self.linux_distribution.return_value = ['centos']
        self.installer.install()

    def test_install_suse(self):
        self.linux_distribution.return_value = ['suse']
        self.installer.install()
