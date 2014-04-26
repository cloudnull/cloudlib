# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
"""Example Usage:

>>> # In your shell create a file named .example.ini in your home folder
>>> # dd sections to the file IE:
>>> # [default]
>>> # key = value

>>> config = ConfigurationSetup(name='example')
>>> default_args = config.config_args(section='default')
>>> print(default_args)
... {'key': 'value'}
"""

import ConfigParser
import logging
import os
import stat
import sys

from cloudlib.utils import basic


class ConfigurationSetup(object):

    def __init__(self, name, log_name=__name__):
        """Parse values in a given configuration file.

        :param name: ``str``
        :param log_name: ``str`` This is used to log against an existing log
                                 handler.
        """
        self.log = logging.getLogger(log_name)
        self.name = name
        self.config_file = None
        self.filename = None

    def load_config(self, path=None, home=False, ext='ini'):
        """Return the full path to a configuration file.

        This will look for configuration files in the ``full_path``, in
        the users home folder, or in a config directory in "/etc".  If you set
        `home=True`, the system will look for a "hidden" configuration file in
        the executing users $HOME folder.

        The precedence is as follows:
            full_path/name.ini
            /home/$USER/.name.ini
            /etc/name/name.ini

        :param path: ``str``
        :param home: ``bol``
        :param ext: ``str``
        :return: ``str``
        """

        opj = os.path.join

        self.filename = '%s.%s' % (self.name, ext)

        if path is not None:
            self.config_file = self._find_config(
                config_file=opj(path.rstrip(os.sep), self.filename)
            )
        elif home is True:
            self.config_file = self._find_config(
                config_file=opj(os.getenv('HOME'), '.%s' % self.filename)
            )
        else:
            self.config_file = self._find_config(
                config_file=opj('/etc', self.name, self.filename)
            )

    def _find_config(self, config_file):
        """Return the full path to a known configuration file.

        This method will check if the configuration file "exist", if it does
        NOT then the method will bail calling the system to Exit.

        :return: ``str``
        """
        if os.path.exists(config_file):
            return config_file
        else:
            msg = (
                'Configuration file [ %s ] was not found.' % self.filename
            )
            self.log.fatal(msg)
            raise SystemExit(msg)

    def check_perms(self, perms='0600,0400'):
        """Check and enforce the permissions of the config file.

        Enforce permission on a provided configuration file. This will check
        and see if the permission are set based on the permission octet as
        set in the ``perms`` value. ``perms`` is a comma separated list
        of acceptable perms in octal form. Defaults permissions to, 0600 and
        0400.

        :param perms: ``str``
        """
        confpath = os.path.realpath(self.config_file)
        mode = oct(stat.S_IMODE(os.stat(confpath).st_mode))
        if not any([mode == i for i in perms.split(',')]):
            msg = (
                'To use a configuration file the permissions'
                ' need to be any of the following "%s"' % perms
            )
            self.log.fatal(msg)
            raise SystemExit(msg)
        else:
            self.log.info(
                'Configuration file [ %s ] has been loaded',
                self.config_file
            )
            return True

    def config_args(self, section='default'):
        """Loop through the configuration file and set all of our values.

        Note:
          that anything can be set as a "section" in the argument file. If a
          section does not exist an empty dict will be returned.


        :param section: ``str``
        :return: ``dict``
        """
        if sys.version_info >= (2, 7, 0):
            parser = ConfigParser.SafeConfigParser(allow_no_value=True)
        else:
            parser = ConfigParser.SafeConfigParser()

        # Set to preserve Case
        parser.optionxform = str
        args = {}
        try:
            parser.read(self.config_file)
            for name, value in parser.items(section):
                name = name.encode('utf8')
                if any([value == 'False', value == 'false']):
                    value = False
                elif any([value == 'True', value == 'true']):
                    value = True
                else:
                    value = basic.is_int(value=value)
                args[name] = value
        except Exception as exp:
            self.log.error(
                'Failure Reading the configuration file section [ %s ].'
                ' Error: %s', section, exp
            )
            return {}
        else:
            return args