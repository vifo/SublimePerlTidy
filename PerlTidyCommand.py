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
    'perltidy_platform_default_paths': {
        'nt': [
            ["C:\\Strawberry\\perl\\bin\\perl.exe", "C:\\Strawberry\\perl\\site\\bin\\perltidy"],
            ["C:\\Strawberry\\perl\\site\\bin\\perltidy.bat"],
        ],
        'default': [
            ['/usr/bin/perltidy'],
        ],
    },
    'perltidy_rc_paths': ['.perltidyrc', 'perltidyrc'],
}

class PerlTidyRuntimeError(Exception):
    def __init__(self, value):
        self.value = value


class PerlTidyCommand(sublime_plugin.TextCommand):

    _perltidy_cmd = None
    _perltidy_log_level = None
    _perltidy_options = None
    _perltidy_rc_paths = None

    def run(self, edit):
        self.load_settings()

        # Bailout, if we don't have a valid perltidy command to run.
        cmd = self.get_perltidy_cmd()
        if cmd is None:
            sublime.error_message(
                'PerlTidy: Cannot find perltidy in any directory given in environment variable ' +
                'PATH. Please setup your environment variable PATH, so it contains perltidy, ' +
                'or specify perltidy location in user setting "perltidy_cmd". Please refer ' +
                'to documentation at https://github.com/rbo/st2-perltidy for details.')
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

    # Check, if given perltidy command is valid. For now, we can only check,
    # if the elements given in list cmd are valid file system objects. Returns
    # True, if command appears to be valid, False otherwise.
    def is_valid_perltidy_cmd(self, cmd=[], cmd_source=None):
        if cmd is None or len(cmd) == 0:
            return False

        self.log(2, 'Checking for perltidy (' + cmd_source + '): ' + self.pp(cmd))
        if not os.path.isfile(cmd[0]):
            if cmd_source == 'user':
                self.log(0, 'Command {0} specified in user setting "perltidy_cmd" could not be found. Ignoring and searching for perltidy in PATH'.format(self.pp(cmd[0])))
            else:
                self.log(2, 'Command not found: ' + self.pp(cmd[0]))
            return False

        # Passed command seems to be valid.
        return True

    # Search for perltidyrc file in current project, based on possible file
    # paths configured in user setting "perltidy_rc_paths". Return first
    # perltidyrc path found, or None, if the project does not contain any
    # perltidyrc files.
    def find_perltidyrc_in_project(self):
        perltidy_rc_path = None

        try:
            for folder in self.view.window().folders():
                for perltidy_rc_path in self.get_perltidy_rc_paths():

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
            self.log(2, 'No perltidyrc found in project')

        return perltidy_rc_path

    # Find perltidy in PATH.
    def find_perltidy_in_path(self):
        cmd = []

        perltidy_filename = 'perltidy'
        if os.name == 'nt':
            perltidy_filename += '.bat'

        for path in os.environ["PATH"].split(os.pathsep):
            cmd_path = os.path.join(path, perltidy_filename)
            cmd = [cmd_path]

            if self.is_valid_perltidy_cmd(cmd, cmd_source='path'):
                break

        return cmd

    # Search for perltidy in platform default locations.
    def find_perltidy_in_platform_default_paths(self):
        cmds = DEFAULT_SETTINGS['perltidy_platform_default_paths']['default']
        if os.name == 'nt':
            cmds = DEFAULT_SETTINGS['perltidy_platform_default_paths']['nt']

        for cmd in cmds:
            if self.is_valid_perltidy_cmd(cmd, cmd_source='platform defs'):
                return cmd

        return None

    def get_perltidy_cmd(self):

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
                # cmd = self.find_perltidy_in_path()
                # if cmd is not None:
                #     #raise StopIteration()
                #     pass

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

    # Return list containing perltidy options as defined in user setting
    # "perltidy_options" or DEFAULT_SETTINGS['perltidy_options']
    def get_perltidy_options(self):
        return self._perltidy_options

    # Return list containing possible perltidyrc paths as defined in user
    # setting "perltidy_rc_paths" or DEFAULT_SETTINGS['perltidy_rc_paths']
    def get_perltidy_rc_paths(self):
        return self._perltidy_rc_paths

    # Load PerlTidy settings from Sublime preferences.
    def load_settings(self, force=False):
        if force or self._perltidy_log_level is None:
            self._perltidy_log_level = self.view.settings().get('perltidy_log_level', DEFAULT_SETTINGS['perltidy_log_level'])
        if force or self._perltidy_options is None:
            self._perltidy_options = self.view.settings().get('perltidy_options', DEFAULT_SETTINGS['perltidy_options'])
        if force or self._perltidy_rc_paths is None:
            self._perltidy_rc_paths = self.view.settings().get('perltidy_rc_paths', DEFAULT_SETTINGS['perltidy_rc_paths'])

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
        cmd.extend(self.get_perltidy_cmd())
        cmd.extend(self.get_perltidy_options())

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
        if os.name == 'nt':
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

            # If we're using temporary files for I/O, load output from output
            # file and cleanup temporary files.
            if use_temporary_files:
                with codecs.open(perltidy_output_filepath, 'rb', encoding='utf-8') as fh:
                    output = fh.read()
                os.unlink(perltidy_input_filepath)
                os.unlink(perltidy_output_filepath)

            if error:
                raise PerlTidyRuntimeError(error)

        # Handle OS errors. Check, if we can give the user some hints.
        except (WindowsError, OSError) as e:
            self.log(0, 'Unable to run perltidy: ' + self.pp(cmd))
            self.log(0, 'PerlTidy: OS error was: ' + repr(e))

            hints = []

            # Check current error and give user some hints about error reason
            if os.name == 'nt' and type(e) is exceptions.WindowsError:
                if e.winerror == 193:       # bad exe format
                    if os.path.basename(cmd[0]) == 'perltidy':
                        hints.append(
                            'Maybe you have specified the path to "perltidy" instead ' +
                            'of "perltidy.bat" in your "perltidy_cmd"?')

            if len(hints) == 0:
                if self._perltidy_log_level < 2:
                    hints.append(
                        'Try to increase PerlTidy log level via user setting ' +
                        '"perltidy_log_level" and try again')

            if len(hints):
                for hint in hints:
                    self.log(0, hint)

            sublime.error_message(
                'PerlTidy: Unable to run perltidy. Please inspect console (hit Ctrl+` ' +
                'or select View->Show Console from menu) for detailed diagnostic ' +
                'messages, error output and hints.')
            return False

        # Handle perltidy errors. Show them in scratch window.
        except PerlTidyRuntimeError as e:
            results = self.view.window().new_file()
            results.set_scratch(True)
            results.set_name('PerlTidy: Error output')
            edit = results.begin_edit()
            results.insert(edit, 0, error)
            results.end_edit(edit)
            return False

        # Everything went okay so far.
        else:
            self.view.replace(edit, region, output)
            return True
