# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


def test_Exception_exception():
    """Raise Exception exception."""
    raise Exception('Test Exception')


class FakeSmtp(object):
    """Setup a FAKE SMTP request."""
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.enabled_debug = False
        self.using_starttls = False
        self.logged_in = False
        self.mail_sent = False
        self.make_quit = False
        self.key = None
        self.cert = None
        self.message = None

    def set_debuglevel(self, *args, **kwargs):
        self.enabled_debug = True

    def starttls(self, key=None, cert=None):
        self.key = key
        self.cert = cert
        self.using_starttls = True

    def login(self, *args, **kwargs):
        self.logged_in = True

    def sendmail(self, *args, **kwargs):
        self.mail_sent = True
        self.message = kwargs

    def quit(self, *args, **kwargs):
        self.make_quit = True


class Handlers(object):
    def __init__(self, filename=None, maxBytes=None, backupCount=None):
        self.filename = filename
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def setLevel(self, *args):
        pass

    def setFormatter(self, *args):
        pass


def returnstring(fmt=None, datefmt=None):
    if fmt is not None and datefmt is not None:
        return fmt, datefmt
    elif fmt is not None:
        return fmt
    elif datefmt is not None:
        return datefmt


class Logger(object):
    def __init__(self, name=None):
        self.name = name
        self.debug = self._debug
        self.info = self._info
        self.error = self._error
        self.warn = self._warn
        self.fatal = self._fatal
        self.handlers = []

    def addHandler(self, handler):
        self.handlers.append(handler)

    def setLevel(self, *args):
        pass

    def _check(self, *args):
        if not args[0]:
            raise AttributeError('Nothing passed to logger')

    def _debug(self, *args):
        return self._check(*args)

    def _info(self, *args):
        return self._check(*args)

    def _error(self, *args):
        return self._check(*args)

    def _warn(self, *args):
        return self._check(*args)

    def _fatal(self, *args):
        return self._check(*args)


class FakeHttpResponse(object):
    def __init__(self, *args, **kwargs):
        """Accept user input and return a response for HTTP."""
        self.content = 'testbody'
        self.status_code = 200
        self.reason = 'OK'
        self.headers = {'test-headers': 'test'}
        self.response = 'response'
        self.request = 'FakeRequest'


class FakeHttp(object):
    """Setup a FAKE http request."""
    def get(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def put(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def post(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def head(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)

    def option(self, *args, **kwargs):
        return FakeHttpResponse(*args, **kwargs)


class ParseResult(object):
    scheme = 'https'
    netloc = 'TEST.url'
    path = '/v2.0/tokens'
    params = ''
    query = ''
    fragment = ''


class StatResult(object):
    st_mode = 33152
    st_ino = 1698903
    st_dev = 16777220
    st_nlink = 1
    st_uid = 100
    st_gid = 100
    st_size = 2230944256
    st_atime = 1396506114
    st_mtime = 1396506114
    st_ctime = 1396506114


CONFIG_FILE = """
[default]
true_value = True
false_value = False
string_value = string
integer_value = 1

[other_section]
true_value = True
false_value = False
string_value = string
integer_value = 1
"""


class FakePopen(object):
    """Fake Shell Commands."""
    def __init__(self, return_code=0, *args, **kwargs):
        self.returncode = return_code

    @staticmethod
    def communicate():
        return 'stdout', 'stderr'
