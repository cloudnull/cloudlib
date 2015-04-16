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

import cloudlib
from cloudlib import tests, mail


class TestMessagingMail(unittest.TestCase):
    def setUp(self):
        self.logger_patched = mock.patch('cloudlib.mail.logger.getLogger')
        self.logger = self.logger_patched.start()
        self.logger.return_value = tests.Logger()

        self.mail_smtp_patched = mock.patch('cloudlib.mail.smtplib.SMTP')
        self.mail_smtp = self.mail_smtp_patched.start()
        self.mail_smtp.side_effect = tests.FakeSmtp

        self.mail = mail.Mailer

    def tearDown(self):
        self.logger_patched.stop()
        self.mail_smtp_patched.stop()

    def test_no_config(self):
        self.assertRaises(cloudlib.MissingConfig, self.mail, None)

    def test_no_missing_values(self):
        self.assertRaises(cloudlib.MissingConfigValue, self.mail, {})

    def test_no_missing_port(self):
        config = {'mail_url': 'test'}
        self.assertRaises(cloudlib.MissingConfigValue, self.mail, config)

    def test_no_missing_url(self):
        config = {'mail_port': 9000}
        self.assertRaises(cloudlib.MissingConfigValue, self.mail, config)

    def test_smtp_debug(self):
        config = {'mail_port': 9000, 'mail_url': 'test', 'debug': True}
        mailer = self.mail(config)
        self.assertTrue(mailer.smtp.url == 'test')
        self.assertTrue(mailer.smtp.port == 9000)
        self.assertTrue(mailer.smtp.starttls)
        self.assertTrue(mailer.smtp.key is None)
        self.assertTrue(mailer.smtp.cert is None)
        self.assertFalse(mailer.smtp.logged_in)

    def test_smtp_login_debug(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test',
            'debug': True,
            'mail_username': 'test',
            'mail_password': 'test_password'
        }

        mailer = self.mail(config)
        self.assertTrue(mailer.smtp.url == 'test')
        self.assertTrue(mailer.smtp.port == 9000)
        self.assertTrue(mailer.smtp.starttls)
        self.assertTrue(mailer.smtp.key is None)
        self.assertTrue(mailer.smtp.cert is None)
        self.assertTrue(mailer.smtp.set_debuglevel)
        self.assertTrue(mailer.smtp.login)

    def test_smtp_login_debug_ssl(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test',
            'debug': True,
            'mail_username': 'test',
            'mail_password': 'test_password',
            'mail_key': 'test_key_file',
            'mail_cert': 'test_cert_file'
        }

        mailer = self.mail(config)
        self.assertTrue(mailer.smtp.url == 'test')
        self.assertTrue(mailer.smtp.port == 9000)
        self.assertTrue(mailer.smtp.starttls)
        self.assertEqual(mailer.smtp.key, 'test_key_file')
        self.assertEqual(mailer.smtp.cert, 'test_cert_file')
        self.assertTrue(mailer.smtp.set_debuglevel)
        self.assertTrue(mailer.smtp.login)

    def test_smtp(self):
        config = {'mail_port': 9000, 'mail_url': 'test'}

        mailer = self.mail(config)
        self.assertTrue(mailer.smtp.url is not None)
        self.assertTrue(mailer.smtp.port is not None)
        self.assertTrue(mailer.smtp.starttls)
        self.assertEqual(mailer.smtp.key, None)
        self.assertEqual(mailer.smtp.cert, None)

    def test_smtp_login(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test',
            'debug': False,
            'mail_username': 'test',
            'mail_password': 'test_password'
        }

        mailer = self.mail(config)
        self.assertTrue(mailer.smtp)
        self.assertTrue(mailer.smtp.starttls)
        self.assertTrue(mailer.smtp.set_debuglevel)
        self.assertTrue(mailer.smtp.login)

    def test_smtp_login_ssl(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test',
            'mail_username': 'test',
            'mail_password': 'test_password',
            'mail_key': 'test_key_file',
            'mail_cert': 'test_cert_file'
        }

        mailer = self.mail(config)
        self.assertTrue(mailer.smtp.url == 'test')
        self.assertTrue(mailer.smtp.port == 9000)
        self.assertTrue(mailer.smtp.starttls)
        self.assertEqual(mailer.smtp.key, 'test_key_file')
        self.assertEqual(mailer.smtp.cert, 'test_cert_file')
        self.assertTrue(mailer.smtp.set_debuglevel)
        self.assertTrue(mailer.smtp.login)

    def test_smtp_send(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test'
        }
        mailer = self.mail(config)

        mailer_kwargs = {
            'send_to': 'send_to@test',
            'from_who': 'from_who@test',
            'subject': 'test subject',
            'message': 'test nessage'
        }
        mailer.send(**mailer_kwargs)

        self.assertEqual(mailer.smtp.message['from_addr'], 'from_who@test')
        self.assertEqual(mailer.smtp.message['to_addrs'], 'send_to@test')
        self.assertTrue(isinstance(mailer.smtp.message['msg'], str))
        self.assertTrue(
            'Reply-To: from_who@test' in mailer.smtp.message['msg']
        )
        self.assertTrue(mailer.smtp.make_quit)

    def test_smtp_send_reply(self):
        config = {
            'mail_port': 9000,
            'mail_url': 'test'
        }
        mailer = self.mail(config)

        mailer_kwargs = {
            'send_to': 'send_to@test',
            'from_who': 'from_who@test',
            'subject': 'test subject',
            'message': 'test nessage',
            'reply_to': 'reply_to@test'
        }
        mailer.send(**mailer_kwargs)

        self.assertEqual(mailer.smtp.message['from_addr'], 'from_who@test')
        self.assertEqual(mailer.smtp.message['to_addrs'], 'send_to@test')
        self.assertTrue(isinstance(mailer.smtp.message['msg'], str))
        self.assertTrue(
            'Reply-To: reply_to@test' in mailer.smtp.message['msg']
        )
        self.assertTrue(mailer.smtp.make_quit)


class TestMessagingMailException(unittest.TestCase):
    def setUp(self):

        self.mail_smtp_patched = mock.patch('cloudlib.mail.smtplib.SMTP')
        self.mail_smtp = self.mail_smtp_patched.start()
        self.mail_smtp.side_effect = tests.FakeSmtp

        self.mail_mime_patched = mock.patch('cloudlib.mail.text.MIMEText')
        self.mail_mimetype = self.mail_mime_patched.start()

        self.mail = mail.Mailer

    def tearDown(self):
        self.mail_mime_patched.stop()
        self.mail_smtp_patched.stop()

    def test_smtp_send_exception(self):
        self.mail_mimetype.side_effect = Exception('Fail Test')
        config = {
            'mail_port': 9000,
            'mail_url': 'test'
        }
        mailer = self.mail(config)

        mailer_kwargs = {
            'send_to': 'send_to@test',
            'from_who': 'from_who@test',
            'subject': 'test subject',
            'message': 'test nessage',
            'reply_to': 'reply_to@test'
        }

        self.assertRaises(
            cloudlib.MessageFailure, mailer.send, **mailer_kwargs
        )
        self.assertTrue(mailer.smtp.make_quit)

