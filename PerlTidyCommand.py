import sublime
import sublime_plugin
import subprocess
import os
import os.path
import tempfile
import codecs

# PerlTidy for Sublime Text 2
#   rbo@cpan.org

DEFAULT_SETTINGS = {
    'perltidy_log_level': 0,
    'perltidy_options': ['-sbl', '-bbt=1', '-pt=2', '-nbbc', '-l=100', '-ole=unix', '-w', '-se'],
    'perltidy_rc_paths': ['.perltidyrc', 'perltidyrc'],
    'perltidy_cmd': '/usr/bin/perltidy',
}

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

        # Check, if we have any non-empty selections and tidy them.
        regions_tidied = 0
        for region in self.view.sel():
            if not region.empty():
                regions_tidied += 1
                self.tidy_region(edit, region)

        # If no selections have been tidied so far, go ahead and tidy entire
        # view. Reposition cursor after tidying up.
        if regions_tidied == 0:
            cursor_pos = self.view.sel()[0]
            if self.tidy_region(edit, sublime.Region(0L, self.view.size())):
                if cursor_pos.empty():
                    self.view.sel().add(cursor_pos)
                    if len(self.view.sel()) > 1:
                        self.view.sel().subtract(self.view.sel()[1])
                    self.view.show_at_center(self.view.sel()[0].begin())

    def pp(self, string):
        result = []

        if type(string) is list:
            for i in string:
                result.append('"' + i + '"')
        else:
            result.append('"' + string + '"')

        return ' '.join(result)

    def load_settings(self):
        if self._perltidy_log_level is None:
            self._perltidy_log_level = self.view.settings().get('perltidy_log_level', DEFAULT_SETTINGS['perltidy_log_level'])
        if self._perltidy_options is None:
            self._perltidy_options = self.view.settings().get('perltidy_options', DEFAULT_SETTINGS['perltidy_options'])
        if self._perltidy_rc_paths is None:
            self._perltidy_rc_paths = self.view.settings().get('perltidy_rc_paths', DEFAULT_SETTINGS['perltidy_rc_paths'])

    def get_perltidy_cmd(self):

        # If not already done, load perltidy command from settings, or fall
        # back to default command defined in class above.
        if self._perltidy_cmd is None:
            cmd = self.view.settings().get('perltidy_cmd')
            user_provided_perltidy_cmd = True

            if cmd is None:
                cmd = DEFAULTS['perltidy_cmd']
                user_provided_perltidy_cmd = False

            if type(cmd) is not list:
                cmd = [cmd]

            # First element of self._perltidy_cmd must be (an executable)
            # file. If not assume that the command is invalid and try to find
            # perltidy within path. Emit warning, if the command is invalid,
            # and has been provided by the user.
            if not os.path.isfile(cmd[0]):
                if user_provided_perltidy_cmd:
                    print 'PerlTidy: Command {0} specified in user setting "perltidy_cmd" could not be found. Ignoring and searching perltidy in PATH.'.format(self.pp(cmd[0]))
                cmd = None

                # Search for perltidy (or perltidy.bat on Win32) within PATH.
                perltidy_filename = 'perltidy'
                if os.name == 'nt':
                    perltidy_filename += '.bat'

                for path in os.environ["PATH"].split(os.pathsep):
                    cmd_path = os.path.join(path, perltidy_filename)
                    if self._perltidy_log_level >= 2:
                        print 'PerlTidy: Checking for perltidy: ' + self.pp(cmd_path)

                    if os.path.isfile(cmd_path):
                        if self._perltidy_log_level >= 1:
                            print 'PerlTidy: Using perltidy: ' + self.pp(cmd_path)
                        cmd = [cmd_path]
                        break

            # Save cmd for later usage.
            if cmd is not None:
                if self._perltidy_log_level >= 2:
                    print 'PerlTidy: Using perltidy command: ' + self.pp(cmd)
                self._perltidy_cmd = cmd

        return self._perltidy_cmd

    # Return list containing perltidy options as defined in user setting
    # "perltidy_options" or DEFAULTS['perltidy_options']
    def get_perltidy_options(self):
        return self._perltidy_options

    # Return list containing possible perltidyrc paths as defined in user
    # setting "perltidy_rc_paths" or DEFAULTS['perltidy_rc_paths']
    def get_perltidy_rc_paths(self):
        return self._perltidy_rc_paths

    # Search for perltidyrc file in current project, based on possible file
    # paths configured in user setting "perltidy_rc_paths". Return first
    # perltidyrc path found, or None, if the project does not contain any
    # perltidyrc files.
    def get_perltidy_rc_path(self):
        try:
            for folder in self.view.window().folders():
                for perltidy_rc_path in self.get_perltidy_rc_paths():

                    # Construct absolute path, if not absolute yet.
                    perltidy_rc_path = perltidy_rc_path if os.path.isabs(perltidy_rc_path) else os.path.join(folder, perltidy_rc_path)

                    if self._perltidy_log_level >= 2:
                        print 'PerlTidy: Checking for perltidyrc: ' + self.pp(perltidy_rc_path)

                    # Does this perltidyrc file exist?
                    if os.path.isfile(perltidy_rc_path):
                        if self._perltidy_log_level >= 2:
                            print 'PerlTidy: Using perltidyrc: ' + self.pp(perltidy_rc_path)
                        raise StopIteration()
                    else:
                        perltidy_rc_path = None

        except StopIteration:
            pass

        if perltidy_rc_path is None and self._perltidy_log_level >= 2:
            print 'PerlTidy: No perltidyrc found in project'

        return perltidy_rc_path

    # Tidy given region; returns True on success or False on perltidy runtime
    # error.
    def tidy_region(self, edit, region):

        # Build command.
        cmd = []
        cmd.extend(self.get_perltidy_cmd())
        cmd.extend(self.get_perltidy_options())

        # Check, if we have a perltidyrc in the current project and append to
        # command.
        perltidy_rc_path = self.get_perltidy_rc_path()
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
            subprocess_args['stdout'] = None
            subprocess_args['stdin'] = None

            perltidy_input_fh, perltidy_input_filepath = tempfile.mkstemp()
            perltidy_output_fh, perltidy_output_filepath = tempfile.mkstemp()
            os.close(perltidy_input_fh)
            os.close(perltidy_output_fh)

            with codecs.open(perltidy_input_filepath, 'w+b', encoding='utf-8') as fh:
                fh.write(input)

            cmd.append(perltidy_input_filepath)
            cmd.append('-o=' + perltidy_output_filepath)
            input = None

        if self._perltidy_log_level >= 1:
            print 'PerlTidy: Running command: ' + ' '.join(cmd)

        p = subprocess.Popen(cmd, **subprocess_args)
        output, error = p.communicate(input)

        # If we're using temporary files for I/O, load output from output file
        # and cleanup temporary files.
        if use_temporary_files:
            with codecs.open(perltidy_output_filepath, 'rb', encoding='utf-8') as fh:
                output = fh.read();
            os.unlink(perltidy_input_filepath)
            os.unlink(perltidy_output_filepath)

        # Replace region with output, if we had no errors. Otherwise create a
        # scratch window with perltidy error output.
        if not error:
            self.view.replace(edit, region, output)
            return True
        else:
            results = self.view.window().new_file()
            results.set_scratch(True)
            results.set_name('PerlTidy: Error output')
            edit = results.begin_edit()
            results.insert(edit, 0, error)
            results.end_edit(edit)
            return False
