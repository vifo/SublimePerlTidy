# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import codecs
import os
import os.path
import sys
import re
import sublime
import subprocess
import tempfile


# Support Python 2.6/Python 3.x at same time with workarounds taken from
# https://pypi.python.org/pypi/six
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
    text_type = str
    binary_type = bytes
else:
    string_types = basestring,
    integer_types = (int, long)
    text_type = unicode
    binary_type = str

# Create null WindowsError exception non-Windows.
try:
    WindowsError
except NameError:
    class WindowsError(Exception):
        pass


class PerlTidyRuntimeError(Exception):

    def __init__(self, value):
        self.value = value


class PerlTidyNullLogger:

    def log(self, level, message):
        pass

    def log_level(self):
        return 0


# Convert absolute file path in Windows notation to Cygwin notation.
def cygwin_path_from_windows_path(filepath=None):
    """Returns filepath in Cygwin notation.

    Ensures, that file path given in "filepath" is absolute, and returns it in
    Cygwin notation. Raises ValueError, if "filepath" is not absolute, since
    we have no easy way to convert a relative path into a Cygwin path.

    Works on Windows only. On other platforms, always returns None.
    """

    if filepath is None or not sys.platform.startswith('win'):
        return None

    if not os.path.isabs(filepath):
        raise ValueError(
            'Argument "filepath" passed to cygwin_path_from_windows_path() must be an absolute file path')

    def repl(m):
        return '/cygdrive/{0}/{1}'.format(m.group(1).lower(), re.sub(r'\\', '/', m.group(2)))

    if re.match(r'^[A-Za-z]\:\\', filepath):
        filepath = re.sub(r'^([A-Za-z])\:\\(.*)$', repl, filepath)
        return filepath


# Find perltidy in PATH.
def find_perltidy_in_path(logger=PerlTidyNullLogger()):
    cmd = None
    perltidy_filename = 'perltidy.bat' if sublime.platform(
    ) == 'windows' else 'perltidy'

    for path in os.environ['PATH'].split(os.pathsep):
        cmd_path = os.path.join(path, perltidy_filename)
        cmd = [cmd_path]

        if is_valid_perltidy_cmd(cmd, cmd_source='path', logger=logger):
            break
        else:
            cmd = None

    return cmd


# Search for perltidy in platform default locations.
def find_perltidy_in_platform_default_paths(logger=PerlTidyNullLogger()):

    if sublime.platform() == 'windows':
        # Check for default locations of perltidy, if running under Windows
        # and using Strawberry Perl/ActivePerl or Cygwin.

        if not get_perltidy_env_flag('ignore_strawberry_perl'):
            cmd = ["C:\\Strawberry\\perl\\bin\\perl.exe",
                   "C:\\Strawberry\\perl\\site\\bin\\perltidy"]
            if is_valid_perltidy_cmd(cmd, cmd_source='platform defs', logger=logger):
                if os.path.isfile(cmd[1]):
                    return cmd

        if not get_perltidy_env_flag('ignore_activeperl_64'):
            cmd = ["C:\\Perl64\\bin\\perl.exe", "C:\\Perl64\\site\\bin\\perltidy"]
            if is_valid_perltidy_cmd(cmd, cmd_source='platform defs', logger=logger):
                if os.path.isfile(cmd[1]):
                    return cmd

        if not get_perltidy_env_flag('ignore_activeperl_32'):
            cmd = ["C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy"]
            if is_valid_perltidy_cmd(cmd, cmd_source='platform defs', logger=logger):
                if os.path.isfile(cmd[1]):
                    return cmd

        if not get_perltidy_env_flag('ignore_cygwin'):
            cmd = ["C:\\Cygwin\\bin\\perl.exe", "/usr/local/bin/perltidy"]
            if is_valid_perltidy_cmd(cmd, cmd_source='platform defs', logger=logger):
                if os.path.isfile("C:\\Cygwin\\usr\\local\\bin\\perltidy"):
                    return cmd
    else:
        # Some default locations for Unix. Should be covered by PATH already.
        for cmd in ['/usr/bin/perltidy', '/usr/local/bin/perltidy']:
            if is_valid_perltidy_cmd(cmd, cmd_source='platform defs', logger=logger):
                return cmd

    return None


# Search for perltidyrc file in given directories. Returns first perltidyrc
# path found, or None, if the given directories do not any perltidyrc files.
def find_perltidyrc_in_project(directories=[], perltidyrc_paths=[], logger=PerlTidyNullLogger()):
    perltidyrc_path = None

    if directories is None:
        directories = []
    if perltidyrc_paths is None:
        perltidyrc_paths = []

    try:
        for directory in directories:
            for perltidyrc_path in perltidyrc_paths:

                # Construct absolute path, if not absolute yet.
                perltidyrc_path = perltidyrc_path if os.path.isabs(
                    perltidyrc_path) else os.path.join(directory, perltidyrc_path)
                logger.log(2, 'Checking for perltidyrc: ' + pp(
                    perltidyrc_path))

                # Does this perltidyrc file exist?
                if os.path.isfile(perltidyrc_path):
                    logger.log(1, 'Using perltidyrc: ' + pp(perltidyrc_path))
                    raise StopIteration()
                else:
                    logger.log(2, 'File not found: ' + pp(perltidyrc_path))
                    perltidyrc_path = None
    except StopIteration:
        pass
    else:
        logger.log(2, 'No perltidyrc found in project.')

    return perltidyrc_path


# Return, whether string can be encoded in ASCII without losing information.
def is_ascii_safe_string(input):
    """Returns True, if string passed in "input" can be safely encoded in ASCII, False otherwise."""

    input_bytes = input.encode('utf-8')

    try:
        input_bytes.decode('ascii')
        return True
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        return False


# Check, if given perltidy command is valid. For now, we can only check, if
# the elements given in list cmd are valid file system objects. Returns True,
# if command appears to be valid, False otherwise.
def is_valid_perltidy_cmd(cmd, cmd_source=None, logger=PerlTidyNullLogger()):
    """Returns True, if command given in "cmd" seems to be a valid perltidy command. False otherwise.

    Validates, whether command given in "cmd" seems to be a valid perltidy
    command. Currently this will only check, whether the first element of
    "cmd" is a valid file.

    "cmd_source" specifies the source of the command, and will be used in
    diagnostic messages on the console, which will be emitted, when running
    with a log level >= 2. In addition, if "cmd_source" is "user", a warning
    will be issued, if the command is invalid.

    Returns True, if command seems to be valid, False otherwise.
    """

    if type(cmd) is list and len(cmd) > 0:
        if logger.log_level() >= 2:
            cmd_source_verbose = ' (' + cmd_source + \
                '): ' if cmd_source is not None else ': '
            logger.log(
                2, 'Checking for perltidy' + cmd_source_verbose + pp(cmd))

        if os.path.isfile(cmd[0]):
            return True

        if cmd_source == 'user':
            logger.log(0, 'Command {0} specified in user setting "perltidy_cmd" seems to be invalid. Ignoring and trying to find perltidy automatically.'.format(
                pp(cmd[0])))
        else:
            logger.log(2, 'Command not found: ' + pp(cmd[0]))

    return False


# Pretty print given string for diagnostic output.
def pp(string):
    """Return a pretty printed representation of string for debugging/logging purposes."""

    if string is None:
        return '<None>'

    tokens = []
    if type(string) is list:
        for i in string:
            tokens.append('"{0}"'.format(i))
    else:
        tokens.append('"{0}"'.format(string))

    return ' '.join(tokens)


# Tidy given region; returns True on success or False on perltidy runtime
# error.
def run_perltidy(cmd, input, logger=PerlTidyNullLogger()):
    """Run perltidy using given "cmd" and "input".

    Runs perltidy specified by "cmd" and passes data given in "input" to
    perltidy. Returns following tuple: (success, output, error_output,
    error_hints).
    """

    if type(cmd) is not list:
        raise ValueError(
            'Argument "cmd" passed to run_perltidy() must be a list')
    if not isinstance(input, string_types):
        raise ValueError(
            'Argument "input" passed to run_perltidy() must be a string')

    # Prepare arguments for subprocess call.
    subprocess_args = {
        'bufsize': -1,
        'shell': False,
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    }

    # Hide console window on Windows.
    if sublime.platform() == 'windows':
        subprocess_args['startupinfo'] = subprocess.STARTUPINFO()
        subprocess_args[
            'startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW

    cmd_final = []
    cmd_final.extend(cmd)

    # Ensure, that perltidy always returns LF line endings, so we match the
    # internal buffer line endings.
    cmd_final.append('-ole=unix')

    # Check, if the data to be tidied has any non-ASCII characters. If yes,
    # prepare temporary files for input and output with UTF-8 encoding, and
    # spool the input to file. Adjust perltidy call, so data will be read and
    # written from/to temporary files.
    use_temporary_files = False

    if is_ascii_safe_string(input):
        input = input.encode('ascii')       # convert input from str to bytes
    else:
        use_temporary_files = True

    if use_temporary_files:
        # Create temporary files for input/output and reopen them with
        # codecs.open, so we can specify an encoding for the files. At least
        # with Python 2.6, there seems to be no other option.
        perltidy_input_fh, perltidy_input_filepath = tempfile.mkstemp()
        perltidy_output_fh, perltidy_output_filepath = tempfile.mkstemp()
        os.close(perltidy_input_fh)
        os.close(perltidy_output_fh)

        with codecs.open(perltidy_input_filepath, 'w+b', encoding='utf-8') as fh:
            fh.write(input)
        input = None

        cmd_final.append('-nst')
        cmd_final.append(perltidy_input_filepath)
        cmd_final.append('-o=' + perltidy_output_filepath)

    # Show time!
    success, output, error_output, error_hints = False, None, None, []
    logger.log(1, 'Running command: ' + pp(cmd_final))

    orig_cygwin_environ = None
    orig_lang_environ = None

    try:
        # On Windows, ensure, that we have CYGWIN environment variables set,
        # even if we don't known, whether we actually are using Cygwin.
        if sublime.platform() == 'windows':
            if 'CYGWIN' in os.environ and not re.match(r'\bnodosfilewarning\b', os.environ['CYGWIN']):
                orig_cygwin_environ = os.environ['CYGWIN']
                os.environ['CYGWIN'] += ' nodosfilewarning'
            else:
                os.environ['CYGWIN'] = 'nodosfilewarning'

            if 'LANG' in os.environ:
                orig_lang_environ = os.environ['LANG']
            os.environ['LANG'] = 'C'

        p = subprocess.Popen(cmd_final, **subprocess_args)

        output, error_output = p.communicate(input)
        logger.log(2, 'Command exited with code: {0}'.format(p.returncode))

        # If we're using temporary files for I/O, load output from output file
        # and cleanup temporary files. Otherwise decode pipe output from bytes
        # to str.
        if use_temporary_files:
            with codecs.open(perltidy_output_filepath, 'rb', encoding='utf-8') as fh:
                output = fh.read()
        else:
            output = output.decode('utf-8')

        # Decode error output (if any), otherwise clear it and set success.
        if error_output:
            error_output = error_output.decode('utf-8')
        else:
            success = True
            error_output = ''

    # Handle OS errors. Check, if we can give the user some hints.
    except (WindowsError, EnvironmentError) as e:
        logger.log(0, 'Unable to run perltidy: ' + pp(cmd_final))
        logger.log(0, 'Error was: ' + repr(e))

        hints = []

        # Check current error and give user some hints about error reason
        if sublime.platform() == 'windows' and type(e) is exceptions.WindowsError and e.winerror == 193 and os.path.basename(cmd_final[0]) == 'perltidy':
            # bad exe format
            hints.append(
                'Maybe you have specified the path to "perltidy" instead of ' +
                '"perltidy.bat" in your "perltidy_cmd"?')

        if len(hints) == 0:
            if logger.log_level() < 2:
                hints.append(
                    'Try to increase PerlTidy log level via user setting ' +
                    '"perltidy_log_level" and try again.')

    finally:
        # Cleanup.
        if use_temporary_files and not get_perltidy_env_flag('keep_temp_files'):
            os.unlink(perltidy_input_filepath)
            os.unlink(perltidy_output_filepath)

        if sublime.platform() == 'windows':

            # Restore environment variables.
            if orig_cygwin_environ is None:
                del os.environ['CYGWIN']
            else:
                os.environ['CYGWIN'] = orig_cygwin_environ

            if orig_lang_environ is None:
                del os.environ['LANG']
            else:
                os.environ['LANG'] = orig_lang_environ

    return success, output, error_output, error_hints


# Returns given PerlTidy environment flag. Used for test suite support.
def get_perltidy_env_flag(key):
    """Returns given PerlTidy environment flag. Used for test suite support."""

    key = 'PERLTIDY_TEST_' + key.upper()
    if key in os.environ and os.environ[key] == "1":
        return True
    else:
        return False


# Sets given PerlTidy environment flag. Used for test suite support.
def set_perltidy_env_flag(key, value=None):
    """Sets given PerlTidy environment flag. Used for test suite support."""

    key = 'PERLTIDY_TEST_' + key.upper()

    if value is None:
        if key in os.environ:
            del os.environ[key]
        return
    else:
        os.environ[key] = "1" if value else "0"
