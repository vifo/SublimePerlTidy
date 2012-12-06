# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import subprocess
import os
import os.path
import tempfile
import codecs
import exceptions

# PerlTidy for Sublime Text 2
#   rbo@cpan.org

DEFAULT_SETTINGS = {
    'perltidy_enabled': True,
    'perltidy_log_level': 0,
    'perltidy_options': ['-sbl', '-bbt=1', '-pt=2', '-nbbc', '-l=100', '-ole=unix', '-w', '-se'],
    'perltidy_rc_paths': ['.perltidyrc', 'perltidyrc'],
}


class PerlTidyRuntimeError(Exception):
    def __init__(self, value):
        self.value = value


class PerlTidyCommand(sublime_plugin.TextCommand):

    _callbacks_registered = False
    _perltidy_cmd = None
    _perltidy_log_level = None
    _perltidy_options = None
    _perltidy_rc_paths = None

    def run(self, edit):
        self.register_callbacks()
        self.load_settings()

        # Bailout, if we don't have a valid perltidy command to run.
        if not self.find_perltidy():
            sublime.error_message(
                'PerlTidy: Cannot find perltidy in any directory given in environment variable ' +
                'PATH, nor in platform specific default locations. Please setup your environment ' +
                'variable PATH, so it contains perltidy, or specify perltidy location in user ' +
                'setting "perltidy_cmd". Please refer to documentation at ' +
                'https://github.com/rbo/st2-perltidy for details.')
            return

        # Check, if we have any non-empty regions and tidy them.
        regions_tidied = 0
        for region in self.view.sel():
            if not region.empty():
                regions_tidied += 1
                self.tidy_region(edit, region)

        # If no regions have been tidied so far, go ahead and tidy entire
        # view. Reposition cursor after tidying up.
        if regions_tidied == 0:
            cursor_pos = self.view.sel()[0]
            if self.tidy_region(edit, sublime.Region(0L, self.view.size())):
                if cursor_pos.empty():
                    self.view.sel().add(cursor_pos)
                    if len(self.view.sel()) > 1:
                        self.view.sel().subtract(self.view.sel()[1])
                    self.view.show_at_center(self.view.sel()[0].begin())

    # Report to Sublime Text 2 whether PerlTidy is enabled, or not.
    def is_enabled(self):
        return self.view.settings().get('perltidy_enabled', DEFAULT_SETTINGS['perltidy_enabled'])

    # Register callback, so on_view_settings_changed() gets called, whenever
    # user settings have been changed.
    def register_callbacks(self):
        if not self._callbacks_registered:
            self.log(3, 'Registering on change callbacks')
            self.view.settings().add_on_change('perltidy_on_change', self.on_view_settings_changed)
            self._callbacks_registered = True

    # Reload settings callback.
    def on_view_settings_changed(self):
        if self.is_enabled:
            self.log(3, 'View settings changed, reloading')
            self.load_settings(reload=True)

    # Check, if given perltidy command is valid. For now, we can only check,
    # if the elements given in list cmd are valid file system objects. Returns
    # True, if command appears to be valid, False otherwise.
    def is_valid_perltidy_cmd(self, cmd=[], cmd_source=None):
        if cmd is None or len(cmd) == 0:
            return False

        self.log(2, 'Checking for perltidy (' + cmd_source + '): ' + self.pp(cmd))
        if os.path.isfile(cmd[0]):
            return True

        if cmd_source == 'user':
            self.log(0, 'Command {0} specified in user setting "perltidy_cmd" seems to be invalid. Ignoring and searching for perltidy in PATH.'.format(self.pp(cmd[0])))
        else:
            self.log(2, 'Command not found: ' + self.pp(cmd[0]))

        return False

    # Search for perltidyrc file in current project, based on possible file
    # paths configured in user setting "perltidy_rc_paths". Return first
    # perltidyrc path found, or None, if the project does not contain any
    # perltidyrc files.
    def find_perltidyrc_in_project(self):
        perltidy_rc_path = None

        try:
            for folder in self.view.window().folders():
                for perltidy_rc_path in self._perltidy_rc_paths:

                    # Construct absolute path, if not absolute yet.
                    perltidy_rc_path = perltidy_rc_path if os.path.isabs(perltidy_rc_path) else os.path.join(folder, perltidy_rc_path)
                    self.log(2, 'Checking for perltidyrc: ' + self.pp(perltidy_rc_path))

                    # Does this perltidyrc file exist?
                    if os.path.isfile(perltidy_rc_path):
                        self.log(1, 'Using perltidyrc: ' + self.pp(perltidy_rc_path))
                        raise StopIteration()
                    else:
                        self.log(2, 'File not found: ' + self.pp(perltidy_rc_path))
                        perltidy_rc_path = None
        except StopIteration:
            pass
        else:
            self.log(2, 'No perltidyrc found in project.')

        return perltidy_rc_path

    # Find perltidy in PATH.
    def find_perltidy_in_path(self):
        cmd = None
        perltidy_filename = 'perltidy.bat' if sublime.platform() == 'windows' else 'perltidy'

        for path in os.environ['PATH'].split(os.pathsep):
            cmd_path = os.path.join(path, perltidy_filename)
            cmd = [cmd_path]

            if self.is_valid_perltidy_cmd(cmd, cmd_source='path'):
                break
            else:
                cmd = None

        return cmd

    # Search for perltidy in platform default locations.
    def find_perltidy_in_platform_default_paths(self):

        if sublime.platform() == 'windows':
            # Check for default locations of perltidy, if running under Win32
            # and using Strawberry Perl/ActivePerl or Cygwin.
            cmd = ["C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy"]
            if self.is_valid_perltidy_cmd(cmd, cmd_source='platform defs'):
                if os.path.isfile(cmd[1]):
                    return cmd

            cmd = ["C:\\Perl\\bin\\perl.exe", "C:\\Perl\\site\\bin\\perltidy"]
            if self.is_valid_perltidy_cmd(cmd, cmd_source='platform defs'):
                if os.path.isfile(cmd[1]):
                    return cmd

            cmd = ["C:\\Cygwin\\bin\\perl.exe", "/usr/local/bin/perltidy"]
            if self.is_valid_perltidy_cmd(cmd, cmd_source='platform defs'):
                if os.path.isfile("C:\\Cygwin\\usr\\local\\bin\\perltidy"):
                    return cmd
        else:
            # Some default locations for Unix. Should be covered by PATH
            # already.
            for cmd in ['/usr/bin/perltidy', '/usr/local/bin/perltidy']:
                if self.is_valid_perltidy_cmd(cmd, cmd_source='platform defs'):
                    return cmd

        return None

    # Try to locate perltidy and set self._perltidy_cmd.
    def find_perltidy(self):

        # Determine perltidy command to run in the following order:
        # 1. From user setting "perltidy_cmd"
        # 2. Within PATH (search for "perltidy" or "perltidy.bat" on Win32)
        # 3. From platform specific defaults
        if self._perltidy_cmd is None:
            cmd = None

            try:
                # 1. From user setting "perltidy_cmd", this may be either a
                # single string or a list, handle appropriately.
                cmd = self.view.settings().get('perltidy_cmd')
                if cmd is not None and type(cmd) is not list:
                    cmd = [cmd]

                if self.is_valid_perltidy_cmd(cmd, cmd_source='user'):
                    raise StopIteration()

                # 2. Within PATH (search for "perltidy" or "perltidy.bat" on Win32)
                cmd = self.find_perltidy_in_path()
                if cmd is not None:
                    raise StopIteration()

                # 3. From platform specific defaults
                cmd = self.find_perltidy_in_platform_default_paths()
                if cmd is not None:
                    raise StopIteration()

            except StopIteration:
                # Save command for later usage
                self.log(1, 'Using perltidy: ' + self.pp(cmd))
                self._perltidy_cmd = cmd
            else:
                pass

        return self._perltidy_cmd

    # Load PerlTidy settings from Sublime preferences.
    def load_settings(self, reload=True):
        settings = self.view.settings()

        if reload or self._perltidy_log_level is None:
            self._perltidy_log_level = settings.get('perltidy_log_level', DEFAULT_SETTINGS['perltidy_log_level'])
        if reload or self._perltidy_options is None:
            self._perltidy_options = settings.get('perltidy_options', DEFAULT_SETTINGS['perltidy_options'])
        if reload or self._perltidy_rc_paths is None:
            self._perltidy_rc_paths = settings.get('perltidy_rc_paths', DEFAULT_SETTINGS['perltidy_rc_paths'])
        if reload and self._perltidy_cmd is not None:
            self._perltidy_cmd = None           # will be set by find_perltidy()

    # Simple logging.
    def log(self, level, message):
        if level <= self._perltidy_log_level:
            print 'PerlTidy: ' + message

    # Pretty print given string for diagnostic output.
    def pp(self, string):
        result = []

        if type(string) is list:
            for i in string:
                result.append('"' + i + '"')
        else:
            result.append('"' + string + '"')

        return ' '.join(result)

    # Tidy given region; returns True on success or False on perltidy runtime
    # error.
    def tidy_region(self, edit, region):

        # Map WindowsError exception to None on non-Win32
        try:
            WindowsError
        except NameError:
            WindowsError = None

        # Build command.
        cmd = []
        cmd.extend(self._perltidy_cmd)
        cmd.extend(self._perltidy_options)

        # Check, if we have a perltidyrc in the current project and append to
        # command.
        perltidy_rc_path = self.find_perltidyrc_in_project()
        if perltidy_rc_path is not None:
            cmd.append('-pro=' + perltidy_rc_path)

        # Prepare arguments for subprocess call.
        subprocess_args = {
            'bufsize': -1,
            'shell': False,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'stdin': subprocess.PIPE
        }

        # Hide console window on Win32.
        if sublime.platform() == 'windows':
            subprocess_args['startupinfo'] = subprocess.STARTUPINFO()
            subprocess_args['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Check, if the data to be tidied has any non-ASCII characters. If
        # yes, prepare temporary files for input and output with UTF-8
        # encoding, and spool the input to file. Adjust perltidy call, so data
        # will be read and written to temporary files.
        input = self.view.substr(region)
        use_temporary_files = False

        try:
            input.decode('ascii')
        except UnicodeEncodeError:
            use_temporary_files = True

        if use_temporary_files:
            # Create temporary files for input/output and reopen them with
            # codecs.open, so we can specify an encoding for the files. At
            # least with Python 2.6, there seems to be no other option.
            perltidy_input_fh, perltidy_input_filepath = tempfile.mkstemp()
            perltidy_output_fh, perltidy_output_filepath = tempfile.mkstemp()
            os.close(perltidy_input_fh)
            os.close(perltidy_output_fh)

            with codecs.open(perltidy_input_filepath, 'w+b', encoding='utf-8') as fh:
                fh.write(input)

            cmd.append(perltidy_input_filepath)
            cmd.append('-o=' + perltidy_output_filepath)
            input = None

        # Show time!
        output, error = None, None
        self.log(1, 'Running command: ' + self.pp(cmd))
        try:
            p = subprocess.Popen(cmd, **subprocess_args)
            output, error = p.communicate(input)
            # TODO: check p.returncode

            # If we're using temporary files for I/O, load output from output
            # file and cleanup temporary files.
            if use_temporary_files:
                with codecs.open(perltidy_output_filepath, 'rb', encoding='utf-8') as fh:
                    output = fh.read()
                os.unlink(perltidy_input_filepath)
                os.unlink(perltidy_output_filepath)

            if error:
                raise PerlTidyRuntimeError(error)

        # Handle perltidy errors. Show them in scratch window.
        except PerlTidyRuntimeError as e:
            results = self.view.window().new_file()
            results.set_scratch(True)
            results.set_name('PerlTidy: Error output')
            edit = results.begin_edit()
            results.insert(edit, 0, error)
            results.end_edit(edit)
            return False

        # Handle OS errors. Check, if we can give the user some hints.
        except (WindowsError, EnvironmentError) as e:
            self.log(0, 'Unable to run perltidy: ' + self.pp(cmd))
            self.log(0, 'Error was: ' + repr(e))

            hints = []

            # Check current error and give user some hints about error reason
            if sublime.platform() == 'windows' and type(e) is exceptions.WindowsError and e.winerror == 193 and os.path.basename(cmd[0]) == 'perltidy':
                # bad exe format
                hints.append(
                    'Maybe you have specified the path to "perltidy" ' +
                    'instead of "perltidy.bat" in your "perltidy_cmd"?')

            if len(hints) == 0:
                if self._perltidy_log_level < 2:
                    hints.append(
                        'Try to increase PerlTidy log level via user setting ' +
                        '"perltidy_log_level" and try again.')

            if len(hints):
                for hint in hints:
                    self.log(0, hint)

            sublime.error_message(
                'PerlTidy: Unable to run perltidy. Please inspect console (hit Ctrl+` ' +
                'or select View->Show Console from menu) for detailed diagnostic ' +
                'messages, error output and hints.')
            return False

        # Everything went okay so far.
        else:
            self.view.replace(edit, region, output)
            return True
