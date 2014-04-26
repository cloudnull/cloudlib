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

import cloudlib

from cloudlib.messaging import mail
from cloudlib import tests


class TestMessagingMail(unittest.TestCase):
    def setUp(self):
        mail.smtplib.SMTP = mock.Mock(side_effect=tests.FakeSmtp)
        self.mail = mail.Mailer

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
        mail.smtplib.SMTP = mock.Mock(side_effect=tests.FakeSmtp)
        mail.text.MIMEText = mock.Mock(
            side_effect=Exception('Fail Test')
        )
        self.mail = mail.Mailer

    def test_smtp_send_exception(self):
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
