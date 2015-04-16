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
import requests

from cloudlib import http
from cloudlib import tests


class TestHttpMakeRequest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://example.com'

        self.logger_patched = mock.patch('cloudlib.http.logger.getLogger')
        self.logger = self.logger_patched.start()
        self.logger.return_value = tests.Logger()

        self.make_req = http.MakeRequest()
        self.fakehttp = tests.FakeHttp()

    def tearDown(self):
        self.logger_patched.stop()

    def test_custom_headers(self):
        test_headers = {'X-Test-Header': 'TEST'}
        base_headers = self.make_req.headers
        base_headers.update(test_headers)

        config = {'headers': test_headers}
        make_request = http.MakeRequest(config=config)
        self.assertEqual(base_headers, make_request.headers)

    def test_enable_debug(self):
        config = {'debug': True}
        http.MakeRequest(config=config)
        debug_level = http.httplib.HTTPConnection.debuglevel
        self.assertEqual(1, debug_level)
        http.httplib.HTTPConnection.debuglevel = 0

    def test_timeout_set(self):
        config = {'timeout': 120}
        make_request = http.MakeRequest(config=config)
        timeout = make_request.request_kwargs['timeout']
        self.assertEqual(config['timeout'], timeout)

    def test_report_error(self):
        self.assertRaises(
            requests.RequestException,
            self.make_req._report_error,
            'TEST',
            'Failure'
        )

    def test_get_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.get = self.fakehttp.get
            resp = self.make_req.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_get_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.get = self.fakehttp.get
            resp = self.make_req.get(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_get_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.get = self.fakehttp.get
            resp = self.make_req.get(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_head_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.head = self.fakehttp.head
            resp = self.make_req.head(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_head_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.head = self.fakehttp.head
            resp = self.make_req.head(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_head_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.head = self.fakehttp.head
            resp = self.make_req.head(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_put_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.put = self.fakehttp.put
            resp = self.make_req.put(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_put_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.put = self.fakehttp.put
            resp = self.make_req.put(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_put_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.put = self.fakehttp.put
            resp = self.make_req.put(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_put_request_body(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.put = self.fakehttp.put
            resp = self.make_req.put(self.url, body='TestBody')
        self.assertEqual(resp.status_code, 200)

    def test_delete_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.delete = self.fakehttp.delete
            resp = self.make_req.delete(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_delete_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.delete = self.fakehttp.delete
            resp = self.make_req.delete(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_delete_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.delete = self.fakehttp.delete
            resp = self.make_req.delete(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_post_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.post = self.fakehttp.post
            resp = self.make_req.post(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_post_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.post = self.fakehttp.post
            resp = self.make_req.post(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_post_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.post = self.fakehttp.post
            resp = self.make_req.post(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_post_request_body(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.post = self.fakehttp.post
            resp = self.make_req.post(self.url, body='TestBody')
        self.assertEqual(resp.status_code, 200)

    def test_patch_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.patch = self.fakehttp.patch
            resp = self.make_req.patch(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_patch_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.patch = self.fakehttp.patch
            resp = self.make_req.patch(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_patch_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.patch = self.fakehttp.patch
            resp = self.make_req.patch(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_patch_request_body(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.patch = self.fakehttp.patch
            resp = self.make_req.patch(self.url, body='TestBody')
        self.assertEqual(resp.status_code, 200)

    def test_option_request(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.option = self.fakehttp.option
            resp = self.make_req.option(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_option_request_headers(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.option = self.fakehttp.option
            resp = self.make_req.option(self.url, headers={'test1': 'test1'})
        self.assertEqual(resp.status_code, 200)

    def test_option_request_kwargs(self):
        with mock.patch('cloudlib.http.requests') as mock_request:
            mock_request.option = self.fakehttp.option
            resp = self.make_req.option(self.url, kwargs={'timeout': 1})
        self.assertEqual(resp.status_code, 200)

    def test_request_failure(self):
        self.assertRaises(
            requests.RequestException,
            self.make_req._request,
            'BadMethod',
            self.url
        )

    def test_parse_url_double_slash_url(self):
        url = http.parse_url('//example.com')
        self.assertEqual(type(url), http.urlparse.ParseResult)
        self.assertEqual(url.scheme, 'http')

    def test_parse_url_http_url(self):
        url = http.parse_url('http://example.com')
        self.assertEqual(type(url), http.urlparse.ParseResult)
        self.assertEqual(url.scheme, 'http')

    def test_parse_url_https_url(self):
        url = http.parse_url('https://example.com')
        self.assertEqual(type(url), http.urlparse.ParseResult)
        self.assertEqual(url.scheme, 'https')

    def test_html_encode_url(self):
        test_path = 'this%20is%20a%20test'
        url = http.html_encode(path='this is a test')
        self.assertEqual(url, test_path)
