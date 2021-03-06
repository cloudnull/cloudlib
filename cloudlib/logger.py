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

"""Example Usage:
>>> from cloudlib import logger
>>> log = logger.LogSetup()
>>> log.default_logger(name='test_logger')

>>> # The following can then be placed in any module that you like
>>> # Just use the name of the logger you created
>>> from cloudlib import logger
>>> LOG = logger.getLogger(name='test_logger')
>>> LOG.info('This is a test message')
"""

import logging
import os
import platform
import getpass
import sys

from logging import handlers

from cloudlib import utils


# This creates a colorized log message if the colorized option is set.
class ColorLogRecord(logging.LogRecord):
    def __init__(self, *args):
        super(ColorLogRecord, self).__init__(*args)

    def getMessage(self):
        """Returns a colorized log message based on the log level.

        If the platform is windows the original message will be returned
        without colorization windows escape codes are crazy.

        :returns: ``str``
        """
        msg = str(self.msg)
        if self.args:
            msg = msg % self.args

        if platform.system().lower() == 'windows' or self.levelno < 10:
            return msg
        elif self.levelno >= 50:
            return utils.return_colorized(msg, 'critical')
        elif self.levelno >= 40:
            return utils.return_colorized(msg, 'error')
        elif self.levelno >= 30:
            return utils.return_colorized(msg, 'warn')
        elif self.levelno >= 20:
            return utils.return_colorized(msg, 'info')
        else:
            return utils.return_colorized(msg, 'debug')


def getLogger(name):
    """Return a logger from a given name.

    If the name does not have a log handler, this will create one for it based
    on the module name which will log everything to a log file in a location
    the executing user will have access to.

    :param name: ``str``
    :return: ``object``
    """
    log = logging.getLogger(name=name)
    for handler in log.handlers:
        if name == handler.name:
            return log
    else:
        return LogSetup().default_logger(name=name.split('.')[0])


class LogSetup(object):

    def __init__(self, max_size=500, max_backup=5, debug_logging=False,
                 colorized_messages=False):
        """Setup Logging.

        :param max_size: ``int``
        :param max_backup: ``int``
        :param debug_logging: ``bol``
        :param colorized_messages: ``bol``
        """
        self.max_size = (max_size * 1024 * 1024)
        self.max_backup = max_backup
        self.debug_logging = debug_logging
        self.format = None
        self.name = None
        if colorized_messages:
            logging._logRecordFactory = ColorLogRecord

    def default_logger(self, name=__name__, enable_stream=False,
                       enable_file=True):
        """Default Logger.

        This is set to use a rotating File handler and a stream handler.
        If you use this logger all logged output that is INFO and above will
        be logged, unless debug_logging is set then everything is logged.
        The logger will send the same data to a stdout as it does to the
        specified log file.

        You can disable the default handlers by setting either `enable_file` or
        `enable_stream` to `False`

        :param name: ``str``
        :param enable_stream: ``bol``
        :param enable_file: ``bol``
        :return: ``object``
        """
        if self.format is None:
            self.format = logging.Formatter(
                '%(asctime)s - %(module)s:%(levelname)s => %(message)s'
            )

        log = logging.getLogger(name)
        self.name = name

        if enable_file is True:
            file_handler = handlers.RotatingFileHandler(
                filename=self.return_logfile(filename='%s.log' % name),
                maxBytes=self.max_size,
                backupCount=self.max_backup
            )
            self.set_handler(log, handler=file_handler)

        if enable_stream is True or self.debug_logging is True:
            stream_handler = logging.StreamHandler()
            self.set_handler(log, handler=stream_handler)

        log.info('Logger [ %s ] loaded', name)
        return log

    def set_handler(self, log, handler):
        """Set the logging level as well as the handlers.

        :param log: ``object``
        :param handler: ``object``
        """
        if self.debug_logging is True:
            log.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)

        handler.name = self.name
        handler.setFormatter(self.format)
        log.addHandler(handler)

    @staticmethod
    def return_logfile(filename, log_dir='/var/log'):
        """Return a path for logging file.

        If ``log_dir`` exists and the userID is 0 the log file will be written
        to the provided log directory. If the UserID is not 0 or log_dir does
        not exist the log file will be written to the users home folder.

        :param filename: ``str``
        :param log_dir: ``str``
        :return: ``str``
        """
        if sys.platform == 'win32':
            user = getpass.getuser()
        else:
            user = os.getuid()
        home = os.path.expanduser('~')

        if not os.path.isdir(log_dir):
            return os.path.join(home, filename)

        log_dir_stat = os.stat(log_dir)
        if log_dir_stat.st_uid == user:
            return os.path.join(log_dir, filename)
        elif log_dir_stat.st_gid == user:
            return os.path.join(log_dir, filename)
        else:
            return os.path.join(home, filename)